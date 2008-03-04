%define name	libtiff
%define	version	3.8.2
%define	picver	3.8.0

%define lib_version	3.8.2
%define lib_major	3
%define lib_name_orig	%mklibname tiff
%define lib_name	%{lib_name_orig}%{lib_major}

Summary:	A library of functions for manipulating TIFF format image files
Name:		%{name}
Version:	%{version}
Release:	%mkrel 10
License:	BSD-like
Group:		System/Libraries
URL:		http://www.libtiff.org/
Source0:	ftp://ftp.remotesensing.org/pub/libtiff/tiff-%{version}.tar.bz2
Source1:	ftp://ftp.remotesensing.org/pub/libtiff/pics-%{picver}.tar.bz2
Patch0:		tiffsplit-overflow.patch
Patch1:		tiff.tiff2pdf-octal-printf.patch
Patch2:		tiff-3.8.2-goo-sec.diff

BuildRequires:	libjpeg-devel
BuildRequires:	zlib-devel
BuildRequires:	chrpath
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
The libtiff package contains a library of functions for manipulating TIFF
(Tagged Image File Format) image format files. TIFF is a widely used file
format for bitmapped images. TIFF files usually end in the .tif extension
and they are often quite large.

%package	progs
Summary:	Binaries needed to manipulate TIFF format image files
Group:		Graphics
Requires:	%{lib_name} = %{version}
Obsoletes:	libtiff3-progs
Provides:	libtiff3-progs = %{version}-%{release}

%description	progs
This package provides binaries needed to manipulate TIFF format image files.

%package -n	%{lib_name}
Summary:	A library of functions for manipulating TIFF format image files
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n	%{lib_name}
The libtiff package contains a library of functions for manipulating TIFF
(Tagged Image File Format) image format files. TIFF is a widely used file
format for bitmapped images. TIFF files usually end in the .tif extension
and they are often quite large.

%package -n	%{lib_name}-devel
Summary:	Development tools for programs which will use the libtiff library
Group:		Development/C
Requires:	%{lib_name} = %{version}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	tiff-devel = %{version}-%{release}

%description -n	%{lib_name}-devel
This package contains the header files and .so libraries for developing
programs which will manipulate TIFF format image files using the libtiff
library.

%package -n	%{lib_name}-static-devel
Summary:	Static libraries for programs which will use the libtiff library
Group:		Development/C
Requires:	%{lib_name}-devel = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	tiff-static-devel = %{version}-%{release}

%description -n	%{lib_name}-static-devel
This package contains the static libraries for developing
programs which will manipulate TIFF format image files using the libtiff
library.

%prep

%setup -q -n tiff-%{version} -a 1
ln -s pics-* pics
%patch0 -p1 -b .cve-2006-2656
%patch1 -p1 -b .cve-2006-2193
%patch2 -p1 -b .cve-2006-3459-thru-3465

%build
find . -type 'd' -name 'CVS' | xargs rm -fr
%{?__cputoolize: %{__cputoolize}}
./configure \
	--with-GCOPTS="$RPM_OPT_FLAGS" \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} \
	--includedir=%{_includedir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libdir} \
        --localstatedir=%{_localstatedir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir}

%make

make test

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/{%{_bindir},%{_datadir}}

%makeinstall

install -m0644 libtiff/tiffiop.h %{buildroot}%{_includedir}/
install -m0644 libtiff/tif_dir.h %{buildroot}%{_includedir}/

# let %doc handle this
rm -fr %{buildroot}%{_docdir}/tiff-%{version}

# multiarch policy
%multiarch_includes %{buildroot}%{_includedir}/tiffconf.h

# rpmlint
chrpath -d %{buildroot}%{_bindir}/*
chrpath -d %{buildroot}%{_libdir}/libtiffxx.so.%{version}

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files progs
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root,755)
%doc COPYRIGHT README TODO VERSION html
%{_includedir}/*.h*
%{multiarch_includedir}/tiffconf.h
%{_libdir}/*.la
%{_libdir}/*.so
%{_mandir}/man3/*

%files -n %{lib_name}-static-devel
%defattr(-,root,root,-)
%doc COPYRIGHT README TODO VERSION
%{_libdir}/*.a


