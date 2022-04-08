%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-ftp-control
%global soname 1
%global _name %(echo %{name} | tr - _)
Version:	9.9
Release:	1%{?dist}
Summary:	Grid Community Toolkit - GridFTP Control Library

Group:		System Environment/Libraries
License:	%{?suse_version:Apache-2.0}%{!?suse_version:ASL 2.0}
URL:		https://github.com/gridcf/gct/
Source:		%{_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc
BuildRequires:	globus-common-devel >= 14
BuildRequires:	globus-gss-assist-devel >= 11
BuildRequires:	globus-gssapi-gsi-devel >= 13
BuildRequires:	globus-io-devel >= 11
BuildRequires:	globus-xio-devel >= 3
BuildRequires:	globus-gssapi-error-devel >= 4
BuildRequires:	globus-xio-gsi-driver-devel >= 4
BuildRequires:	doxygen
#		Additional requirements for make check
BuildRequires:	openssl

%if %{?suse_version}%{!?suse_version:0}
%global mainpkg lib%{_name}%{soname}
%global nmainpkg -n %{mainpkg}
%else
%global mainpkg %{name}
%endif

%if %{?nmainpkg:1}%{!?nmainpkg:0}
%package %{?nmainpkg}
Summary:	Grid Community Toolkit - GridFTP Control Library
Group:		System Environment/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}
%endif

Requires:	globus-gss-assist%{?_isa} >= 11
Requires:	globus-gssapi-gsi%{?_isa} >= 13
Requires:	globus-io%{?_isa} >= 11
Requires:	globus-xio-gsi-driver%{?_isa} >= 4

%package devel
Summary:	Grid Community Toolkit - GridFTP Control Library Development Files
Group:		Development/Libraries
Requires:	%{mainpkg}%{?_isa} = %{version}-%{release}

%package doc
Summary:	Grid Community Toolkit - GridFTP Control Library Documentation Files
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
GridFTP Control Library
%endif

%description
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name} package contains:
GridFTP Control Library

%description devel
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-devel package contains:
GridFTP Control Library Development Files

%description doc
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-doc package contains:
GridFTP Control Library Documentation Files

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

%check
GLOBUS_HOSTNAME=localhost make %{?_smp_mflags} check VERBOSE=1

%post %{?nmainpkg} -p /sbin/ldconfig

%postun %{?nmainpkg} -p /sbin/ldconfig

%files %{?nmainpkg}
%defattr(-,root,root,-)
%{_libdir}/libglobus_ftp_control.so.*
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/globus/*
%{_libdir}/libglobus_ftp_control.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%defattr(-,root,root,-)
%doc %{_mandir}/man3/*
%dir %{_pkgdocdir}
%dir %{_pkgdocdir}/html
%doc %{_pkgdocdir}/html/*
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%changelog
* Wed Mar 09 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.9-1
- Fix some compiler and doxygen warnings

* Sun Mar 06 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.8-1
- Use sha256 hash when generating test certificates

* Fri Aug 20 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.7-1
- Typo fixes

* Wed Jun 03 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.6-1
- Use -nameopt sep_multiline to derive certificate subject string

* Tue Mar 10 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.5-1
- Make makefiles exit sooner on errors

* Wed Nov 21 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.4-1
- Doxygen fixes

* Fri Jul 13 2018 Globus Toolkit <support@globus.org> - 9.3-1
- force encryption on tls control channel

* Fri Jun 22 2018 Globus Toolkit <support@globus.org> - 9.2-1
- check for missing signing policy req flag

* Sat May 05 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.1-1
- Use 2048 bit RSA key for tests

* Sat Mar 31 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.0-1
- First Grid Community Toolkit release

* Wed Mar 28 2018 Globus Toolkit <support@globus.org> - 8.3-1
- Default to host authz when using tls control channel

* Fri Sep 22 2017 Globus Toolkit <support@globus.org> - 8.2-1
- fix leak

* Fri Sep 22 2017 Globus Toolkit <support@globus.org> - 8.1-1
- reading when eof will result in callback indicating eof instead of error

* Tue Sep 05 2017 Globus Toolkit <support@globus.org> - 8.0-1
- Add function globus_ftp_control_use_tls() for TLS control channel

* Fri Jun 30 2017 Globus Toolkit <support@globus.org> - 7.8-1
- fix hang/failure when using udt driver with local client transfer

* Thu Oct 13 2016 Globus Toolkit <support@globus.org> - 7.7-2
- more ordered mode fixes
- more updates for el.5 openssl101e

* Tue Oct 04 2016 Globus Toolkit <support@globus.org> - 7.6-1
- improve forced ordering

* Thu Sep 08 2016 Globus Toolkit <support@globus.org> - 7.5-1
- Update for el.5 openssl101e

* Thu Aug 25 2016 Globus Toolkit <support@globus.org> - 7.4-3
- Updates for SLES 12

* Thu Aug 18 2016 Globus Toolkit <support@globus.org> - 7.4-1
- Makefile fix

* Tue Aug 16 2016 Globus Toolkit <support@globus.org> - 7.3-1
- Updates for OpenSSL 1.1.0

* Mon Jul 25 2016 Globus Toolkit <support@globus.org> - 7.2-1
- add buffering to data ordering mode

* Thu Jul 14 2016 Globus Toolkit <support@globus.org> - 7.1-1
- forced data order fixes

* Thu Jul 14 2016 Globus Toolkit <support@globus.org> - 7.0-1
- add ability to request ordered data on reads

* Mon Apr 18 2016 Globus Toolkit <support@globus.org> - 6.10-1
- Updated version numbers

* Mon Apr 18 2016 Globus Toolkit <support@globus.org> - 6.9-1
- Use prelinks for tests so that they run on El Capitan

* Fri Oct 23 2015 Globus Toolkit <support@globus.org> - 6.8-1
- GT-594: enable keepalives

* Thu Aug 06 2015 Globus Toolkit <support@globus.org> - 6.7-2
- Add vendor

* Tue Jul 14 2015 Globus Toolkit <support@globus.org> - 6.7-1
- Fix old-style function definitions
- Fix scope of socklen variable

* Fri Jan 09 2015 Globus Toolkit <support@globus.org> - 6.6-1
- Fix undefined return code

* Fri Jan 09 2015 Globus Toolkit <support@globus.org> - 6.5-1
- Better fix for testing on localhost

* Thu Jan 08 2015 Globus Toolkit <support@globus.org> - 6.4-1
- Missing check for netinet/tcp.h

* Mon Nov 03 2014 Globus Toolkit <support@globus.org> - 6.3-1
- fix memleak

* Mon Nov 03 2014 Globus Toolkit <support@globus.org> - 6.2-1
- Use localhost for tests

* Tue Oct 28 2014 Globus Toolkit <support@globus.org> - 6.1-1
- GT-477: Tracking TCP retransmits on the GridFTP server

* Tue Sep 23 2014 Globus Toolkit <support@globus.org> - 5.12-1
- Doxygen markup fixes
- Fix typos and clarify some documentation

* Fri Aug 22 2014 Globus Toolkit <support@globus.org> - 5.11-1
- Merge fixes from ellert-globus_6_branch

* Wed Aug 20 2014 Globus Toolkit <support@globus.org> - 5.10-3
- Fix Source path

* Wed Jul 23 2014 Globus Toolkit <support@globus.org> - 5.10-2
- Add make check step

* Mon Jun 09 2014 Globus Toolkit <support@globus.org> - 5.10-1
- Merge changes from Mattias Ellert

* Wed Apr 23 2014 Globus Toolkit <support@globus.org> - 5.9-1
- Packaging fixes

* Tue Apr 22 2014 Globus Toolkit <support@globus.org> - 5.8-1
- Test fixes

* Fri Apr 18 2014 Globus Toolkit <support@globus.org> - 5.7-1
- Version bump for consistency

* Thu Feb 27 2014 Globus Toolkit <support@globus.org> - 5.6-1
- Packaging fixes, Warning Cleanup

* Thu Feb 13 2014 Globus Toolkit <support@globus.org> - 5.5-1
- Test fixes

* Wed Feb 12 2014 Globus Toolkit <support@globus.org> - 5.4-1
- Test fixes

* Wed Feb 12 2014 Globus Toolkit <support@globus.org> - 5.3-1
- Test fixes

* Wed Feb 12 2014 Globus Toolkit <support@globus.org> - 5.2-1
- Test fixes

* Wed Feb 12 2014 Globus Toolkit <support@globus.org> - 5.1-1
- Pull in tests

* Tue Jan 21 2014 Globus Toolkit <support@globus.org> - 5.0-1
- Repackage for GT6 without GPT

* Tue Oct 15 2013 Globus Toolkit <support@globus.org> - 4.7-1
- GT-428: Improve handling of hanging GridFTP server processes - prevent missing force_close callback

* Wed Jun 26 2013 Globus Toolkit <support@globus.org> - 4.6-2
- GT-424: New Fedora Packaging Guideline - no %%_isa in BuildRequires

* Wed Mar 06 2013 Globus Toolkit <support@globus.org> - 4.6-1
- GT-366 fix delegation bug introduced in last release.

* Wed Feb 20 2013 Globus Toolkit <support@globus.org> - 4.5-2
- Workaround missing F18 doxygen/latex dependency

* Mon Feb 04 2013 Globus Toolkit <support@globus.org> - 4.5-1
- GT-334: segfault using ftp control lib
- GT-357: Extend globus_ftp_control_authenticate() to allow the caller to set req flags such as delegation.

* Mon Nov 26 2012 Globus Toolkit <support@globus.org> - 4.4-6
- 5.2.3

* Mon Jul 16 2012 Joseph Bester <bester@mcs.anl.gov> - 4.4-5
- GT 5.2.2 final

* Fri Jun 29 2012 Joseph Bester <bester@mcs.anl.gov> - 4.4-4
- GT 5.2.2 Release

* Wed May 09 2012 Joseph Bester <bester@mcs.anl.gov> - 4.4-3
- RHEL 4 patches

* Fri May 04 2012 Joseph Bester <bester@mcs.anl.gov> - 4.4-2
- SLES 11 patches

* Tue Mar 06 2012 Joseph Bester <bester@mcs.anl.gov> - 4.4-1
- GRIDFTP-199: improve globus_ftp_control control channel message processing to
  better handle large messages.

* Tue Feb 14 2012 Joseph Bester <bester@mcs.anl.gov> - 4.3-1
- RIC-226: Some dependencies are missing in GPT metadata

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 4.2-4
- Update for 5.2.0 release

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 4.2-3
- Last sync prior to 5.2.0

* Tue Oct 11 2011 Joseph Bester <bester@mcs.anl.gov> - 4.2-2
- Add explicit dependencies on >= 5.2 libraries

* Thu Oct 06 2011 Joseph Bester <bester@mcs.anl.gov> - 4.2-1
- Add backward-compatibility aging

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 4.0-2
- Update for 5.1.2 release

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.11-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-3
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch

* Thu Jun 04 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-2
- Update to official Fedora Globus packaging guidelines

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages
- Put GLOBUS_LICENSE file in extracted source tarball

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-0.4
- Add s390x to the list of 64 bit platforms

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-0.3
- Adapt to updated GPT package

* Mon Oct 20 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-0.2
- Update to Globus Toolkit 4.2.1

* Tue Jul 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.8-0.1
- Autogenerated
