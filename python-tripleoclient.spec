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
BuildRequires:  python-websocket-client
BuildRequires:  PyYAML
BuildRequires:  python-passlib
BuildRequires:  openstack-tripleo-common
BuildRequires:  python2-osc-lib-tests
BuildRequires:  python-requests-mock
BuildRequires:  git

Requires:       docker >= 1.12.6
Requires:       instack
Requires:       instack-undercloud
Requires:       openstack-heat-api
Requires:       openstack-heat-engine
Requires:       openstack-heat-monolith
Requires:       openstack-kolla
Requires:       openstack-puppet-modules
Requires:       openstack-tripleo-common >= 5.0.0
Requires:       openvswitch
Requires:       python-babel >= 2.3.4
Requires:       python-cliff
Requires:       python-heat-agent
Requires:       python-heat-agent-apply-config
Requires:       python-heat-agent-docker-cmd
Requires:       python-heat-agent-hiera
Requires:       python-heat-agent-json-file
Requires:       python-heat-agent-puppet
Requires:       python-heatclient >= 1.6.1
Requires:       python-ipaddr
Requires:       python-ipaddress
Requires:       python-ironic-inspector-client >= 1.5.0
Requires:       python-ironicclient >= 1.10.0
Requires:       python-mistralclient >= 2.0.0
Requires:       python-openstackclient >= 3.3.0
Requires:       python-osc-lib >= 1.2.0
Requires:       python-passlib
Requires:       python-pbr
Requires:       python-six
Requires:       python-websocket-client
Requires:       sos

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
