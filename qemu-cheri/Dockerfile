FROM ubuntu:18.04
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN apt-get update && apt-get install -y libpixman-1-0 libjpeg8 libnuma1 libxml2 libpng12-0 libsdl1.2debian libglib2.0-0 samba --no-install-recommends

# Install the dependencies for boot_cheribsd.py
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-minimal libpython3.5-stdlib python3-pip bzip2 xz-utils openssh-client wget git \
    && mkdir /usr/local/share/cheribsd && chmod 777 /usr/local/share/cheribsd \
    && pip3 install pexpect
# add SSH key
RUN mkdir -p /root/.ssh && ssh-keygen -t ed25519 -N '' -f /root/.ssh/id_ed25519 < /dev/null && chmod 700 ~/.ssh && chmod 600 ~/.ssh/*

COPY ./qemu-linux /usr/local

CMD ["bash"]
