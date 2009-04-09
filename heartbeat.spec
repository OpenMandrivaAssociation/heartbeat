%define _disable_ld_as_needed 1
%define _disable_ld_no_undefined 1

# compatability macros
%{!?lib: %global lib lib}
%{!?mklibname: %global mklibname(ds) %lib%{1}%{?2:%{2}}%{?3:_%{3}}%{-s:-static}%{-d:-devel}}
%{!?mkrel:%define mkrel(c:) %{-c:0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*)(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

%if %mdkversion <= 1000
%define __libtoolize /bin/true
%endif

%define heartmajor 1
%define libheart %mklibname heartbeat %heartmajor

%define stonithmajor 1
%define libstonith %mklibname heartbeat-stonith %stonithmajor

%define pilsmajor 1
%define libpils %mklibname heartbeat-pils %pilsmajor

%define apphbmajor 0
%define libapphb %mklibname heartbeat-apphb %apphbmajor

Summary:	Heartbeat subsystem for High-Availability Linux
Name:		heartbeat
Version:	2.1.3
Release:	%mkrel 2
License:	GPLv2+
URL:		http://linux-ha.org/
Group:		System/Servers
Source0:	http://linux-ha.org/download/%{name}-%{version}.tar.gz
Source1:	haresources
Source2:	ha.cf
Source3:	authkeys
Source4:	www.cf
Source5:	http://linux-ha.org/download/%{name}-%{version}.sums.asc
Patch0:		heartbeat-1.2.4-ldirectory-usage.patch
Patch1:		heartbeat-2.1.3-init.patch
Requires:	sysklogd
# http://qa.mandriva.com/show_bug.cgi?id=23050
Requires:	heartbeat-pils = %{version}-%{release}
BuildRequires:	bzip2-devel
BuildRequires:	db-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel
BuildRequires:	libcurl-devel
BuildRequires:	libgnutls-devel
BuildRequires:	libnet1.1.2-devel
BuildRequires:	libxml2-devel
BuildRequires:	lynx
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp
BuildRequires:	net-snmp-devel
BuildRequires:	openssh-clients
BuildRequires:	openssl-devel
BuildRequires:  pam-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	swig
Requires(pre):	rpm-helper
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-%{release}-buildroot

%description
heartbeat is a basic heartbeat subsystem for Linux-HA.
It will run scripts at initialization, and when machines go up or down.
This version will also perform IP address takeover using gratuitious ARPs.
It works correctly for a 2-node configuration, and is extensible to larger
configurations.

It implements the following kinds of heartbeats:
	- Bidirectional Serial Rings ("raw" serial ports)
	- UDP/IP braodcast (ethernet, etc)
	- Bidirectional Serial PPP/UDP Rings (using PPP)

%package -n	%{libheart}
Summary:	Development files from heartbeat
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n	%{libheart}
Library need by heartbeat
heartbeat is a basic heartbeat subsystem for Linux-HA.
It will run scripts at initialization, and when machines go up or down.
This version will also perform IP address takeover using gratuitious ARPs.
It works correctly for a 2-node configuration, and is extensible to larger
configurations.

It implements the following kinds of heartbeats:
    - Bidirectional Serial Rings ("raw" serial ports)
    - UDP/IP braodcast (ethernet, etc)
    - Bidirectional Serial PPP/UDP Rings (using PPP)

%package -n	%{libheart}-devel
Summary:	Development files from heartbeat
Group:		Development/Other
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libheart} = %{version}
Conflicts:	libheartbeat0-devel

%description -n	%{libheart}-devel
Development files from heartbeat
heartbeat is a basic heartbeat subsystem for Linux-HA.
It will run scripts at initialization, and when machines go up or down.
This version will also perform IP address takeover using gratuitious ARPs.
It works correctly for a 2-node configuration, and is extensible to larger
configurations.

It implements the following kinds of heartbeats:
    - Bidirectional Serial Rings ("raw" serial ports)
    - UDP/IP braodcast (ethernet, etc)
    - Bidirectional Serial PPP/UDP Rings (using PPP)

%package	ldirectord
Summary:	Monitor daemon for maintaining high availability resources
Group:		System/Servers
Requires:	perl perl-libwww-perl perl-Net_SSLeay.pm ipvsadm
Requires(pre): rpm-helper

%description	ldirectord
ldirectord is a stand-alone daemon to monitor services of real
for virtual services provided by The Linux Virtual Server
(http://www.linuxvirtualserver.org/). It is simple to install
and works with the heartbeat code (http://www.linux-ha.org/).

%package	stonith
Summary:	Provides an interface to Shoot The Other Node In The Head
Group:		System/Servers
Requires:	telnet

%description	stonith
The STONITH module (a.k.a. STOMITH) provides an extensible interface
for remotely powering down a node in the cluster.  The idea is quite simple:
When the software running on one machine wants to make sure another
machine in the cluster is not using a resource, pull the plug on the other
machine. It's simple and reliable, albeit admittedly brutal.

# this library was split from the main library package because
# it didn't change soname from heartbeat-1 to heartbeat-2, so it was
# conflicting
%package -n	%{libapphb}
Summary:	Library from heartbeat
Group:		System/Libraries
Provides:	libapphb = %{version}-%{release}
Provides:	libheartbeat-apphb = %{version}-%{release}
Conflicts:	libheartbeat0

%description -n %libapphb
This package contains the library used by the Application Heartbeat Monitor for
High-Availability Linux.

%package -n	%{libstonith}
Summary:	Library from heartbeat
Group:		System/Libraries
Provides:	libstonith = %{version}-%{release}
Provides:	libhearbeat-stonith = %{version}-%{release}

%description -n	%libstonith
The STONITH module (a.k.a. STOMITH) provides an extensible interface
for remotely powering down a node in the cluster.  The idea is quite simple:
When the software running on one machine wants to make sure another
machine in the cluster is not using a resource, pull the plug on the other
machine. It's simple and reliable, albeit admittedly brutal.

%package -n	%{libstonith}-devel
Summary:	Development files from heartbeat
Group:		Development/Other
Provides:	libstonith-devel = %{version}-%{release}
Provides:	libhearbeat-stonith-devel = %{version}-%{release}
Requires:	%{libstonith} = %{version}
Conflicts:	libheartbeat-stonith0-devel
# some files moved from one package to the other
Conflicts:	heartbeat-stonith < 2.0.7-2mdv2007.0

%description -n	%{libstonith}-devel
The STONITH module (a.k.a. STOMITH) provides an extensible interface
for remotely powering down a node in the cluster.  The idea is quite simple:
When the software running on one machine wants to make sure another
machine in the cluster is not using a resource, pull the plug on the other
machine. It's simple and reliable, albeit admittedly brutal.

%package	pils
Summary:	Provides a general plugin and interface loading library
Group:		System/Servers

%description	pils
PILS is an generalized and portable open source
Plugin and Interface Loading System.
PILS was developed as part of the Open Cluster Framework
reference implementation, and is designed
to be directly usable by a wide variety of other applications.
PILS manages both plugins (loadable objects),
and the interfaces these plugins implement.
PILS is designed to support any number of plugins
implementing any number of interfaces.

%package -n	%{libpils}
Summary:	Provides a general plugin and interface loading library
Group:		System/Libraries
Provides:	libpils = %{version}-%{release}
Provides:	libheartbeat-pils = %{version}-%{release}

%description -n %{libpils}
PILS is an generalized and portable open source
Plugin and Interface Loading System.
PILS was developed as part of the Open Cluster Framework
reference implementation, and is designed
to be directly usable by a wide variety of other applications.
PILS manages both plugins (loadable objects),
and the interfaces these plugins implement.
PILS is designed to support any number of plugins
implementing any number of interfaces.

%package -n	%{libpils}-devel
Summary:	Provides a general plugin and interface loading library
Group:		Development/Other
Requires:	%{libpils} = %{version}
Provides:	libpils-devel = %{version}-%{release}
Provides:	libheartbeat-pils-devel = %{version}-%{release}
Conflicts:	libheartbeat-pils0-devel

%description -n	%{libpils}-devel
PILS is an generalized and portable open source
Plugin and Interface Loading System.
PILS was developed as part of the Open Cluster Framework
reference implementation, and is designed
to be directly usable by a wide variety of other applications.
PILS manages both plugins (loadable objects),
and the interfaces these plugins implement.
PILS is designed to support any number of plugins
implementing any number of interfaces.

%prep
%setup -q
%patch0 -p1 -b .ldirectory-usage
%patch1 -p1 -b .provides

%build
%serverbuild

%configure2_5x \
    --enable-checkpointd \
    --localstatedir=/var \
    --with-initdir=%{_initrddir} \
    --disable-fatal-warnings

export LIBS="-L%{_libdir}"
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DUSE_VENDOR_CF_PATH=1"
%make

%install
rm -Rf %{buildroot}

%makeinstall_std docdir=%{_docdir}/%{name}
%multiarch_includes %{buildroot}%{_includedir}/pils/plugin.h
%multiarch_includes %{buildroot}%{_includedir}/heartbeat/heartbeat.h

install -d %{buildroot}%{_sysconfdir}/ha.d/ppp.d
install -d %{buildroot}%{_sysconfdir}/ha.d/conf

install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/ha.d
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/ha.d
install -m600 %{SOURCE3} %{buildroot}%{_sysconfdir}/ha.d
install -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/ha.d/conf

cd %{buildroot}%{_sysconfdir}/ha.d/resource.d
    ln -snf %{_sbindir}/ldirectord ldirectord
cd -

TEMPL=%{buildroot}%_localstatedir/lib/heartbeat/fillup-templates
install -d $TEMPL
install -m0644 rc.config.heartbeat $TEMPL
install -m0644 ldirectord/ldirectord.cf  %{buildroot}%{_sysconfdir}/ha.d/conf
perl -pi -e "s,$RPM_BUILD_DIR/%{name}-%{version},,g" %{buildroot}%{_libdir}/libstonith.la
rm -f %{buildroot}%{_libdir}/*.so

# python cleanup
find %{buildroot}%{_libdir}/heartbeat/ -type f -name '*.pyc' -exec rm -f {} \;
find %{buildroot}%{_libdir}/heartbeat/ -type f -name '*.pyo' -exec rm -f {} \;

%pre
if grep -q '^haclient:' etc/group >/dev/null ; then
: 
else
	GROUPOPT="-g 60"
	if
			usr/sbin/groupadd $GROUPOPT haclient 2>/dev/null
		then
		:
		else
			usr/sbin/groupadd haclient
		fi
fi

%post
#
#	Hack to allow ppp-udp to be notified about PPP processes starting
#
Install_PPP_hack() {
  file2hack=/etc/ppp/ip-up.local
  echo "NOTE: Modifying $file2hack"
  if
    [ ! -f $file2hack ]
  then
    echo '#!/bin/bash' > $file2hack
    chmod 755 $file2hack
  fi
  MARKER="Heartbeat"
  ed -s $file2hack <<-!EOF  2>/dev/null
H
g/ $MARKER\$/d
\$a
#	The following lines added for Linux-HA support		# $MARKER
DEVFILE=\`echo \$DEVICE | sed -e 's!^/dev/!!' -e 's!/!.!g'\`	# $MARKER
OUTFILE=/etc/ha.d/ppp.d/\$DEVFILE				# $MARKER
(			# $MARKER
echo "\$IPREMOTE"	# $MARKER
echo "\$IFNAME"		# $MARKER
echo "\$PPPD_PID"	# $MARKER
echo "\$IPLOCAL"		# $MARKER
) > \$OUTFILE		# $MARKER
.
w
!EOF
}

if
  [ ! -x /etc/ppp/ip-up.heart ]
then
  Install_PPP_hack
fi

# Run heartbeat on startup
%_post_service heartbeat

%preun

Uninstall_PPP_hack() {
  file2hack=/etc/ppp/ip-up.local
  echo "NOTE: Restoring $file2hack"
  MARKER="Heartbeat"
  ed -s $file2hack <<-!EOF  2>/dev/null
H
g/ $MARKER\$/d
w
!EOF
}

if [ $1 = 0 ]; then
%_preun_service heartbeat
  if [ ! -x /etc/ppp/ip-up.heart ]; then
    Uninstall_PPP_hack
  fi
fi

%post ldirectord
%_post_service ldirectord

%preun ldirectord
%_preun_service ldirectord

%if %mdkversion < 200900
%post -n %{libheart} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libheart} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libpils} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libpils} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libstonith} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libstonith} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README doc/AUTHORS doc/COPYING doc/ChangeLog
%doc doc/*.html doc/*.txt
%dir %{_sysconfdir}/ha.d
%config(noreplace) %{_sysconfdir}/ha.d/README.config
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ha.d/authkeys
%config(noreplace) %{_sysconfdir}/ha.d/ha.cf
%config(noreplace) %{_sysconfdir}/ha.d/harc
%config(noreplace) %{_sysconfdir}/ha.d/haresources
%config(noreplace) %{_sysconfdir}/ha.d/shellfuncs
%dir %{_sysconfdir}/ha.d/rc.d
%config(noreplace) %{_sysconfdir}/ha.d/rc.d/ask_resources
%config(noreplace) %{_sysconfdir}/ha.d/rc.d/ip-request
%config(noreplace) %{_sysconfdir}/ha.d/rc.d/ip-request-resp
%config(noreplace) %{_sysconfdir}/ha.d/rc.d/status
%config(noreplace) %{_sysconfdir}/ha.d/rc.d/hb_takeover
%dir %{_sysconfdir}/ha.d/ppp.d/
%dir %{_sysconfdir}/ha.d/conf/
%config(noreplace) %{_sysconfdir}/ha.d/conf/*
%config(noreplace) %{_sysconfdir}/pam.d/hbmgmtd
%dir %{_sysconfdir}/ha.d/resource.d/
%config(noreplace) %{_sysconfdir}/ha.d/resource.d/*
%config(noreplace) %{_sysconfdir}/logrotate.d/heartbeat
%attr(0755,root,root) %{_initrddir}/heartbeat
%{_bindir}/cl_status
%{_bindir}/cl_respawn
%{_bindir}/hb_gui
%{_sbindir}/attrd_updater
%{_sbindir}/ccm_tool
%{_sbindir}/cibadmin
%{_sbindir}/ciblint
%{_sbindir}/crm_*
%{_sbindir}/crmadmin
%{_sbindir}/ha_logger
%{_sbindir}/hb_report
%{_sbindir}/iso8601
%{_sbindir}/ocf-tester
%{_sbindir}/ptest
%{_mandir}/man1/cl_status.1*
%{_mandir}/man1/ha_logger.1*
%{_mandir}/man1/hb_addnode.1*
%{_mandir}/man1/hb_delnode.1*
%{_mandir}/man8/ha_logd.8*
%{_mandir}/man8/crm_resource.8*
%dir %{_libdir}/heartbeat
%{_libdir}/heartbeat/api_test
%{_libdir}/heartbeat/apphbd
%{_libdir}/heartbeat/apphbtest
%{_libdir}/heartbeat/atest
%{_libdir}/heartbeat/attrd
%{_libdir}/heartbeat/base64_md5_test
%{_libdir}/heartbeat/BasicSanityCheck
%{_libdir}/heartbeat/ccm
%{_libdir}/heartbeat/ccm_testclient
%{_libdir}/heartbeat/cib
%{_libdir}/heartbeat/cibmon
%{_libdir}/heartbeat/clmtest
%{_libdir}/heartbeat/crm_commands.py
%{_libdir}/heartbeat/crmd
%{_libdir}/heartbeat/crm.dtd
%{_libdir}/heartbeat/crm_primitive.py
%{_libdir}/heartbeat/crm_utils.py
%{_libdir}/heartbeat/cts
%{_libdir}/heartbeat/dopd
%{_libdir}/heartbeat/drbd-peer-outdater
%{_libdir}/heartbeat/findif
%{_libdir}/heartbeat/ha_config
%{_libdir}/heartbeat/ha_logd
%{_libdir}/heartbeat/ha_logger
%{_libdir}/heartbeat/ha_propagate
%{_libdir}/heartbeat/haresources2cib.py
%{_libdir}/heartbeat/hb_addnode
%{_libdir}/heartbeat/hb_delnode
%{_libdir}/heartbeat/hb_setsite
%{_libdir}/heartbeat/hb_setweight
%{_libdir}/heartbeat/hb_standby
%{_libdir}/heartbeat/hb_takeover
%{_libdir}/heartbeat/heartbeat
%{_libdir}/heartbeat/ipctest
%{_libdir}/heartbeat/ipctransientclient
%{_libdir}/heartbeat/ipctransientserver
%{_libdir}/heartbeat/ipfail
%{_libdir}/heartbeat/logtest
%{_libdir}/heartbeat/lrmadmin
%{_libdir}/heartbeat/lrmd
%{_libdir}/heartbeat/lrmtest
%{_libdir}/heartbeat/lrmtest/LRMBasicSanityCheck
%{_libdir}/heartbeat/mach_down
%{_libdir}/heartbeat/mgmtd
%{_libdir}/heartbeat/mgmtdtest
%{_libdir}/heartbeat/mlock
%{_libdir}/heartbeat/ocf-returncodes
%{_libdir}/heartbeat/ocf-shellfuncs
%{_libdir}/heartbeat/pengine
%{_libdir}/heartbeat/pingd
%{_libdir}/heartbeat/quorumd
%{_libdir}/heartbeat/quorumdtest
%{_libdir}/heartbeat/recoverymgrd
%{_libdir}/heartbeat/req_resource
%{_libdir}/heartbeat/ResourceManager
%{_libdir}/heartbeat/send_arp
%{_libdir}/heartbeat/tengine
%{_libdir}/heartbeat/TestHeartbeatComm
%{_libdir}/heartbeat/transient-test.sh
%{_libdir}/heartbeat/ttest
%{_libdir}/heartbeat/utillib.sh
%dir %{_libdir}/heartbeat-gui
%{_libdir}/heartbeat-gui/*
%exclude %{_libdir}/heartbeat-gui/*.a
%exclude %{_libdir}/heartbeat-gui/*.la
%exclude %{_libdir}/heartbeat-gui/*.so
%dir %{_libdir}/heartbeat/plugins
%dir %{_libdir}/heartbeat/plugins/*
%{_libdir}/heartbeat/plugins/*/*.so
%{_datadir}/locale/zh_CN/LC_MESSAGES/haclient.mo
%{_mandir}/man8/apphbd*
%{_mandir}/man8/heartbeat*
%{_mandir}/man1/hb_standby*
%{_mandir}/man1/hb_takeover*
%{_mandir}/man8/cibadmin*
%dir %{_localstatedir}/lib/heartbeat
%dir %{_localstatedir}/lib/heartbeat/fillup-templates
%{_localstatedir}/lib/heartbeat/fillup-templates/*
%{_datadir}/heartbeat/BasicSanityCheck
%{_datadir}/heartbeat/crm.dtd
%{_datadir}/heartbeat/cts/CIB.py
%{_datadir}/heartbeat/cts/CIB.pyc
%{_datadir}/heartbeat/cts/CIB.pyo
%{_datadir}/heartbeat/cts/CM_fs.py
%{_datadir}/heartbeat/cts/CM_fs.pyc
%{_datadir}/heartbeat/cts/CM_fs.pyo
%{_datadir}/heartbeat/cts/CM_hb.py
%{_datadir}/heartbeat/cts/CM_hb.pyc
%{_datadir}/heartbeat/cts/CM_hb.pyo
%{_datadir}/heartbeat/cts/CM_LinuxHAv2.py
%{_datadir}/heartbeat/cts/CM_LinuxHAv2.pyc
%{_datadir}/heartbeat/cts/CM_LinuxHAv2.pyo
%{_datadir}/heartbeat/cts/CTSaudits.py
%{_datadir}/heartbeat/cts/CTSaudits.pyc
%{_datadir}/heartbeat/cts/CTSaudits.pyo
%{_datadir}/heartbeat/cts/CTSlab.py
%{_datadir}/heartbeat/cts/CTSlab.pyc
%{_datadir}/heartbeat/cts/CTSlab.pyo
%{_datadir}/heartbeat/cts/CTSproxy.py
%{_datadir}/heartbeat/cts/CTS.py
%{_datadir}/heartbeat/cts/CTS.pyc
%{_datadir}/heartbeat/cts/CTS.pyo
%{_datadir}/heartbeat/cts/CTStests.py
%{_datadir}/heartbeat/cts/CTStests.pyc
%{_datadir}/heartbeat/cts/CTStests.pyo
%{_datadir}/heartbeat/cts/extracttests.py
%{_datadir}/heartbeat/cts/extracttests.pyc
%{_datadir}/heartbeat/cts/extracttests.pyo
%{_datadir}/heartbeat/cts/getpeinputs.sh
%{_datadir}/heartbeat/cts/LSBDummy
%{_datadir}/heartbeat/cts/OCFIPraTest.py
%{_datadir}/heartbeat/cts/OCFIPraTest.pyc
%{_datadir}/heartbeat/cts/OCFIPraTest.pyo
%{_datadir}/heartbeat/cts/README
%{_datadir}/heartbeat-gui/active-node.png
%{_datadir}/heartbeat-gui/add-resource.png
%{_datadir}/heartbeat-gui/cleanup-resource.png
%{_datadir}/heartbeat-gui/default-resource.png
%{_datadir}/heartbeat-gui/down-resource.png
%{_datadir}/heartbeat-gui/exit.png
%{_datadir}/heartbeat-gui/haclient.glade
%{_datadir}/heartbeat-gui/haclient.py
%{_datadir}/heartbeat-gui/ha.png
%{_datadir}/heartbeat-gui/login.png
%{_datadir}/heartbeat-gui/logout.png
%{_datadir}/heartbeat-gui/master-resource.png
%{_datadir}/heartbeat-gui/mgmtcmd.py
%{_datadir}/heartbeat-gui/remove-resource.png
%{_datadir}/heartbeat-gui/slave-resource.png
%{_datadir}/heartbeat-gui/standby-node.png
%{_datadir}/heartbeat-gui/start-resource.png
%{_datadir}/heartbeat-gui/stop-resource.png
%{_datadir}/heartbeat-gui/up-resource.png
%{_datadir}/heartbeat/ha_config
%{_datadir}/heartbeat/ha_propagate
%{_datadir}/heartbeat/hb_addnode
%{_datadir}/heartbeat/hb_delnode
%{_datadir}/heartbeat/hb_setsite
%{_datadir}/heartbeat/hb_setweight
%{_datadir}/heartbeat/hb_standby
%{_datadir}/heartbeat/hb_takeover
%{_datadir}/heartbeat/lrmtest/defaults
%{_datadir}/heartbeat/lrmtest/descriptions
%{_datadir}/heartbeat/lrmtest/evaltest.sh
%{_datadir}/heartbeat/lrmtest/language
%{_datadir}/heartbeat/lrmtest/lrmadmin-interface
%{_datadir}/heartbeat/lrmtest/LRMBasicSanityCheck
%{_datadir}/heartbeat/lrmtest/lrmregtest
%{_datadir}/heartbeat/lrmtest/lrmregtest-heartbeat
%{_datadir}/heartbeat/lrmtest/lrmregtest-lsb
%{_datadir}/heartbeat/lrmtest/README.regression
%{_datadir}/heartbeat/lrmtest/regression.sh
%{_datadir}/heartbeat/lrmtest/testcases/BSC
%{_datadir}/heartbeat/lrmtest/testcases/common.filter
%{_datadir}/heartbeat/lrmtest/testcases/metadata
%{_datadir}/heartbeat/lrmtest/testcases/metadata.exp
%{_datadir}/heartbeat/lrmtest/testcases/ra-list.sh
%{_datadir}/heartbeat/lrmtest/testcases/rscexec
%{_datadir}/heartbeat/lrmtest/testcases/rscexec.exp
%{_datadir}/heartbeat/lrmtest/testcases/rscmgmt
%{_datadir}/heartbeat/lrmtest/testcases/rscmgmt.exp
%{_datadir}/heartbeat/lrmtest/testcases/rscmgmt.log_filter
%{_datadir}/heartbeat/lrmtest/testcases/xmllint.sh
%{_datadir}/heartbeat/mach_down
%{_datadir}/heartbeat/req_resource
%{_datadir}/heartbeat/ResourceManager
%{_datadir}/heartbeat/stonithdtest/STONITHDBasicSanityCheck
%{_datadir}/heartbeat/TestHeartbeatComm
%{_datadir}/heartbeat/utillib.sh

%files -n %libheart
%defattr(-,root,root)
%doc README doc/AUTHORS doc/COPYING doc/ChangeLog
%{_libdir}/libcib.so.*
%{_libdir}/libcrmcommon.so.*
%{_libdir}/libhbclient.so.*
%{_libdir}/libhbmgmt.so.*
%{_libdir}/libhbmgmtclient.so.*
%{_libdir}/libhbmgmtcommon.so.*
%{_libdir}/libhbmgmttls.so.*
%{_libdir}/libccmclient.so.*
%{_libdir}/librecoverymgr.so.*
%{_libdir}/libclm.so.*
%{_libdir}/liblrm.so.*
%{_libdir}/libpengine.so.*
%{_libdir}/libpe_rules.so.*
%{_libdir}/libpe_status.so.*
%{_libdir}/libplumbgpl.so.*
%{_libdir}/libtransitioner.so.*
%_prefix/lib/ocf/resource.d/heartbeat/*
%_prefix/lib/ocf/resource.d/heartbeat/.ocf-*

%files -n %libapphb
%defattr(-,root,root)
%{_libdir}/libapphb.so.*

%files -n %libheart-devel
%defattr(-,root,root)
%doc README doc/AUTHORS doc/COPYING doc/ChangeLog
%{_libdir}/libapphb.a
%{_libdir}/libapphb.la
%{_libdir}/libccmclient.a
%{_libdir}/libccmclient.la
%{_libdir}/libcib.a
%{_libdir}/libcib.la
%{_libdir}/libcrmcommon.a
%{_libdir}/libcrmcommon.la
%{_libdir}/libhbmgmt.a
%{_libdir}/libhbmgmt.la
%{_libdir}/libhbmgmtclient.a
%{_libdir}/libhbmgmtclient.la
%{_libdir}/libhbmgmtcommon.a
%{_libdir}/libhbmgmtcommon.la
%{_libdir}/libhbmgmttls.a
%{_libdir}/libhbmgmttls.la
%{_libdir}/liblrm.a
%{_libdir}/liblrm.la
%{_libdir}/libpengine.a
%{_libdir}/libpengine.la
%{_libdir}/libplumbgpl.a
%{_libdir}/libplumbgpl.la
%{_libdir}/librecoverymgr.a
%{_libdir}/librecoverymgr.la
%{_libdir}/libtransitioner.a
%{_libdir}/libtransitioner.la
%{_libdir}/libhbclient.a
%{_libdir}/libhbclient.la
%{_libdir}/libpe_rules.a
%{_libdir}/libpe_rules.la
%{_libdir}/libpe_status.a
%{_libdir}/libpe_status.la
%{_libdir}/libplumb.a
%{_libdir}/libplumb.la
%{_libdir}/libclm.a
%{_libdir}/libclm.la
%{_libdir}/heartbeat/plugins/*/*.a
%{_libdir}/heartbeat/plugins/*/*.la
%{_libdir}/heartbeat-gui/*.a
%{_libdir}/heartbeat-gui/*.la
%{_libdir}/heartbeat-gui/*.so
%dir %{_includedir}/heartbeat
%{_includedir}/heartbeat/*.h
%{multiarch_includedir}/heartbeat/heartbeat.h
%dir %{_includedir}/ocf
%{_includedir}/ocf/*.h
%dir %{_includedir}/clplumbing
%{_includedir}/clplumbing/*.h
%{_includedir}/saf
%dir %{_includedir}/heartbeat/crm
%{_includedir}/heartbeat/crm/*
%dir %{_includedir}/heartbeat/fencing
%{_includedir}/heartbeat/fencing/*.h
%dir %{_includedir}/heartbeat/lrm
%{_includedir}/heartbeat/lrm/*.h
%dir %{_includedir}/heartbeat/mgmt
%{_includedir}/heartbeat/mgmt/*.h

%files ldirectord
%defattr(-,root,root)
%doc README doc/AUTHORS doc/COPYING doc/ChangeLog
%doc ldirectord/ldirectord.cf ldirectord/README
%config(noreplace) %{_sysconfdir}/ha.d/conf/ldirectord.cf
%config(noreplace) %{_sysconfdir}/logrotate.d/ldirectord
%attr(0755,root,root) %{_initrddir}/ldirectord
%{_sbindir}/ldirectord
%{_mandir}/man8/ldirectord*

%files stonith
%defattr(-,root,root)
%doc README doc/AUTHORS doc/COPYING doc/ChangeLog
%{_sbindir}/stonith
%{_sbindir}/meatclient
%{_libdir}/heartbeat/stonithd
%dir %{_libdir}/heartbeat/stonithdtest
%{_libdir}/heartbeat/stonithdtest/apitest
%dir %{_libdir}/stonith
%dir %{_libdir}/stonith/plugins
%dir %{_libdir}/stonith/plugins/stonith2
%dir %{_libdir}/stonith/plugins/external
%{_libdir}/stonith/plugins/stonith2/*.so
%{_libdir}/stonith/plugins/stonith2/ribcl.py
%{_libdir}/stonith/plugins/external/*
%{_mandir}/man8/stonith*
%{_mandir}/man8/meatclient*

%files -n %libstonith
%defattr(-,root,root)
%doc README doc/AUTHORS doc/COPYING doc/ChangeLog
%{_libdir}/libstonith.so.*
%{_libdir}/libstonithd.so.*

%files -n %libstonith-devel
%defattr(-,root,root)
%doc README doc/AUTHORS doc/COPYING doc/ChangeLog
%{_libdir}/libstonith.a
%{_libdir}/libstonith.la
%{_libdir}/libstonithd.a
%{_libdir}/libstonithd.la
%{_libdir}/stonith/plugins/stonith2/*.a
%{_libdir}/stonith/plugins/stonith2/*.la
%dir %{_includedir}/stonith
%{_includedir}/stonith/*.h

%files pils
%defattr(-,root,root)
%dir %{_libdir}/pils
%dir %{_libdir}/pils/plugins
%dir %{_libdir}/pils/plugins/InterfaceMgr
%{_libdir}/pils/plugins/InterfaceMgr/*.so

%files -n %libpils
%defattr(-,root,root)
%doc README doc/AUTHORS doc/COPYING doc/ChangeLog
%{_libdir}/libpils.so.*
%{_libdir}/libplumb.so.*

%files -n %libpils-devel
%defattr(-,root,root)
%doc README doc/AUTHORS doc/COPYING doc/ChangeLog
%dir %{_includedir}/pils
%{_includedir}/pils/*.h
%{multiarch_includedir}/pils/plugin.h
%{_libdir}/libpils.a
%{_libdir}/libpils.la
%{_libdir}/pils/plugins/InterfaceMgr/*.a
%{_libdir}/pils/plugins/InterfaceMgr/*.la
