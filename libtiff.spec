%define major 5
%define libname %mklibname tiff %{major}
%define develname %mklibname tiff -d
%define staticdevelname %mklibname tiff -d -s

Summary:	A library of functions for manipulating TIFF format image files
Name:		libtiff
Version:	4.0.2
Release:	1
License:	BSD-like
Group:		System/Libraries
URL:		http://www.remotesensing.org/libtiff/
Source0:	ftp://ftp.remotesensing.org/pub/libtiff/tiff-%{version}.tar.gz
Patch1:		tiff-3.9.1-no_contrib.diff
BuildRequires:	autoconf automake libtool m4
BuildRequires:	jbig-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(glut)
BuildRequires:	zlib-devel

%description
The libtiff package contains a library of functions for manipulating TIFF
(Tagged Image File Format) image format files. TIFF is a widely used file
format for bitmapped images. TIFF files usually end in the .tif extension
and they are often quite large.

%package	progs
Summary:	Binaries needed to manipulate TIFF format image files
Group:		Graphics
Requires:	%{libname} = %{version}

%description	progs
This package provides binaries needed to manipulate TIFF format image files.

%package -n	%{libname}
Summary:	A library of functions for manipulating TIFF format image files
Group:		System/Libraries

%description -n	%{libname}
The libtiff package contains a library of functions for manipulating TIFF
(Tagged Image File Format) image format files. TIFF is a widely used file
format for bitmapped images. TIFF files usually end in the .tif extension
and they are often quite large.

%package -n	%{develname}
Summary:	Development tools for programs which will use the libtiff library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	tiff-devel = %{version}-%{release}
Obsoletes:	%{mklibname tiff 3 -d}

%description -n	%{develname}
This package contains the header files and .so libraries for developing
programs which will manipulate TIFF format image files using the libtiff
library.

%prep

%setup -q -n tiff-%{version}
%patch1 -p1

# cleanup
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# Use build system's libtool.m4, not the one in the package.
rm -f libtool.m4

libtoolize --force  --copy
aclocal -I . -I m4
automake --add-missing --copy
autoconf
autoheader

%build
export LDFLAGS="%{ldflags}"
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

%configure2_5x

# the "JPEG 8/12 bit dual mode" is too messy..., maybe later?
# http://trac.osgeo.org/gdal/wiki/TIFF12BitJPEG
# --with-jpeg12-include-dir=
# --with-jpeg12-lib=

%make

%check
LD_LIBRARY_PATH=$PWD:$LD_LIBRARY_PATH make check

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/{%{_bindir},%{_datadir}}

rm -rf installed_docs

%makeinstall LIBTIFF_DOCDIR=`pwd`/installed_docs

install -m0644 libtiff/tiffiop.h %{buildroot}%{_includedir}/
install -m0644 libtiff/tif_dir.h %{buildroot}%{_includedir}/

# multiarch policy
%multiarch_includes %{buildroot}%{_includedir}/tiffconf.h

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files progs
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc installed_docs/*
%{_includedir}/*.h*
%{multiarch_includedir}/tiffconf.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
