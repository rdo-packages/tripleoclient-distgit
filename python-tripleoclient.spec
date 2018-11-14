# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver 3
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
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

%package -n python%{pyver}-%{client}
Summary: OpenstackClient plugin for tripleoclient
%{?python_provide:%python_provide python%{pyver}-%{client}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
# testing requirements
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-cliff
BuildRequires:  python%{pyver}-ironicclient
BuildRequires:  python%{pyver}-ironic-inspector-client
BuildRequires:  python%{pyver}-heatclient
BuildRequires:  python%{pyver}-mistralclient
BuildRequires:  python%{pyver}-openstackclient
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-passlib
BuildRequires:  python%{pyver}-osc-lib-tests
BuildRequires:  openstack-tripleo-common
BuildRequires:  redhat-lsb-core
BuildRequires:  openstack-macros
%if %{pyver} == 2
BuildRequires:  PyYAML
BuildRequires:  python-psutil
BuildRequires:  python-requests-mock
BuildRequires:  python-websocket-client
%else
BuildRequires:  python%{pyver}-PyYAML
BuildRequires:  python%{pyver}-psutil
BuildRequires:  python%{pyver}-requests-mock
BuildRequires:  python%{pyver}-websocket-client
%endif

Requires:       jq
Requires:       openstack-selinux
Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-cliff
Requires:       python%{pyver}-cryptography >= 2.1
Requires:       python%{pyver}-heatclient >= 1.10.0
Requires:       python%{pyver}-ironic-inspector-client >= 1.5.0
Requires:       python%{pyver}-ironicclient >= 2.3.0
Requires:       python%{pyver}-mistralclient >= 3.1.0
Requires:       python%{pyver}-openstackclient >= 3.12.0
Requires:       python%{pyver}-osc-lib >= 1.8.0
Requires:       python%{pyver}-passlib
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-six
Requires:       python%{pyver}-zaqarclient >= 1.0.0

%if %{pyver} == 2
Requires:       python-ipaddress
Requires:       python-psutil
Requires:       python-simplejson >= 3.5.1
Requires:       python-websocket-client
%else
Requires:       python%{pyver}-psutil
Requires:       python%{pyver}-simplejson >= 3.5.1
Requires:       python%{pyver}-websocket-client
%endif

Requires:       sos
Requires:       openstack-tripleo-common >= 10.0.0
Requires:       python%{pyver}-tripleo-common >= 10.0.0
Requires:       os-net-config

# Dependencies for a containerized undercloud
Requires:       python%{pyver}-tripleoclient-heat-installer
# Dependency for correct validations
Requires:       openstack-tripleo-validations
# Dependency for image building
Requires:       openstack-tripleo-image-elements
Requires:       openstack-tripleo-puppet-elements

Obsoletes: python-rdomanager-oscplugin < 0.0.11
Provides: python-rdomanager-oscplugin = %{version}-%{release}

%description -n python%{pyver}-%{client}
%{common_desc}

%package -n python%{pyver}-%{client}-heat-installer
Summary:        Components required for a containerized undercloud
%{?python_provide:%python_provide python%{pyver}-%{client}-heat-installer}

# Required for containerized undercloud
Requires:       docker
Requires:       docker-distribution
Requires:       podman
Requires:       python-ipaddr
Requires:       openvswitch
Requires:       openstack-heat-agents >= 1.6.0
Requires:       openstack-heat-api >= 11.0.0
Requires:       openstack-heat-engine >= 11.0.0
# required as we now use --heat-native
Requires:       openstack-heat-monolith >= 11.0.0
Requires:       openstack-tripleo-heat-templates >= 9.0.0
Requires:       puppet-tripleo >= 9.3.0

%description -n python%{pyver}-%{client}-heat-installer
python-tripleoclient-heat-installer is a sub-package that contains all dependencies to
deploy a containerized undercloud with tripleo client.

%prep
%autosetup -n %{name}-%{upstream_version} -S git
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{pyver_build}
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=config-generator/undercloud.conf

%install
%{pyver_install}
# undercloud.conf.sample needs to be copied by the user when deploying an undercloud,
# so 644 is enough to make it happen. Note instack-undercloud had similar permissions for
# this file.
install -p -D -m 644 undercloud.conf.sample  %{buildroot}/%{_datadir}/%{name}/undercloud.conf.sample
mkdir -p %{buildroot}/%{_sharedstatedir}/tripleo-heat-installer

%check
PYTHON=%{pyver_bin} PYTHONPATH=. %{pyver_bin} setup.py testr

%files -n python%{pyver}-%{client}
%{_datadir}/%{name}
%{pyver_sitelib}/tripleoclient*
%{pyver_sitelib}/python_tripleoclient*
%doc LICENSE README.rst
%dir %{_sharedstatedir}/tripleo-heat-installer

%files -n python%{pyver}-%{client}-heat-installer

%changelog
