%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-xio-gridftp-multicast
%global _name %(echo %{name} | tr - _)
Version:	2.2
Release:	1%{?dist}
Summary:	Grid Community Toolkit - Globus XIO GridFTP Multicast Driver

Group:		System Environment/Libraries
License:	%{?suse_version:Apache-2.0}%{!?suse_version:ASL 2.0}
URL:		https://github.com/gridcf/gct/
Source:		%{_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc
BuildRequires:	globus-common-devel >= 14
BuildRequires:	globus-xio-devel >= 3
BuildRequires:	globus-ftp-client-devel >= 7

%if %{?suse_version}%{!?suse_version:0}
%global mainpkg libglobus_xio_gridftp_multicast_driver
%global nmainpkg -n %{mainpkg}
%else
%global mainpkg %{name}
%endif

%if %{?nmainpkg:1}%{!?nmainpkg:0}
%package %{?nmainpkg}
Summary:	Grid Community Toolkit - Globus XIO GridFTP Multicast Driver
Group:		System Environment/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}
%endif

%package devel
Summary:	Grid Community Toolkit - Globus XIO GridFTP Multicast Driver Development Files
Group:		Development/Libraries
Requires:	%{mainpkg}%{?_isa} = %{version}-%{release}

%if %{?nmainpkg:1}%{!?nmainpkg:0}
%description %{?nmainpkg}
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{mainpkg} package contains:
Globus XIO GridFTP Multicast Driver
%endif

%description
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name} package contains:
Globus XIO GridFTP Multicast Driver

%description devel
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-devel package contains:
Globus XIO GridFTP Multicast Driver Development Files

%prep
%setup -q -n %{_name}-%{version}

%build
%configure --disable-static \
	   --includedir=%{_includedir}/globus \
	   --libexecdir=%{_datadir}/globus \
	   --docdir=%{_pkgdocdir}

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool archives (.la files)
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%post %{?nmainpkg} -p /sbin/ldconfig

%postun %{?nmainpkg} -p /sbin/ldconfig

%files %{?nmainpkg}
%defattr(-,root,root,-)
# This is a loadable module (plugin)
%{_libdir}/libglobus_xio_gridftp_multicast_driver.so
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/globus/*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Mar 11 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.2-1
- Fix some compiler warnings

* Thu Jul 18 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.1-1
- Add AC_CONFIG_MACRO_DIR and ACLOCAL_AMFLAGS

* Sat Mar 31 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.0-1
- First Grid Community Toolkit release

* Thu Sep 08 2016 Globus Toolkit <support@globus.org> - 1.7-4
- Rebuild after changes for el.5 with openssl101e

* Fri Aug 26 2016 Globus Toolkit <support@globus.org> - 1.7-3
- Updates for SLES 12

* Sat Aug 20 2016 Globus Toolkit <support@globus.org> - 1.7-1
- Update bug report URL

* Thu Aug 06 2015 Globus Toolkit <support@globus.org> - 1.6-2
- Add vendor

* Tue Jul 14 2015 Globus Toolkit <support@globus.org> - 1.6-1
- Remove dead code
- Fix uninitialized variables
- Fix string parsing error

* Fri Aug 22 2014 Globus Toolkit <support@globus.org> - 1.5-1
- Merge fixes from ellert-globus_6_branch

* Wed Aug 20 2014 Globus Toolkit <support@globus.org> - 1.4-2
- Fix Source path

* Mon Jun 09 2014 Globus Toolkit <support@globus.org> - 1.4-1
- Merge changes from Mattias Ellert

* Tue May 06 2014 Globus Toolkit <support@globus.org> - 1.3-1
- Don't version dynamic module

* Fri Apr 18 2014 Globus Toolkit <support@globus.org> - 1.2-1
- Version bump for consistency

* Mon Feb 17 2014 Globus Toolkit <support@globus.org> - 1.1-1
- Packaging fixes

* Mon Feb 17 2014 Globus Toolkit <support@globus.org> - 1.0-2
- Packaging fixes

* Wed Jan 22 2014 Globus Toolkit <support@globus.org> - 1.0-1
- Repackage for GT6 without GPT

* Wed Jun 26 2013 Globus Toolkit <support@globus.org> - 2.2-7
- GT-424: New Fedora Packaging Guideline - no %%_isa in BuildRequires

* Tue Mar 05 2013 Globus Toolkit <support@globus.org> - 2.2-6
- Add missing build dependency

* Mon Nov 26 2012 Globus Toolkit <support@globus.org> - 2.2-5
- 5.2.3

* Mon Jul 16 2012 Joseph Bester <bester@mcs.anl.gov> - 2.2-4
- GT 5.2.2 final

* Fri Jun 29 2012 Joseph Bester <bester@mcs.anl.gov> - 2.2-3
- GT 5.2.2 Release

* Wed May 09 2012 Joseph Bester <bester@mcs.anl.gov> - 2.2-2
- RHEL 4 patches

* Tue Feb 14 2012 Joseph Bester <bester@mcs.anl.gov> - 2.2-1
- RIC-226: Some dependencies are missing in GPT metadata
- RIC-229: Clean up GPT metadata

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 2.1-4
- Update for 5.2.0 release

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 2.1-3
- Last sync prior to 5.2.0

* Tue Oct 11 2011 Joseph Bester <bester@mcs.anl.gov> - 2.1-2
- Add explicit dependencies on >= 5.2 libraries

* Thu Oct 06 2011 Joseph Bester <bester@mcs.anl.gov> - 2.1-1
- Add backward-compatibility aging

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 2.0-2
- Update for 5.1.2 release

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.1-1
- Autogenerated
