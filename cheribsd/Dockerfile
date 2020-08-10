FROM ctsrd/cheri-sdk:latest
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

COPY ./cheribsd-*.img.xz ./kernel.xz ./sysroot/ /cheri-sdk/
# TODO: generate a clang config file so that --sysroot is set automatically
CMD ["bash"]
