FROM ctsrd/cheri-sdk:latest
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN mkdir -p /usr/local/share/cheribsd
COPY ./cheribsd-*.img.xz /usr/local/share/cheribsd
# TODO: generate a clang config file so that --sysroot is set automatically
COPY ./sysroot* /cheri-sdk
CMD ["bash"]
