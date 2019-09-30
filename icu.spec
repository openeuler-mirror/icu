Name:      icu
Version:   63.2
Release:   3
Summary:   International Components for Unicode
License:   MIT and UCD and Public Domain
URL:       http://site.icu-project.org/
Source0:   https://github.com/unicode-org/icu/releases/download/release-63-2/icu4c-63_2-src.tgz
Source1:   icu-config.sh

BuildRequires: gcc gcc-c++ doxygen autoconf python2 icu libicu-devel
Requires:      lib%{name} = %{version}-%{release}

Patch4:    gennorm2-man.patch
Patch5:    icuinfo-man.patch
%ifarch armv7hl
Patch100:  armv7hl-disable-tests.patch
%endif

%description
Tools and utilities for developing with icu.

%package -n libicu
Summary:   libs package for icu

%description -n libicu
libs package for icu
e
%package -n libicu-devel
Summary:    header files for libicu
Requires:   lib%{name} = %{version}-%{release} pkgconfig

%description -n libicu-devel
header files for libicu

%package_help

%{!?endian: %global endian %(%{__python} -c "import sys;print (0 if sys.byteorder=='big' else 1)")}
# " this line just fixes syntax highlighting for vim that is confused by the above and continues literal

%prep
%autosetup -n %{name} -p1

%build
pushd source
autoconf
CFLAGS='%optflags -fno-strict-aliasing'
CXXFLAGS='%optflags -fno-strict-aliasing'
# Endian: BE=0 LE=1
%if ! 0%{?endian}
CPPFLAGS='-DU_IS_BIG_ENDIAN=1'
%endif

OPTIONS='--with-data-packaging=library --disable-samples'
%if 0%{?debugtrace}
OPTIONS=$OPTIONS' --enable-debug --enable-tracing'
%endif
%configure $OPTIONS

sed -i 's|-nodefaultlibs -nostdlib||' config/mh-linux
sed -i 's| \$(docfilesdir)/installdox||' Makefile
sed -i '/^\s\+\$(INSTALL_DATA) \$(docsrchfiles) \$(DESTDIR)\$(docdir)\/\$(docsubsrchdir)\s*$/d' Makefile
test -f uconfig.h.prepend && sed -e '/^#define __UCONFIG_H__/ r uconfig.h.prepend' -i common/unicode/uconfig.h

sed -i -r 's|(PKGDATA_OPTS = )|\1-v |' data/Makefile

make %{?_smp_mflags} VERBOSE=1
make %{?_smp_mflags} doc


%install
rm -rf $RPM_BUILD_ROOT source/__docs
make %{?_smp_mflags} -C source install DESTDIR=$RPM_BUILD_ROOT
make %{?_smp_mflags} -C source install-doc docdir=__docs
chmod +x $RPM_BUILD_ROOT%{_libdir}/*.so.*
(
 cd $RPM_BUILD_ROOT%{_bindir}
 mv icu-config icu-config-%{__isa_bits}
)
install -p -m755 -D %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/icu-config

#Include previous icu version for temporary binary compatibility
cp -a %{_libdir}/libicu*.so* %{buildroot}%{_libdir}


%check
if grep -q @VERSION@ source/tools/*/*.8 source/tools/*/*.1 source/config/*.1; then
    exit 1
fi
make %{?_smp_mflags} -C source check


pushd source
LD_LIBRARY_PATH=lib:stubdata:tools/ctestfw:$LD_LIBRARY_PATH bin/uconv -l


%ldconfig_scriptlets libicu


%files
%defattr(-,root,root)
%license license.html LICENSE
%exclude %{_datadir}/%{name}/*/LICENSE
%{_bindir}/derb
%{_bindir}/gen*
%{_bindir}/makeconv
%{_bindir}/pkgdata
%{_bindir}/uconv
%{_sbindir}/*

%files -n libicu
%defattr(-,root,root)
%license license.html LICENSE
%{_libdir}/*.so.*

%files -n libicu-devel
%defattr(-,root,root)
%doc source/samples/
%{_bindir}/%{name}-config*
%{_bindir}/icuinfo
%{_includedir}/unicode
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/%{name}
%{_datadir}/%{name}/%{version}/install-sh
%{_datadir}/%{name}/%{version}/mkinstalldirs
%{_datadir}/%{name}/%{version}/config

%files help
%defattr(-,root,root)
%doc readme.html
%doc source/__docs/%{name}/html/*
%{_mandir}/man1/*
%{_mandir}/man8/*


%changelog
* Wed Sep 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 63.2-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC: provides libicu-devel(aarch64)

* Wed Sep 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 63.2-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add previous icu version for temporary binary compatibility

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 63.2-1
- Package init
