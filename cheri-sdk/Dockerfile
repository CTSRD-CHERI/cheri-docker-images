FROM ctsrd/qemu-cheri:latest
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

ARG cmake_version

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
  make ninja-build \
  autoconf automake autotools-dev libsigsegv2 m4 \
  flex bison \
  git ca-certificates \
  python3-minimal libpython3-stdlib \
  unzip bzip2 zip zutils xz-utils libarchive13
# last line is libraries needed by QEMU

# install CMake
ADD ./cmake-${cmake_version}-Linux-x86_64.tar.gz /usr/local

# install clang SDK
COPY ./cheri-clang-llvm.tar.xz /tmp
ADD ./cheri-clang-llvm.tar.xz /cheri-sdk
 
# For now don't install cheribsd sysroot
# COPY ./${target}-vanilla-jemalloc-cheribsd-world.tar.xz /tmp
# --exclude=bin so that we don't extract the freebsd binaries
# RUN tar Jxf /tmp/${target}-vanilla-jemalloc-cheribsd-world.tar.xz --strip-components 1 -C /cheri-sdk --exclude=bin \
#  && rm /tmp/${target}-vanilla-jemalloc-cheribsd-world.tar.xz

# Do this last, it will change frequently
RUN git clone https://github.com/CTSRD-CHERI/cheribuild.git /cheri-sdk/cheribuild

# VOLUME /workspace
# WORKDIR /
# ENV WORKSPACE=/workspace
ENV PATH=/cheri-sdk/bin:/cheri-sdk/cheribuild:$PATH

#CMD ["qemu-system-cheri"]
CMD ["bash"]
