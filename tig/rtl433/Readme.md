mos_sub -v -t test/fb/temperature -t fb/fb_docinfo -t fb/fb_tr069 -t metrics/snmp/netgear

docker run --rm -it --device $(readlink -f /dev/rtl-sdr) tig-rtl433 rtl_433 -p22 -g42 -f434086k -Csi -Fjson

Timezone: UTC
