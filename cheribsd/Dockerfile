FROM ctsrd/qemu-${CPU}:latest
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

# TODO: setup NFS so that cheribsd can access it
RUN mkdir -p /usr/local/share/cheribsd
COPY ./cheribsd-malta64-kernel.bz2 /usr/local/share/cheribsd
COPY ./cheribsd-full.img.xz /usr/local/share/cheribsd
COPY ./cheribsd-minimal.img.xz /usr/local/share/cheribsd
COPY ./boot_cheribsd.py /usr/local/bin

#CMD ["bash"]
CMD ["/usr/local/bin/boot_cheribsd.py"]
