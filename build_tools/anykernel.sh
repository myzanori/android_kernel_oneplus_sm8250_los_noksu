### AnyKernel3 Ramdisk Mod Script
## Mystic Kernel (SM8250 / Kona Unified for OnePlus 9R, 8T, 8, 8 Pro)

### AnyKernel setup
# global properties
properties() { '
kernel.string=Mystic Kernel v1.0.40 (hybrid stable) for OnePlus 9R / 8T (SM8250) by myzanori
do.devicecheck=1
do.modules=0
do.systemless=1
do.cleanup=1
do.cleanuponabort=0
device.name1=lemonades
device.name2=lemonadep
device.name3=kebab
device.name4=kebabt
device.name5=instantnoodle
device.name6=instantnoodlep
device.name7=OnePlus9R
device.name8=OnePlus8T
device.name9=OnePlus8
device.name10=OnePlus8Pro
device.name11=LE2101
device.name12=KB2001
device.name13=KB2000
device.name14=KB2003
device.name15=KB2005
device.name16=KB2007
device.name17=IN2011
device.name18=IN2021
device.name19=20809
device.name20=20828
device.name21=20838
device.name22=opkona
device.name23=ossi
device.name24=kona
supported.versions=11-18
supported.patchlevels=
supported.vendorpatchlevels=
'; } # end properties

### AnyKernel install
## boot files attributes
boot_attributes() {
set_perm_recursive 0 0 755 644 $RAMDISK/*;
set_perm_recursive 0 0 750 750 $RAMDISK/init* $RAMDISK/sbin;
} # end attributes

# boot shell variables
BLOCK=boot;
IS_SLOT_DEVICE=1;
RAMDISK_COMPRESSION=auto;
PATCH_VBMETA_FLAG=auto;

# import functions/variables and setup patching - see for reference (DO NOT REMOVE)
. tools/ak3-core.sh;

ui_print " ";
ui_print "========================================";
ui_print "  Mystic Kernel v1.0.40 (hybrid stable) ";
ui_print "  OnePlus 9R / 8T (SM8250 Kona)         ";
ui_print "  ReSukiSU + SUSFS v2.3.0 + NoMount v2.1.0";
ui_print "----------------------------------------";
ui_print "  Developer : myzanori                  ";
ui_print "  GitHub    : https://github.com/myzanori";
ui_print "========================================";
ui_print " ";

# boot install
dump_boot;

# Align boot header OS version and patch level to Android 14 / ColorOS 15
if [ -f $home/split_img/header ]; then
    sed -i 's/os_version=.*/os_version=14.0.0/' $home/split_img/header;
    sed -i 's/os_patch_level=.*/os_patch_level=2025-10/' $home/split_img/header;
fi;

# write new kernel Image while keeping stock DTB & ramdisk
write_boot;

# Install persistent runtime tuning and patch level alignment
if [ -d /data/adb/post-fs-data.d ]; then
    cp -f $home/mystic-tune.sh /data/adb/post-fs-data.d/mystic-tune.sh 2>/dev/null;
    chmod 755 /data/adb/post-fs-data.d/mystic-tune.sh 2>/dev/null;
fi;

ui_print " ";
ui_print ">> Installation Successful!";
ui_print ">> Enjoy Mystic Kernel by myzanori!";
ui_print " ";
## end boot install
