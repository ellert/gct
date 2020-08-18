%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-common
%global soname 0
%global _name %(echo %{name} | tr - _)
Version:	18.9
Release:	1%{?dist}
Summary:	Grid Community Toolkit - Common Library

Group:		System Environment/Libraries
License:	%{?suse_version:Apache-2.0}%{!?suse_version:ASL 2.0}
URL:		https://github.com/gridcf/gct/
Source:		%{_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc
%if %{?suse_version}%{!?suse_version:0}
BuildRequires:	libtool
%else
BuildRequires:	libtool-ltdl-devel
%endif
BuildRequires:	doxygen
%if ! %{?suse_version}%{!?suse_version:0}
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
%endif

%if %{?suse_version}%{!?suse_version:0}
%global mainpkg lib%{_name}%{soname}
%global nmainpkg -n %{mainpkg}
%else
%global mainpkg %{name}
%endif

%if %{?nmainpkg:1}%{!?nmainpkg:0}
%package %{?nmainpkg}
Summary:	Grid Community Toolkit - Common Library
Group:		System Environment/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}
%endif

%if %{?suse_version}%{!?suse_version:0}
%{perl_requires}
%else
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%endif
#		Obsolete dropped packages from Globus Toolkit 4.2.1
Obsoletes:	globus-data-conversion < 3
Obsoletes:	globus-mp < 3
Obsoletes:	globus-nexus < 7
Obsoletes:	globus-duct-common < 3
Obsoletes:	globus-duct-control < 3
Obsoletes:	globus-duroc-common < 3
Obsoletes:	globus-duroc-control < 3
#		Obsolete dropped packages from Globus Toolkit 5.2.0
Obsoletes:	globus-libtool < 2
Obsoletes:	globus-openssl < 6
Obsoletes:	globus-libxml2 < 2
#		Obsolete dropped packages from Globus Toolkit 6.0
Obsoletes:	globus-rls-client < 6
Obsoletes:	globus-rls-client-doc < 6
Obsoletes:	globus-rls-client-progs < 6
Obsoletes:	globus-rls-server < 5
#		Obsolete dropped packages from GCT
Obsoletes:	globus-usage < 6

%package progs
Summary:	Grid Community Toolkit - Common Library Programs
Group:		Applications/Internet
Requires:	%{mainpkg}%{?_isa} = %{version}-%{release}

%package devel
Summary:	Grid Community Toolkit - Common Library Development Files
Group:		Development/Libraries
Requires:	%{mainpkg}%{?_isa} = %{version}-%{release}
%if %{?suse_version}%{!?suse_version:0}
Requires:	libtool
%else
Requires:	libtool-ltdl-devel
%endif
#		Obsolete dropped packages from Globus Toolkit 4.2.1
Obsoletes:	globus-data-conversion-devel < 3
Obsoletes:	globus-mp-devel < 3
Obsoletes:	globus-nexus-devel < 7
Obsoletes:	globus-duct-common-devel < 3
Obsoletes:	globus-duct-control-devel < 3
Obsoletes:	globus-duroc-common-devel < 3
Obsoletes:	globus-duroc-control-devel < 3
#		Obsolete dropped packages from Globus Toolkit 5.2.0
Obsoletes:	globus-libtool-devel < 2
Obsoletes:	globus-openssl-devel < 6
Obsoletes:	globus-libxml2-devel < 2
#		Obsolete dropped packages from Globus Toolkit 6.0
Obsoletes:	grid-packaging-tools < 3.7
Obsoletes:	globus-core < 9
Obsoletes:	globus-rls-client-devel < 6
#		Obsolete dropped packages from GCT
Obsoletes:	globus-usage-devel < 6

%package doc
Summary:	Grid Community Toolkit - Common Library Documentation Files
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
Common Library
%endif

%description
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name} package contains:
Common Library

%description progs
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-progs package contains:
Common Library Programs

%description devel
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-devel package contains:
Common Library Development Files

%description doc
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-doc package contains:
Common Library Documentation Files

%prep
%setup -q -n %{_name}-%{version}

%build
export GLOBUS_VERSION=6.2
export SH=/bin/sh
%configure --disable-static \
	   --includedir=%{_includedir}/globus \
	   --libexecdir=%{_datadir}/globus \
	   --docdir=%{_pkgdocdir} \
	   --with-perlmoduledir=%{perl_vendorlib} \
	   --with-backward-compatibility-hack

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool archives (.la files)
rm $RPM_BUILD_ROOT%{_libdir}/*.la

# Remove environment scripts
rm $RPM_BUILD_ROOT%{_datadir}/globus-user-env.csh
rm $RPM_BUILD_ROOT%{_datadir}/globus-user-env.sh

%check
make %{?_smp_mflags} check VERBOSE=1 NO_EXTERNAL_NET=1

%post %{?nmainpkg} -p /sbin/ldconfig

%postun %{?nmainpkg} -p /sbin/ldconfig

%files %{?nmainpkg}
%defattr(-,root,root,-)
%{_libdir}/libglobus_common.so.*
%{_libdir}/libglobus_memory_debug.so.*
# This is a loadable module (plugin)
%{_libdir}/libglobus_thread_pthread.so
%dir %{perl_vendorlib}/Globus
%dir %{perl_vendorlib}/Globus/Core
%{perl_vendorlib}/Globus/Core/Config.pm
%{perl_vendorlib}/Globus/Core/Paths.pm
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%files progs
%defattr(-,root,root,-)
%{_bindir}/globus-domainname
%{_bindir}/globus-hostname
%{_bindir}/globus-sh-exec
%{_bindir}/globus-version
%{_sbindir}/globus-libc-hostname
%{_sbindir}/globus-redia
%dir %{_datadir}/globus
%{_datadir}/globus/config.guess
%{_datadir}/globus/globus-args-parser-header
%{_datadir}/globus/globus-script-initializer*
%{_datadir}/globus/globus-sh-tools.sh
%{_datadir}/globus/globus-sh-tools-vars.sh
%doc %{_mandir}/man1/globus-domainname.1*
%doc %{_mandir}/man1/globus-hostname.1*
%doc %{_mandir}/man1/globus-sh-exec.1*
%doc %{_mandir}/man1/globus-version.1*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/globus
%{_includedir}/globus/*
%{_libdir}/libglobus_common.so
%{_libdir}/libglobus_memory_debug.so
%{_libdir}/pkgconfig/%{name}.pc
%{_bindir}/globus-makefile-header

%files doc
%defattr(-,root,root,-)
%doc %{_mandir}/man3/*
%dir %{_pkgdocdir}
%dir %{_pkgdocdir}/html
%doc %{_pkgdocdir}/html/*
%doc %{_pkgdocdir}/GLOBUS_LICENSE

%changelog
* Thu Jul 16 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.9-1
- Check for LTO use in CFLAGS instead of LDFLAGS

* Thu Mar 12 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.8-2
- Add BuildRequires perl-interpreter

* Thu Mar 12 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.8-1
- Remove unused doxygen filter

* Tue Mar 10 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.7-1
- Make makefiles exit sooner on errors

* Thu Jan 09 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.6-1
- For pure IP addresses globus-domainname should be empty

* Sat Jul 20 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.5-1
- Obsolete globus-usage packages
- Remove unused perlmoduledir references

* Wed Jul 17 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.4-1
- Make symbol versioning work with link time optimization (LTO)

* Wed Apr 17 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.3-1
- Clean up old GPT references

* Wed Nov 28 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.2-1
- Fix FTBR (failed to build reproducibly)

* Wed Nov 21 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.1-1
- Doxygen fixes

* Mon Nov 05 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.0-2
- Bump GCT release version to 6.2

* Sat Mar 31 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 18.0-1
- First Grid Community Toolkit release
- Move globus-makefile-header to devel package

* Wed Feb 07 2018 Globus Toolkit <support@globus.org> - 17.4-1
- win32 fix

* Thu Jan 25 2018 Globus Toolkit <support@globus.org> - 17.3-1
- use win compatible unsetenv

* Thu Sep 28 2017 Globus Toolkit <support@globus.org> - 17.2-1
- Merge #110 from ellert: Fix regex for perl 5.26 compatibility
- Fix globus_location_test when GLOBUS_LOCATION environment is set

* Mon Jun 19 2017 Globus Toolkit <support@globus.org> - 17.1-2
- Skip network tests on fedora 26

* Fri Mar 03 2017 Globus Toolkit <support@globus.org> - 17.1-1
- Add missing file

* Fri Mar 03 2017 Globus Toolkit <support@globus.org> - 17.0-1
- add additional error handling api

* Fri Jan 06 2017 Globus Toolkit <support@globus.org> - 16.9-1
- Fix crash in globus_eval_path

* Thu Sep 08 2016 Globus Toolkit <support@globus.org> - 16.8-2
- Rebuild after changes for el.5 with openssl101e

* Thu Sep 08 2016 Globus Toolkit <support@globus.org> - 16.8-1
- Replace docbook with asciidoc

* Wed Aug 24 2016 Globus Toolkit <support@globus.org> - 16.7-4
- SLES 12 packaging conditionals

* Sat Aug 20 2016 Globus Toolkit <support@globus.org> - 16.7-1
- Update bug report URL

* Tue Aug 16 2016 Globus Toolkit <support@globus.org> - 16.6-1
- Updates for running thread tests without installing

* Wed Jun 22 2016 Globus Toolkit <support@globus.org> - 16.5-1
- don't redefine snprintf and vsnprintf when using mingw versions

* Tue May 03 2016 Globus Toolkit <support@globus.org> - 16.4-1
- Spelling

* Thu Apr 07 2016 Globus Toolkit <support@globus.org> - 16.3-1
- Thread pc files dlpreopen and dlopen variables

* Tue Jan 26 2016 Globus Toolkit <support@globus.org> - 16.2-1
- Fix missing doxygen comment header

* Fri Dec 11 2015 Globus Toolkit <support@globus.org> - 16.1-1
- fix windows setenv impl

* Fri Oct 23 2015 Globus Toolkit <support@globus.org> - 16.0-1
- Add globus_extension_get_module_version

* Thu Aug 06 2015 Globus Toolkit <support@globus.org> - 15.31-2
- Add vendor

* Wed Jul 29 2015 Globus Toolkit <support@globus.org> - 15.31-1
- Fix in-tree run of GRAM tests by not having Config.pm in the perl5lib dir

* Fri Jun 05 2015 Globus Toolkit <support@globus.org> - 15.30-1
- Make globus-version executable during build time

* Tue Apr 07 2015 Globus Toolkit <support@globus.org> - 15.29-1
- Fix skip() regression in tests

* Tue Apr 07 2015 Globus Toolkit <support@globus.org> - 15.28-1
- Disable network tests when NO_EXTERNAL_NET is in the environment

* Sat Mar 07 2015 Globus Toolkit <support@globus.org> - 15.27-2
- move thread plugins to base

* Thu Dec 18 2014 Globus Toolkit <support@globus.org> - 15.27-1
- Don't add empty entries in list_from_string

* Tue Sep 30 2014 Globus Toolkit <support@globus.org> - 15.26-1
- Doxygen markup fixes
- Fix typos and clarify some documentation

* Fri Sep 05 2014 Globus Toolkit <support@globus.org> - 15.25-1
- Set GLOBUS_VERSION in bootstrap

* Fri Sep 05 2014 Globus Toolkit <support@globus.org> - 15.24-2
- GT 6.0

* Fri Aug 22 2014 Globus Toolkit <support@globus.org> - 15.24-1
- Merge fixes from ellert-globus_6_branch

* Wed Aug 20 2014 Globus Toolkit <support@globus.org> - 15.23-4
- Fix Source path

* Fri Jul 25 2014 Globus Toolkit <support@globus.org> - 15.23-3
- Adjust -devel dependency on ltdl-devel to exclude SuSE

* Wed Jul 23 2014 Globus Toolkit <support@globus.org> - 15.23-2
- Add -devel dependency on ltdl-devel

* Mon Jun 09 2014 Globus Toolkit <support@globus.org> - 15.23-1
- Merge changes from Mattias Ellert

* Fri May 23 2014 Globus Toolkit <support@globus.org> - 15.22-1
- Use globus_libc_[un]setenv

* Wed May 07 2014 Globus Toolkit <support@globus.org> - 15.21-1
- Time-related fixes on windows

* Wed Apr 23 2014 Globus Toolkit <support@globus.org> - 15.20-1
- Packaging fixes

* Wed Apr 23 2014 Globus Toolkit <support@globus.org> - 15.19-1
- Packaging fixes

* Wed Apr 23 2014 Globus Toolkit <support@globus.org> - 15.18-1
- Packaging fixes

* Sat Apr 19 2014 Globus Toolkit <support@globus.org> - 15.17-1
- Test fixes

* Fri Apr 18 2014 Globus Toolkit <support@globus.org> - 15.16-1
- Version bump for consistency

* Thu Feb 27 2014 Globus Toolkit <support@globus.org> - 15.15-1
- Packaging fixes, Warning Cleanup

* Tue Feb 25 2014 Globus Toolkit <support@globus.org> - 15.14-1
- Packaging fixes

* Tue Feb 18 2014 Globus Toolkit <support@globus.org> - 15.13-1
- Packaging fixes

* Tue Feb 18 2014 Globus Toolkit <support@globus.org> - 15.12-1
- Don't depend on finding initializer/args parser

* Fri Feb 14 2014 Globus Toolkit <support@globus.org> - 15.11-1
- Test Fixes

* Fri Feb 07 2014 Globus Toolkit <support@globus.org> - 15.10-1
- Use Libs.private for common deps

* Fri Feb 07 2014 Globus Toolkit <support@globus.org> - 15.9-1
- Fix some configure problems

* Fri Feb 07 2014 Globus Toolkit <support@globus.org> - 15.8-1
- fix inconsistent arch-specific initializer

* Thu Feb 06 2014 Globus Toolkit <support@globus.org> - 15.7-1
- Fix some configure problems

* Thu Jan 30 2014 Globus Toolkit <support@globus.org> - 15.6-1
- Make scripts the same for arches

* Wed Jan 29 2014 Globus Toolkit <support@globus.org> - 15.5-1
- initializer tweak

* Wed Jan 29 2014 Globus Toolkit <support@globus.org> - 15.4-1
- Tweak initializer

* Wed Jan 29 2014 Globus Toolkit <support@globus.org> - 15.3-1
- Add arch-specific initializer

* Mon Jan 27 2014 Globus Toolkit <support@globus.org> - 15.2-1
- Repackage for GT6 without GPT

* Mon Jul 08 2013 Globus Toolkit <support@globus.org> - 14.10-3
- Incorrect %%dir for license file

* Wed Jun 26 2013 Globus Toolkit <support@globus.org> - 14.10-2
- GT-424: New Fedora Packaging Guideline - no %%_isa in BuildRequires

* Mon Mar 18 2013 Globus Toolkit <support@globus.org> - 14.10-1
- GT-354: Compatibility with automake 1.13

* Wed Feb 20 2013 Globus Toolkit <support@globus.org> - 14.9-4
- Workaround missing F18 doxygen/latex dependency

* Mon Feb 4 2013 Globus Toolkit <support@globus.org> - 14.9-3

* Mon Nov 26 2012 Globus Toolkit <support@globus.org> - 14.9-2
- 5.2.3

* Tue Oct 09 2012 Globus Toolkit <support@globus.org> - 14.9-1
- GT-288: Deprecate globus_libc_setenv

* Thu Aug 09 2012 Joseph Bester <bester@mcs.anl.gov> - 14.8-1
- GT-264: link error in globus-redia

* Mon Jul 16 2012 Joseph Bester <bester@mcs.anl.gov> - 14.7-3
- GT 5.2.2 final

* Fri Jun 29 2012 Joseph Bester <bester@mcs.anl.gov> - 14.7-2
- GT 5.2.2 Release

* Wed Jun 13 2012 Joseph Bester <bester@mcs.anl.gov> - 14.7-1
- GT-227: API Documentation for Globus Priority Queue

* Wed May 09 2012 Joseph Bester <bester@mcs.anl.gov> - 14.6-3
- RHEL 4 patches

* Fri May 04 2012 Joseph Bester <bester@mcs.anl.gov> - 14.6-2
- SLES 11 patches

* Tue Feb 14 2012 Joseph Bester <bester@mcs.anl.gov> - 14.6-1
- RIC-221: Remove unnecessary evals of path components from script initializers
- RIC-223: Some commands in globus_common have no manpage
- RIC-224: Eliminate some doxygen warnings
- RIC-228: potentially unsafe format strings in common
- RIC-230: Remove obsolete globus_libtool_windows code
- RIC-255: Missing default value for shell script variable in globus-sh-exec

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 14.5-2
- Update for 5.2.0 release

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 14.5-1
- Last sync prior to 5.2.0

* Wed Nov 23 2011 Joseph Bester <bester@mcs.anl.gov> - 14.4-1
- make GPT_EXTERNAL_LIBS=-lpthread for backward-compatibility hack

* Fri Nov 11 2011 Joseph Bester <bester@mcs.anl.gov> - 14.3-2
- Set default GLOBUS_VERSION to version 5.1.3

* Thu Nov 03 2011 Joseph Bester <bester@mcs.anl.gov> - 14.3-1
- RIC-199: Can't install 32 and 64 bit Globus RPMs at the same time (missed
  perl libdir change)

* Fri Oct 28 2011 Joseph Bester <bester@mcs.anl.gov> - 14.2-1
- Allow pthread extensions to be activated, but warn in globus_extension_activate debug output

* Mon Oct 24 2011 Joseph Bester <bester@mcs.anl.gov> - 14.1-2
- Add explicit dependencies on >= 5.2 libraries
- Move libglobus_thread_pthread.so symlink to globus-common package
  from globus-common-devel
- Add backward-compatibility hack
- Obsolete globus-libtool-devel instead of globus-libtool in devel package
- Remove text about extracting source from installer

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 14.0-2
- Update for 5.1.2 release

* Mon Sep 06 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.5-3
- Updated pthread exception patch for better compatibility with boost's headers

* Sun Aug 08 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.5-2
- Fix perl dependncies (use vs. require)

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.5-1
- Update to Globus Toolkit 5.0.2

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 11.4-2
- Mass rebuild with perl-5.12.0

* Tue Apr 13 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.4-1
- Update to Globus Toolkit 5.0.1

* Wed Feb 24 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.2-2
- Make the globus-version script return the right value

* Thu Jan 21 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.2-1
- Update to Globus Toolkit 5.0.0

* Fri Dec 04 2009 Stepan Kasal <skasal@redhat.com> - 10.2-9
- rebuild against perl 5.10.1

* Sun Nov 08 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-8
- Let globus-makefile-header fail gracefully when GPT is not present
- Workaround a bug in doxygen

* Mon Aug 03 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-7
- Patch globus_location function to allow unset GLOBUS_LOCATION
- Put back config.guess file

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-6
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch
- Replace /usr/bin/env shebangs

* Tue Jun 02 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-5
- Update to official Fedora Globus packaging guidelines

* Mon Apr 27 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-4
- Rebuild with updated libtool

* Tue Apr 21 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-3
- Put GLOBUS_LICENSE file in extracted source tarball

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-2
- Remove config.guess file

* Tue Apr 07 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-1
- Change defines to globals

* Mon Apr 06 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-0.6
- Make comment about source retrieval more explicit

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-0.4
- Add s390x to the list of 64 bit platforms
- Move globus-makefile-header to devel package

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-0.3
- Adapt to updated GPT package

* Wed Oct 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-0.2
- Update to Globus Toolkit 4.2.1

* Mon Jul 14 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-0.1
- Autogenerated
