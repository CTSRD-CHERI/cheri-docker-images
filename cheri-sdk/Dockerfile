FROM ubuntu:16.04
ARG target=cheri256
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN apt-get update && apt-get install -y  --no-install-recommends \
  make ninja-build \
  autoconf automake autotools-dev libsigsegv2 m4 \
  flex bison \
  git \
  python3-minimal libpython3.5-stdlib \
  unzip bzip2 zip zutils xz-utils \
  libpixman-1-0 libjpeg8 libnuma1 libpng12-0 libsdl1.2debian libglib2.0-0
# last line is libraries needed by QEMU


# install CMake 3.9
ADD ./cmake-3.9.1-Linux-x86_64.tar.gz /usr/local

# install cheri binutils (only ld.bfd and objdump from the ancient binutils)
COPY ./binutils.tar.bz2 /tmp
RUN tar xjf /tmp/binutils.tar.bz2 -C /tmp \
  && mkdir -p /cheri-sdk/bin \
  && (cd /cheri-sdk/bin && mv /tmp/binutils/bin/mips64-ld /tmp/binutils/bin/mips64-ld.bfd \
      && for TOOL in ld.bfd objdump; do \
        cp -fv /tmp/binutils/bin/mips64-$TOOL $TOOL \
        ln -fs $TOOL cheri-unknown-freebsd-$TOOL ; \
        ln -fs $TOOL mips64-unknown-freebsd-$TOOL ; \
      done) \
  && rm -r /tmp/binutils.tar.bz2 /tmp/binutils

# Add the remaining binutils from elftoolchain:
COPY ./elftoolchain.tar.xz /tmp
RUN tar xJf /tmp/elftoolchain.tar.bz2 -C /tmp && mv /tmp/opt/elftoolchain/bin/* /cheri-sdk/bin \
  && rm -rv /tmp/elftoolchain.tar.bz2 /tmp/opt

# install QEMU
#COPY ./qemu-${target}-install.zip /tmp
#RUN unzip /tmp/qemu-${target}-install.zip -d /tmp \
#  && chmod +x /tmp/qemu-cheri-install/bin/* \
#  && cp -rv /tmp/qemu-cheri-install/* /cheri-sdk \
#  && rm /tmp/qemu-${target}-install.zip && rm -r /tmp/qemu-cheri-install
COPY ./QEMU-${target}/qemu-cheri-install /cheri-sdk

# install clang SDK (and delete some unnecessary files as they are really big statically linked)
COPY ./${target}-master-clang-llvm.tar.xz /tmp
RUN tar Jxf /tmp/${target}-master-clang-llvm.tar.xz --strip-components 1 -C /cheri-sdk \
  && ln -s ld.lld /cheri-sdk/bin/ld && rm /usr/bin/ld \
  && rm /tmp/${target}-master-clang-llvm.tar.xz \
  && (cd /cheri-sdk/bin && rm -vf clang-check opt llc lli llvm-lto2 llvm-lto llvm-c-test \
         llvm-dsymutil llvm-dwp llvm-nm llvm-ar llvm-rtdyld *-llc \
         llvm-extract llvm-xray llvm-split llvm-cov llvm-symbolizer llvm-dwarfdump \
         llvm-link llvm-stress llvm-cxxdump llvm-cvtres llvm-cat llvm-as \
         llvm-diff llvm-modextract llvm-tblgen llvm-dis llvm-pdbdump llvm-profdata \
         llvm-opt-report llvm-bcanalyzer llvm-mcmarkup llvm-lib llvm-ranlib \
         verify-uselistorder sanstats clang-offload-bundler c-index-test \
         clang-import-test bugpoint sancov obj2yaml yaml2obj)
 
# install cheribsd sysroot
COPY ./${target}-vanilla-jemalloc-cheribsd-world.tar.xz /tmp
# --exclude=bin so that we don't extract the freebsd binaries
RUN tar Jxf /tmp/${target}-vanilla-jemalloc-cheribsd-world.tar.xz --strip-components 1 -C /cheri-sdk --exclude=bin \
  && rm /tmp/${target}-vanilla-jemalloc-cheribsd-world.tar.xz

# Do this last, it will change frequently
# RUN git clone https://github.com/CTSRD-CHERI/cheribuild.git /cheri-sdk/cheribuild

# VOLUME /workspace
# WORKDIR /
# ENV WORKSPACE=/workspace
ENV PATH=/cheri-sdk/bin:/cheri-sdk/cheribuild:$PATH

#CMD ["qemu-system-cheri"]
CMD ["bash"]
