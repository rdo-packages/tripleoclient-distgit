# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pydefault 3
%else
%global pydefault 2
%endif

%global pydefault_bin python%{pydefault}
%global pydefault_sitelib %python%{pydefault}_sitelib
%global pydefault_install %py%{pydefault}_install
%global pydefault_build %py%{pydefault}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global client tripleoclient

%global common_desc \
python-tripleoclient is a Python plugin to OpenstackClient \
for TripleO <https://github.com/openstack/python-tripleoclient>.

Name:           python-tripleoclient
Version:        XXX
Release:        XXX
Summary:        OpenstackClient plugin for tripleoclient

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-tripleoclient
Source0:        https://tarballs.openstack.org/python-tripleoclient/python-tripleoclient-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pydefault}-%{client}
Summary: OpenstackClient plugin for tripleoclient
%{?python_provide:%python_provide python%{pydefault}-%{client}}

BuildRequires:  python%{pydefault}-devel
BuildRequires:  python%{pydefault}-pbr
BuildRequires:  python%{pydefault}-setuptools
# testing requirements
BuildRequires:  python%{pydefault}-fixtures
BuildRequires:  python%{pydefault}-mock
BuildRequires:  python%{pydefault}-testrepository
BuildRequires:  python%{pydefault}-testtools
BuildRequires:  python%{pydefault}-cliff
BuildRequires:  python%{pydefault}-ironicclient
BuildRequires:  python%{pydefault}-ironic-inspector-client
BuildRequires:  python%{pydefault}-heatclient
BuildRequires:  python%{pydefault}-mistralclient
BuildRequires:  python%{pydefault}-openstackclient
BuildRequires:  python%{pydefault}-oslo-config
BuildRequires:  python%{pydefault}-zaqarclient
BuildRequires:  python%{pydefault}-testscenarios
BuildRequires:  python%{pydefault}-passlib
BuildRequires:  python%{pydefault}-osc-lib-tests
BuildRequires:  openstack-tripleo-common
BuildRequires:  redhat-lsb-core
BuildRequires:  openstack-macros
%if %{pydefault} == 2
BuildRequires:  PyYAML
BuildRequires:  python-psutil
BuildRequires:  python-requests-mock
BuildRequires:  python-websocket-client
%else
BuildRequires:  python%{pydefault}-PyYAML
BuildRequires:  python%{pydefault}-psutil
BuildRequires:  python%{pydefault}-requests-mock
BuildRequires:  python%{pydefault}-websocket-client
%endif

Requires:       jq
Requires:       openstack-selinux
Requires:       python%{pydefault}-babel >= 2.3.4
Requires:       python%{pydefault}-cliff
Requires:       python%{pydefault}-cryptography >= 1.7.2
Requires:       python%{pydefault}-heatclient >= 1.10.0
Requires:       python%{pydefault}-ironic-inspector-client >= 1.5.0
Requires:       python%{pydefault}-ironicclient >= 2.2.0
Requires:       python%{pydefault}-mistralclient >= 3.1.0
Requires:       python%{pydefault}-openstackclient >= 3.12.0
Requires:       python%{pydefault}-osc-lib >= 1.8.0
Requires:       python%{pydefault}-passlib
Requires:       python%{pydefault}-pbr
Requires:       python%{pydefault}-six
Requires:       python%{pydefault}-zaqarclient >= 1.0.0

%if %{pydefault} == 2
Requires:       python-ipaddress
Requires:       python-psutil
Requires:       python-simplejson >= 3.5.1
Requires:       python-websocket-client
%else
Requires:       python%{pydefault}-psutil
Requires:       python%{pydefault}-simplejson >= 3.5.1
Requires:       python%{pydefault}-websocket-client
%endif

Requires:       sos
Requires:       openstack-tripleo-common >= 9.1.0
Requires:       os-net-config

# Dependencies for a containerized undercloud
Requires:       python%{pydefault}-tripleoclient-heat-installer
# Dependency for correct validations
Requires:       openstack-tripleo-validations
# Dependency for image building
Requires:       openstack-tripleo-image-elements
Requires:       openstack-tripleo-puppet-elements

Obsoletes: python-rdomanager-oscplugin < 0.0.11
Provides: python-rdomanager-oscplugin = %{version}-%{release}

%description -n python%{pydefault}-%{client}
%{common_desc}

%package -n python%{pydefault}-%{client}-heat-installer
Summary:        Components required for a containerized undercloud
%{?python_provide:%python_provide python%{pydefault}-%{client}-heat-installer}

# Required for containerized undercloud
Requires:       docker
Requires:       docker-distribution
Requires:       python-ipaddr
Requires:       openvswitch
Requires:       openstack-heat-agents >= 1.6.0
Requires:       openstack-heat-api
Requires:       openstack-heat-engine
# required as we now use --heat-native
Requires:       openstack-heat-monolith
Requires:       openstack-tripleo-heat-templates >= 9.0.0
Requires:       puppet-tripleo >= 9.0.0

%description -n python%{pydefault}-%{client}-heat-installer
python-tripleoclient-heat-installer is a sub-package that contains all dependencies to
deploy a containerized undercloud with tripleo client.

%prep
%autosetup -n %{name}-%{upstream_version} -S git
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{pydefault_build}
PYTHONPATH=. oslo-config-generator-%{pydefault} --config-file=config-generator/undercloud.conf

%install
%{pydefault_install}
# undercloud.conf.sample needs to be copied by the user when deploying an undercloud,
# so 644 is enough to make it happen. Note instack-undercloud had similar permissions for
# this file.
install -p -D -m 644 undercloud.conf.sample  %{buildroot}/%{_datadir}/%{name}/undercloud.conf.sample
mkdir -p %{buildroot}/%{_sharedstatedir}/tripleo-heat-installer

%check
PYTHON=%{pydefault_bin} PYTHONPATH=. %{pydefault_bin} setup.py testr

%files -n python%{pydefault}-%{client}
%{_datadir}/%{name}
%{pydefault_sitelib}/tripleoclient*
%{pydefault_sitelib}/python_tripleoclient*
%doc LICENSE README.rst
%dir %{_sharedstatedir}/tripleo-heat-installer

%files -n python%{pydefault}-%{client}-heat-installer

%changelog
