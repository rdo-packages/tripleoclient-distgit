Name:           python-rdomanager-oscplugin
Version:        XXX
Release:        XXX{?dist}
Summary:        OpenstackClient plugin for RDO Manager

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-rdomanager-oscplugin
Source0:        https://pypi.python.org/packages/source/p/python-rdomanager-oscplugin/python-rdomanager-oscplugin-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr

Requires:       instack
Requires:       instack-undercloud
Requires:       python-ironic-discoverd
Requires:       python-ironicclient
Requires:       python-openstackclient

%description
python-rdomanager-oscplugin is a Python plugin to OpenstackClient
for RDO Manager <https://github.com/rdo-management>.


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
%{python2_sitelib}/rdomanager_oscplugin*
%{python2_sitelib}/python_rdomanager_oscplugin*
%doc LICENSE README.rst

%changelog
* Thu Mar 19 2015 Brad P. Crochet <brad@redhat.com> - 0.1.0-1
- Initial package.
