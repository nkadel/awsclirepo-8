%global dummy Cython

Name:       python2-%dummy
Version:    0.14.1
Release:    0%{?dist}
Summary:    Dummy package depending on python-%dummy
License:    Public Domain
# On RHEL 6, EPEL package is Cython
%if 0%{?rhel} == 6
Requires:   Cython >= %version
%else
Requires:   python-%%dummy >= %%version
%endif
BuildArch:  noarch

%description
This package exists only to allow packagers to uniformly depend on
python2-%dummy instead of conditionalizing those dependencies based on the
version of EPEL or Fedora.  It contains no files.

%files

%changelog
* Sat Apr 13 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 0.3.12-0
- Initial version.
- Reset requirements on RHEL 6 to Cython, not python-Cyton
