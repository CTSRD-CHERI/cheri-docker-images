FROM ubuntu:16.04
ARG target=cheri256
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN apt-get update && apt-get install -y \
  binutils \
  git \
  python3-minimal \
  unzip \
  xz-utils
# QEMU needs these libraries
RUN apt-get install -y libpixman-1-0 libjpeg8 libnuma1 libpng12-0 libsdl1.2debian

# install QEMU
#COPY ./qemu-${target}-install.zip /tmp
#RUN unzip /tmp/qemu-${target}-install.zip -d /tmp \
#  && chmod +x /tmp/qemu-cheri-install/bin/* \
#  && cp -rv /tmp/qemu-cheri-install/* /cheri-sdk \
#  && rm /tmp/qemu-${target}-install.zip && rm -r /tmp/qemu-cheri-install
COPY ./QEMU-${cpu}/qemu-cheri-install /cheri-sdk

# install CHERI SDK
RUN mkdir /cheri-sdk
COPY ./${target}-vanilla-jemalloc-sdk.tar.xz /tmp
RUN tar Jxf /tmp/${target}-vanilla-jemalloc-sdk.tar.xz --strip-components 1 -C /cheri-sdk \
  && rm /tmp/${target}-vanilla-jemalloc-sdk.tar.xz

# Do this last, it will change frequently
RUN git clone https://github.com/CTSRD-CHERI/cheribuild.git /cheri-sdk/cheribuild

# install CMake 3.9
# ADD https://cmake.org/files/v3.9/cmake-3.9.0-rc5-Linux-x86_64.tar.gz /usr/local

# VOLUME /workspace
# WORKDIR /
# ENV WORKSPACE=/workspace
ENV PATH=/cheri-sdk/bin:/cheri-sdk/cheribuild:$PATH

#CMD ["qemu-system-cheri"]
CMD ["bash"]