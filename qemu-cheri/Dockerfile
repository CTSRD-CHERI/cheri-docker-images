FROM ubuntu:18.04
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    libpixman-1-0 libjpeg8 libpng16-16 libnuma1 libxml2 libsdl1.2debian libglib2.0-0 samba \
    python3-minimal libpython3-stdlib bzip2 xz-utils openssh-client wget git ca-certificates
# add SSH key
RUN mkdir -p /root/.ssh && ssh-keygen -t ed25519 -N '' -f /root/.ssh/id_ed25519 < /dev/null && chmod 700 ~/.ssh && chmod 600 ~/.ssh/*
RUN mkdir -p /cheri-sdk/
ENV PATH=/cheri-sdk/bin:$PATH
COPY ./qemu-linux /cheri-sdk

CMD ["bash"]
