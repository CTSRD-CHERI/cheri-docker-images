FROM ubuntu:16.04
ARG target=cheri256
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN apt-get update && apt-get install -y libpixman-1-0 libjpeg8 libnuma1 libpng12-0 libsdl1.2debian libglib2.0-0 --no-install-recommends

COPY ./QEMU-${target}/qemu-cheri-install /usr/local

#CMD ["qemu-system-cheri"]
CMD ["bash"]