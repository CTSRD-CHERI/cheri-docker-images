FROM ctsrd/cheri-sdk:latest
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

ADD ./cheribsd-sysroot.tar.xz /cheri-sdk/
# TODO: generate a clang config file so that --sysroot is set automatically
CMD ["bash"]
