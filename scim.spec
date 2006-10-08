Summary:	Smart Common Input Method
Summary(pl):	Smart Common Input Method - ogólna metoda wprowadzania
Name:		scim
Version:	1.4.4
Release:	1
License:	LGPL
Group:		Applications
Source0:	http://dl.sourceforge.net/scim/%{name}-%{version}.tar.gz
# Source0-md5:	6805403b2151e89f17f5686e7ebcd515
URL:		http://www.scim-im.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	intltool >= 0.33
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pango-devel >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
scim is the core package of the SCIM project, which provides the
fundamental routines and data types. A gtk+2 based Panel (User
Interface) and setup dialog are also shipped within this package.

%description -l pl
scim to g³ówny pakiet projektu SCIM, udostêpniaj±cy podstawowe funkcje
i typy danych. W pakiecie za³±czony jest tak¿e oparty na GTK+ 2 panel
(interfejs u¿ytkownika) i konfiguracyjne okno dialogowe.

%prep
%setup -q

%build
%{__intltoolize}
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS TODO
