%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gsi-credential
%global soname 1
%global _name %(echo %{name} | tr - _)
Version:	8.3
Release:	1%{?dist}
Summary:	Grid Community Toolkit - Globus GSI Credential Library

Group:		System Environment/Libraries
License:	%{?suse_version:Apache-2.0}%{!?suse_version:ASL 2.0}
URL:		https://github.com/gridcf/gct/
Source:		%{_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc
BuildRequires:	globus-common-devel >= 14
BuildRequires:	globus-gsi-openssl-error-devel >= 2
BuildRequires:	globus-gsi-cert-utils-devel >= 8
BuildRequires:	globus-gsi-sysconfig-devel >= 5
BuildRequires:	globus-gsi-callback-devel >= 4
%if %{?suse_version}%{!?suse_version:0}
BuildRequires:	libopenssl-devel
%else
BuildRequires:	openssl-devel
%endif
BuildRequires:	doxygen

%if %{?suse_version}%{!?suse_version:0}
%global mainpkg lib%{_name}%{soname}
%global nmainpkg -n %{mainpkg}
%else
%global mainpkg %{name}
%endif

%if %{?nmainpkg:1}%{!?nmainpkg:0}
%package %{?nmainpkg}
Summary:	Grid Community Toolkit - Globus GSI Credential Library
Group:		System Environment/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}
%endif

%package devel
Summary:	Grid Community Toolkit - Globus GSI Credential Library Development Files
Group:		Development/Libraries
Requires:	%{mainpkg}%{?_isa} = %{version}-%{release}

%package doc
Summary:	Grid Community Toolkit - Globus GSI Credential Library Documentation Files
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
Globus GSI Credential Library
%endif

%description
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name} package contains:
Globus GSI Credential Library

%description devel
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-devel package contains:
Globus GSI Credential Library Development Files

%description doc
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-doc package contains:
Globus GSI Credential Library Documentation Files

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
%{_libdir}/libglobus_gsi_credential.so.*
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/globus/*
%{_libdir}/libglobus_gsi_credential.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%defattr(-,root,root,-)
%doc %{_mandir}/man3/*
%dir %{_pkgdocdir}
%dir %{_pkgdocdir}/html
%doc %{_pkgdocdir}/html/*
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%changelog
* Fri Aug 20 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.3-1
- Typo fixes

* Tue Mar 10 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.2-1
- Make makefiles exit sooner on errors

* Wed Nov 21 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.1-1
- Doxygen fixes

* Sat Mar 31 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.0-1
- First Grid Community Toolkit release

* Wed Nov 08 2017 Globus Toolkit <support@globus.org> - 7.14-1
- Fix issue with voms proxy and openssl 1.1 (#115)

* Wed Nov 01 2017 Globus Toolkit <support@globus.org> - 7.13-1
- Fix crash when cert not set.
- Remove compatibility shims for old versions of OpenSSL

* Mon Oct 30 2017 Globus Toolkit <support@globus.org> - 7.12-1
- Remove prototype for non-existing function

* Thu Sep 08 2016 Globus Toolkit <support@globus.org> - 7.11-1
- Update for el.5 openssl101e

* Thu Aug 25 2016 Globus Toolkit <support@globus.org> - 7.10-3
- Updates for SLES 12

* Tue Aug 16 2016 Globus Toolkit <support@globus.org> - 7.10-1
- Updates for OpenSSL 1.1.0

* Thu Aug 06 2015 Globus Toolkit <support@globus.org> - 7.9-2
- Add vendor

* Wed Jul 01 2015 Globus Toolkit <support@globus.org> - 7.9-1
- add missing const to parameters

* Thu May 28 2015 Globus Toolkit <support@globus.org> - 7.8-1
- Add deprecation comment to obsolete functions
- Tighten up const on some parameters

* Wed Sep 24 2014 Globus Toolkit <support@globus.org> - 7.7-1
- Doxygen markup fixes
- Include more manpages for API
- Fix typos and clarify some documentation
- Quiet some autoconf/automake warnings
- GT-106: Free requirement for cred_get_subject_name not in API docs

* Fri Aug 22 2014 Globus Toolkit <support@globus.org> - 7.6-1
- Merge fixes from ellert-globus_6_branch

* Wed Aug 20 2014 Globus Toolkit <support@globus.org> - 7.5-2
- Fix Source path

* Mon Jun 09 2014 Globus Toolkit <support@globus.org> - 7.5-1
- Merge changes from Mattias Ellert

* Fri Apr 18 2014 Globus Toolkit <support@globus.org> - 7.4-1
- Version bump for consistency

* Thu Feb 27 2014 Globus Toolkit <support@globus.org> - 7.3-1
- Packaging fixes, Warning Cleanup

* Tue Feb 25 2014 Globus Toolkit <support@globus.org> - 7.2-1
- Packaging fixes

* Mon Feb 10 2014 Globus Toolkit <support@globus.org> - 7.1-1
- Packaging fixes

* Tue Jan 21 2014 Globus Toolkit <support@globus.org> - 7.0-1
- Repackage for GT6 without GPT

* Mon Oct 28 2013 Globus Toolkit <support@globus.org> - 6.0-1
- Update Major version for globus_gsi_cred_read_cert_buffer and globus_gsi_cred_verify_cert_chain_when

* Wed Jul 17 2013 Globus Toolkit <support@globus.org> - 5.7-1
- GT-437: grid-proxy-init broken for PKCS12 files with CA certificates

* Wed Jun 26 2013 Globus Toolkit <support@globus.org> - 5.6-2
- GT-424: New Fedora Packaging Guideline - no %%_isa in BuildRequires

* Fri Apr 26 2013 Globus Toolkit <support@globus.org> - 5.6-1
- fix leak in verify_when

* Mon Apr 15 2013 Globus Toolkit <support@globus.org> - 5.5-1
- verify sharing cert chain

* Tue Mar 19 2013 Globus Toolkit <support@globus.org> - 5.4-1
- Update sharing to support a full cert chain at logon

* Wed Feb 20 2013 Globus Toolkit <support@globus.org> - 5.3-7
- Workaround missing F18 doxygen/latex dependency

* Mon Nov 26 2012 Globus Toolkit <support@globus.org> - 5.3-6
- 5.2.3

* Mon Jul 16 2012 Joseph Bester <bester@mcs.anl.gov> - 5.3-5
- GT 5.2.2 final

* Fri Jun 29 2012 Joseph Bester <bester@mcs.anl.gov> - 5.3-4
- GT 5.2.2 Release

* Wed May 09 2012 Joseph Bester <bester@mcs.anl.gov> - 5.3-3
- RHEL 4 patches

* Fri May 04 2012 Joseph Bester <bester@mcs.anl.gov> - 5.3-2
- SLES 11 patches

* Tue Feb 14 2012 Joseph Bester <bester@mcs.anl.gov> - 5.3-1
- RIC-213: support for private keys in PKCS8 format broken
- RIC-226: Some dependencies are missing in GPT metadata

* Thu Jan 05 2012 Joseph Bester <bester@mcs.anl.gov> - 5.2-1
- RIC-213: support for private keys in PKCS8 format broken

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 5.1-4
- Update for 5.2.0 release

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 5.1-3
- Last sync prior to 5.2.0

* Tue Oct 11 2011 Joseph Bester <bester@mcs.anl.gov> - 5.1-2
- Add explicit dependencies on >= 5.2 libraries

* Thu Oct 06 2011 Joseph Bester <bester@mcs.anl.gov> - 5.1-1
- Add backward-compatibility aging

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 5.0-3
- Fix missing whitespace in Requires

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 5.0-2
- Update for 5.1.2 release

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.5-1
- Update to Globus Toolkit 5.0.2
- Drop patch globus-gsi-credential-oid.patch (fixed upstream)

* Mon May 31 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.3-2
- Fix OID registration pollution

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.3-1
- Update to Globus Toolkit 5.0.1
- Drop patch globus-gsi-credential-openssl.patch (fixed upstream)

* Fri Jan 22 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.2-1
- Update to Globus Toolkit 5.0.0

* Sat Aug 22 2009 Tomas Mraz <tmraz@redhat.com> - 2.2-4
- rebuilt with new openssl

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.2-3
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch

* Wed Jun 03 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.2-2
- Update to official Fedora Globus packaging guidelines

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.2-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages
- Put GLOBUS_LICENSE file in extracted source tarball

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.2-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.2-0.4
- Add s390x to the list of 64 bit platforms

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.2-0.3
- Adapt to updated GPT package

* Wed Oct 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.2-0.2
- Update to Globus Toolkit 4.2.1

* Mon Jul 14 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0-0.1
- Autogenerated
