%define kealibs asiodns asiolink cc cfgclient cryptolink d2srv database dhcp++ dhcp_ddns dhcpsrv dns++ eval exceptions hooks http log process stats util util-io
%define devel %mklibname -d kea

Name: kea
Version: 2.3.2
Release: 1
Source0: https://gitlab.isc.org/isc-projects/kea/-/archive/Kea-%{version}/kea-Kea-%{version}.tar.bz2
Patch0: kea-2.3.2-no-Lusrlib.patch
Summary: A DHCPv4 and DHCPv6 server
URL: https://www.isc.org/kea/
License: MPL-2.0
Group: Servers
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: make
BuildRequires: bison
BuildRequires: flex
BuildRequires: boost-devel
BuildRequires: python-sphinx
BuildRequires: cmake(log4cplus)
BuildRequires: python

%description
Kea provides DHCPv4 and DHCPv6 servers, a dynamic DNS update module,
a portable DHCP library, libdhcp++, a control agent that provides a management
REST interface, a NETCONF agent that provides a YANG/NETCONF interface for Kea,
and a DHCP benchmarking tool, perfdhcp.

%(for lib in %{kealibs}; do
cat <<EOF
%package -n %{_lib}kea-$lib
Summary: KEA $lib library
Group: System/Libraries

%description -n %{_lib}kea-$lib
KEA $lib library

%files -n %{_lib}kea-$lib
%{_libdir}/libkea-$lib.so*
EOF
done)

%package -n %{devel}
Summary: Development files for the KEA DHCP libraries
Group: Development/C
%(
for lib in %{kealibs}; do
echo "Requires: %{_lib}kea-$lib = %{EVRD}"
done)

%description -n %{devel}
Development files for the KEA DHCP libraries

%files -n %{devel}
%{_includedir}/kea

%prep
%autosetup -p1 -n kea-Kea-%{version}
libtoolize --force
autoheader
aclocal -I m4macros
automake -a
autoconf
%configure \
	--enable-perfdhcp \
	--enable-pgsql-ssl \
	--enable-generate-parser \
	--enable-shell \
	--enable-generate-docs

%build
%make_build

%install
%make_install

%files
%dir %{_sysconfdir}/kea
%config(noreplace) %{_sysconfdir}/kea/kea-ctrl-agent.conf
%config(noreplace) %{_sysconfdir}/kea/keactrl.conf
%config(noreplace) %{_sysconfdir}/kea/kea-dhcp4.conf
%config(noreplace) %{_sysconfdir}/kea/kea-dhcp6.conf
%config(noreplace) %{_sysconfdir}/kea/kea-dhcp-ddns.conf
%{_bindir}/kea-admin
%{_bindir}/kea-ctrl-agent
%{_bindir}/kea-dhcp-ddns
%{_bindir}/kea-dhcp4
%{_bindir}/kea-dhcp6
%{_bindir}/kea-lfc
%{_bindir}/kea-shell
%{_bindir}/keactrl
%{_bindir}/perfdhcp
%{_mandir}/man8/kea-admin.8*
%{_mandir}/man8/kea-ctrl-agent.8*
%{_mandir}/man8/kea-dhcp-ddns.8*
%{_mandir}/man8/kea-dhcp4.8*
%{_mandir}/man8/kea-dhcp6.8*
%{_mandir}/man8/kea-lfc.8*
%{_mandir}/man8/kea-netconf.8*
%{_mandir}/man8/kea-shell.8*
%{_mandir}/man8/keactrl.8*
%{_mandir}/man8/perfdhcp.8*
%dir %{_datadir}/kea
%{_datadir}/kea/api
%dir %{_datadir}/kea/scripts
%{_datadir}/kea/scripts/admin-utils.sh
%{_datadir}/kea/scripts/mysql
%{_datadir}/kea/scripts/pgsql
%doc %{_docdir}/kea
%{_libdir}/kea
%{python_sitelib}/kea
