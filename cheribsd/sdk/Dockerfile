ARG toolchain
FROM ctsrd/${toolchain}-sdk:latest

ADD --chown=cheri:cheri ./cheribsd-sysroot.tar.xz /opt/cheri/output

FROM ctsrd/${toolchain}-sdk:latest

ARG TARGET_ARCH
ARG llvm_sdk_dir

COPY --from=0 --chown=cheri:cheri /opt/cheri/output/sysroot /opt/cheri/output/rootfs-${TARGET_ARCH}
RUN ln -s ../rootfs-${TARGET_ARCH} /opt/cheri/output/${llvm_sdk_dir}/sysroot
# TODO: generate a clang config file so that --sysroot is set automatically
CMD ["bash"]
