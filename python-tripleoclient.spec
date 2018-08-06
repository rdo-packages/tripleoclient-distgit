%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

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

%package -n python2-%{client}
Summary: OpenstackClient plugin for tripleoclient
%{?python_provide:%python_provide python2-%{client}}

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
BuildRequires:  python2-testscenarios
BuildRequires:  PyYAML
BuildRequires:  python2-passlib
BuildRequires:  openstack-tripleo-common
BuildRequires:  python2-osc-lib-tests
BuildRequires:  python-requests-mock
BuildRequires:  instack-undercloud

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
Requires:       openstack-tripleo-common >= 9.1.0
Requires:       os-net-config
Requires:       python2-zaqarclient >= 1.0.0
Requires:       python2-cryptography >= 1.7.2
# Dependencies for a containerized undercloud
Requires:       python-tripleoclient-heat-installer
# Dependency for correct validations
Requires:       openstack-tripleo-validations

Obsoletes: python-rdomanager-oscplugin < 0.0.11
Provides: python-rdomanager-oscplugin = %{version}-%{release}

%description -n python2-%{client}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{client}
Summary: OpenstackClient plugin for tripleoclient
%{?python_provide:%python_provide python3-%{client}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
# testing requirements
BuildRequires:  python3-fixtures
BuildRequires:  python3-mock
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools
BuildRequires:  python3-cliff
BuildRequires:  python3-ironicclient
BuildRequires:  python3-ironic-inspector-client
BuildRequires:  python3-heatclient
BuildRequires:  python3-mistralclient
BuildRequires:  python3-openstackclient
BuildRequires:  python3-oslo-config
BuildRequires:  python-websocket-client
BuildRequires:  python3-zaqarclient
BuildRequires:  python3-testscenarios
BuildRequires:  python3-PyYAML
BuildRequires:  python3-passlib
BuildRequires:  openstack-tripleo-common
BuildRequires:  python3-osc-lib-tests
BuildRequires:  python3-requests-mock
BuildRequires:  instack-undercloud

Requires:       instack
Requires:       instack-undercloud
Requires:       openstack-selinux
Requires:       python3-babel >= 2.3.4
Requires:       python3-cliff
Requires:       python3-ipaddress
Requires:       python3-ironic-inspector-client >= 1.5.0
Requires:       python3-ironicclient >= 2.2.0
Requires:       python3-heatclient >= 1.10.0
Requires:       python3-mistralclient >= 3.1.0
Requires:       python3-openstackclient >= 3.12.0
Requires:       python3-osc-lib >= 1.8.0
Requires:       python3-pbr
Requires:       python3-psutil
Requires:       python-websocket-client
Requires:       python3-passlib
Requires:       python-simplejson >= 3.5.1
Requires:       python3-six
Requires:       sos
Requires:       openstack-tripleo-common >= 9.1.0
Requires:       os-net-config
Requires:       python3-zaqarclient >= 1.0.0
Requires:       python3-cryptography >= 1.7.2
# Dependencies for a containerized undercloud
Requires:       python3-tripleoclient-heat-installer
# Dependency for correct validations
Requires:       openstack-tripleo-validations

%description -n python3-%{client}
%{common_desc}
%endif

%package -n python2-%{client}-heat-installer
Summary:        Components required for a containerized undercloud
%{?python_provide:%python_provide python2-%{client}-heat-installer}

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

%description -n python2-%{client}-heat-installer
python-tripleoclient-heat-installer is a sub-package that contains all dependencies to
deploy a containerized undercloud with tripleo client.

%if 0%{?with_python3}
%package -n  python3-%{client}-heat-installer
Summary:        Components required for a containerized undercloud
%{?python_provide:%python_provide python3-%{client}-heat-installer}

# Required for containerized undercloud
Requires:       docker
Requires:       docker-distribution
Requires:       python3-ipaddr
Requires:       openvswitch
Requires:       openstack-heat-agents >= 1.6.0
Requires:       openstack-heat-api
Requires:       openstack-heat-engine
# required as we now use --heat-native
Requires:       openstack-heat-monolith
Requires:       openstack-tripleo-heat-templates >= 9.0.0
Requires:       puppet-tripleo >= 9.0.0

%description -n python2-%{client}-heat-installer
python-tripleoclient-heat-installer is a sub-package that contains all dependencies to
deploy a containerized undercloud with tripleo client.

%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py2_build}
%if 0%{?with_python3}
%{py3_build}
%endif
PYTHONPATH=. oslo-config-generator --config-file=config-generator/undercloud.conf

%install
%{py2_install}
%if 0%{?with_python3}
%{py3_install}
%endif
# undercloud.conf.sample needs to be copied by the user when deploying an undercloud,
# so 644 is enough to make it happen. Note instack-undercloud had similar permissions for
# this file.
install -p -D -m 644 undercloud.conf.sample  %{buildroot}/%{_datadir}/%{name}/undercloud.conf.sample
mkdir -p %{buildroot}/%{_sharedstatedir}/tripleo-heat-installer

%check
PYTHONPATH=. %{__python2} setup.py testr
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{client}
%{_datadir}/%{name}
%{python2_sitelib}/tripleoclient*
%{python2_sitelib}/python_tripleoclient*
%doc LICENSE README.rst
%dir %{_sharedstatedir}/tripleo-heat-installer

%files -n python2-%{client}-heat-installer

%if 0%{?with_python3}
%files -n python3-%{client}
%{_datadir}/%{name}
%{python3_sitelib}/tripleoclient*
%{python3_sitelib}/python_tripleoclient*
%doc LICENSE README.rst
%dir %{_sharedstatedir}/tripleo-heat-installer

%files -n python3-%{client}-heat-installer

%endif

%changelog
