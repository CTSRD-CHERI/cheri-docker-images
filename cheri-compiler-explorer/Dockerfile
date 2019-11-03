FROM ctsrd/cheri-sdk
LABEL maintainer="Alexander.Richardson@cl.cam.ac.uk"

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install -y wget curl make git ca-certificates \
    && apt-get autoremove --purge -y \
    && apt-get autoclean -y \
    && rm -rf /var/cache/apt/* /tmp/*
RUN echo "*** Installing node.js 10 ***" \
    && DEBIAN_FRONTEND=noninteractive curl -sL https://deb.nodesource.com/setup_10.x | bash \
    && apt-get install -y nodejs
RUN git clone https://github.com/mattgodbolt/compiler-explorer.git /compiler-explorer \
    && cd /compiler-explorer \
    && make prereqs
# TODO: Set CHERI paths
# RUN sed -i '' -e 's/compiler.opt.exe=\/usr\/bin\/opt/compiler.opt.exe=\/cheri-sdk\/bin\/opt/g' /compiler-explorer/etc/config/llvm.defaults.properties
# RUN sed -i '' -e 's/compiler.llc.exe=\/usr\/bin\/llc/compiler.llc.exe=\/cheri-sdk\/bin\/llc/g' /compiler-explorer/etc/config/llvm.defaults.properties
COPY "c++.local.properties" "/compiler-explorer/etc/config/c++.defaults.properties"
COPY "c.local.properties" "/compiler-explorer/etc/config/c.defaults.properties"

WORKDIR /compiler-explorer
RUN useradd gcc-user && mkdir -p /compiler-explorer /home/gcc-user && chown -R gcc-user /compiler-explorer && chown gcc-user /home/gcc-user
ENV HOME /home/gcc-user
USER gcc-user

ENTRYPOINT [ "make" ]
EXPOSE 10240
CMD ["run"]