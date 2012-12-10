Summary:	IP Flood Detector
Name:		ipflood
Version:	1.0
Release:	%mkrel 6
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



%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-6mdv2011.0
+ Revision: 619678
- the mass rebuild of 2010.0 packages

* Sun Oct 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-5mdv2010.0
+ Revision: 453484
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-3mdv2009.1
+ Revision: 298260
- rebuilt against libpcap-1.0.0

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.0-2mdv2009.0
+ Revision: 267123
- rebuild early 2009.0 package (before pixel changes)

* Tue Mar 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdv2008.1
+ Revision: 188543
- fix typo
- import ipflood


* Tue Mar 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdv2008.1
- initial Mandriva package
