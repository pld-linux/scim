Summary:	Smart Common Input Method
Summary(pl.UTF-8):	Smart Common Input Method - ogólna metoda wprowadzania
Name:		scim
Version:	1.4.9
Release:	2
License:	LGPL v2+
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/scim/%{name}-%{version}.tar.gz
# Source0-md5:	975ba34b01304ea8166ac8ea27aa9e88
Patch0:		%{name}-1.4.7-syslibltdl.patch
Patch1:		%{name}-1.4.8-fix-dlopen.patch
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		immodulesdir	%{_libdir}/gtk-2.0/%(pkg-config --variable=gtk_binary_version gtk+-2.0)/immodules

%description
scim is the core package of the SCIM project, which provides the
fundamental routines and data types. A GTK+ 2 based Panel (User
Interface) and setup dialog are also shipped within this package.

%description -l pl.UTF-8
scim to główny pakiet projektu SCIM, udostępniający podstawowe funkcje
i typy danych. W pakiecie załączony jest także oparty na GTK+ 2 panel
(interfejs użytkownika) i konfiguracyjne okno dialogowe.

%package devel
Summary:	Header files for SCIM libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek SCIM
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# evil empty file, source fails to find real ltdl.h because of this
! test -s src/ltdl.h
%{__rm} src/ltdl.h

for f in m4/intltool.m4 $(grep -l gettext- m4/*.m4 | xargs); do
	:> $f
done

%build
%{__gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%configure \
	--enable-ld-version-script \
	--with-gtk-im-module-dir=%{immodulesdir} \
	--disable-ltdl-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	gnomeccdir=%{_datadir}/gnome/capplets

rm -f $RPM_BUILD_ROOT%{_libdir}/scim-1.0/*/*/*.{la,a}
rm -f $RPM_BUILD_ROOT%{immodulesdir}/im-scim.{la,a}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS TODO
%attr(755,root,root) %{_bindir}/scim
%attr(755,root,root) %{_bindir}/scim-config-agent
%attr(755,root,root) %{_bindir}/scim-setup
%attr(755,root,root) %{_libdir}/libscim-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libscim-gtkutils-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libscim-x11utils-1.0.so.*.*.*
%dir %{_libdir}/scim-1.0
%dir %{_libdir}/scim-1.0/*
%dir %{_libdir}/scim-1.0/*/Config
%dir %{_libdir}/scim-1.0/*/Filter
%dir %{_libdir}/scim-1.0/*/FrontEnd
%dir %{_libdir}/scim-1.0/*/Helper
%dir %{_libdir}/scim-1.0/*/IMEngine
%dir %{_libdir}/scim-1.0/*/SetupUI
%attr(755,root,root) %{_libdir}/scim-1.0/*/*/*.so
%attr(755,root,root) %{_libdir}/scim-1.0/scim-helper-launcher
%attr(755,root,root) %{_libdir}/scim-1.0/scim-helper-manager
%attr(755,root,root) %{_libdir}/scim-1.0/scim-launcher
%attr(755,root,root) %{_libdir}/scim-1.0/scim-panel-gtk
%attr(755,root,root) %{immodulesdir}/im-scim.so
%dir %{_sysconfdir}/scim
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scim/config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scim/global
%{_datadir}/scim
#%{_datadir}/gnome/capplets/scim-setup.desktop
%{_desktopdir}/scim-setup.desktop
%{_pixmapsdir}/scim-setup.png

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libscim-1.0.so
%attr(755,root,root) %{_libdir}/libscim-gtkutils-1.0.so
%attr(755,root,root) %{_libdir}/libscim-x11utils-1.0.so
%{_libdir}/libscim-1.0.la
%{_libdir}/libscim-gtkutils-1.0.la
%{_libdir}/libscim-x11utils-1.0.la
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
