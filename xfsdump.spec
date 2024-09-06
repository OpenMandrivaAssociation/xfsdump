Summary:	Administrative utilities for the XFS filesystem
Name:		xfsdump
Version:	3.2.0
Release:	1
License:	GPLv2
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	https://kernel.org/pub/linux/utils/fs/xfs/xfsdump/%{name}-%{version}.tar.xz

BuildRequires:	libtool
BuildRequires:	attr-devel
BuildRequires:	gettext-devel
BuildRequires:	xfsprogs-devel
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(ncursesw)

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
make configure

# make it lib64 aware, better make a patch?
#perl -pi -e "/(libuuid|pkg_s?lib_dir)=/ and s|/lib\b|/%{_lib}|;" configure

%build
%configure OPTIMIZER="%{optflags}" \
		--enable-gettext=yes
%make DEBUG="-DNDEBUG"

%install
make install DIST_ROOT=%{buildroot}/

# nuke files already packaged as %doc
rm -rf %{buildroot}%{_datadir}/doc/xfsdump/

# for coherency, rename xfsdump|xfsrestore to dump|restore.xfs
ln %{buildroot}/sbin/{xfsdump,dump.xfs}
ln %{buildroot}/sbin/{xfsrestore,restore.xfs}
ln -sf xfsdump.8%{_extension} %{buildroot}%{_mandir}/man8/dump.xfs.8%{_extension}
ln -sf xfsrestore.8%{_extension} %{buildroot}%{_mandir}/man8/restore.xfs.8%{_extension}

%find_lang %{name}

%files -f %{name}.lang
%doc doc/README.xfsdump
/sbin/*
%{_sbindir}/*
%{_mandir}/*/*

