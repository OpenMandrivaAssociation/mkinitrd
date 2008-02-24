Summary: Creates an initial ramdisk image for preloading modules
Name: mkinitrd
Version: 6.0.29
Release: %manbo_mkrel 4
License: GPLv2+
URL: http://www.redhat.com/
Group: System/Kernel and hardware
Source: mkinitrd-%{version}.tar.bz2
# Mandriva sources
Source100: mkinitrd-sysconfig
# RH patches
# Mandriva patches
Patch100: mkinitrd-6.0.28-noselinux.patch
# no proper dhcp lib package yet
Patch101: mkinitrd-6.0.28-nonetwork.patch
Patch102: mkinitrd-6.0.28-etc-blkid.patch
# fix regexp match with bash-3.2, notably to fix RAID with mdadm
# (similar to initscripts bug: Mdv #32501, RH #220087)
Patch103: mkinitrd-6.0.28-rmatch.patch
Patch104: mkinitrd-6.0.28-use-both-ahci-ata_piix.patch
Patch105: mkinitrd-6.0.28-source-sysconfig-later.patch
Patch106: mkinitrd-6.0.29-resume.patch
Patch107: mkinitrd-6.0.28-closedir.patch
Patch108: mkinitrd-6.0.28-usage-uname-r.patch
Patch109: mkinitrd-6.0.28-fix-modules-check.patch
Patch110: mkinitrd-6.0.28-ide.patch
Patch111: mkinitrd-6.0.28-dsdt.patch
# handle root=<devnum> from lilo
Patch112: mkinitrd-6.0.29-root-devnum.patch
Patch113: mkinitrd-6.0.28-kbd.patch
Patch115: mkinitrd-6.0.29-resume-md.patch
Patch119: mkinitrd-6.0.28-fstab-auto.patch
Patch123: mkinitrd-6.0.28-relatime.patch
# resolve UUID/LABEL with /dev devices, not /sys
# (so that resolved LVM devices can be used with lvs)
Patch124: mkinitrd-6.0.28-resolve-uuid-in-dev.patch
Patch130: mkinitrd-6.0.28-gz-modules.patch
Requires: util-linux-ng
Requires: mktemp >= 1.5-9mdk findutils >= 4.1.7-3mdk
Requires: grep, mount, gzip, tar
Requires: filesystem >= 2.1.0, cpio, initscripts >= 8.63-1mdv2008.1
Requires: e2fsprogs >= 1.38-12, coreutils
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
Summary: C header files and library for functionality exported by libnash
Group: Development/C
Requires: glibc-devel, pkgconfig, e2fsprogs-devel, mkinitrd, glib2-devel
Requires: nash = %{version}-%{release}

%package -n libbdevid-python
Summary: Python bindings for libbdevid
Group: Development/Other
Requires: python, nash = %{version}-%{release}

%package -n nash
Summary: Nash shell
Group: System/Kernel and hardware
Provides: libbdevid = %{version}-%{release}
Obsoletes: libbdevid < %{version}-%{release}
Conflicts: mkinitrd < 6.0.28-2mdv2008.1

%description devel
C header files and library for functionality exported by libnash

%description -n libbdevid-python
Python bindings for libbdevid.

%description -n nash
nash shell used by initrd

%prep
%setup -q
# Mandriva
%patch100 -p1 -b .noselinux
%patch101 -p1 -b .nonetwork
%patch102 -p1 -b .etc-blkid
%patch103 -p1 -b .rmatch
%patch104 -p1 -b .use-both-ahci-ata_piix
%patch105 -p1 -b .source-sysconfig-later
%patch106 -p1 -b .resume
%patch107 -p1 -b .closedir
%patch108 -p1 -b .usage-uname-r
%patch109 -p1 -b .fix-modules-check
%patch110 -p1 -b .ide
%patch111 -p1 -b .dsdt
%patch112 -p1 -b .root-devnum
%patch113 -p1 -b .kbd
%patch115 -p1 -b .resume-md
%patch119 -p1 -b .fstab-auto
%patch123 -p1 -b .relatime
%patch124 -p1 -b .resolve-uuid-in-dev
%patch130 -p1 -b .gz-modules
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
install -m 644 %{SOURCE100} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mkinitrd

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
%{python_sitearch}/bdevid.so

%files -n nash
%defattr(-,root,root)
%attr(644,root,root) %{_mandir}/man8/nash.8*
%attr(755,root,root) /sbin/nash
/%{_lib}/bdevid
%{_libdir}/libnash.so.*
%{_libdir}/libbdevid.so.*
