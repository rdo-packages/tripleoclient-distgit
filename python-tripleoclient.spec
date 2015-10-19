%global commit0 2aac09de13f4cfd4b9d87cdcdd860388e21aef0a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%{!?upstream_version: %global upstream_version %{version}}

Name:           python-tripleoclient
Version:        0.0.11
Release:        1%{?dist}
Summary:        OpenstackClient plugin for tripleoclient

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-tripleoclient
# Once we have stable branches and stable releases we can go back to using release tarballs
Source0:  https://github.com/openstack/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-pbr

Requires:       instack
Requires:       instack-undercloud
Requires:       python-ironic-inspector-client
Requires:       python-ironicclient
Requires:       python-openstackclient
Requires:       sos
Requires:       tripleo-common

Obsoletes: python-rdomanager-oscplugin < 0.0.9-1
Provides: python-rdomanager-oscplugin = %{version}-%{release}

%description
python-tripleoclient is a Python plugin to OpenstackClient
for TripleO <https://github.com/openstack/python-tripleoclient>.


%prep
%autosetup -n %{name}-%{commit0} -S git
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
* Mon Oct 19 2015 John Trowbridge <trown@redhat.com> - 0.0.11-1
- Use a source tarball for a git hash that has passed delorean CI for liberty release

* Thu Mar 19 2015 Brad P. Crochet <brad@redhat.com> - 0.0.10-1
- Initial package.
