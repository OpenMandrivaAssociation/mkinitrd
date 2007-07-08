%define name mkinitrd
%define version 4.2.17
%define release %mkrel 35

%define use_dietlibc 0
%ifarch %{ix86} x86_64 ppc ppc64
%define use_dietlibc 1
%endif

Name: %{name}
Summary: Creates an initial ramdisk image for preloading modules
Version: %{version}
Release: %{release}
License: GPL
URL: http://www.redhat.com/
Group: System/Kernel and hardware
Source: ftp://ftp.redhat.com/mkinitrd-%{version}.tar.bz2
Source1: mkinitrd-sysconfig
Patch0: mkinitrd-%{version}-mdk.patch
Patch1: mkinitrd-4.2.17-label.patch
Patch2:	mkinitrd-4.2.17-cdrom.patch
Patch3: mkinitrd-4.2.17-migrate-mptscsih.patch
Patch4: mkinitrd-4.2.17-use-both-ahci-ata_piix.patch
Patch5: mkinitrd-4.2.17-initramfs.patch
Patch6: mkinitrd-4.2.17-resume.patch
Patch7: mkinitrd-4.2.17-closedir.patch
Patch8: mkinitrd-4.2.17-dmraid.patch
Patch9: mkinitrd-4.2.17-evms.patch
Patch10: mkinitrd-4.2.17-scsidriver.patch
Patch11: mkinitrd-4.2.17-initramfs-dsdt.patch
Patch12: mkinitrd-4.2.17-ide.patch
Patch13: mkinitrd-4.2.17-atkbd.patch
Patch14: mkinitrd-4.2.17-suspend2.patch
Patch15: mkinitrd-4.2.17-resumemd.patch
Patch16: mkinitrd-4.2.17-usb-1394.patch
Patch17: mkinitrd-4.2.17-new_raid.patch
Patch18: mkinitrd-4.2.17-switchroot.patch
Patch19: mkinitrd-4.2.17-fstabauto.patch
Patch20: mkinitrd-4.2.17-getKernelArg.patch
Patch21: mkinitrd-4.2.17-strnlen.patch
Patch22: mkinitrd-4.2.17-uuid.patch
Requires: mktemp >= 1.5-9mdk e2fsprogs /bin/sh coreutils grep mount gzip tar findutils >= 4.1.7-3mdk gawk cpio
BuildRequires: /usr/bin/perl
%if %{use_dietlibc}
BuildRequires: dietlibc-devel >= 0.24-2mdk
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
%patch0 -p1 -b .mdk
%patch1 -p1 -b .label
%patch2 -p1 -b .cdrom
%patch3 -p1 -b .migrate-mptscsih
%patch4 -p1 -b .use-both-ahci-ata_piix
%patch5 -p1 -b .initramfs
%patch6 -p1 -b .resume
%patch7 -p1 -b .closedir
%patch8 -p1 -b .dmraid
%patch9 -p1 -b .evms
%patch10 -p1 -b .scsidriver
%patch11 -p1 -b .initramfs-dsdt
%patch12 -p1 -b .ide
%patch13 -p1 -b .atkbd
%patch14 -p1 -b .resume2
%patch15 -p1 -b .resumemd
%patch16 -p1 -b .usb-1394
%patch17 -p1 -b .new_raid
%patch18 -p1 -b .switchroot
%patch19 -p1 -b .fstab-auto
%patch20 -p1 -b .getKernelArg
%patch21 -p1 -b .strnlen
%patch22 -p1 -b .uuid

%build
%if %{use_dietlibc}
make DIET=1
%else
make
%endif

%install
rm -rf $RPM_BUILD_ROOT
make BUILDROOT=$RPM_BUILD_ROOT mandir=%{_mandir} install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mkinitrd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/mkinitrd
/sbin/*
%{_mandir}/*/*


