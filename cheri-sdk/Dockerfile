FROM ctsrd/qemu-cheri
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN apt-get update && apt-get install -y  --no-install-recommends \
  make ninja-build \
  autoconf automake autotools-dev libsigsegv2 m4 \
  flex bison \
  git ca-certificates \
  python3-minimal libpython3.5-stdlib \
  unzip bzip2 zip zutils xz-utils libarchive13 \
  libpixman-1-0 libjpeg8 libnuma1 libpng12-0 libsdl1.2debian libglib2.0-0
# last line is libraries needed by QEMU

# install CMake 3.12
COPY ./cmake-3.12.4-Linux-x86_64.tar.gz /tmp
RUN tar xf /tmp/cmake-3.12.4-Linux-x86_64.tar.gz --strip 1 -C /usr/local && rm /tmp/cmake-3.12.4-Linux-x86_64.tar.gz
RUN mkdir -p /cheri-sdk/bin

# Binutils is no longer required, we can probably delete this
# install cheri binutils (only ld.bfd and objdump from the ancient binutils)
# COPY ./binutils.tar.bz2 /tmp
# RUN tar xjf /tmp/binutils.tar.bz2 -C /tmp \
#  && mkdir -p /cheri-sdk/bin \
#  && (cd /cheri-sdk/bin && mv /tmp/binutils/bin/mips64-ld /tmp/binutils/bin/mips64-ld.bfd \
#      && for TOOL in ld.bfd objdump; do \
#        cp -fv /tmp/binutils/bin/mips64-$TOOL $TOOL \
#        ln -fs $TOOL cheri-unknown-freebsd-$TOOL ; \
#        ln -fs $TOOL mips64-unknown-freebsd-$TOOL ; \
#      done) \
#  && rm -r /tmp/binutils.tar.bz2 /tmp/binutils


# Similarly for elftoolchain, most of these tools can be replaced with the llvm version
# Add the remaining binutils from elftoolchain:
COPY ./elftoolchain.tar.xz /tmp
RUN mkdir -p /tmp/elftoolchain && tar xJf /tmp/elftoolchain.tar.xz -C /tmp/elftoolchain && mv /tmp/elftoolchain/bin/* /cheri-sdk/bin \
  && rm -rv /tmp/elftoolchain.tar.xz /tmp/elftoolchain

# install clang SDK (and delete some unnecessary files as they are really big statically linked)
COPY ./cheri-multi-master-clang-llvm.tar.xz /tmp
RUN tar Jxf /tmp/cheri-multi-master-clang-llvm.tar.xz --strip-components 1 -C /cheri-sdk \
  && ln -s ld.lld /cheri-sdk/bin/ld && rm -fv /usr/bin/ld \
  && rm /tmp/cheri-multi-master-clang-llvm.tar.xz \
  && (cd /cheri-sdk/bin && rm -vf clang-check opt llc lli llvm-lto2 llvm-lto llvm-c-test \
         llvm-dsymutil llvm-dwp llvm-rtdyld *-llc \
         llvm-extract llvm-xray llvm-split llvm-cov llvm-symbolizer llvm-dwarfdump \
         llvm-link llvm-stress llvm-cxxdump llvm-cvtres llvm-cat llvm-as \
         llvm-diff llvm-modextract llvm-tblgen llvm-dis llvm-pdbdump llvm-profdata \
         llvm-opt-report llvm-bcanalyzer llvm-mcmarkup llvm-lib \
         verify-uselistorder sanstats clang-offload-bundler c-index-test \
         clang-import-test bugpoint sancov obj2yaml yaml2obj)
 
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
