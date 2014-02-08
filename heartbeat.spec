# When downloading directly from Mercurial, it will automatically add this prefix
# Invoking 'hg archive' wont but you can add one with:
# hg archive -t tgz -p "Linux-HA-Dev-" -r $upstreamversion $upstreamversion.tar.gz
%define upstreamprefix Heartbeat-3-0-
%define upstreamversion STABLE-3.0.5

%define gname haclient
%define uname hacluster

Summary:	Messaging and membership subsystem for High-Availability Linux
Name:		heartbeat
Version:	3.0.5
Release:	3
License:	GPLv2 and LGPLv2+
Url:		http://linux-ha.org/
Group:		System/Servers
Source0:	http://hg.linux-ha.org/heartbeat-STABLE_3_0/archive/STABLE-%{version}.tar.bz2
Patch1:		heartbeat-3.0.4-disable-xinclude.patch
Patch2:		heartbeat-3.0.0-haresources.patch
Patch3:		heartbeat-3.0.4-link.patch
Patch4:		heartbeat-3.0.4-lsbinit.patch
Patch5:		heartbeat-automake-1.13.patch

BuildRequires:	bison
BuildRequires:	docbook-style-xsl
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	iputils
BuildRequires:	mailx
BuildRequires:	which
BuildRequires:	xsltproc
BuildRequires:	bzip2-devel
BuildRequires:	cluster-glue-devel
BuildRequires:	libtool-devel
BuildRequires:	net-snmp-devel >= 5.4
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(zlib)
Requires:	python-pyxml
Requires:	resource-agents

%description
heartbeat is a basic high-availability subsystem for Linux-HA.
It will run scripts at initialization, and when machines go up or down.
This version will also perform IP address takeover using gratuitous ARPs.

Heartbeat contains a cluster membership layer, fencing, and local and
clusterwide resource management functionality.

When used with Pacemaker, it supports "n-node" clusters with significant 
capabilities for managing resources and dependencies.

In addition it continues to support the older release 1 style of
2-node clustering.

It implements the following kinds of heartbeats:
 - Serial ports
 - UDP/IP multicast (ethernet, etc)
 - UDP/IP broadcast (ethernet, etc)
 - UDP/IP heartbeats
 - "ping" heartbeats (for routers, switches, etc.)
 (to be used for breaking ties in 2-node systems)

%files
%doc %{_datadir}/doc/%{name}-%{version}
%dir %{_sysconfdir}/ha.d
%{_sysconfdir}/ha.d/harc
%{_sysconfdir}/ha.d/rc.d
%config(noreplace) %{_sysconfdir}/ha.d/README.config
%{_datadir}/heartbeat/
%{_sysconfdir}/ha.d/resource.d/
%{_sysconfdir}/init.d/heartbeat
%config(noreplace) %{_sysconfdir}/logrotate.d/heartbeat
%dir %{_var}/lib/heartbeat
%dir %{_var}/run/heartbeat
%attr (2755, %{uname}, %{gname}) %{_bindir}/cl_status
%{_bindir}/cl_respawn
%dir %attr (755, %{uname}, %{gname}) %{_var}/run/heartbeat/ccm
%{_mandir}/man1/cl_status.1*
%{_mandir}/man1/hb_standby.1*
%{_mandir}/man1/hb_takeover.1*
%{_mandir}/man1/hb_addnode.1*
%{_mandir}/man1/hb_delnode.1*
%{_mandir}/man8/heartbeat.8*
%{_mandir}/man8/apphbd.8*
%{_mandir}/man5/authkeys.5*
%{_mandir}/man5/ha.cf.5*
%{_libdir}/heartbeat

#---------------------------------------------------------
%define apphbmajor 2
%define libapphb %mklibname apphb %apphbmajor

%package -n %libapphb
Summary:	Heartbeat libraries
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %libapphb
Heartbeat library package.

%files -n %libapphb
%{_libdir}/libapphb.so.%{apphbmajor}*

#---------------------------------------------------------
%define ccmclientmajor 1
%define libccmclient %mklibname ccmclient %ccmclientmajor

%package -n %libccmclient
Summary:	Heartbeat libraries
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{_lib}heartbeat1 < 3.0.0

%description -n %libccmclient
Heartbeat library package.

%files -n %libccmclient
%{_libdir}/libccmclient.so.%{ccmclientmajor}*

#---------------------------------------------------------
%define clmmajor 1
%define libclm %mklibname clm %clmmajor

%package -n %libclm
Summary:	Heartbeat libraries
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{_lib}heartbeat1 < 3.0.0

%description -n %libclm
Heartbeat library package.

%files -n %libclm
%{_libdir}/libclm.so.%{clmmajor}*

#---------------------------------------------------------
%define hbclientmajor 1
%define libhbclient %mklibname hbclient %hbclientmajor

%package -n %libhbclient
Summary:	Heartbeat libraries
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{_lib}heartbeat1 < 3.0.0

%description -n %libhbclient
Heartbeat library package.

%files -n %libhbclient
%{_libdir}/libhbclient.so.%{hbclientmajor}*

#---------------------------------------------------------
%package devel
Summary:	Heartbeat development package
Group:		Development/Other
Requires:	%libapphb = %{version}-%{release}
Requires:	%libccmclient = %{version}-%{release}
Requires:	%libclm = %{version}-%{release}
Requires:	%libhbclient = %{version}-%{release}
Obsoletes:	%{_lib}heartbeat1-devel < 3.0.0

%description devel
Headers and shared libraries for writing programs for Heartbeat.

%files devel
%{_includedir}/*
%{_libdir}/*.so

#---------------------------------------------------------
%prep
%setup -q -n %{upstreamprefix}%{upstreamversion}
%patch1 -p1
%patch2 -p1 
%patch3 -p0 -b .link
%patch4 -p0
%patch5 -p1 -b .am113~

%build
./bootstrap
%configure2_5x --disable-fatal-warnings --disable-static

# get rid of rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
mkdir -p %{buildroot}
# disable xsltproc from trying to hit the net
export XSLTPROC_OPTIONS=""
%makeinstall_std

# cleanup
[ -d %{buildroot}/usr/man ] && rm -rf %{buildroot}/usr/man
[ -d %{buildroot}/usr/share/libtool ] && rm -rf %{buildroot}/usr/share/libtool
mv %{buildroot}/%{_datadir}/doc/%{name} %{buildroot}/%{_datadir}/doc/%{name}-%{version}
rm -rf %{buildroot}/%{_datadir}/heartbeat/cts

%post
%_post_service heartbeat

%preun
%_preun_service heartbeat

