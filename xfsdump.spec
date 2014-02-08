%bcond_without	uclibc

Summary:	Administrative utilities for the XFS filesystem
Name:		xfsdump
Version:	3.1.1
Release:	2
License:	GPLv2
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/cmd_tars/%{name}-%{version}.tar.gz

BuildRequires:	libtool
BuildRequires:	attr-devel
BuildRequires:	gettext-devel
BuildRequires:	xfsprogs-devel
BuildRequires:	pkgconfig(ext2fs) 
BuildRequires:	pkgconfig(ncursesw)
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-16
%endif

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

%package -n	uclibc-%{name}
Summary:	Administrative utilities for the XFS filesystem (uClibc build)
Group:		System/Kernel and hardware

%description -n	uclibc-%{name}
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
%if %{with uclibc}
mkdir .uclibc
pushd .uclibc
cp -a ../* .
popd
%endif

# make it lib64 aware, better make a patch?
#perl -pi -e "/(libuuid|pkg_s?lib_dir)=/ and s|/lib\b|/%{_lib}|;" configure

%build
%if %{with uclibc}
pushd .uclibc
%uclibc_configure \
		OPTIMIZER="%{uclibc_cflags}" \
		--enable-gettext=yes
%make DEBUG="-DNDEBUG"
popd
%endif

%configure2_5x	OPTIMIZER="%{optflags}" \
		--enable-gettext=yes
%make DEBUG="-DNDEBUG"

%install
%if %{with uclibc}
%makeinstall_std -C .uclibc
# something is fudged here..
rm %{buildroot}%{uclibc_root}%{_sbindir}/xfs{dump,restore}
install -m755 .uclibc/dump/xfsdump -D %{buildroot}%{uclibc_root}/sbin/xfsdump
install -m755 .uclibc/restore/xfsrestore -D %{buildroot}%{uclibc_root}/sbin/xfsrestore

# for coherency
ln %{buildroot}%{uclibc_root}/sbin/{xfsdump,dump.xfs}
ln %{buildroot}%{uclibc_root}/sbin/{xfsrestore,restore.xfs}
%endif

%makeinstall_std

# nuke files already packaged as %doc
rm -rf %{buildroot}%{_datadir}/doc/xfsdump/

# for coherency, rename xfsdump|xfsrestore to dump|restore.xfs
ln %{buildroot}/sbin/{xfsdump,dump.xfs}
ln %{buildroot}/sbin/{xfsrestore,restore.xfs}
ln -sf xfsdump.8%{_extension} %{buildroot}%{_mandir}/man8/dump.xfs.8%{_extension}
ln -sf xfsrestore.8%{_extension} %{buildroot}%{_mandir}/man8/restore.xfs.8%{_extension}

%find_lang %{name}

%files -f %{name}.lang
%doc doc/CHANGES.gz doc/README.xfsdump
/sbin/*
%{_sbindir}/*
%{_mandir}/*/*

%files -n uclibc-%{name}
%{uclibc_root}/sbin/*
%{uclibc_root}%{_sbindir}/*

