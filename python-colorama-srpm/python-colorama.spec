# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

%global with_python3 1
%global with_python2 1

%global pypi_name colorama

Name:           python-%{pypi_name}
Version:        0.3.2
#Release:        3%%{?dist}
Release:        0%{?dist}
Summary:        Cross-platform colored terminal text

License:        BSD
URL:            http://pypi.python.org/pypi/colorama/
Source0:        http://pypi.python.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
%if %{with_python2}
BuildRequires:  python2-devel
%endif
%if %{with_python3}
BuildRequires: python%{python3_pkgversion}-devel
%endif

%description
Makes ANSI escape character sequences, for producing colored
terminal text and cursor positioning, work under MS Windows.

ANSI escape character sequences have long been used to produce colored terminal
text and cursor positioning on Unix and Macs. Colorama makes this work on
Windows, too.
It also provides some shortcuts to help generate ANSI sequences, and works fine
in conjunction with any other ANSI sequence generation library, such as
Termcolor.

%if 0%{?with_python2}
%package -n python2-%{pypi_name}
Summary:       Cross-platform colored terminal text
Requires:      python2
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Makes ANSI escape character sequences, for producing colored
terminal text and cursor positioning, work under MS Windows.

ANSI escape character sequences have long been used to produce colored terminal
text and cursor positioning on Unix and Macs. Colorama makes this work on
Windows, too.
It also provides some shortcuts to help generate ANSI sequences, and works fine
in conjunction with any other ANSI sequence generation library, such as
Termcolor.
%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:       Cross-platform colored terminal text
Requires:      python%{python3_pkgversion}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
Makes ANSI escape character sequences, for producing colored
terminal text and cursor positioning, work under MS Windows.

ANSI escape character sequences have long been used to produce colored terminal
text and cursor positioning on Unix and Macs. Colorama makes this work on
Windows, too.
It also provides some shortcuts to help generate ANSI sequences, and works fine
in conjunction with any other ANSI sequence generation library, such as
Termcolor.
%endif

%prep
%setup -q -n %{pypi_name}-%{version}

# remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%if %{with_python3}
cp -a . %{py3dir}
%endif

%build
%if %{with_python2}
%{py2_build}
%endif

%if %{with_python3}
pushd %{py3dir}
%{py3_build}
popd
%endif # with_python3

%install
%if %{with_python2}
%{py2_install}
%endif

%if %{with_python3}
pushd %{py3dir}
%{py3_install}
popd
%endif # with_python3



%if %{with_python2}
%files -n python2-%{pypi_name}
%{!?_licensedir:%global license %doc} 
%doc README.rst
%license LICENSE.txt
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%{!?_licensedir:%global license %doc} 
%doc README.rst
%license LICENSE.txt
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 05 2014 Matthias Runge <mrunge@redhat.com> - 0.3.2-1
- update to 0.3.2 (rhbz#1090014)

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.2.7-5
- Skip the python3 %%files section if we don't build the python3 package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Mar 12 2014 Matthias Runge <mrunge@redhat.com> - 0.2.7-2
- introduce python3 package (rhbz#1075410)

* Mon Sep 30 2013 Matthias Rugne <mrunge@redhat.com> - 0.2.7-1
- uddate to 0.2.7 (rhbz#1010924)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Matthias Runge <mrunge@redhat.com> - 0.2.5-1
- update to 0.2.5 (rhbz#913431)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 11 2012 Matthias Runge <mrunge@redhat.com> - 0.2.4-1
- Initial package.
