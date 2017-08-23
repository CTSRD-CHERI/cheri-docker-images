#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -
# Copyright (c) 2016-2017 SRI International
# All rights reserved.
#
# This software was developed by SRI International and the University of
# Cambridge Computer Laboratory under DARPA/AFRL contract FA8750-10-C-0237
# ("CTSRD"), as part of the DARPA CRASH research programme.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# runtests.py - run FreeBSD tests and export them to a tarfile via a disk
# device.
#
import argparse
import os
import pexpect
import signal
import shlex
import subprocess
import sys
import time
import tempfile
from pathlib import Path

STARTING_INIT = b"start_init: trying /sbin/init"
BOOT_FAILURE = b"Enter full pathname of shell or RETURN for /bin/sh"
SHELL_OPEN = b"exec /bin/sh"
LOGIN = b"login:"
PROMPT = b"root@.+:"
STOPPED = b"Stopped at"
PANIC = b"panic: trap"
PANIC_KDB = b"KDB: enter: panic"


def success(*args, **kwargs):
    print("\n\033[0;32m", *args, "\033[0m", sep="", file=sys.stderr)


def failure(*args, exit=True, **kwargs):
    print("\n\033[0;31m", *args, "\033[0m", sep="", file=sys.stderr)
    if exit:
        sys.exit(1)
    return False


def decompress(archive: Path, force_decompression: bool, *, cmd=None) -> Path:
    result = archive.with_suffix("")
    if result.exists():
        if not force_decompression:
            return result
        result.unlink()
    print("Extracting", archive)
    subprocess.check_call(cmd + [str(archive)])
    return result


def maybe_decompress(path: Path, force_decompression: bool) -> Path:
    # drop the suffix and then try decompressing
    def bunzip(archive):
        return decompress(archive, force_decompression, cmd=["bunzip2", "-k", "-v"])

    def unxz(archive):
        return decompress(archive, force_decompression, cmd=["xz", "-d", "-k", "-v"])

    if path.suffix == ".bz2":
        return bunzip(path)
    elif path.suffix == ".xz":
        return unxz(path)
    # try adding the arhive suffix suffix
    elif path.with_suffix(path.suffix + ".bz2").exists():
        return bunzip(path.with_suffix(path.suffix + ".bz2"))
    elif path.with_suffix(path.suffix + ".xz").exists():
        return unxz(path.with_suffix(path.suffix + ".xz"))
    elif not path.exists():
        sys.exit("Could not find " + str(path))
    assert path.exists(), path
    return path


def setup_ssh(qemu: pexpect.spawn, pubkey: Path):
    qemu.sendline("mkdir -p /root/.ssh")
    qemu.expect_exact("#")
    contents = pubkey.read_text(encoding="utf-8").strip()
    qemu.sendline("echo " + shlex.quote(contents) + " >> /root/.ssh/authorized_keys")
    qemu.expect_exact("#")
    qemu.sendline("echo 'PermitRootLogin without-password' >> /etc/ssh/sshd_config")
    qemu.expect_exact("#")
    # TODO: check for bluehive images without /sbin/service
    qemu.sendline("service sshd restart")
    # time.sleep(2)
    success("===> SSH authorized_keys set up")


def boot_cheribsd(qemu_cmd: str, kernel_image: str, disk_image: str, ssh_port: int) -> pexpect.spawn:
    child = pexpect.spawn(qemu_cmd, ["-M", "malta", "-kernel", kernel_image, "-hda", disk_image,
                                     "-m", "2048", "-nographic",
                                     #  ssh forwarding:
                                     "-net", "nic", "-net", "user", "-redir", "tcp:" + str(ssh_port) + "::22"],
                          echo=False)
    # child.logfile=sys.stdout.buffer
    child.logfile_read = sys.stdout.buffer
    # ignore SIGINT for the python code, the child should still receive it
    # signal.signal(signal.SIGINT, signal.SIG_IGN)

    i = child.expect([pexpect.TIMEOUT, STARTING_INIT, BOOT_FAILURE, PANIC_KDB, PANIC, STOPPED], timeout=5 * 60)
    if i == 0:  # Timeout
        failure("timeout before booted: ", str(child))
    elif i != 1:  # start up scripts failed
        failure("start up scripts failed to run")
    success("===> init running")

    i = child.expect([pexpect.TIMEOUT, LOGIN, SHELL_OPEN, BOOT_FAILURE, PANIC, STOPPED], timeout=15 * 60)
    if i == 0:  # Timeout
        failure("timeout awaiting login prompt: ", str(child))
    elif i == 1:
        success("===> got login prompt")
        child.sendline(b"root")
        i = child.expect([pexpect.TIMEOUT, PROMPT], timeout=60)
        if i == 0:  # Timeout
            failure("timeout awaiting command prompt ", str(child))
        success("===> got command prompt")
    elif i == 2:
        # shell started from /etc/rc:
        child.expect_exact("#", timeout=30)
        success("===> /etc/rc completed, got command prompt")
        # set up network (bluehive image tries to use atse0)
        child.sendline("ifconfig le0 up && dhclient le0")
        i = child.expect([pexpect.TIMEOUT, b"DHCPACK from 10.0.2.2"], timeout=120)
        if i == 0:  # Timeout
            failure("timeout awaiting command prompt ", str(child))
    else:
        failure("error during boot login prompt: ", str(child))
    return child


def runtests(qemu: pexpect.spawn, archive: Path, test_command: str,
             ssh_keyfile: str, ssh_port: int, timeout: int) -> bool:
    # create tmpfs on opt
    qemu.sendline("mkdir -p /opt && mount -t tmpfs -o size=300m tmpfs /opt")
    with tempfile.TemporaryDirectory(dir=os.getcwd(), prefix="test_files_") as tmp:
        subprocess.check_call(["tar", "xJf", str(archive), "-C", tmp])
        scp_cmd = ["scp", "-r", "-P", str(ssh_port), "-o", "StrictHostKeyChecking=no",
                   "-i", ssh_keyfile, ".", "root@localhost:/"]
        print("Running", scp_cmd)
        subprocess.check_call(scp_cmd, cwd=tmp)

    # Run the tests
    qemu.sendline(test_command +
                  " ;if test $? -eq 0; then echo 'TESTS' 'COMPLETED'; else echo 'TESTS' 'FAILED'; fi")
    i = qemu.expect([pexpect.TIMEOUT, b'TESTS COMPLETED', b'TESTS FAILED', PANIC, STOPPED], timeout=timeout)
    if i == 0:  # Timeout
        return failure("timeout waiting for tests: ", str(qemu), exit=False)
    elif i == 1:
        success("===> Tests completed!")
        return True
    else:
        return failure("error while running tests: ", str(qemu), exit=False)

def main():
    # TODO: look at click package?
    parser = argparse.ArgumentParser()
    parser.add_argument("--qemu-cmd", default="qemu-system-cheri")
    parser.add_argument("--kernel", default="/usr/local/share/cheribsd/cheribsd-malta64-kernel")
    parser.add_argument("--disk-image", default="/usr/local/share/cheribsd/cheribsd-full.img")
    parser.add_argument("--reuse-image", action="store_true")
    parser.add_argument("--ssh-key", default=os.path.expanduser("~/.ssh/id_ed25519.pub"))
    parser.add_argument("--ssh-port", type=int, default=12345)
    parser.add_argument("--test-archive", "-t")
    parser.add_argument("--test-command", "-c")
    parser.add_argument("--test-timeout", "-tt", type=int, default=60 * 60)
    parser.add_argument("--interact", "-i", action="store_true")
    try:
        # noinspection PyUnresolvedReferences
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    args = parser.parse_args()

    # validate args:
    test_archive = args.test_archive  # type: str
    if test_archive:
        if not Path(test_archive).exists():
            failure("Test archive is missing: ", test_archive)
        if not test_archive.endswith(".tar.xz"):
            failure("Currently only .tar.xz archives are supported")
        if not args.test_command:
            print("WARNING: No test command specified, tests will fail")
            args.test_command = "false"

    force_decompression = not args.reuse_image  # type: bool
    kernel = str(maybe_decompress(Path(args.kernel), force_decompression))
    diskimg = str(maybe_decompress(Path(args.disk_image), force_decompression))

    qemu = boot_cheribsd(args.qemu_cmd, kernel, diskimg, args.ssh_port)

    # TODO: run the test script here, scp files over, etc.
    tests_okay = True
    if test_archive:
        try:
            setup_ssh(qemu, Path(args.ssh_key))
            tests_okay = runtests(qemu, archive=Path(test_archive), test_command=args.test_command,
                                  ssh_keyfile=args.ssh_key, ssh_port=args.ssh_port, timeout=args.test_timeout)
        except Exception:
            import traceback
            traceback.print_exc(file=sys.stderr)
            failure("FAILED to run tests!! ", exit=False)
            tests_okay = False

    if args.interact:
        success("===> Interacting with CheriBSD, use CTRL+A,x to exit")
        # interac() prints all input+output -> disable logfile
        qemu.logfile = None
        qemu.logfile_read = None
        qemu.logfile_send = None
        while True:
            try:
                if not qemu.isalive():
                    break
                qemu.interact()
            except KeyboardInterrupt:
                continue

    success("===> DONE")
    if not tests_okay:
        exit(1)


if __name__ == "__main__":
    main()
