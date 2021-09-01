# Staged build: import, decompress, and convert disk images (and kernel).  Doing
# this dance before another "FROM" statement below means that, while we "COPY"
# the Jenkins artifacts in for processing, only things we explicitly "COPY
# --from" this stage end up in the final docker layers generated.
FROM ctsrd/qemu-cheri:latest

ARG TARGET_ARCH

RUN mkdir -p /opt/cheri/output/rootfs-${TARGET_ARCH}/boot/kernel
COPY --chown=cheri:cheri ./kernel.xz /opt/cheri/output/rootfs-${TARGET_ARCH}/boot/kernel/
RUN unxz /opt/cheri/output/rootfs-${TARGET_ARCH}/boot/kernel/kernel.xz
COPY --chown=cheri:cheri ./cheribsd-*.img.xz /opt/cheri/output/
# TODO: When everything's at least as new as Ubuntu Focal, add back
# "-o compression_type=zstd" to the `qemu-img convert` invocation below.  For
# the moment, tho', we'll leave `-c` to its default (i.e., zlib).
RUN for i in /opt/cheri/output/cheribsd-*.img.xz; do \
  unxz $i; i=${i%.xz}; \
  /opt/cheri/output/sdk/bin/qemu-img convert -O qcow2 -c $i ${i%.img}.qcow2; \
  rm $i; \
 done

# Staged build: the actual image
FROM ctsrd/qemu-cheri:latest

ARG TARGET_ARCH

ENV PATH=/opt/cheri/output/sdk/bin:/opt/cheri/output/cheribuild:$PATH
COPY --from=0 --chown=cheri:cheri /opt/cheri/output /opt/cheri/output
# Do this last, it will change frequently
RUN git clone https://github.com/CTSRD-CHERI/cheribuild.git /opt/cheri/output/cheribuild

#CMD ["qemu-system-cheri"]
CMD ["bash"]
