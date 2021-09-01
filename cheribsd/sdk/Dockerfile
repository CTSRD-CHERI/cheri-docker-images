FROM ctsrd/cheri-sdk:latest

ARG TARGET_ARCH

ADD --chown=cheri:cheri ./cheribsd-sysroot.tar.xz /opt/cheri/output/rootfs-${TARGET_ARCH}
RUN ln -s ../rootfs-${TARGET_ARCH} /opt/cheri/output/sdk/sysroot
# TODO: generate a clang config file so that --sysroot is set automatically
CMD ["bash"]
