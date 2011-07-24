Summary:	Smart Common Input Method
Summary(pl.UTF-8):	Smart Common Input Method - ogólna metoda wprowadzania
Name:		scim
Version:	1.4.10
Release:	1
License:	LGPL v2+
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/scim/%{name}_%{version}.tar.gz
# Source0-md5:	74a768e30c3b521e6c133be6359a868c
Source1:	%{name}.xinputd
Patch0:		%{name}-gtk2-immodule-dir.patch
Patch1:		%{name}-config.patch
URL:		http://www.scim-im.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	intltool >= 0.33
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pango-devel >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	im-chooser
Requires:	imsettings
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
scim is the core package of the SCIM project, which provides the
fundamental routines and data types. A GTK+ 2 based Panel (User
Interface) and setup dialog are also shipped within this package.

%description -l pl.UTF-8
scim to główny pakiet projektu SCIM, udostępniający podstawowe funkcje
i typy danych. W pakiecie załączony jest także oparty na GTK+ 2 panel
(interfejs użytkownika) i konfiguracyjne okno dialogowe.

%package libs
Summary:	Smart Common Input Method libraries
Summary(pl.UTF-8):	Biblioteki Smart Common Input Method
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}

%description libs
Smart Common Input Method libraries.

%description libs -l pl.UTF-8
Biblioteki Smart Common Input Method.

%package devel
Summary:	Header files for SCIM libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek SCIM
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for SCIM libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek SCIM.

%package static
Summary:	Static SCIM libraries
Summary(pl.UTF-8):	Statyczne biblioteki SCIM
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SCIM libraries.

%description static -l pl.UTF-8
Statyczne biblioteki SCIM.

%package gtk2
Summary:	Smart Common Input Method Gtk IM module
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2
Requires(post):	gtk+2
Requires(postun):	gtk+2

%description gtk2
This package provides a GTK input method module for SCIM.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--enable-ld-version-script

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinput.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -e 's|@@LIB@@|%{_lib}|g' %{SOURCE1} >$RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinput.d/scim.conf

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/scim-1.0/*/*/*.{la,a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/immodules/im-scim.{la,a}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post gtk2
%if "%{_lib}" != "lib"
%{_bindir}/gtk-query-immodules-2.0-64 > %{_sysconfdir}/gtk64-2.0/gtk.immodules
%else
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules
%endif

%postun gtk2
%if "%{_lib}" != "lib"
%{_bindir}/gtk-query-immodules-2.0-64 > %{_sysconfdir}/gtk64-2.0/gtk.immodules
%else
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules
%endif

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS TODO
%dir %{_sysconfdir}/scim
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scim/config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scim/global
%{_sysconfdir}/X11/xinit/xinput.d/scim.conf
%attr(755,root,root) %{_bindir}/scim
%attr(755,root,root) %{_bindir}/scim-config-agent
%attr(755,root,root) %{_bindir}/scim-setup
%dir %{_libdir}/scim-1.0/*/Filter
%dir %{_libdir}/scim-1.0/*/FrontEnd
%dir %{_libdir}/scim-1.0/*/Helper
%dir %{_libdir}/scim-1.0/*/SetupUI
%attr(755,root,root) %{_libdir}/scim-1.0/*/Filter/*.so
%attr(755,root,root) %{_libdir}/scim-1.0/*/FrontEnd/*.so
%attr(755,root,root) %{_libdir}/scim-1.0/*/Helper/*.so
%attr(755,root,root) %{_libdir}/scim-1.0/*/SetupUI/*.so
%attr(755,root,root) %{_libdir}/scim-1.0/scim-helper-launcher
%attr(755,root,root) %{_libdir}/scim-1.0/scim-helper-manager
%attr(755,root,root) %{_libdir}/scim-1.0/scim-launcher
%attr(755,root,root) %{_libdir}/scim-1.0/scim-panel-gtk
%{_datadir}/scim
#%{_datadir}/gnome/capplets/scim-setup.desktop
%{_desktopdir}/scim-setup.desktop
%{_pixmapsdir}/scim-setup.png

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libscim-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libscim-1.0.so.[0-9]
%attr(755,root,root) %{_libdir}/libscim-gtkutils-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libscim-gtkutils-1.0.so.[0-9]
%attr(755,root,root) %{_libdir}/libscim-x11utils-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libscim-x11utils-1.0.so.[0-9]
%dir %{_libdir}/scim-1.0
%dir %{_libdir}/scim-1.0/*
%dir %{_libdir}/scim-1.0/*/Config
%dir %{_libdir}/scim-1.0/*/IMEngine
%attr(755,root,root) %{_libdir}/scim-1.0/*/Config/*.so
%attr(755,root,root) %{_libdir}/scim-1.0/*/IMEngine/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libscim-1.0.so
%attr(755,root,root) %{_libdir}/libscim-gtkutils-1.0.so
%attr(755,root,root) %{_libdir}/libscim-x11utils-1.0.so
%dir %{_includedir}/scim-1.0
%{_includedir}/scim-1.0/scim*.h
%{_includedir}/scim-1.0/gtk
%{_includedir}/scim-1.0/x11
%{_pkgconfigdir}/scim.pc
%{_pkgconfigdir}/scim-gtkutils.pc
%{_pkgconfigdir}/scim-x11utils.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libscim-1.0.a
%{_libdir}/libscim-gtkutils-1.0.a
%{_libdir}/libscim-x11utils-1.0.a

%files gtk2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gtk-2.0/*/immodules/im-scim.so
