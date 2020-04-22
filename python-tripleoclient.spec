%global rhosp 0

# Macros for openvswitch/rdo-openvswitch
%if 0%{?rhel} > 7 && 0%{?rhosp} == 0
%global ovs_dep rdo-openvswitch
%else
%global ovs_dep openvswitch
%endif

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

%package -n python3-%{client}
Summary: OpenstackClient plugin for tripleoclient
%{?python_provide:%python_provide python3-%{client}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
# testing requirements
BuildRequires:  python3-stestr
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
BuildRequires:  python3-testscenarios
BuildRequires:  python3-passlib
BuildRequires:  python3-osc-lib-tests
BuildRequires:  python3-ansible-runner
BuildRequires:  openstack-tripleo-common
BuildRequires:  redhat-lsb-core
BuildRequires:  openstack-macros
BuildRequires:  validations-common
BuildRequires:  python3-PyYAML
BuildRequires:  python3-psutil
BuildRequires:  python3-requests-mock
BuildRequires:  python3-websocket-client

Requires:       jq
Requires:       ncurses
Requires:       openstack-selinux
Requires:       python3-babel >= 2.3.4
Requires:       python3-cliff
Requires:       python3-cryptography >= 2.1
Requires:       python3-heatclient >= 1.10.0
Requires:       python3-ironic-inspector-client >= 1.5.0
Requires:       python3-ironicclient >= 2.3.0
Requires:       python3-mistralclient >= 3.1.0
Requires:       python3-openstackclient >= 3.12.0
Requires:       python3-osc-lib >= 1.8.0
Requires:       python3-passlib
Requires:       python3-pbr
Requires:       python3-six
Requires:       python3-zaqarclient >= 1.0.0
Requires:       python3-ansible-runner >= 1.4.4
Requires:       validations-common

Requires:       python3-psutil
Requires:       python3-simplejson >= 3.5.1
Requires:       python3-websocket-client

Requires:       sos
Requires:       openstack-tripleo-common >= 10.7.0
Requires:       python3-tripleo-common >= 10.7.0
Requires:       os-net-config
Requires:       rsync

# Dependency for correct validations
Requires:       openstack-tripleo-validations
# Dependency for image building
Requires:       openstack-ironic-python-agent-builder
Requires:       openstack-tripleo-image-elements
Requires:       openstack-tripleo-puppet-elements
Requires:       xfsprogs

Requires:       buildah
Requires:       podman
Requires:       %{ovs_dep}
Requires:       openstack-heat-agents >= 1.6.0
Requires:       openstack-heat-api >= 11.0.0
Requires:       openstack-heat-engine >= 11.0.0
Requires:       python3-paunch >= 4.2.0
Requires:       openstack-heat-monolith >= 11.0.0
Requires:       openstack-tripleo-heat-templates >= 9.0.0
Requires:       puppet-tripleo >= 9.3.0

Obsoletes: python-rdomanager-oscplugin < 0.0.11
Provides: python-rdomanager-oscplugin = %{version}-%{release}

%description -n python3-%{client}
%{common_desc}

%prep
%autosetup -n %{name}-%{upstream_version} -S git
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}
PYTHONPATH=. oslo-config-generator --config-file=config-generator/undercloud.conf
PYTHONPATH=. oslo-config-generator --config-file=config-generator/minion.conf

%install
%{py3_install}
# undercloud.conf.sample needs to be copied by the user when deploying an undercloud,
# so 644 is enough to make it happen. Note instack-undercloud had similar permissions for
# this file.
install -p -D -m 644 undercloud.conf.sample  %{buildroot}/%{_datadir}/%{name}/undercloud.conf.sample
install -p -D -m 644 minion.conf.sample  %{buildroot}/%{_datadir}/%{name}/minion.conf.sample

%check
PYTHON=%{__python3} stestr run

%files -n python3-%{client}
%{_datadir}/%{name}
%{python3_sitelib}/tripleoclient*
%{python3_sitelib}/python_tripleoclient*
%doc LICENSE README.rst

%changelog
