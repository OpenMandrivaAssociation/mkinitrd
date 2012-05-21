Summary:	Creates an initial ramdisk image for preloading modules
Name:		mkinitrd
Version:	6.0.93
Release:	24
License:	GPLv2+
URL:		http://www.redhat.com/
Group: 		System/Kernel and hardware
Source0: 	mkinitrd-%{version}.tar.bz2
# Mandriva sources
Source100:	mkinitrd-sysconfig

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
# (proyvind): /usr/libexec/initrd-functions is located in non-sense directory
# 	      for when being required by /sbin/mkinitrd,
Patch151: mkinitrd-6.0.93-required-initrd-functions-cannot-be-on-usr.patch
Patch201: 0001-Do-not-load-KMS-drivers-when-booted-with-nokmsboot-o.patch
Patch202: 0002-Whitelist-nouveau-and-radeon-drivers.patch
Patch203: 0003-Fix-build-with-gcc4.6.patch
Patch204: mkinitrd-6.0.93-link.patch
# found at MGA
Patch205: mkinitrd-usb-input-usbhid-only.patch
Patch206: mkinitrd-6.0.93-use-oom_score_adj.patch
Patch207: mkinitrd-6.0.93-xz-support.patch

BuildRequires:	python
BuildRequires:	util-linux-ng
BuildRequires:	elfutils-devel
BuildRequires:	python-devel
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	pkgconfig(libparted)
BuildRequires:	pkgconfig(popt)

Requires:	coreutils
Requires:	cpio
Requires:	diffutils
Requires:	e2fsprogs
Requires:	filesystem
Requires:	findutils
Requires:	grep
Requires:	gzip
Requires:	initscripts
Requires:	kpartx
Requires:	mktemp
Requires:	mount
Requires:	module-init-tools >= 3.3-pre11
Requires:	nash = %{version}-%{release}
Requires:	tar
Requires(post,postun):	update-alternatives
Requires:	util-linux-ng
%ifarch ppc
Requires:	ppc64-utils >= 0.3-1
%endif

%description
mkinitrd creates filesystem images for use as initial ram filesystem
(initramfs) images.  These images are used to find and mount the root
filesystem.

%package devel
Summary: C header files and library for functionality exported by libnash
Group: Development/C
Requires: mkinitrd
Requires: nash = %{version}-%{release}

%package -n libbdevid-python
Summary: Python bindings for libbdevid
Group: Development/Other
Requires: python
Requires: nash = %{version}-%{release}

%package -n nash
Summary: Nash shell
Group: System/Kernel and hardware
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
#export LDFLAGS="%ldflags"
cd bdevid
make libbdevid.so LIB=%{_lib} LDFLAGS="%ldflags"
cd ..
export LDFLAGS="%ldflags"
make LIB=%{_lib}

%check
make LIB=%{_lib} test

%install
make LIB=%{_lib} DESTDIR=%{buildroot} mandir=%{_mandir} install
rm -f %{buildroot}/sbin/bdevid %{buildroot}/%{_includedir}/blkent.h

# Mandriva
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE100} %{buildroot}%{_sysconfdir}/sysconfig/mkinitrd

rm -f %{buildroot}/sbin/installkernel
rm -f %{buildroot}/lib/mkinitrd/mkliveinitrd
mv -f %{buildroot}/sbin/mkinitrd %{buildroot}/sbin/mkinitrd-mkinitrd
mv -f %{buildroot}/sbin/lsinitrd %{buildroot}/sbin/lsinitrd-mkinitrd

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
%attr(755,root,root) /sbin/mkinitrd-mkinitrd
%attr(644,root,root) %{_mandir}/man8/mkinitrd.8*
# Mandriva
%config(noreplace) %{_sysconfdir}/sysconfig/mkinitrd
%dir /lib/mkinitrd
/lib/mkinitrd/functions

%files devel
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
%attr(644,root,root) %{_mandir}/man8/nash.8*
%attr(755,root,root) /sbin/nash
%attr(755,root,root) /sbin/lsinitrd-mkinitrd
/%{_lib}/bdevid
%{_libdir}/libnash.so.*
%{_libdir}/libbdevid.so.*

