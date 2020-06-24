FROM ctsrd/qemu-cheri
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

ARG cmake_version

RUN apt-get update && apt-get install -y  --no-install-recommends \
  make ninja-build \
  autoconf automake autotools-dev libsigsegv2 m4 \
  flex bison \
  git ca-certificates \
  python3-minimal libpython3.5-stdlib \
  unzip bzip2 zip zutils xz-utils libarchive13 \
# last line is libraries needed by QEMU

# install CMake
COPY ./cmake-${cmake_version}-Linux-x86_64.tar.gz /tmp
RUN tar xf /tmp/cmake-${cmake_version}-Linux-x86_64.tar.gz --strip 1 -C /usr/local && rm /tmp/cmake-${cmake_version}-Linux-x86_64.tar.gz
RUN mkdir -p /cheri-sdk/bin

# install clang SDK (and delete some unnecessary files as they are really big statically linked)
COPY ./cheri-multi-master-clang-llvm.tar.xz /tmp
RUN tar Jxf /tmp/cheri-multi-master-clang-llvm.tar.xz --strip-components 1 -C /cheri-sdk \
  && rm -fv /usr/bin/ld \
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
