%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname tripleoclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-tripleoclient
Version:        XXX
Release:        XXX
Summary:        OpenstackClient plugin for tripleoclient

License:        ASL 2.0
URL:            http://launchpad.net/python-tripleoclient/
Source0:        http://tarballs.openstack.org/python-tripleoclient/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
python-tripleoclient is a Python plugin to OpenstackClient
for TripleO <https://github.com/openstack/python-tripleoclient>.

%package -n python2-%{sname}
Summary:        OpenstackClient plugin for tripleoclient
%{?python_provide:%python_provide python2-%{sname}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr

Requires:       python-ironic-inspector-client
Requires:       python-ironicclient
Requires:       python-openstackclient
Requires:       python-websocket-client
Requires:       tripleo-common
Requires:       python-babel
Requires:       python-cliff
Requires:       python-passlib
Requires:       python-six
Requires:       python-ipaddress
Requires:       os-cloud-config
Requires:       python-websocket-client

Obsoletes: python-rdomanager-oscplugin < 0.0.11
Provides: python-rdomanager-oscplugin = %{version}-%{release}

%description -n python2-%{sname}
python-tripleoclient is a Python plugin to OpenstackClient
for TripleO <https://github.com/openstack/python-tripleoclient>.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:        OpenstackClient plugin for tripleoclient
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr

Requires:       python3-ironic-inspector-client
Requires:       python3-ironicclient
Requires:       python3-openstackclient
Requires:       python3-websocket-client
# FIX tripleo-common python 3 package name
Requires:       tripleo-common
Requires:       python3-babel
Requires:       python3-cliff
Requires:       python3-passlib
Requires:       python3-six
Requires:       python3-ipaddress
Requires:       python3-os-cloud-config
Requires:       python3-websocket-client

Obsoletes: python3-rdomanager-oscplugin < 0.0.11
Provides: python3-rdomanager-oscplugin = %{version}-%{release}

%description -n python3-%{sname}
python-tripleoclient is a Python plugin to OpenstackClient
for TripleO <https://github.com/openstack/python-tripleoclient>.
%endif

%package doc
Summary:          Documentation for OpenStack Tripleo API Client

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
Client library and command line utility for interacting with OpenStack
Tripleo's API.

%prep
%setup -q -n %{name}-%{upstream_version}

rm -rf {test-,}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/%{sname}/tests
%endif

%py2_install
# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/%{sname}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{sname}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%endif

%files doc
%doc html
%license LICENSE



%changelog
