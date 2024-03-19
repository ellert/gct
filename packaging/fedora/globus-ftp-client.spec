%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-ftp-client
%global soname 2
%global _name %(echo %{name} | tr - _)
Version:	9.9
Release:	1%{?dist}
Summary:	Grid Community Toolkit - GridFTP Client Library

Group:		System Environment/Libraries
License:	%{?suse_version:Apache-2.0}%{!?suse_version:ASL 2.0}
URL:		https://github.com/gridcf/gct/
Source:		%{_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc
BuildRequires:	globus-common-devel >= 15
BuildRequires:	globus-ftp-control-devel >= 4
BuildRequires:	globus-gsi-callback-devel >= 4
BuildRequires:	globus-gsi-credential-devel >= 5
BuildRequires:	globus-gsi-sysconfig-devel >= 5
BuildRequires:	globus-gssapi-gsi-devel >= 10
BuildRequires:	globus-xio-devel >= 3
BuildRequires:	globus-xio-popen-driver-devel >= 2
%if %{?suse_version}%{!?suse_version:0}
BuildRequires:	libopenssl-devel
%else
BuildRequires:	openssl-devel
%endif
BuildRequires:	doxygen
#		Additional requirements for make check
BuildRequires:	globus-gridftp-server-devel >= 7
BuildRequires:	globus-gridftp-server-progs >= 7
BuildRequires:	openssl
BuildRequires:	perl-interpreter
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(FileHandle)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(lib)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(strict)
BuildRequires:	perl(Sys::Hostname)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(vars)

%if %{?suse_version}%{!?suse_version:0}
%global mainpkg lib%{_name}%{soname}
%global nmainpkg -n %{mainpkg}
%else
%global mainpkg %{name}
%endif

%if %{?nmainpkg:1}%{!?nmainpkg:0}
%package %{?nmainpkg}
Summary:	Grid Community Toolkit - GridFTP Client Library
Group:		System Environment/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}
%endif

Requires:	globus-xio-popen-driver%{?_isa} >= 2

%package devel
Summary:	Grid Community Toolkit - GridFTP Client Library Development Files
Group:		Development/Libraries
Requires:	%{mainpkg}%{?_isa} = %{version}-%{release}

%package doc
Summary:	Grid Community Toolkit - GridFTP Client Library Documentation Files
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
GridFTP Client Library
%endif

%description
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name} package contains:
GridFTP Client Library

%description devel
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-devel package contains:
GridFTP Client Library Development Files

%description doc
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-doc package contains:
GridFTP Client Library Documentation Files

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
GLOBUS_HOSTNAME=localhost make %{?_smp_mflags} check VERBOSE=1

%post %{?nmainpkg} -p /sbin/ldconfig

%postun %{?nmainpkg} -p /sbin/ldconfig

%files %{?nmainpkg}
%defattr(-,root,root,-)
%{_libdir}/libglobus_ftp_client.so.*
%dir %{_datadir}/globus
%{_datadir}/globus/gridftp-ssh
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/globus/*
%{_libdir}/libglobus_ftp_client.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%defattr(-,root,root,-)
%doc %{_mandir}/man3/*
%dir %{_pkgdocdir}
%dir %{_pkgdocdir}/html
%doc %{_pkgdocdir}/html/*
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%changelog
* Fri Mar 01 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.9-1
- Fix format warnings on 32 bit systems

* Wed Mar 09 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.8-1
- Fix some compiler and doxygen warnings

* Sun Mar 06 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.7-1
- Use sha256 hash when generating test certificates

* Fri Aug 20 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.6-1
- Typo fixes

* Wed Jun 03 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.5-1
- Use -nameopt sep_multiline to derive certificate subject string

* Thu Mar 12 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.4-2
- Add BuildRequires perl-interpreter
- Add additional perl dependencies for tests

* Thu Mar 12 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.4-1
- Remove some unused test scripts

* Tue Mar 10 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.3-1
- Make makefiles exit sooner on errors

* Wed Nov 21 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.2-1
- Doxygen fixes

* Mon Nov 05 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.1-2
- Bump GCT release version to 6.2

* Sat May 05 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.1-1
- Use 2048 bit RSA key for tests

* Sat Mar 31 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.0-1
- First Grid Community Toolkit release
- Remove support for openssl101e (RHEL5 is EOL)

* Mon Jun 26 2017 Globus Toolkit <support@globus.org> - 8.36-1
- Replace deprecated perl POSIX::tmpnam with File::Temp::tmpnam

* Fri Mar 24 2017 Globus Toolkit <support@globus.org> - 8.35-1
- Remove some redundent tests to reduce test time

* Thu Mar 09 2017 Globus Toolkit <support@globus.org> - 8.34-1
- add FTP_TEST_RESTART_AFTER_RANGE=n to force restarts after n range markers for restart points 22 and 24 (RETR_RESPONSE and STOR_RESPONSE)

* Thu Sep 08 2016 Globus Toolkit <support@globus.org> - 8.33-1
- Update for el.5 openssl101e

* Fri Aug 26 2016 Globus Toolkit <support@globus.org> - 8.32-2
- Updates for SLES 12

* Fri Aug 19 2016 Globus Toolkit <support@globus.org> - 8.32-1
- Fix tests run as root

* Thu Aug 18 2016 Globus Toolkit <support@globus.org> - 8.31-1
- Makefile fix

* Tue Aug 16 2016 Globus Toolkit <support@globus.org> - 8.30-1
- Updates for OpenSSL 1.1.0

* Tue May 03 2016 Globus Toolkit <support@globus.org> - 8.29-1
- Don't overwite LDFLAGS

* Mon Apr 18 2016 Globus Toolkit <support@globus.org> - 8.28-1
- Use prelinks for tests so that they run on El Capitan

* Mon Nov 23 2015 Globus Toolkit <support@globus.org> - 8.27-1
- prevent endless loop when auto-retrying failed pasv on other server

* Fri Nov 20 2015 Globus Toolkit <support@globus.org> - 8.26-1
- Disable mandatory IPv6 in tests. Can be enabled via the environment if needed

* Fri Oct 23 2015 Globus Toolkit <support@globus.org> - 8.25-1
- GT-604: fix ipv6 negotiation when source does not pre-connect

* Thu Aug 06 2015 Globus Toolkit <support@globus.org> - 8.24-2
- Add vendor

* Tue Jul 28 2015 Globus Toolkit <support@globus.org> - 8.24-1
- use SIGINT to terminating test server for gcov

* Wed Jul 15 2015 Globus Toolkit <support@globus.org> - 8.23-1
- Fix crash in error handling

* Wed Apr 15 2015 Globus Toolkit <support@globus.org> - 8.22-1
- Fix tests on jessie with pbuilder

* Thu Mar 12 2015 Globus Toolkit <support@globus.org> - 8.21-1
- GT-587: ssh path not being set in globus-ftp-client for sshftp in GT6

* Wed Mar 04 2015 Globus Toolkit <support@globus.org> - 8.20-1
- improve fix for GT-568

* Thu Feb 12 2015 Globus Toolkit <support@globus.org> - 8.19-2
- Add openssl build requirement for tests

* Thu Feb 12 2015 Globus Toolkit <support@globus.org> - 8.19-1
- GT-568: Fix incompatibility between IPV4-only source and IPV6 dest when IPV6 is enabled

* Mon Feb 09 2015 Globus Toolkit <support@globus.org> - 8.18-1
- GT-534: Fix for crash after error with delayed pasv response

* Tue Nov 18 2014 Globus Toolkit <support@globus.org> - 8.17-1
- Disable segfaulting test on GNU/Hurd

* Mon Nov 03 2014 Globus Toolkit <support@globus.org> - 8.16-1
- don't use $HOME in tests

* Mon Nov 03 2014 Globus Toolkit <support@globus.org> - 8.15-1
- doxygen fixes

* Tue Oct 28 2014 Globus Toolkit <support@globus.org> - 8.14-1
- GT-572: globus-ftp-client performs MLSD with incorrect TYPE

* Tue Sep 23 2014 Globus Toolkit <support@globus.org> - 8.13-1
- Include more manpages for API
- Fix some Doxygen issues
- Fix dependency
- Quiet some autoconf/automake warnings
- Use mixed case man page install for all packages

* Fri Aug 22 2014 Globus Toolkit <support@globus.org> - 8.12-1
- Merge fixes from ellert-globus_6_branch

* Wed Aug 20 2014 Globus Toolkit <support@globus.org> - 8.11-2
- Fix Source path

* Wed Aug 06 2014 Globus Toolkit <support@globus.org> - 8.11-1
- Skip put-test.pl on mingw

* Tue Aug 05 2014 Globus Toolkit <support@globus.org> - 8.10-1
- Skip put-test.pl on mingw

* Mon Jun 09 2014 Globus Toolkit <support@globus.org> - 8.9-1
- Merge changes from Mattias Ellert

* Thu Apr 24 2014 Globus Toolkit <support@globus.org> - 8.8-1
- Test fixes

* Fri Apr 18 2014 Globus Toolkit <support@globus.org> - 8.7-1
- Version bump for consistency

* Thu Feb 27 2014 Globus Toolkit <support@globus.org> - 8.6-1
- Packaging fixes, Warning Cleanup

* Thu Feb 20 2014 Globus Toolkit <support@globus.org> - 8.5-1
- GLOBUS_USAGE_OPTOUT tests

* Mon Feb 17 2014 Globus Toolkit <support@globus.org> - 8.4-1
- Packaging fixes

* Mon Feb 17 2014 Globus Toolkit <support@globus.org> - 8.3-1
- Packaging fixes

* Fri Feb 14 2014 Globus Toolkit <support@globus.org> - 8.2-1
- Packaging fixes

* Fri Feb 14 2014 Globus Toolkit <support@globus.org> - 8.1-2
- Test fixes

* Fri Feb 14 2014 Globus Toolkit <support@globus.org> - 8.1-1
- Packaging fixes

* Wed Jan 22 2014 Globus Toolkit <support@globus.org> - 8.0-1
- Repackage for GT6 without GPT

* Thu Aug 15 2013 Globus Toolkit <support@globus.org> - 7.6-1
- GT-425: add environment variable to force IPV6 compatibility

* Wed Jun 26 2013 Globus Toolkit <support@globus.org> - 7.5-2
- GT-424: New Fedora Packaging Guideline - no %%_isa in BuildRequires

* Thu May 09 2013 Globus Toolkit <support@globus.org> - 7.5-1
- Fix performance issue, don't need to check binary data buffers for newlines

* Wed Feb 20 2013 Globus Toolkit <support@globus.org> - 7.4-5
- Workaround missing F18 doxygen/latex dependency

* Mon Nov 26 2012 Globus Toolkit <support@globus.org> - 7.4-4
- 5.2.3

* Mon Jul 16 2012 Joseph Bester <bester@mcs.anl.gov> - 7.4-3
- GT 5.2.2 final

* Fri Jun 29 2012 Joseph Bester <bester@mcs.anl.gov> - 7.4-2
- GT 5.2.2 Release

* Wed Jun 27 2012 Joseph Bester <bester@mcs.anl.gov> - 7.4-1
- GT-153: make gridftp-v2 GET/PUT the default for server that support it
- GT-15: Add explicit CWD command to client API
- GT-9: Failure in globus_ftp_client_operationattr_set_authorization() results in using freed memory
- RIC-226: Some dependencies are missing in GPT metadata

* Wed May 09 2012 Joseph Bester <bester@mcs.anl.gov> - 7.3-3
- RHEL 4 patches

* Fri May 04 2012 Joseph Bester <bester@mcs.anl.gov> - 7.3-2
- SLES 11 patches

* Tue Feb 14 2012 Joseph Bester <bester@mcs.anl.gov> - 7.3-1
- RIC-226: Some dependencies are missing in GPT metadata

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 7.2-4
- Update for 5.2.0 release

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 7.2-3
- Last sync prior to 5.2.0

* Tue Oct 11 2011 Joseph Bester <bester@mcs.anl.gov> - 7.1-2
- Add explicit dependencies on >= 5.2 libraries

* Thu Oct 06 2011 Joseph Bester <bester@mcs.anl.gov> - 7.1-1
- Add backward-compatibility aging

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 7.0-2
- Update for 5.1.2 release

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.3-2
- Update to Globus Toolkit 5.0.2

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.3-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.2-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-3
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch

* Thu Jun 04 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-2
- Update to official Fedora Globus packaging guidelines

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages
- Put GLOBUS_LICENSE file in extracted source tarball

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-0.4
- Add s390x to the list of 64 bit platforms

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-0.3
- Adapt to updated GPT package

* Tue Oct 21 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-0.2
- Update to Globus Toolkit 4.2.1

* Tue Jul 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.11-0.1
- Autogenerated
