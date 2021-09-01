FROM ctsrd/cheri-sdk:latest

ADD --chown=cheri:cheri ./cheribsd-sysroot.tar.xz /cheri-sdk/
# TODO: generate a clang config file so that --sysroot is set automatically
CMD ["bash"]
