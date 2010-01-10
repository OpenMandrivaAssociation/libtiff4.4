%define major 3
%define libname %mklibname tiff %{major}
%define develname %mklibname tiff -d
%define staticdevelname %mklibname tiff -d -s

Summary:	A library of functions for manipulating TIFF format image files
Name:		libtiff
Version:	3.9.2
Release:	%mkrel 2
License:	BSD-like
Group:		System/Libraries
URL:		http://www.remotesensing.org/libtiff/
Source0:	ftp://ftp.remotesensing.org/pub/libtiff/tiff-%{version}.tar.gz
Patch1:		tiff-3.9.1-no_contrib.diff
BuildRequires:	jbig-devel
BuildRequires:	libjpeg-devel
BuildRequires:	mesaglut-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The libtiff package contains a library of functions for manipulating TIFF
(Tagged Image File Format) image format files. TIFF is a widely used file
format for bitmapped images. TIFF files usually end in the .tif extension
and they are often quite large.

%package	progs
Summary:	Binaries needed to manipulate TIFF format image files
Group:		Graphics
Requires:	%{libname} = %{version}
Obsoletes:	libtiff3-progs
Provides:	libtiff3-progs = %{version}-%{release}

%description	progs
This package provides binaries needed to manipulate TIFF format image files.

%package -n	%{libname}
Summary:	A library of functions for manipulating TIFF format image files
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

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

%package -n	%{staticdevelname}
Summary:	Static libraries for programs which will use the libtiff library
Group:		Development/C
Requires:	%{develname} = %{version}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	tiff-static-devel = %{version}-%{release}
Obsoletes:	%{mklibname tiff 3 -d -s}

%description -n	%{staticdevelname}
This package contains the static libraries for developing
programs which will manipulate TIFF format image files using the libtiff
library.

%prep

%setup -q -n tiff-%{version}
%patch1 -p1

# cleanup
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
export LDFLAGS="%{ldflags}"
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

%configure2_5x

%make

%check
make check

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/{%{_bindir},%{_datadir}}

rm -rf installed_docs

%makeinstall LIBTIFF_DOCDIR=`pwd`/installed_docs

install -m0644 libtiff/tiffiop.h %{buildroot}%{_includedir}/
install -m0644 libtiff/tif_dir.h %{buildroot}%{_includedir}/

# multiarch policy
%multiarch_includes %{buildroot}%{_includedir}/tiffconf.h

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files progs
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root,755)
%doc installed_docs/*
%{_includedir}/*.h*
%{multiarch_includedir}/tiffconf.h
%{_libdir}/*.la
%{_libdir}/*.so
%{_mandir}/man3/*

%files -n %{staticdevelname}
%defattr(-,root,root,-)
%doc COPYRIGHT README TODO VERSION
%{_libdir}/*.a
