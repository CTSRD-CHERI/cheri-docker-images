# Staged build: import, decompress, and convert disk images (and kernel).  Doing
# this dance before another "FROM" statement below means that, while we "COPY"
# the Jenkins artifacts in for processing, only things we explicitly "COPY
# --from" this stage end up in the final docker layers generated.
FROM ctsrd/qemu-cheri:latest
COPY --chown=cheri:cheri ./cheribsd-*.img.xz ./kernel.xz /cheri-sdk/
RUN unxz /cheri-sdk/kernel.xz
# TODO: When everything's at least as new as Ubuntu Focal, add back
# "-o compression_type=zstd" to the `qemu-img convert` invocation below.  For
# the moment, tho', we'll leave `-c` to its default (i.e., zlib).
RUN for i in /cheri-sdk/cheribsd-*.img.xz; do \
  unxz $i; i=${i%.xz}; \
  /cheri-sdk/bin/qemu-img convert -O qcow2 -c $i ${i%.img}.qcow2; \
 done

# Staged build: the actual image
FROM ctsrd/qemu-cheri:latest
ENV PATH=/cheri-sdk/bin:/cheri-sdk/cheribuild:$PATH
COPY --from=0 --chown=cheri:cheri /cheri-sdk/kernel /cheri-sdk/cheribsd-*.qcow2 /cheri-sdk/
# Do this last, it will change frequently
RUN git clone https://github.com/CTSRD-CHERI/cheribuild.git /cheri-sdk/cheribuild

#CMD ["qemu-system-cheri"]
CMD ["bash"]
