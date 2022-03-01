%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/python-tripleoclient/python-tripleoclient-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
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
BuildRequires:  python3-openstackclient
BuildRequires:  python3-oslo-config
BuildRequires:  python3-testscenarios
BuildRequires:  python3-passlib
BuildRequires:  python3-osc-lib-tests
BuildRequires:  python3-ansible-runner
BuildRequires:  openstack-tripleo-common
BuildRequires:  hostname
BuildRequires:  openstack-macros
BuildRequires:  validations-common
BuildRequires:  python3-PyYAML
BuildRequires:  python3-psutil
BuildRequires:  python3-requests-mock
# Dependencies for task-core
BuildRequires:  python3-stevedore
BuildRequires:  python3-taskflow
BuildRequires:  python3-jsonschema
BuildRequires:  python3-networkx


Requires:       jq
Requires:       ncurses
Requires:       openstack-selinux
Requires:       python3-cliff
Requires:       python3-cryptography >= 2.1
Requires:       python3-heatclient >= 1.10.0
Requires:       python3-ironic-inspector-client >= 1.5.0
Requires:       python3-ironicclient >= 2.3.0
Requires:       python3-openstackclient >= 5.2.0
Requires:       python3-osc-lib >= 2.3.0
Requires:       python3-passlib
Requires:       python3-pbr
Requires:       python3-ansible-runner >= 1.4.5
Requires:       python3-openstacksdk >= 0.48.0
Requires:       validations-common
Requires:       python3-validations-libs >= 1.5.0

Requires:       python3-psutil
Requires:       python3-simplejson >= 3.5.1

Requires:       sos
Requires:       openstack-tripleo-common >= 16.3.0
Requires:       python3-tripleo-common >= 16.3.0
Requires:       os-net-config
Requires:       rsync

# Dependencies for task-core
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-taskflow >= 4.5.0
Requires:       python3-jsonschema >= 3.2.0
Requires:       python3-PyYAML >= 3.13
Requires:       python3-networkx >= 2.1.0

# Dependency for correct validations
Requires:       openstack-tripleo-validations

Requires:       buildah
Requires:       podman
Requires:       %{ovs_dep}
Requires:       openstack-heat-agents >= 1.6.0
Requires:       openstack-heat-api >= 1:16.0.0
Requires:       openstack-heat-engine >= 1:16.0.0
Requires:       openstack-heat-monolith >= 1:16.0.0
Requires:       openstack-tripleo-heat-templates >= 14.1.1
Requires:       puppet-tripleo >= 14.1.0
# Required for image uploading
Requires:       qemu-img

%description -n python3-%{client}
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}
PYTHONPATH=. oslo-config-generator --config-file=config-generator/undercloud.conf

%install
%{py3_install}
# undercloud.conf.sample needs to be copied by the user when deploying an undercloud,
# so 644 is enough to make it happen. Note instack-undercloud had similar permissions for
# this file.
install -p -D -m 644 undercloud.conf.sample  %{buildroot}/%{_datadir}/%{name}/undercloud.conf.sample

%check
PYTHON=%{__python3} stestr run

%files -n python3-%{client}
%{_datadir}/%{name}
%{python3_sitelib}/tripleoclient*
%{python3_sitelib}/python_tripleoclient*
%doc LICENSE README.rst

%changelog
