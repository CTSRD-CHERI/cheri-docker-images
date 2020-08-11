FROM ctsrd/qemu-cheri:latest
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

ENV PATH=/cheri-sdk/bin:/cheri-sdk/cheribuild:$PATH
# install disk images and kernels:
COPY ./cheribsd-*.img.xz ./kernel.xz /cheri-sdk/
# Do this last, it will change frequently
RUN git clone https://github.com/CTSRD-CHERI/cheribuild.git /cheri-sdk/cheribuild

#CMD ["qemu-system-cheri"]
CMD ["bash"]
