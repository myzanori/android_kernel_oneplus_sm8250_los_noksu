#!/system/bin/sh
MODDIR=${0%/*}

# Load WLAN driver early so cnss/wlan interface is present before network services.
# CONFIG_QCA_CLD_WLAN=y in the stable build => /sys/module/wlan already exists.
# Only insmod the external wlan.ko if the driver is genuinely NOT built in.
if [ ! -d /sys/module/wlan ] && [ -f "$MODDIR/wlan.ko" ]; then
    insmod "$MODDIR/wlan.ko" 2>/dev/null
fi


# Only set LZ4 comp_algorithm if zram has not yet initialized swap
if [ -f /sys/block/zram0/comp_algorithm ]; then
    if ! grep -q '\[lz4\]' /sys/block/zram0/comp_algorithm; then
        echo lz4 > /sys/block/zram0/comp_algorithm 2>/dev/null || true
    fi
fi
