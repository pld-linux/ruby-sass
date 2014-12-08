%define		pkgname	sass
Summary:	A powerful but elegant CSS compiler that makes CSS fun again
Name:		ruby-%{pkgname}
Version:	3.4.2
Release:	3
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	51f92be34834e250f4f55d93dbd2024a
Patch0:		version.patch
URL:		http://github.com/rtomayko/sass
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	sed >= 4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sass makes CSS fun again. Sass is an extension of CSS3, adding nested
rules, variables, mixins, selector inheritance, and more. It's
translated to well-formatted, standard CSS using the command line tool
or a web-framework plugin.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
s=$(ruby -e "puts File.read('VERSION').strip.split('.').map {|n| n =~ /^[0-9]+$/ ? n.to_i : n}.inspect")
%{__sed} -i -e "s#__VERSION__#$s#" lib/sass/version.rb
s=$(ruby -e "puts File.read('VERSION_NAME').strip.inspect")
%{__sed} -i -e "s#__VERSION_NAME__#$s#" lib/sass/version.rb

# write .gemspec
%__gem_helper spec

rdoc --ri --op ri lib
rdoc --op rdoc lib
rm ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir},%{_bindir}}

cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}

cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
install -d $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{ruby_specdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/sass
%attr(755,root,root) %{_bindir}/sass-convert
%attr(755,root,root) %{_bindir}/scss
%{ruby_rubylibdir}/sass
%{ruby_rubylibdir}/sass.rb
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Sass
