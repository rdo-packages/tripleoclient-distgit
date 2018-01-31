%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-tripleoclient
Version:        XXX
Release:        XXX
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
BuildRequires:  python-oslo-config
BuildRequires:  python-websocket-client
BuildRequires:  python-zaqarclient
BuildRequires:  PyYAML
BuildRequires:  python-passlib
BuildRequires:  openstack-tripleo-common
BuildRequires:  python2-osc-lib-tests
BuildRequires:  python-requests-mock
BuildRequires:  git
BuildRequires:  instack-undercloud
BuildRequires:  openstack-macros

Requires:       instack
Requires:       instack-undercloud
Requires:       openstack-selinux
Requires:       python-babel >= 2.3.4
Requires:       python-cliff
Requires:       python-ipaddress
Requires:       python-ironic-inspector-client >= 1.5.0
Requires:       python-ironicclient >= 1.14.0
Requires:       python-heatclient >= 1.6.1
Requires:       python-mistralclient >= 3.1.0
Requires:       python-openstackclient >= 3.12.0
Requires:       python-osc-lib >= 1.7.0
Requires:       python-pbr
Requires:       python-psutil
Requires:       python-websocket-client
Requires:       python-passlib
Requires:       python-simplejson >= 2.2.0
Requires:       python-six
Requires:       python-tripleoclient-heat-installer
Requires:       sos
Requires:       openstack-tripleo-common >= 7.1.0
Requires:       python-zaqarclient >= 1.0.0
Requires:       python-cryptography >= 1.6

Obsoletes: python-rdomanager-oscplugin < 0.0.11
Provides: python-rdomanager-oscplugin = %{version}-%{release}

%description
python-tripleoclient is a Python plugin to OpenstackClient
for TripleO <https://github.com/openstack/python-tripleoclient>.

%package heat-installer
Summary:        Components required for a containerized undercloud

# Required for containerized undercloud
Requires:       docker
Requires:       docker-distribution
Requires:       python-ipaddr
Requires:       openvswitch
Requires:       openstack-heat-agents
Requires:       openstack-heat-api
# required as we now use --heat-native
Requires:       openstack-heat-monolith
Requires:       openstack-puppet-modules
Requires:       openstack-tripleo-heat-templates
Requires:       puppet-tripleo

%description heat-installer
python-tripleoclient-heat-installer is a sub-package that contains all dependencies to
deploy a containerized undercloud with tripleo client.

%prep
%autosetup -n %{name}-%{upstream_version} -S git
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{__python2} setup.py build
PYTHONPATH=. oslo-config-generator --config-file=config-generator/undercloud.conf

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
install -p -D -m 640 undercloud.conf.sample  %{buildroot}/%{_datadir}/%{name}/undercloud.conf.sample

%check
PYTHONPATH=. %{__python2} setup.py testr

%files
%{_datadir}/%{name}
%{python2_sitelib}/tripleoclient*
%{python2_sitelib}/python_tripleoclient*
%doc LICENSE README.rst

%files heat-installer

%changelog
