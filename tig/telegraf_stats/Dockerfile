FROM docker.io/telegraf:1.37.3-alpine

RUN apk add --update smartmontools sudo nvme-cli && rm -rf /var/cache/apk/*

RUN echo "telegraf  ALL=(ALL) NOPASSWD: /usr/sbin/smartctl" >/etc/sudoers.d/telegraf
