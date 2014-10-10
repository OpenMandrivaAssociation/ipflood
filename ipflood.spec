Summary:	IP Flood Detector
Name:		ipflood
Version:	1.0
Release:	8
License:	GPL
Group:		System/Servers
URL:		http://www.adotout.com/
Source0:	http://www.adotout.com/ip_flood_detector.tar.gz
Source1:	%{name}.service
Source2:	%{name}.sysconfig
BuildRequires:	libpcap-devel

%description
IP Flood Detector is a derivative of an earlier project, DNS Flood Detector. It
provides managers with an audit trail of TCP, UDP, and ICMP packet floods
directed at Internet-facing servers. When packet rates exceed a specified
threshold, IP Flood Detector will syslog the offending IP address, along with
the associated protocol and traffic volume.

%prep

%setup -q -n ip_flood_detector

cp %{SOURCE1} %{name}.service
cp %{SOURCE2} %{name}.sysconfig

%build
%serverbuild

gcc $CFLAGS -D_BSD_SOURCE -lpcap -lpthread -lm -o ip_flood_detector ip_flood_detector.c

%install
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/sysconfig

install -m0755 ip_flood_detector %{buildroot}%{_sbindir}/
install -m0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m0644 %{name}.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/ip_flood_detector

sed "s:sysconfig:%{_sysconfdir}/sysconfig:" -i %{buildroot}%{_unitdir}/%{name}.service

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean

%files
%doc README LICENSE
%config(noreplace) %{_sysconfdir}/sysconfig/ip_flood_detector
%attr(0644,root,root) %{_unitdir}/%{name}.service
%attr(0755,root,root) %{_sbindir}/ip_flood_detector
