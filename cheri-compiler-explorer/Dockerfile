# Note: leap 15.2 ships with old glibc so can't run our clang
FROM opensuse/tumbleweed:latest
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN zypper in -y git nodejs12 npm12 make which libncurses5
RUN useradd gcc-user && mkdir -p /compiler-explorer /home/gcc-user && chown -R gcc-user /compiler-explorer && chown gcc-user /home/gcc-user

ADD ./cheri-clang-llvm.tar.xz /cheri-sdk
ADD ./morello-clang-llvm.tar.xz /morello-sdk
COPY sysroot-mips64-purecap /cheri-sdk/sysroot-mips64-purecap
COPY sysroot-riscv64-purecap /cheri-sdk/sysroot-riscv64-purecap
# TODO: Add Morello sysroot
RUN ln -sfn /cheri-sdk/sysroot-riscv64-purecap /morello-sdk/sysroot-morello-purecap
# Sanity check that compilers work
RUN /cheri-sdk/bin/clang --version && /morello-sdk/bin/clang --version

ENV HOME /home/gcc-user
USER gcc-user
# Build newest version of compiler-explorer (and ensure that we do the clone as gcc-user)
RUN if [ "$(whoami)" = "gcc-user" ]; then echo "Correct UID"; else echo "WRONG USER: $(whoami)"; false; fi && \
      git clone --depth=1 https://github.com/mattgodbolt/compiler-explorer.git /compiler-explorer && make -C /compiler-explorer dist

COPY *.local.properties /compiler-explorer/etc/config/
WORKDIR /compiler-explorer
VOLUME ["/compiler-explorer/lib/storage/data"]

ENTRYPOINT [ "make" ]
EXPOSE 10240
CMD ["run"]
