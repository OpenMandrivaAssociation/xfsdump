Summary:	Administrative utilities for the XFS filesystem
Name:		xfsdump
Version:	3.1.0
Release:	%mkrel 1
Source0:	ftp://oss.sgi.com/projects/xfs/cmd_tars/%{name}-%{version}.tar.gz
License:	GPLv2
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	attr-devel
BuildRequires:	ext2fs-devel
BuildRequires:	xfsprogs-devel
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

# make it lib64 aware, better make a patch?
#perl -pi -e "/(libuuid|pkg_s?lib_dir)=/ and s|/lib\b|/%{_lib}|;" configure

%build
export DEBUG="-DNDEBUG"
export OPTIMIZER="%{optflags}"
%configure2_5x
%make DEBUG="-DNDEBUG" OPTIMIZER="%{optflags}"

%install
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

%files
%doc doc/CHANGES.gz doc/COPYING doc/INSTALL doc/README.xfsdump
/sbin/*
%{_sbindir}/*
%{_mandir}/*/*
