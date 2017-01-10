%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-tripleoclient
Version:        5.4.1
Release:        1%{?dist}
Summary:        OpenstackClient plugin for tripleoclient

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-tripleoclient
Source0:        https://tarballs.openstack.org/python-tripleoclient/python-tripleoclient-%{upstream_version}.tar.gz

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
BuildRequires:  os-cloud-config
BuildRequires:  python-websocket-client
BuildRequires:  PyYAML
BuildRequires:  python-passlib
BuildRequires:  openstack-tripleo-common
BuildRequires:  python2-osc-lib-tests
BuildRequires:  python-requests-mock
BuildRequires:  git

Requires:       instack
Requires:       instack-undercloud
Requires:       python-cliff
Requires:       python-ironic-inspector-client
Requires:       python-ironicclient
Requires:       python-heatclient
Requires:       python-mistralclient
Requires:       python-openstackclient
Requires:       python-osc-lib >= 0.3.0
Requires:       os-cloud-config
Requires:       python-websocket-client
Requires:       python-passlib
Requires:       python-six
Requires:       sos
Requires:       openstack-tripleo-common

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
* Tue Jan 10 2017 Alfredo Moralejo <amoralej@redhat.com> 5.4.1-1
- Update to 5.4.1

* Tue Nov 15 2016 Alfredo Moralejo <amoralej@redhat.com> 5.4.0-1
- Update to 5.4.0

* Tue Oct 18 2016 Alfredo Moralejo <amoralej@redhat.com> 5.3.0-1
- Update to 5.3.0

* Wed Oct 6 2016 Alfredo Moralejo <amoralej@redhat.com> 5.2.1-0.1.34590ccgit
- Updated to post 5.2.0 (34590cc25b28581d964c68e459bd3a01b2cce4ec)

* Fri Sep 30 2016 Haikel Guemar <hguemar@fedoraproject.org> 5.2.0-1
- Update to 5.2.0

* Tue Sep 13 2016 Haikel Guemar <hguemar@fedoraproject.org> 5.0.0-1
- Update to 5.0.0

