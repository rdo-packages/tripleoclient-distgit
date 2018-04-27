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
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
# testing requirements
BuildRequires:  python2-fixtures
BuildRequires:  python2-mock
BuildRequires:  python2-testrepository
BuildRequires:  python2-testtools
BuildRequires:  python2-cliff
BuildRequires:  python2-ironicclient
BuildRequires:  python-ironic-inspector-client
BuildRequires:  python2-heatclient
BuildRequires:  python2-mistralclient
BuildRequires:  python2-openstackclient
BuildRequires:  python2-oslo-config
BuildRequires:  python-websocket-client
BuildRequires:  python2-zaqarclient
BuildRequires:  PyYAML
BuildRequires:  python2-passlib
BuildRequires:  openstack-tripleo-common
BuildRequires:  python2-osc-lib-tests
BuildRequires:  python-requests-mock
BuildRequires:  git
BuildRequires:  instack-undercloud
BuildRequires:  openstack-macros

Requires:       instack
Requires:       instack-undercloud
Requires:       openstack-selinux
Requires:       python2-babel >= 2.3.4
Requires:       python2-cliff
Requires:       python-ipaddress
Requires:       python-ironic-inspector-client >= 1.5.0
Requires:       python2-ironicclient >= 2.2.0
Requires:       python2-heatclient >= 1.10.0
Requires:       python2-mistralclient >= 3.1.0
Requires:       python2-openstackclient >= 3.12.0
Requires:       python2-osc-lib >= 1.8.0
Requires:       python2-pbr
Requires:       python2-psutil
Requires:       python-websocket-client
Requires:       python2-passlib
Requires:       python-simplejson >= 3.5.1
Requires:       python2-six
Requires:       sos
Requires:       openstack-tripleo-common >= 9.0.1
Requires:       python2-zaqarclient >= 1.0.0
Requires:       python2-cryptography >= 1.7.2
# Dependencies for a containerized undercloud
Requires:       python-tripleoclient-heat-installer

Obsoletes: python-rdomanager-oscplugin < 0.0.11
Provides: python-rdomanager-oscplugin = %{version}-%{release}

%description
python-tripleoclient is a Python plugin to OpenstackClient
for TripleO <https://github.com/openstack/python-tripleoclient>.

# Not supported by OSP yet
%package heat-installer
Summary:        Components required for a containerized undercloud

# Required for containerized undercloud
Requires:       docker
Requires:       docker-distribution
Requires:       python-ipaddr
Requires:       openvswitch
Requires:       openstack-heat-agents
Requires:       openstack-heat-api
Requires:       openstack-heat-engine
# required as we now use --heat-native
Requires:       openstack-heat-monolith
Requires:       openstack-tripleo-heat-templates >= 9.0.0
Requires:       puppet-tripleo >= 9.0.0

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
# undercloud.conf.sample needs to be copied by the user when deploying an undercloud,
# so 644 is enough to make it happen. Note instack-undercloud had similar permissions for
# this file.
install -p -D -m 644 undercloud.conf.sample  %{buildroot}/%{_datadir}/%{name}/undercloud.conf.sample

%check
PYTHONPATH=. %{__python2} setup.py testr

%files
%{_datadir}/%{name}
%{python2_sitelib}/tripleoclient*
%{python2_sitelib}/python_tripleoclient*
%doc LICENSE README.rst

%files heat-installer

%changelog
