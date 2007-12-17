%define	name	xfsdump
%define	version	2.2.42
%define	release	%mkrel 4

Summary:	Administrative utilities for the XFS filesystem
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-1.tar.bz2
Patch0:		xfsdump-CVE-2007-2654.patch
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	attr-devel
BuildRequires:	libext2fs-devel
BuildRequires:	xfs-devel
BuildRequires:	dm-devel
BuildRequires:	ncurses-devel
BuildRequires:	libtool

%description
The xfsdump package contains xfsdump, xfsrestore and a number of
other utilities for administering XFS filesystems.

xfsdump examines files in a filesystem, determines which need to be
backed up, and copies those files to a specified disk, tape or other
storage medium.  It uses XFS-specific directives for optimizing the
dump of an XFS filesystem, and also knows how to backup XFS extended
attributes.  Backups created with xfsdump are "endian safe" and can
thus be transfered between Linux machines of different architectures
and also between IRIX machines.

xfsrestore performs the inverse function of xfsdump; it can restore a
full backup of a filesystem.  Subsequent incremental backups can then
be layered on top of the full backup.  Single files and directory
subtrees may be restored from full or partial backups.

%prep
%setup -q
%patch0 -p0
# make it lib64 aware, better make a patch?
#perl -pi -e "/(libuuid|pkg_s?lib_dir)=/ and s|/lib\b|/%{_lib}|;" configure

%build
aclocal && autoconf
%configure2_5x --libdir=/%{_lib}  --sbindir=/sbin --bindir=/usr/sbin
%make DEBUG=-DNDEBUG OPTIMIZER="${RPM_OPT_FLAGS}"

%install
rm -rf $RPM_BUILD_ROOT
make install DIST_ROOT=%{buildroot}/

# nuke files already packaged as %doc
rm -rf %{buildroot}%{_datadir}/doc/xfsdump/

# for coerency, rename xfsdump|xfsrestore to dump|restore.xfs
mv %{buildroot}/sbin/xfsdump %{buildroot}/sbin/dump.xfs
mv %{buildroot}/sbin/xfsrestore %{buildroot}/sbin/restore.xfs
ln -sf /sbin/dump.xfs %{buildroot}/sbin/xfsdump
ln -sf /sbin/restore.xfs %{buildroot}/sbin/xfsrestore
ln -sf %{_mandir}/man8/xfsdump.8 %{buildroot}%{_mandir}/man8/dump.xfs
ln -sf %{_mandir}/man8/xfsrestore.8 %{buildroot}%{_mandir}/man8/restore.xfs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/COPYING doc/INSTALL doc/PORTING doc/README.xfsdump
/sbin/*
%{_sbindir}/*
%{_mandir}/*/*


