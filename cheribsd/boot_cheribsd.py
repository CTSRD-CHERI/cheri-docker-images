#!/usr/bin/env python3
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
import subprocess
import sys
import time
from pathlib import Path

ALMOST_BOOTED = b"Starting background file system checks in 60 seconds"
BOOT_FAILURE = b"Enter full pathname of shell or RETURN for /bin/sh"
LOGIN = b"login:"
PROMPT = b"root@beri1:"
STOPPED = b"Stopped at"
PANIC = b"panic: trap"


def success(*args, **kwargs):
    print("\n\033[0;32m", *args, "\033[0m", sep="", file=sys.stderr)


def failure(*args, **kwargs):
    print("\n\033[0;31m", *args, "\033[0m", sep="", file=sys.stderr)
    sys.exit(1)


def maybe_decompress(path: Path, force_decompression: bool) -> Path:
    # drop the suffix and then try decompressing
    if path.exists() and not force_decompression:
        return path
    elif path.with_suffix(path.suffix + ".bz2").exists():
        print("Extracting", path.with_suffix(path.suffix + ".bz2"))
        subprocess.check_call(["bunzip2", "-k", str(path.with_suffix(path.suffix + ".bz2"))])
    elif path.with_suffix(path.suffix + ".xz").exists():
        print("Extracting", path.with_suffix(path.suffix + ".xz"))
        subprocess.check_call(["xz", "-d", "-k", "-v", str(path.with_suffix(path.suffix + ".xz"))])

    if not path.exists():
        sys.exit("Could not find " + str(path))
    return path


def main():
    global ALMOST_BOOTED, LOGIN, PROMPT
    parser = argparse.ArgumentParser()
    parser.add_argument("--qemu-cmd", default="qemu-system-cheri")
    parser.add_argument("--kernel", default="/usr/local/share/cheribsd/cheribsd-malta64-kernel")
    parser.add_argument("--disk-image", default="/usr/local/share/cheribsd/cheribsd-full.img")
    parser.add_argument("--reuse-image", action="store_true")
    parser.add_argument("--interact", "-i", action="store_true")
    args = parser.parse_args()
    force_decompression = not args.reuse_image  # type: bool
    qemu = args.qemu_cmd
    kernel = str(maybe_decompress(Path(args.kernel), force_decompression))
    diskimg = str(maybe_decompress(Path(args.disk_image), force_decompression))

    child = pexpect.spawn(qemu, ["-M", "malta", "-kernel", kernel, "-hda", diskimg, "-m", "2048", "-nographic"],
                          logfile=sys.stdout.buffer, echo=False, )
    i = child.expect([pexpect.TIMEOUT, ALMOST_BOOTED, BOOT_FAILURE], timeout=15 * 60)
    if i == 0:  # Timeout
        failure("timeout before booted: ", str(child))
        sys.exit(1)
    elif i == 0:  # start up scripts failed
        failure("start up scripts failed to run")
    success("===> nearly booted")

    i = child.expect([pexpect.TIMEOUT, LOGIN], timeout=30)
    if i == 0:  # Timeout
        failure("timeout awaiting login prompt: ", str(child))
    success("===> got login prompt")

    child.sendline(b"root")
    i = child.expect([pexpect.TIMEOUT, PROMPT], timeout=60)
    if i == 0:  # Timeout
        failure("timeout awaiting command prompt ", str(child))
    success("===> got command prompt")

    # TODO: run the test script here, scp files over, etc.

    if args.interact:
        # interact print all in and output -> clear logfile
        child.logfile = None
        child.interact()


if __name__ == "__main__":
    main()
