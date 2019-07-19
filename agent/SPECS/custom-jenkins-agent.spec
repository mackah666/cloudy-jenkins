Name: custom-jenkins-agent
Version: 0.1.0%{?BUILD_NUMBER:.%{BUILD_NUMBER}}
Release: 1%{?dist}
Group: Applications/Internet
License: Internal BBC use only
Summary: custom-jenkins-agent
Source: src.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: cloud-jenkins-agents

# Uncomment the following to pull in the full set of extra packages from the
# cloud-jenkins seed repositories; they're disabled by default because they may
# interfere with other external packages.
#Requires: cloud-jenkins-agents-cosmos-cli
#Requires: cloud-jenkins-agents-forge-svn
#%if 0%{?rhel} < 7
#Requires: cloud-jenkins-agents-docker
#Requires: cloud-jenkins-agents-forge-artifactory
#Requires: cloud-jenkins-agents-houston
#Requires: cloud-jenkins-agents-mbt
#%endif

%description
custom-jenkins-agent


%prep
%setup -q -n src

%build

%install
mkdir -p %{buildroot}
cp -r * %{buildroot}/


%clean
rm -rf %{buildroot}


%files
%defattr(0644, root, root, 0755)
/etc/sudoers.d/*

%defattr(-, root, root, 0755)
/etc/bake-scripts/custom-agent
/usr/libexec/cloud-jenkins/*.d/*

%exclude /etc/bake-scripts/custom-agent/README
%exclude /etc/sudoers.d/README
%exclude /usr/libexec/cloud-jenkins/*.d/README
