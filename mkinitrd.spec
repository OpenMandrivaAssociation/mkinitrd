Summary: Creates an initial ramdisk image for preloading modules
Name: mkinitrd
Version: 6.0.93
Release: %manbo_mkrel 19
License: GPLv2+
URL: http://www.redhat.com/
Group: System/Kernel and hardware
Source0: mkinitrd-%{version}.tar.bz2
# Mandriva sources
Source100: mkinitrd-sysconfig

# These patches come from our git branch
# Please add the patches there
# git checkout mandriva
# sed -i '/^#BEGINGIT/,/^#ENDGIT/ {/^[^#]/d}' ~/co/mkinitrd/SPECS/mkinitrd.spec
# git format-patch -N master | while read p; do name=$(echo $p | sed 's/^....-//'); n=$(echo $p | sed 's/^00\(..\)-.*$/\1/'); mv -f $p ~/co/mkinitrd/SOURCES/$name; sed -i "s/^#ENDGIT/Patch1$n: $name\n#ENDGIT/" ~/co/mkinitrd/SPECS/mkinitrd.spec; done
#BEGINGIT
Patch101: Create-etc-blkid.patch
Patch102: Fix-regexp-usage-to-work-on-bash-3.2.patch
Patch103: Add-missing-closedir.patch
Patch104: Display-current-kernel-version-in-usage.patch
Patch105: Handle-root-devno-from-lilo.patch
Patch106: Include-driver-for-current-keyboard.patch
Patch107: Get-correct-module-when-rootfs-is-auto-in-fstab.patch
Patch108: Handle-gzip-compressed-modules.patch
Patch109: Fix-handling-return-value-of-dm_task_run.patch
Patch110: Enforce-loading-correct-disk-driver.patch
Patch111: Fix-detection-of-usb_storage-module.patch
Patch112: Fix-resolving-library-deps.patch
Patch113: Disable-selinux.patch
Patch114: Disable-network-support.patch
Patch115: Add-support-for-bootchartd.patch
Patch116: Disable-usb-by-default.patch
Patch117: Don-t-overflow-ppoll.patch
Patch118: Reset-counter-between-the-tree-traversals.patch
Patch119: Return-the-last-kernel-arg-with-given-name.patch
Patch120: Let-readlink-compute-the-absolute-path-for-us.patch
Patch121: Include-both-ahci-and-ata_piix.patch
Patch122: Source-sysconfig-later.patch
Patch123: Resume.patch
Patch124: Include-ide-modules.patch
Patch125: Allow-overriding-DSDT.patch
Patch126: scsi_alias.patch
Patch127: checkroot.patch
Patch128: hooks.patch
Patch129: Wait-only-for-needed-devices.patch
Patch130: kbd-is-in-usr.patch
Patch131: Handle-SYSFONTACM-8859-15.patch
Patch132: Restrict-udev-messages-to-handle.patch
Patch133: Fix-waiting-in-devices.patch
Patch134: Fix-dmraid-to-wait-for-needed-disks.patch
Patch135: no-longer-uses-daemonize-to-start-plymouth-upstream-.patch
Patch136: Add-drm-detection-if-module-is-not-loaded.patch
Patch137: devtmpfs-support.patch
Patch138: Workaround-issue-on-dmraid-10.patch
Patch139: Create-urandom-for-LVM.patch
Patch140: Detect-devtmpfs-support-at-boot-time.patch
Patch141: Improve-keyboard-drivers-detection.patch
Patch142: Always-emit-plymouth.patch
Patch143: Revert-Add-drm-detection-if-module-is-not-loaded.patch
Patch144: Add-drm-whitelist-handling.patch
Patch145: Add-drm-drivers-for-hardware-with-no-currently-loade.patch
Patch146: change-filelist-for-new-bootchart.patch
Patch147: Include-additionnal-hid-keyboard-drivers-57872.patch
Patch148: Include-crc32c-for-btrfs-51622.patch
Patch149: Fix-cciss-support-59077.patch
Patch150: Fix-nash-firmware-loading-see-53220.patch
#ENDGIT

Requires: util-linux-ng
Requires: mktemp >= 1.5-9mdk findutils >= 4.1.7-3mdk
Requires: grep, mount, gzip, tar
Requires: filesystem >= 2.1.0, cpio, initscripts >= 8.63-1mdv2008.1
Requires: e2fsprogs >= 1.38-12, coreutils
Requires: module-init-tools >= 3.3-pre11
Requires: kpartx diffutils
BuildRequires: popt-devel
BuildRequires: libblkid-devel parted-devel >= 1.8.5, pkgconfig 
BuildRequires: device-mapper-devel python-devel
BuildRequires: python util-linux-ng
BuildRequires: libelf-devel
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
Conflicts: dmraid < 1.0.0-0.rc15
Requires(post,postun):	update-alternatives
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
mkinitrd creates filesystem images for use as initial ram filesystem
(initramfs) images.  These images are used to find and mount the root
filesystem.

%package devel
Summary: C header files and library for functionality exported by libnash
Group: Development/C
Requires: glibc-devel, pkgconfig, e2fsprogs-devel, mkinitrd
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
Requires(post,postun):	update-alternatives

%description devel
C header files and library for functionality exported by libnash

%description -n libbdevid-python
Python bindings for libbdevid.

%description -n nash
nash shell used by initrd

%prep
%setup -q

%apply_patches

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
rm -f $RPM_BUILD_ROOT/usr/libexec/mkliveinitrd
mv -f $RPM_BUILD_ROOT/sbin/mkinitrd $RPM_BUILD_ROOT/sbin/mkinitrd-mkinitrd
mv -f $RPM_BUILD_ROOT/sbin/lsinitrd $RPM_BUILD_ROOT/sbin/lsinitrd-mkinitrd

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-alternatives --install /sbin/mkinitrd mkinitrd /sbin/mkinitrd-mkinitrd 100 || :

%postun
[[ ! -e /sbin/mkinitrd-mkinitrd ]] && update-alternatives --remove mkinitrd /sbin/mkinitrd-mkinitrd || :

# this is the version we introduced alternatives
%triggerpostun -- mkinitrd < 6.0.93-%manbo_mkrel 10
update-alternatives --install /sbin/mkinitrd mkinitrd /sbin/mkinitrd-mkinitrd 100 || :

%post -n nash
update-alternatives --install /sbin/lsinitrd lsinitrd /sbin/lsinitrd-mkinitrd 100 || :

%postun -n nash
[[ ! -e /sbin/lsinitrd-mkinitrd ]] && update-alternatives --remove lsinitrd /sbin/lsinitrd-mkinitrd || :

# this is the version we introduced alternatives
%triggerpostun -n nash -- nash < 6.0.93-%manbo_mkrel 11
update-alternatives --install /sbin/lsinitrd lsinitrd /sbin/lsinitrd-mkinitrd 100 || :

%files
%defattr(-,root,root)
%attr(755,root,root) /sbin/mkinitrd-mkinitrd
%attr(644,root,root) %{_mandir}/man8/mkinitrd.8*
# Mandriva
%config(noreplace) %{_sysconfdir}/sysconfig/mkinitrd
%dir %{_prefix}/libexec
%{_prefix}/libexec/initrd-functions

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
%attr(755,root,root) /sbin/lsinitrd-mkinitrd
/%{_lib}/bdevid
%{_libdir}/libnash.so.*
%{_libdir}/libbdevid.so.*
