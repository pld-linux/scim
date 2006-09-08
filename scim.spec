#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests
#
Summary:	Smart Common Input Method
Name:		scim
Version:	1.4.4
Release:	1
License:	LGPL
Group:		Applications
Source0:	http://dl.sourceforge.net/scim/scim-1.4.4.tar.gz
# Source0-md5:	6805403b2151e89f17f5686e7ebcd515
URL:		http://www.scim-im.org
BuildRequires:	gtk+2-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
scim is the core package of the SCIM project, which provides the fundamental routines and data types. A gtk+-2 based Panel (User Interface) and setup dialog are also shipped within this package.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%if %{with ldconfig}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%endif

%if %{with initscript}
%post init
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun init
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO

%if 0
# if _sysconfdir != /etc:
#%%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%endif

# initscript and its config
%if %{with initscript}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%endif

#%{_examplesdir}/%{name}-%{version}

%if %{with subpackage}
%files subpackage
%defattr(644,root,root,755)
#%doc extras/*.gz
#%{_datadir}/%{name}-ext
%endif
