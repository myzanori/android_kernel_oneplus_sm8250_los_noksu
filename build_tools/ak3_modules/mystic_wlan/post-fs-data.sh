#!/system/bin/sh
MODDIR=${0%/*}

# Load WLAN driver early so cnss/wlan interface is present before network services.
# CONFIG_QCA_CLD_WLAN=y in the stable build => /sys/module/wlan already exists.
# Only insmod the external wlan.ko if the driver is genuinely NOT built in.
if [ ! -d /sys/module/wlan ] && [ -f "$MODDIR/wlan.ko" ]; then
    insmod "$MODDIR/wlan.ko" 2>/dev/null
fi

# Set ZRAM compression algorithm to LZ4 early before swap fills
if [ -f /sys/block/zram0/comp_algorithm ]; then
    if ! grep -q '\[lz4\]' /sys/block/zram0/comp_algorithm; then
        swapoff /dev/block/zram0 2>/dev/null
        echo 1 > /sys/block/zram0/reset 2>/dev/null
        echo lz4 > /sys/block/zram0/comp_algorithm 2>/dev/null
        swapon /dev/block/zram0 2>/dev/null
    fi
fi
