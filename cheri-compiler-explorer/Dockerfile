FROM ubuntu:18.04
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install -y wget curl make git ca-certificates libxml2 \
    && apt-get autoremove --purge -y \
    && apt-get autoclean -y \
    && rm -rf /var/cache/apt/* /tmp/*
RUN echo "*** Installing node.js 12 ***" \
    && DEBIAN_FRONTEND=noninteractive curl -sL https://deb.nodesource.com/setup_12.x | bash - \
    && apt-get install -y nodejs
RUN useradd gcc-user && mkdir -p /compiler-explorer /home/gcc-user && chown -R gcc-user /compiler-explorer && chown gcc-user /home/gcc-user
COPY *.local.properties /compiler-explorer/etc/config/


# TODO: llvm/bin/llc llvm/bin/opt
#COPY llvm/bin/clang* llvm/bin/ld.lld llvm/bin/lld llvm/bin/llvm-objdump llvm/bin/llvm-mca llvm/bin/llvm-readobj llvm/bin/llvm-readelf llvm/bin/llvm-cxxfilt /cheri-sdk/bin/
#COPY llvm/lib/clang /cheri-sdk/lib/clang
ADD ./cheri-clang-llvm.tar.xz /cheri-sdk
COPY cheribsd/include /cheri-sdk/sysroot/usr/include
RUN ln -sfn /cheri-sdk/bin/ld.lld /cheri-sdk/bin/ld

WORKDIR /compiler-explorer
ENV HOME /home/gcc-user
USER gcc-user
# Build newest version of compiler-explorer
RUN su - gcc-user -c "git clone https://github.com/mattgodbolt/compiler-explorer.git /compiler-explorer && make -C /compiler-explorer dist"


ENTRYPOINT [ "make" ]
EXPOSE 10240
CMD ["run"]