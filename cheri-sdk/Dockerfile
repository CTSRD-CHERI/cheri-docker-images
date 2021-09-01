FROM ctsrd/qemu-cheri:latest

ARG cmake_version

RUN sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y --no-install-recommends \
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
ADD --chown=cheri:cheri ./cheri-clang-llvm.tar.xz /opt/cheri/output/sdk

# Do this last, it will change frequently
RUN git clone https://github.com/CTSRD-CHERI/cheribuild.git /opt/cheri/cheribuild

# VOLUME /workspace
# WORKDIR /
# ENV WORKSPACE=/workspace
ENV PATH=/opt/cheri/output/sdk/bin:/opt/cheri/cheribuild:$PATH

#CMD ["qemu-system-cheri"]
CMD ["bash"]
