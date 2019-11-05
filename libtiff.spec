%define major 5
%define libname %mklibname tiff %{major}
%define libxx %mklibname tiffxx %{major}
%define devname %mklibname tiff -d
%bcond_with bootstrap

%global optflags %{optflags} -O3

# (tpg) enable PGO build
%bcond_without pgo

Summary:	A library of functions for manipulating TIFF format image files
Name:		libtiff
Version:	4.1.0
Release:	1
License:	BSD-like
Group:		System/Libraries
Url:		http://www.remotesensing.org/libtiff/
Source0:	http://download.osgeo.org/libtiff/tiff-%{version}.tar.gz
Patch1:		tiff-3.9.1-no_contrib.diff
BuildRequires:	libtool
BuildRequires:	jbig-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(ice)
%if %{without bootstrap}
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gl)
%endif
BuildRequires:	pkgconfig(zlib)

%description
The libtiff package contains a library of functions for manipulating TIFF
(Tagged Image File Format) image format files. TIFF is a widely used file
format for bitmapped images. TIFF files usually end in the .tif extension
and they are often quite large.

%package	progs
Summary:	Binaries needed to manipulate TIFF format image files
Group:		Graphics

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

%package -n	%{libxx}
Summary:	A library of functions for manipulating TIFF format image files
Group:		System/Libraries
Conflicts:	%{_lib}tiff5 < 4.0.3-2

%description -n	%{libxx}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Development tools for programs which will use the libtiff library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libxx} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	tiff-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the header files and .so libraries for developing
programs which will manipulate TIFF format image files using the libtiff
library.

%prep
%autosetup -n tiff-%{version} -p1

# cleanup
for i in $(find . -type d -name CVS) $(find . -type f -name .cvs\*) $(find . -type f -name .#\*); do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# Use build system's libtool.m4, not the one in the package.
rm -f libtool.m4
autoreconf -fi

%build
export LDFLAGS="%{ldflags}"
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="%{optflags}"

%if %{with pgo}
export LLVM_PROFILE_FILE=%{name}-%p.profile.d
export LD_LIBRARY_PATH="$(pwd)"
CFLAGS="%{optflags} -fprofile-instr-generate" \
CXXFLAGS="%{optflags} -fprofile-instr-generate" \
FFLAGS="$CFLAGS_PGO" \
FCFLAGS="$CFLAGS_PGO" \
LDFLAGS="%{ldflags} -fprofile-instr-generate" \
%configure \
	--disable-static \
	--enable-ld-version-script

%make_build
make check

unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile *.profile.d

make clean

CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
%endif
%configure \
	--disable-static \
	--enable-ld-version-script

%make_build

%install
mkdir -p %{buildroot}/{%{_bindir},%{_datadir}}
rm -rf installed_docs
%make_install

install -m0644 libtiff/tiffiop.h %{buildroot}%{_includedir}/
install -m0644 libtiff/tif_dir.h %{buildroot}%{_includedir}/

%files progs
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libtiff.so.%{major}*

%files -n %{libxx}
%{_libdir}/libtiffxx.so.%{major}*

%files -n %{devname}
%doc %{_docdir}/tiff-%{version}
%{_includedir}/*.h*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
