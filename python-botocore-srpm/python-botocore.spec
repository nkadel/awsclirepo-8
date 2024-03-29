# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

%{?python_enable_dependency_generator}
# Enable tests
%bcond_with test
# Disable documentation generation for now
%bcond_with docs

%global pypi_name botocore

Name:           python-%{pypi_name}
Version:        1.12.157
#Release:        1%%{?dist}
Release:        0%{?dist}
Summary:        Low-level, data-driven core of boto 3

License:        ASL 2.0
URL:            https://github.com/boto/botocore
Source:         https://pypi.io/packages/source/b/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Patch0:         0002-Fix-date-util-version-for-EL7.patch
BuildArch:      noarch

%description
A low-level interface to a growing number of Amazon Web Services. The
botocore package is the foundation for the AWS CLI as well as boto3.

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Low-level, data-driven core of boto 3
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with docs}
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-guzzle_sphinx_theme
%endif # with docs
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-wheel
BuildRequires:  python%{python3_pkgversion}-docutils
BuildRequires:  python%{python3_pkgversion}-dateutil
BuildRequires:  python%{python3_pkgversion}-jmespath
BuildRequires:  python%{python3_pkgversion}-jsonschema
BuildRequires:  python%{python3_pkgversion}-urllib3
%endif # with tests
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
A low-level interface to a growing number of Amazon Web Services. The
botocore package is the foundation for the AWS CLI as well as boto3.

%if %{with docs}
%package doc
Summary: Documentation for %{name}
%description doc
%{summary}.
%endif # with docs

%prep
%setup -q -n %{pypi_name}-%{version}
sed -i -e '1 d' botocore/vendored/requests/packages/chardet/chardetect.py
sed -i -e '1 d' botocore/vendored/requests/certs.py
rm -rf %{pypi_name}.egg-info
# Remove online tests
rm -rf tests/integration

%build
%py3_build

%install
%py3_install
%if %{with docs}
sphinx-build-3 docs/source html
rm -rf html/.{doctrees,buildinfo}
%endif # with docs

%if %{with tests}
%check
# %%{__python3} setup.py test
export PYTHONPATH=%{buildroot}%{python3_sitelib}
nosetests-3 --with-coverage --cover-erase --cover-package botocore --with-xunit --cover-xml -v tests/unit/ tests/functional/
%endif # with tests

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst
%license LICENSE.txt
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*.egg-info/
%if %{with docs}
%files doc
%doc html
%endif # with docs

%changelog
* Sun Jun 9 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 1.12.157-0
- BBackport to RHEL 8

* Tue May 28 2019 David Duncan <davdunc@amazon.com> - 1.12.157-1
- Bumping to version 1.12.157
- resolves #1677950
- update to latest endpoints and models

* Wed Apr 24 2019 David Duncan <dadvunc@amazon.com> - 1.12.135-1
- Bumping version to 1.12.135
- add support for ap-east-1

* Thu Mar 21 2019 David Duncan <davdunc@amazon.com> - 1.12.119-1
- resolves #1677950
- Bumping version to 1.12.119


* Sat Feb 23 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.12.101-1
- Update to 1.12.101

* Fri Feb 15 2019 Kevin Fenzi <kevin@scrye.com> - 1.12.96-1
- Update to 1.12.96.

* Sun Feb 10 2019 David Duncan <davdunc@amazon.com> - 1.12.91
- resolves #1667630
- Update to latest models
- api-change:``discovery``: Update discovery client to latest version
- api-change:``ecs``: Update ecs client to latest version
- api-change:``dlm``: Update dlm client to latest version

* Mon Feb 04 2019 David Duncan <davdunc@amazon.com> - 1.12.87
- Update to latest models
- Improve event stream parser tests
- resolves #1667630

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.12.75-3
- Enable python dependency generator

* Wed Jan 09 2019 Miro Hrončok <mhroncok@redhat.com> - 1.12.75-2
- Subpackage python2-botocore has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Jan 08 2019 David Duncan <davdunc@amazon.com> - 1.12.75
- Update to latest endpoints
- Update to latest models

* Sun Nov 18 2018 David Duncan <davdunc@amazon.com> - 1.12.47
- Update to latest models.

* Sun Oct 07 2018 David Duncan <davdunc@amazon.com> - 1.12.18
- Update to latest models 

* Tue Oct 02 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.12.15-2
- Reinstate python-urllib3 dependency as python-boto3 requires it

* Tue Oct 02 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.12.15-1
- Update to 1.12.15

* Wed Sep 5 2018 David Duncan <davdunc@amazon.com> - 1.10.43-1
- Bumping version to 1.10.43 Updates bz#1531330

* Mon Sep 3 2018 David Duncan <davdunc@amazon.com> - 1.10.42-1
- Bumping version to 1.10.42 Updates bz#1531330

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.10.41-3
- Rebuilt for Python 3.7

* Wed Jun 20 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.10.41-2
- Fix EL7 dateutil patch

* Wed Jun 20 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.10.41-1
- Upstream 1.10.41

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.1-3
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.9.1-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 28 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.8.33-1
- Update to 1.8.33

* Tue Jan 16 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.8.29-1
- Update to 1.8.29

* Wed Jan 10 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.8.26-1
- Update to 1.8.26

* Wed Jan 03 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.8.21-1
- Update to 1.8.21

* Sun Aug 13 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.72-1
- Update to 1.5.72

* Tue May 23 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.53-1
- Update to 1.5.53

* Wed Mar 15 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.26-1
- Update to 1.5.26

* Sat Feb 25 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.18-1
- Update to 1.5.18

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.5.3-1
- Update to 1.5.3
- Rebase patch

* Wed Dec 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.91-1
- Update to 1.4.91

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.4.85-2
- Rebuild for Python 3.6

* Sun Dec 11 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.85-1
- Update to 1.4.85

* Sat Dec 03 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.81-1
- Update to 1.4.81

* Thu Nov 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.78-1
- Update to 1.4.78

* Thu Oct 27 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.67-1
- Update to 1.4.67

* Mon Oct 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.60-1
- Update to 1.4.60

* Sun Oct 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.58-1
- Update to 1.4.58
- Add python-six dependency

* Wed Sep 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.57-1
- Update to 1.4.57

* Tue Sep 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.52-3
- Fix patch

* Tue Sep 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.52-2
- Add testing support for EL7 using a lower version of dateuil library

* Wed Sep 07 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.52-1
- Update to 1.4.52

* Sat Sep 03 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.4.50-1
- Update to 1.4.50

* Wed Aug 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.49-1
- Upstream update

* Tue Aug 23 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.48-1
- Upstream update

* Fri Aug 05 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.43-1
- Upstream update

* Thu Aug 04 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.42-1
- Upstream update

* Tue Aug 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.41-1
- Upstream update

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.35-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.35-1
- New version from upstream

* Wed Jun 08 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.26-1
- New version from upstream

* Sat May 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.24-1
- New version from upstream

* Tue Mar 29 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.7-1
- New version from upstream

* Tue Mar 01 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.30-1
- New version from upstream

* Wed Feb 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.29-1
- New version from upstream

* Fri Feb 19 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.28-1
- New version from upstream

* Wed Feb 17 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.27-1
- New version from upstream

* Fri Feb 12 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.26-1
- New version from upstream

* Wed Feb 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.25-1
- New version from upstream

* Tue Feb 09 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.24-1
- New version from upstream

* Tue Feb 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.23-1
- New version from upstream

* Fri Jan 22 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.22-1
- New version from upstream

* Wed Jan 20 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.21-1
- New version from upstream

* Fri Jan 15 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.20-1
- New version from upstream

* Fri Jan 15 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.19-1
- New version from upstream

* Wed Jan 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.18-1
- New version from upstream

* Tue Jan 12 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.17-2
- Add testing for Fedora

* Thu Jan 07 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.17-1
- Update to upstream version

* Wed Jan 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.16-2
- Fix shabang on botocore/vendored/requests/packages/chardet/chardetect.py
- Fix shabang on botocore/vendored/requests/certs.py
- Remove the useless dependency with python-urllib3

* Wed Jan 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.16-1
- Update to new upstream version
- Fix Provides for EL6

* Tue Dec 29 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.15-1
- Update to current version
- Improve the spec

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 19 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.79.0-1
- New version

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.58.0-2
- Add Python 3 support

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.58.0-1
- Initial packaging
