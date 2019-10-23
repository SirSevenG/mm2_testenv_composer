# based on https://github.com/KomodoPlatform/atomicDEX-API/blob/mm2/Dockerfile
FROM        ubuntu:bionic
LABEL       maintainer="SirSevenG <ottonseven@gmail.com>"

RUN         apt-get update && \
            apt-get install -q \
            git \
            build-essential \
            libssl-dev \
            wget -y && \
# https://github.com/rust-lang/rust-bindgen/blob/master/book/src/requirements.md#debian-based-linuxes
            apt-get install -q \
            llvm-3.9-dev \
            libclang-3.9-dev \
            clang-3.9 -y && \
# openssl-sys requirements, cf. https://crates.io/crates/openssl-sys
            apt-get install -q \
            pkg-config \
            libssl-dev -y && \
            apt-get clean

#Cmake 3.12.0 supports multi-platform -j option, it allows to use all cores for concurrent build to speed up it
RUN         wget https://cmake.org/files/v3.12/cmake-3.12.0-Linux-x86_64.sh && \
            sh cmake-3.12.0-Linux-x86_64.sh --skip-license --exclude-subdir --prefix=/usr/local && \
            rm -rf cmake-3.12.0-Linux-x86_64.sh

RUN         wget -O- https://sh.rustup.rs > /tmp/rustup-init.sh && \
            sh /tmp/rustup-init.sh -y --default-toolchain none && \
            . /root/.cargo/env && \
# It seems that bindgen won't prettify without it:
            rustup install nightly-2019-10-15 && \
            rustup default nightly-2019-10-15 && \
            rustup component add rustfmt-preview && \
            rm -rf /root/.rustup/toolchains/nightly-2019-10-06-x86_64-unknown-linux-gnu/share/doc && \
            rm -f /tmp/rustup-init.sh

ENV         PATH="/root/.cargo/bin:${PATH}"

RUN         cd /tmp && \
            wget https://api.github.com/repos/KomodoPlatform/atomicDEX-API/tarball/mm2 && \
            tar -xzf mm2 && \
            ls && \
            mv KomodoPlatform-atomicDEX-API-* /mmaker2 && \
            rm mm2

RUN         cd /mmaker2 && cargo fetch

# Build MM1 and MM2.
# Increased verbosity here allows us to see the MM1 CMake logs.
RUN         cd /mmaker2 && \
            cargo build --features native -vv && \
            mv /mmaker2/target/debug/mm2 /mmaker2/mm2 && \
            cargo clean

RUN         mkdir /log && \
            touch /log/log.txt

CMD ["echo", "done"]
