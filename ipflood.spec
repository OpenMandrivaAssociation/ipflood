Summary:	IP Flood Detector
Name:		ipflood
Version:	1.0
Release:	%mkrel 4
License:	GPL
Group:		System/Servers
URL:		http://www.adotout.com/
Source0:	http://www.adotout.com/ip_flood_detector.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	libpcap-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
IP Flood Detector is a derivative of an earlier project, DNS Flood Detector. It
provides managers with an audit trail of TCP, UDP, and ICMP packet floods
directed at Internet-facing servers. When packet rates exceed a specified
threshold, IP Flood Detector will syslog the offending IP address, along with
the associated protocol and traffic volume.

%prep

%setup -q -n ip_flood_detector

cp %{SOURCE1} %{name}.init
cp %{SOURCE2} %{name}.sysconfig

%build
%serverbuild

gcc $CFLAGS -D_BSD_SOURCE -lpcap -lpthread -lm -o ip_flood_detector ip_flood_detector.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig

install -m0755 ip_flood_detector %{buildroot}%{_sbindir}/
install -m0755 %{name}.init %{buildroot}%{_initrddir}/%{name}
install -m0644 %{name}.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/ip_flood_detector

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README LICENSE
%config(noreplace) %{_sysconfdir}/sysconfig/ip_flood_detector
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0755,root,root) %{_sbindir}/ip_flood_detector

