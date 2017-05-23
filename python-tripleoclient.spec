%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:           python-tripleoclient
Version:        2.2.0
Release:        1%{?dist}
Summary:        OpenstackClient plugin for tripleoclient

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-tripleoclient
Source0:        https://tarballs.openstack.org/python-tripleoclient/python-tripleoclient-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools

Requires:       instack
Requires:       instack-undercloud
Requires:       python-ironic-inspector-client
Requires:       python-ironicclient
Requires:       python-openstackclient
Requires:	python-passlib
Requires:       sos
Requires:       tripleo-common

Obsoletes: python-rdomanager-oscplugin < 0.0.11
Provides: python-rdomanager-oscplugin = %{version}-%{release}

%description
python-tripleoclient is a Python plugin to OpenstackClient
for TripleO <https://github.com/openstack/python-tripleoclient>.


%prep
%setup -q -n %{name}-%{upstream_version}

sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%{python2_sitelib}/tripleoclient*
%{python2_sitelib}/python_tripleoclient*
%doc LICENSE README.rst

%changelog
* Tue May 23 2017 Alfredo Moralejo <amoralej@redhat.com> 2.2.0-1
- Update to 2.2.0

* Fri May 13 2016 Thierry Vignaud <tvignaud@redhat.com> - 2.0.0-1.0.1
- bump release for rpmdiff

* Wed Mar 23 2016 RDO <rdo-list@redhat.com> 1.0.0-0.1
-  Rebuild for Mitaka 
