ARG TARGET_ARCH

# COPY --from= doesn't seem to like expanding arguments, but FROM is fine
FROM ctsrd/cheribsd-qemu-${TARGET_ARCH}:latest

FROM ctsrd/cheribsd-sdk-${TARGET_ARCH}:latest

COPY --from=0 /cheri-sdk /cheri-sdk
CMD ["bash"]
