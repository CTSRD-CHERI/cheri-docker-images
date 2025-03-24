FROM ubuntu:22.04

RUN apt-get -y update \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install git curl make sudo ca-certificates libxml2 libncurses5

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get -y update \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install nodejs

RUN apt-get autoremove --purge -y \
 && apt-get autoclean -y \
 && rm -rf /var/cache/apt/* /tmp/*

RUN useradd --uid 1000 gcc-user && mkdir -p /compiler-explorer /home/gcc-user && \
    chown -R gcc-user /compiler-explorer && chown gcc-user /home/gcc-user

ADD ./cheri-clang-llvm.tar.xz /cheri-sdk
ADD ./morello-clang-llvm.tar.xz /morello-sdk
COPY sysroot-mips64-purecap /cheri-sdk/sysroot-mips64-purecap
COPY sysroot-riscv64-purecap /cheri-sdk/sysroot-riscv64-purecap
COPY sysroot-morello-purecap /morello-sdk/sysroot-morello-purecap
# Sanity check that compilers work
RUN /cheri-sdk/bin/clang --version && /morello-sdk/bin/clang --version

RUN mkdir -p /tmp/patches && chown gcc-user /tmp/patches

ENV HOME /home/gcc-user
USER gcc-user
# Build newest version of compiler-explorer (and ensure that we do the clone as gcc-user)
COPY patches/*.diff /tmp/patches/
RUN if [ "$(whoami)" = "gcc-user" ]; then echo "Correct UID"; else echo "WRONG USER: $(whoami)"; false; fi && \
      git clone --depth=1 https://github.com/mattgodbolt/compiler-explorer.git /compiler-explorer && \
      cat /tmp/patches/*.diff | patch -p1 -d /compiler-explorer && \
      rm -r /tmp/patches && \
      make -C /compiler-explorer prebuild

COPY *.local.properties /compiler-explorer/etc/config/
# Upstream's example is x86-only (uses jmp); replace with a more portable
# default that just has a nop.
COPY default.asm /compiler-explorer/examples/assembly/default.asm
WORKDIR /compiler-explorer
VOLUME ["/compiler-explorer/lib/storage/data"]

# We have to start as root to chown /compiler-explorer/lib/storage/data
# since docker volumes are always owned by root
USER root
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
EXPOSE 10240
CMD ["run-only"]
