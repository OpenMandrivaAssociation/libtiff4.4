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
Release:	%mkrel 16
License:	BSD-like
Group:		System/Libraries
URL:		http://www.libtiff.org/
Source0:	ftp://ftp.remotesensing.org/pub/libtiff/tiff-%{version}.tar.bz2
Source1:	ftp://ftp.remotesensing.org/pub/libtiff/pics-%{picver}.tar.bz2
Patch0:		tiffsplit-overflow.patch
Patch1:		tiff.tiff2pdf-octal-printf.patch
Patch2:		tiff-3.8.2-goo-sec.diff
Patch3:		libtiff-3.8.2-lzw-bugs.patch
Patch4:		tiff-3.8.2-format_not_a_string_literal_and_no_format_arguments.diff
Patch5:		tiff-3.8.2-mdvbz50788.diff
Patch6:		tiff-3.8.2-CVE-2009-2285.patch
Patch7:		tiff-3.8.2-CVE-2009-2347.patch
BuildRequires:	libjpeg-devel
BuildRequires:	zlib-devel
BuildRequires:	chrpath
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch3 -p1 -b .cve-2008-2327
%patch4 -p0 -b .format_not_a_string_literal_and_no_format_arguments
%patch5 -p0 -b .mdvbz50788
%patch6 -p1 -b .CVE-2009-2285
%patch7 -p1 -b .CVE-2009-2347

# cleanup
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
#%%{?__cputoolize: %{__cputoolize}}

export LDFLAGS="%{ldflags}"
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

%configure2_5x \
    --with-GCOPTS="%{optflags}"

%make

%check
make check

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

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

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


