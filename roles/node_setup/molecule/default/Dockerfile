FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install only essential packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    systemd \
    sudo \
    python3 \
    ca-certificates \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Remove unnecessary systemd services to speed up boot
RUN cd /lib/systemd/system/sysinit.target.wants/ && \
    ls | grep -v systemd-tmpfiles-setup | xargs rm -f && \
    rm -f /lib/systemd/system/multi-user.target.wants/* \
    /etc/systemd/system/*.wants/* \
    /lib/systemd/system/local-fs.target.wants/* \
    /lib/systemd/system/sockets.target.wants/*udev* \
    /lib/systemd/system/sockets.target.wants/*initctl* \
    /lib/systemd/system/basic.target.wants/* \
    /lib/systemd/system/anaconda.target.wants/* \
    /lib/systemd/system/plymouth* \
    /lib/systemd/system/systemd-update-utmp*

# Create a fake cgroup v2 hierarchy
RUN mkdir -p /sys/fs/cgroup

CMD ["/lib/systemd/systemd"]
