FROM ctsrd/qemu-${CPU}:latest
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-minimal libpython3.5-stdlib python3-pip bzip2 xz-utils \
    && mkdir /usr/local/share/cheribsd && chmod 777 /usr/local/share/cheribsd \
    && pip3 install pexpect

# TODO: setup NFS so that cheribsd can access it
COPY ./cheribsd-malta64-kernel.bz2 /usr/local/share/cheribsd
COPY ./cheribsd-full.img.xz /usr/local/share/cheribsd
COPY ./cheribsd-minimal.img.xz /usr/local/share/cheribsd
COPY ./boot_cheribsd.py /usr/local/bin

#CMD ["bash"]
CMD ["/usr/local/bin/boot_cheribsd.py"]
