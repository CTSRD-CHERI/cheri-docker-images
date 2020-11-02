# Note: leap 15.2 ships with old glibc so can't run our clang
FROM opensuse/tumbleweed:latest
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN zypper in -y git nodejs12 npm12 make which libncurses5
RUN useradd gcc-user && mkdir -p /compiler-explorer /home/gcc-user && chown -R gcc-user /compiler-explorer && chown gcc-user /home/gcc-user

# TODO: llvm/bin/llc llvm/bin/opt
#COPY llvm/bin/clang* llvm/bin/ld.lld llvm/bin/lld llvm/bin/llvm-objdump llvm/bin/llvm-mca llvm/bin/llvm-readobj llvm/bin/llvm-readelf llvm/bin/llvm-cxxfilt /cheri-sdk/bin/
#COPY llvm/lib/clang /cheri-sdk/lib/clang
ADD ./cheri-clang-llvm.tar.xz /cheri-sdk
COPY cheribsd/include /cheri-sdk/sysroot/usr/include
RUN ln -sfn /cheri-sdk/bin/ld.lld /cheri-sdk/bin/ld

ENV HOME /home/gcc-user
USER gcc-user
# Build newest version of compiler-explorer (and ensure that we do the clone as gcc-user)
RUN if [ "$(whoami)" = "gcc-user" ]; then echo "Correct UID"; else echo "WRONG USER: $(whoami)"; false; fi && \
      git clone --depth=1 https://github.com/mattgodbolt/compiler-explorer.git /compiler-explorer && make -C /compiler-explorer dist
WORKDIR /compiler-explorer
COPY *.local.properties /compiler-explorer/etc/config/

ENTRYPOINT [ "make" ]
EXPOSE 10240
CMD ["run"]