%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-tripleoclient
Version:        7.3.15
Release:        1%{?dist}
Summary:        OpenstackClient plugin for tripleoclient

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-tripleoclient
Source0:        https://tarballs.openstack.org/python-tripleoclient/python-tripleoclient-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
# testing requirements
BuildRequires:  python-fixtures
BuildRequires:  python-mock
BuildRequires:  python-testrepository
BuildRequires:  python-testtools
BuildRequires:  python-cliff
BuildRequires:  python-ironicclient
BuildRequires:  python-ironic-inspector-client
BuildRequires:  python-heatclient
BuildRequires:  python-mistralclient
BuildRequires:  python-openstackclient
BuildRequires:  python-websocket-client
BuildRequires:  python-zaqarclient
BuildRequires:  PyYAML
BuildRequires:  python-passlib
BuildRequires:  openstack-tripleo-common
BuildRequires:  python2-osc-lib-tests
BuildRequires:  python-requests-mock
BuildRequires:  git
BuildRequires:  instack-undercloud

Requires:       instack
Requires:       instack-undercloud
Requires:       python-babel >= 2.3.4
Requires:       python-cliff
Requires:       python-ipaddress
Requires:       python-ironic-inspector-client >= 1.5.0
Requires:       python-ironicclient >= 1.14.0
Requires:       python-heatclient >= 1.6.1
Requires:       python-mistralclient >= 3.1.0
Requires:       python-openstackclient >= 3.11.0
Requires:       python-osc-lib >= 1.7.0
Requires:       python-pbr
Requires:       python-websocket-client
Requires:       python-passlib
Requires:       python-simplejson >= 2.2.0
Requires:       python-six
Requires:       sos
Requires:       openstack-tripleo-common >= 7.1.0
Requires:       python-zaqarclient >= 1.0.0

Obsoletes: python-rdomanager-oscplugin < 0.0.11
Provides: python-rdomanager-oscplugin = %{version}-%{release}

%description
python-tripleoclient is a Python plugin to OpenstackClient
for TripleO <https://github.com/openstack/python-tripleoclient>.


%prep
%autosetup -n %{name}-%{upstream_version} -S git
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%check
PYTHONPATH=. %{__python2} setup.py testr

%files
%{python2_sitelib}/tripleoclient*
%{python2_sitelib}/python_tripleoclient*
%doc LICENSE README.rst

%changelog
* Tue May 14 2019 RDO <dev@lists.rdoproject.org> 7.3.15-1
- Update to 7.3.15

* Thu Sep 27 2018 RDO <dev@lists.rdoproject.org> 7.3.14-1
- Update to 7.3.14

* Wed Aug 08 2018 RDO <dev@lists.rdoproject.org> 7.3.12-1
- Update to 7.3.12

* Mon Jul 09 2018 RDO <dev@lists.rdoproject.org> 7.3.11-1
- Update to 7.3.11

* Mon Apr 23 2018 RDO <dev@lists.rdoproject.org> 7.3.10-1
- Update to 7.3.10

* Wed Mar 07 2018 RDO <dev@lists.rdoproject.org> 7.3.9-1
- Update to 7.3.9

* Mon Feb 12 2018 RDO <dev@lists.rdoproject.org> 7.3.8-1
- Update to 7.3.8

* Wed Jan 24 2018 RDO <dev@lists.rdoproject.org> 7.3.7-1
- Update to 7.3.7

* Sat Dec 09 2017 RDO <dev@lists.rdoproject.org> 7.3.6-1
- Update to 7.3.6

* Wed Nov 22 2017 RDO <dev@lists.rdoproject.org> 7.3.5-1
- Update to 7.3.5

* Tue Nov 14 2017 RDO <dev@lists.rdoproject.org> 7.3.4-1
- Update to 7.3.4

* Fri Nov 03 2017 RDO <dev@lists.rdoproject.org> 7.3.3-1
- Update to 7.3.3

* Tue Oct 10 2017 rdo-trunk <javier.pena@redhat.com> 7.3.2-1
- Update to 7.3.2

* Wed Oct 04 2017 rdo-trunk <javier.pena@redhat.com> 7.3.1-1
- Update to 7.3.1

* Sun Sep 10 2017 rdo-trunk <javier.pena@redhat.com> 7.3.0-1
- Update to 7.3.0

* Wed Aug 30 2017 Alan Pevec <alan.pevec@redhat.com> 7.2.0-1
- Update to 7.2.0

