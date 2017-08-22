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
import subprocess
import sys
import time
from pathlib import Path

STARTING_INIT = b"start_init: trying /sbin/init"
BOOT_FAILURE = b"Enter full pathname of shell or RETURN for /bin/sh"
SHELL_OPEN = b"exec /bin/sh"
LOGIN = b"login:"
PROMPT = b"root@beri1:"
STOPPED = b"Stopped at"
PANIC = b"panic: trap"


def success(*args, **kwargs):
    print("\n\033[0;32m", *args, "\033[0m", sep="", file=sys.stderr)


def failure(*args, **kwargs):
    print("\n\033[0;31m", *args, "\033[0m", sep="", file=sys.stderr)
    sys.exit(1)


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qemu-cmd", default="qemu-system-cheri")
    parser.add_argument("--kernel", default="/usr/local/share/cheribsd/cheribsd-malta64-kernel")
    parser.add_argument("--disk-image", default="/usr/local/share/cheribsd/cheribsd-full.img")
    parser.add_argument("--reuse-image", action="store_true")
    parser.add_argument("--interact", "-i", action="store_true")
    try:
        # noinspection PyUnresolvedReferences
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    args = parser.parse_args()
    force_decompression = not args.reuse_image  # type: bool
    qemu = args.qemu_cmd
    kernel = str(maybe_decompress(Path(args.kernel), force_decompression))
    diskimg = str(maybe_decompress(Path(args.disk_image), force_decompression))

    child = pexpect.spawn(qemu, ["-M", "malta", "-kernel", kernel, "-hda", diskimg, "-m", "2048", "-nographic"],
                          logfile=sys.stdout.buffer, echo=False)
    # ignore SIGINT for the python code, the child should still receive it
    # signal.signal(signal.SIGINT, signal.SIG_IGN)

    i = child.expect([pexpect.TIMEOUT, STARTING_INIT, BOOT_FAILURE], timeout=5 * 60)
    if i == 0:  # Timeout
        failure("timeout before booted: ", str(child))
    elif i == 2:  # start up scripts failed
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
    else:
        failure("error during boot login prompt: ", str(child))

    # TODO: run the test script here, scp files over, etc.

    if args.interact:
        # interact print all in and output -> clear logfile
        child.logfile = None
        while True:
            try:
                if not child.isalive():
                    break
                child.interact()
            except KeyboardInterrupt:
                continue


if __name__ == "__main__":
    main()
