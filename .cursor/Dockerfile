# Cloud Agent base image for sycamore-hq/work.
# Ledger gates: just, python3. Do not COPY the repo — Cursor checks
# out the requested revision itself.

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PATH=/usr/local/bin:${PATH}

USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      git \
      python3 \
      sudo \
 && rm -rf /var/lib/apt/lists/* \
 && if ! id -u ubuntu >/dev/null 2>&1; then useradd -m -s /bin/bash ubuntu; fi \
 && echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
 && chmod 0440 /etc/sudoers.d/ubuntu

ARG JUST_VERSION=1.58.0
RUN curl -fsSL "https://github.com/casey/just/releases/download/${JUST_VERSION}/just-${JUST_VERSION}-x86_64-unknown-linux-musl.tar.gz" \
    | tar -xz -C /usr/local/bin just \
 && just --version

USER ubuntu
WORKDIR /home/ubuntu
