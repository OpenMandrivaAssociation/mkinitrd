Summary: Creates an initial ramdisk image for preloading modules
Name: mkinitrd
Version: 6.0.28
Release: %mkrel 1
License: GPLv2+
URL: http://www.redhat.com/
Group: System/Kernel and hardware
Source: mkinitrd-%{version}.tar.bz2
# Mandriva sources
Source100: mkinitrd-sysconfig
# RH patches
Patch0: mkinitrd-no-more-lvm-static.patch
Patch1: mkinitrd-no-more-rtc.patch
# Mandriva patches
Patch102: mkinitrd-4.2.17-cdrom.patch
Patch104: mkinitrd-4.2.17-use-both-ahci-ata_piix.patch
Patch106: mkinitrd-4.2.17-resume.patch
Patch107: mkinitrd-6.0.28-closedir.patch
Patch111: mkinitrd-6.0.28-dsdt.patch
Patch113: mkinitrd-6.0.28-kbd.patch
Patch114: mkinitrd-4.2.17-suspend2.patch
Patch115: mkinitrd-4.2.17-resumemd.patch
Patch119: mkinitrd-4.2.17-fstabauto.patch
Patch123: mkinitrd-4.2.17-relatime.patch
Patch125: mkinitrd-4.2.17-omit_ide.patch
Patch130: mkinitrd-4.2.17-tuxonice.patch
Requires: /bin/sh, /sbin/insmod.static, /sbin/losetup
Requires: mktemp >= 1.5-9mdk findutils >= 4.1.7-3mdk
Requires: fileutils, grep, mount, gzip, tar
Requires: filesystem >= 2.1.0, cpio, initscripts >= 8.63-1
Requires: e2fsprogs >= 1.38-12, glib2, coreutils
Requires: module-init-tools >= 3.3-pre11
BuildRequires: popt-devel
BuildRequires: e2fsprogs-devel parted-devel >= 1.8.5, pkgconfig, glib2-devel
BuildRequires: device-mapper-devel python-devel
BuildRequires: python util-linux-ng
%ifarch ppc
Requires: ppc64-utils >= 0.3-1
%endif
Requires: nash = %{version}-%{release}
#mkinitrd can work without those, but lesser versions are broken
#Conflicts: udev <= 0.51-1mdk
Conflicts: lvm1 < 1.0.8-2mdk
Conflicts: lvm2 < 2.01.09
Conflicts: mdadm < 2.5.3-3mdv
Conflicts: bootloader-utils < 1.8-1mdk, bootsplash < 3.1.12
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
mkinitrd creates filesystem images for use as initial ram filesystem
(initramfs) images.  These images are used to find and mount the root
filesystem.

%package devel
Summary: C header files and library for functionality exported by libnash.
Group: Development/Libraries
Requires: glibc-devel, pkgconfig, e2fsprogs-devel, mkinitrd, glib2-devel
Requires: nash = %{version}-%{release}

%package -n libbdevid-python
Summary: Python bindings for libbdevid
Group: System Environment/Libraries
Requires: glib2, e2fsprogs, device-mapper-libs
Requires: python, nash = %{version}-%{release}

%package -n nash
Summary: nash shell
Group: System Environment/Base
Requires: parted, device-mapper-libs, e2fsprogs-libs
Requires: popt, libnl, glib2
Requires: openssl, zlib
Provides: libbdevid = %{version}-%{release}
Obsoletes: libbdevid < %{version}-%{release}

%description devel
C header files and library for functionality exported by libnash.

%description -n libbdevid-python
Python bindings for libbdevid.

%description -n nash
nash shell used by initrd

%prep
%setup -q
%patch0 -p1
%patch1 -p1
# Mandriva
%patch102 -p1 -b .cdrom
%patch104 -p1 -b .use-both-ahci-ata_piix
%patch106 -p1 -b .resume
%patch107 -p1 -b .closedir
%patch111 -p1 -b .dsdt
%patch113 -p1 -b .kbd
%patch114 -p1 -b .resume2
%patch115 -p1 -b .resumemd
%patch119 -p1 -b .fstab-auto
%patch123 -p1 -b .relatime
%patch125 -p1 -b .omit_ide
%patch130 -p1 -b .tuxonice
find . -name "Makefile*" -exec sed -i 's|-Werror||g' {} \;

%build
make LIB=%{_lib}
make LIB=%{_lib} test

%install
rm -rf $RPM_BUILD_ROOT
make LIB=%{_lib} DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir} install
rm -f $RPM_BUILD_ROOT/sbin/bdevid $RPM_BUILD_ROOT/%{_includedir}/blkent.h

# Mandriva
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mkinitrd

rm -f $RPM_BUILD_ROOT/sbin/installkernel

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(755,root,root) /sbin/mkinitrd
%attr(644,root,root) %{_mandir}/man8/mkinitrd.8*
%attr(755,root,root) /sbin/new-kernel-pkg
%attr(755,root,root) /sbin/grubby
%attr(644,root,root) %{_mandir}/man8/grubby.8*
# Mandriva
%config(noreplace) %{_sysconfdir}/sysconfig/mkinitrd

%files devel
%defattr(-,root,root)
%{_libdir}/libnash.so
%{_libdir}/libbdevid.so
%{_libdir}/libbdevidprobe.a
%{_libdir}/pkgconfig/libnash.pc
%{_libdir}/pkgconfig/libbdevid.pc
%{_libdir}/pkgconfig/libbdevidprobe.pc
%{_includedir}/nash.h
%{_includedir}/nash
%{_includedir}/bdevid.h
%{_includedir}/bdevid

%files -n libbdevid-python
/%{python_sitelib}/bdevid.so

%files -n nash
%defattr(-,root,root)
%attr(644,root,root) %{_mandir}/man8/nash.8*
%attr(755,root,root) /sbin/nash
/%{_lib}/bdevid
%{_libdir}/libnash.so.*
%{_libdir}/libbdevid.so.*
