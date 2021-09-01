FROM ubuntu:18.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    libpixman-1-0 libjpeg8 libpng16-16 libnuma1 libxml2 libsdl1.2debian libglib2.0-0 samba \
    python3-minimal libpython3-stdlib bzip2 xz-utils openssh-client wget git ca-certificates \
    libzstd1 sudo
RUN mkdir -p /cheri-sdk
ENV PATH=/cheri-sdk/bin:$PATH

RUN useradd -m -G sudo cheri
RUN chown cheri:cheri /cheri-sdk
USER cheri

# add SSH key
RUN mkdir -p ~/.ssh && ssh-keygen -t ed25519 -N '' -f ~/.ssh/id_ed25519 < /dev/null && chmod 700 ~/.ssh && chmod 600 ~/.ssh/*

COPY --chown=cheri:cheri ./qemu-linux /cheri-sdk

CMD ["bash"]
