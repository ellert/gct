%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gsi-cert-utils
%global soname 0
%global _name %(echo %{name} | tr - _)
Version:	10.11
Release:	1%{?dist}
Summary:	Grid Community Toolkit - Globus GSI Cert Utils Library

Group:		System Environment/Libraries
License:	%{?suse_version:Apache-2.0}%{!?suse_version:ASL 2.0}
URL:		https://github.com/gridcf/gct/
Source:		%{_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc
BuildRequires:	globus-common-devel >= 14
BuildRequires:	globus-openssl-module-devel >= 3
BuildRequires:	globus-gsi-openssl-error-devel >= 2
%if %{?suse_version}%{!?suse_version:0}
BuildRequires:	libopenssl-devel
%else
BuildRequires:	openssl-devel
%endif
BuildRequires:	openssl
BuildRequires:	doxygen
%if ! %{?suse_version}%{!?suse_version:0}
BuildRequires:	perl-generators
%endif

%if %{?suse_version}%{!?suse_version:0}
%global mainpkg lib%{_name}%{soname}
%global nmainpkg -n %{mainpkg}
%else
%global mainpkg %{name}
%endif

%if %{?nmainpkg:1}%{!?nmainpkg:0}
%package %{?nmainpkg}
Summary:	Grid Community Toolkit - Globus GSI Cert Utils Library
Group:		System Environment/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}
%endif

%package progs
Summary:	Grid Community Toolkit - Globus GSI Cert Utils Library Programs
Group:		Applications/Internet
Requires:	openssl
#		Obsolete dropped packages from Globus Toolkit 5.2.0
Obsoletes:	globus-openssl-progs < 6
#		Obsolete dropped packages from Globus Toolkit 6.0
Obsoletes:	globus-openssl-module-progs < 4
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif

%package devel
Summary:	Grid Community Toolkit - Globus GSI Cert Utils Library Development Files
Group:		Development/Libraries
Requires:	%{mainpkg}%{?_isa} = %{version}-%{release}

%package doc
Summary:	Grid Community Toolkit - Globus GSI Cert Utils Library Documentation Files
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif

%if %{?nmainpkg:1}%{!?nmainpkg:0}
%description %{?nmainpkg}
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{mainpkg} package contains:
Globus GSI Cert Utils Library
%endif

%description
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name} package contains:
Globus GSI Cert Utils Library

%description progs
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-progs package contains:
Globus GSI Cert Utils Library Programs

%description devel
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-devel package contains:
Globus GSI Cert Utils Library Development Files

%description doc
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-doc package contains:
Globus GSI Cert Utils Library Documentation Files

%prep
%setup -q -n %{_name}-%{version}

%build
export GLOBUS_VERSION=6.2
%configure --disable-static \
	   --includedir=%{_includedir}/globus \
	   --libexecdir=%{_datadir}/globus \
	   --docdir=%{_pkgdocdir}

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool archives (.la files)
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%check
make %{?_smp_mflags} check VERBOSE=1

%post %{?nmainpkg} -p /sbin/ldconfig

%postun %{?nmainpkg} -p /sbin/ldconfig

%files %{?nmainpkg}
%defattr(-,root,root,-)
%{_libdir}/libglobus_gsi_cert_utils.so.*
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%files progs
%defattr(-,root,root,-)
%{_bindir}/grid-cert-info
%{_bindir}/grid-cert-request
%{_bindir}/grid-change-pass-phrase
%{_sbindir}/globus-update-certificate-dir
%{_sbindir}/grid-default-ca
%doc %{_mandir}/man1/grid-cert-info.1*
%doc %{_mandir}/man1/grid-cert-request.1*
%doc %{_mandir}/man1/grid-change-pass-phrase.1*
%doc %{_mandir}/man8/globus-update-certificate-dir.8*
%doc %{_mandir}/man8/grid-default-ca.8*
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/globus/*
%{_libdir}/libglobus_gsi_cert_utils.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%defattr(-,root,root,-)
%doc %{_mandir}/man3/*
%dir %{_pkgdocdir}
%dir %{_pkgdocdir}/html
%doc %{_pkgdocdir}/html/*
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%changelog
* Thu Jan 19 2023 Mischa Salle <msalle@nikhef.nl> - 10.11-1
- Fix parsing of ASN1 timestamps

* Sat May 07 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.10-1
- Can't use non-existing or non-accessible files as source for random data

* Mon Apr 11 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.9-1
- Add missing comma

* Fri Aug 20 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.8-1
- Typo fixes

* Wed Jun 03 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.7-1
- Use -nameopt sep_multiline to derive certificate subject string

* Mon Jun 01 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.6-1
- Fix format for grid-cert-info -issuer

* Tue Mar 17 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.5-1
- Remove old replace-version.xsl file

* Tue Mar 10 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.4-1
- Make makefiles exit sooner on errors

* Sat Jul 13 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.3-1
- Update additional old document references

* Wed Nov 21 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.2-1
- Doxygen fixes

* Mon Nov 05 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.1-2
- Bump GCT release version to 6.2

* Fri Oct 19 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.1-1
- Fix broken subject in grid-cert-request

* Sat Mar 31 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 10.0-1
- First Grid Community Toolkit release
- Remove support for openssl101e (RHEL5 is EOL)

* Fri Jan 06 2017 Globus Toolkit <support@globus.org> - 9.16-1
- Add const qualifier to avoid casting with OpensSL 1.1.0

* Thu Sep 08 2016 Globus Toolkit <support@globus.org> - 9.15-1
- Update for el.5 openssl101e, replace docbook with asciidoc

* Thu Aug 25 2016 Globus Toolkit <support@globus.org> - 9.14-4
- Updates for SLES 12

* Tue Aug 16 2016 Globus Toolkit <support@globus.org> - 9.14-1
- Updates for OpenSSL 1.1.0

* Tue May 03 2016 Globus Toolkit <support@globus.org> - 9.12-1
- Spelling

* Thu Aug 06 2015 Globus Toolkit <support@globus.org> - 9.11-2
- Add vendor

* Mon Jul 06 2015 Globus Toolkit <support@globus.org> - 9.11-1
- GT-606: fix encoding for CN=(limited) proxy
- GT-610: globus-gsi-cert-utils crash

* Wed Sep 24 2014 Globus Toolkit <support@globus.org> - 9.10-1
- Include more manpages for API
- Doxygen markup fixes
- Fix dependency version
- Fix typos and clarify some documentation
- Quiet some autoconf/automake warnings

* Fri Aug 22 2014 Globus Toolkit <support@globus.org> - 9.9-1
- Merge fixes from ellert-globus_6_branch

* Wed Aug 20 2014 Globus Toolkit <support@globus.org> - 9.8-2
- Fix Source path

* Mon Jun 09 2014 Globus Toolkit <support@globus.org> - 9.8-1
- Merge changes from Mattias Ellert

* Wed Jun 04 2014 Globus Toolkit <support@globus.org> - 9.7-1
- Handle bad CA choice better

* Tue May 27 2014 Globus Toolkit <support@globus.org> - 9.6-1
- Use package-named config.h

* Fri Apr 18 2014 Globus Toolkit <support@globus.org> - 9.5-1
- Version bump for consistency

* Thu Feb 27 2014 Globus Toolkit <support@globus.org> - 9.4-1
- Test Fixes

* Tue Feb 25 2014 Globus Toolkit <support@globus.org> - 9.3-1
- Packaging Fixes

* Mon Feb 10 2014 Globus Toolkit <support@globus.org> - 9.2-1
- Packaging fixes

* Fri Jan 31 2014 Globus Toolkit <support@globus.org> - 9.1-1
- Win32 build problem

* Tue Jan 21 2014 Globus Toolkit <support@globus.org> - 9.0-1
- Repackage for GT6 without GPT

* Thu Oct 10 2013 Globus Toolkit <support@globus.org> - 8.6-1
- GT-445: Doxygen fixes

* Mon Jul 08 2013 Globus Toolkit <support@globus.org> - 8.5-4
- openssl-libs dep for newer fedora

* Wed Jun 26 2013 Globus Toolkit <support@globus.org> - 8.5-3
- GT-424: New Fedora Packaging Guideline - no %%_isa in BuildRequires

* Tue Mar 19 2013 Globus Toolkit <support@globus.org> - 8.5-2
- Update sharing to support a full cert chain at logon

* Mon Mar 18 2013 Globus Toolkit <support@globus.org> - 8.5-1
- GT-354: Compatibility with automake 1.13

* Tue Mar 05 2013 Globus Toolkit <support@globus.org> - 8.4-1
- GT-365: Switch sharing user identification from DN to CERT

* Wed Feb 20 2013 Globus Toolkit <support@globus.org> - 8.3-7
- Workaround missing F18 doxygen/latex dependency

* Mon Nov 26 2012 Globus Toolkit <support@globus.org> - 8.3-6
- 5.2.3

* Mon Jul 16 2012 Joseph Bester <bester@mcs.anl.gov> - 8.3-5
- GT 5.2.2 final

* Fri Jun 29 2012 Joseph Bester <bester@mcs.anl.gov> - 8.3-4
- GT 5.2.2 Release

* Wed May 09 2012 Joseph Bester <bester@mcs.anl.gov> - 8.3-3
- RHEL 4 patches

* Fri May 04 2012 Joseph Bester <bester@mcs.anl.gov> - 8.3-2
- SLES 11 patches

* Thu Mar 29 2012 Joseph Bester <bester@mcs.anl.gov> - 8.3-1
- RIC-248: grid-cert-request can't use non-default CA when a default isn't set

* Thu Feb 23 2012 Joseph Bester <bester@mcs.anl.gov> - 8.2-2
- RIC-237: globus-gsi-cert-utils-progs RPM has missing dependency

* Tue Feb 14 2012 Joseph Bester <bester@mcs.anl.gov> - 8.2-1
- RIC-226: Some dependencies are missing in GPT metadata
- RIC-227: Potentially unsafe format strings in GSI
- RIC-231: grid-cert-request prints incorrect path in diagnostic message

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 8.1-4
- Update for 5.2.0 release

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 8.1-3
- Last sync prior to 5.2.0

* Tue Oct 11 2011 Joseph Bester <bester@mcs.anl.gov> - 8.1-2
- Add explicit dependencies on >= 5.2 libraries

* Thu Oct 06 2011 Joseph Bester <bester@mcs.anl.gov> - 8.1-1
- Add backward-compatibility aging

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 8.0-2
- Update for 5.1.2 release

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.6-1
- Update to Globus Toolkit 5.0.2
- Drop patch globus-gsi-cert-utils-oid.patch (fixed upstream)

* Mon May 31 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-2
- Fix OID registration pollution

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-1
- Update to Globus Toolkit 5.0.1

* Fri Jan 22 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.4-1
- Update to Globus Toolkit 5.0.0

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 5.5-4
- rebuilt with new openssl

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-3
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch

* Wed Jun 03 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-2
- Update to official Fedora Globus packaging guidelines

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-1
- Change defines to globals
- Remove explicit requires on library packages

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-0.4
- Add s390x to the list of 64 bit platforms
- Update to upstream update release 5.5
- Drop the environment elimination patch (accepted upstream)

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-0.3
- Adapt to updated GPT package

* Tue Oct 14 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-0.2
- Update to Globus Toolkit 4.2.1

* Mon Jul 14 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.1-0.1
- Autogenerated
