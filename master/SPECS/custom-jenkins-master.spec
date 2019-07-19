Name: custom-jenkins-master
Version: 0.1.0%{?BUILD_NUMBER:.%{BUILD_NUMBER}}
Release: 1%{?dist}
Group: Applications/Internet
License: Internal BBC use only
Summary: custom-jenkins-master
Source: src.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: cloud-jenkins-master

%description
custom-jenkins-master


%prep
%setup -q -n src

%build

%install
mkdir -p %{buildroot}
cp -r * %{buildroot}/


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
/etc/bake-scripts/custom-master
/usr/libexec/cloud-jenkins/*.d/*

%defattr(0644, root, root, 0755)
/etc/bake-scripts/public-endpoints/*
/etc/cloud-jenkins/backup.d/*

%exclude /etc/bake-scripts/custom-master/README
%exclude /usr/libexec/cloud-jenkins/*.d/README
%exclude /etc/bake-scripts/public-endpoints/README
%exclude /etc/cloud-jenkins/backup.d/README
