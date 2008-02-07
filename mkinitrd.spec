%define use_dietlibc 0
%ifarch %{ix86} x86_64 ppc ppc64
%define use_dietlibc 1
%endif

Summary: Creates an initial ramdisk image for preloading modules
Name: mkinitrd
Version: 4.2.17
Release: %mkrel 57
License: GPLv2+
URL: http://www.redhat.com/
Group: System/Kernel and hardware
Source: mkinitrd-%{version}.tar.bz2
# Mandriva
Source100: mkinitrd-sysconfig
# Mandriva
Patch100: mkinitrd-4.2.17-mdk.patch
Patch101: mkinitrd-4.2.17-label.patch
Patch102: mkinitrd-4.2.17-cdrom.patch
Patch103: mkinitrd-4.2.17-migrate-mptscsih.patch
Patch104: mkinitrd-4.2.17-use-both-ahci-ata_piix.patch
Patch105: mkinitrd-4.2.17-initramfs.patch
Patch106: mkinitrd-4.2.17-resume.patch
Patch107: mkinitrd-4.2.17-closedir.patch
Patch108: mkinitrd-4.2.17-dmraid.patch
Patch109: mkinitrd-4.2.17-evms.patch
Patch110: mkinitrd-4.2.17-scsidriver.patch
Patch111: mkinitrd-4.2.17-initramfs-dsdt.patch
Patch112: mkinitrd-4.2.17-ide.patch
Patch113: mkinitrd-4.2.17-atkbd.patch
Patch114: mkinitrd-4.2.17-suspend2.patch
Patch115: mkinitrd-4.2.17-resumemd.patch
Patch116: mkinitrd-4.2.17-usb-1394.patch
Patch117: mkinitrd-4.2.17-new_raid.patch
Patch118: mkinitrd-4.2.17-switchroot.patch
Patch119: mkinitrd-4.2.17-fstabauto.patch
Patch122: mkinitrd-4.2.17-uuid.patch
Patch123: mkinitrd-4.2.17-relatime.patch
Patch124: mkinitrd-4.2.17-scsi_wait_scan.patch
Patch125: mkinitrd-4.2.17-omit_ide.patch
Patch126: mkinitrd-4.2.17-rtc.patch
Patch127: mkinitrd-4.2.17-modinfo_kver.patch
Patch128: mkinitrd-4.2.17-ide_pata.patch
Patch129: mkinitrd-4.2.17-modfilename.patch
Patch130: mkinitrd-4.2.17-tuxonice.patch
# 31 and 32 for bug #36457
Patch131: nash-mount-by-uuid.patch
# lvm tools don't take UUID in place of a real device
# and they don't like device names outside of their namespace either,
# like /dev/dm-5
Patch132: mkinitrd-4.2.17-uuid_lvm.patch
Requires: mktemp >= 1.5-9mdk e2fsprogs /bin/sh coreutils grep mount gzip tar findutils >= 4.1.7-3mdk gawk cpio
Requires: module-init-tools >= 3.3-pre11
BuildRequires: perl-base
BuildRequires: volume_id-devel
%if %{use_dietlibc}
BuildRequires: dietlibc-devel >= 0.30-2mdk
%else
BuildRequires: glibc-static-devel
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
#mkinitrd can work without those, but lesser versions are broken
#Conflicts: udev <= 0.51-1mdk
Conflicts: lvm1 < 1.0.8-2mdk
Conflicts: lvm2 < 2.01.09
Conflicts: mdadm < 2.5.3-3mdv
Conflicts: bootloader-utils < 1.8-1mdk, bootsplash < 3.1.12

%description
Mkinitrd creates filesystem images for use as initial ramdisk (initrd)
images.  These ramdisk images are often used to preload the block
device modules (SCSI or RAID) needed to access the root filesystem.

In other words, generic kernels can be built without drivers for any
SCSI adapters which load the SCSI driver as a module.  Since the
kernel needs to read those modules, but in this case it isn't able to
address the SCSI adapter, an initial ramdisk is used.  The initial
ramdisk is loaded by the operating system loader (normally LILO) and
is available to the kernel as soon as the ramdisk is loaded.  The
ramdisk image loads the proper SCSI adapter and allows the kernel to
mount the root filesystem.  The mkinitrd program creates such a
ramdisk using information found in the /etc/modules.conf file.

%prep
%setup -q
# Mandriva
%patch100 -p1 -b .mdk
%patch101 -p1 -b .label
%patch102 -p1 -b .cdrom
%patch103 -p1 -b .migrate-mptscsih
%patch104 -p1 -b .use-both-ahci-ata_piix
%patch105 -p1 -b .initramfs
%patch106 -p1 -b .resume
%patch107 -p1 -b .closedir
%patch108 -p1 -b .dmraid
%patch109 -p1 -b .evms
%patch110 -p1 -b .scsidriver
%patch111 -p1 -b .initramfs-dsdt
%patch112 -p1 -b .ide
%patch113 -p1 -b .atkbd
%patch114 -p1 -b .resume2
%patch115 -p1 -b .resumemd
%patch116 -p1 -b .usb-1394
%patch117 -p1 -b .new_raid
%patch118 -p1 -b .switchroot
%patch119 -p1 -b .fstab-auto
%patch122 -p1 -b .uuid
%patch123 -p1 -b .relatime
%patch124 -p1 -b .scsi_wait_scan
%patch125 -p1 -b .omit_ide
%patch126 -p1 -b .rtc
%patch127 -p1 -b .modinfo_kver
%patch128 -p1 -b .ide_pata
%patch129 -p1 -b .modfilename
%patch130 -p1 -b .tuxonice
%patch131 -p0 -b .mount-by-uuid
%patch132 -p1 -b .uuid_lvm

%build
%if %{use_dietlibc}
make DIET=1 DIETLIBC_LIB=%{_prefix}/lib/dietlibc/lib-%{_arch}
%else
make
%endif

%install
rm -rf $RPM_BUILD_ROOT
make BUILDROOT=$RPM_BUILD_ROOT mandir=%{_mandir} install

# Mandriva
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mkinitrd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/sysconfig/mkinitrd
/sbin/*
%{_mandir}/*/*

