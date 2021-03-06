#
# Conditional build:
%bcond_without	doc	# don't build ri/rdoc

%define		pkgname	sass
Summary:	A powerful but elegant CSS compiler that makes CSS fun again
Summary(pl.UTF-8):	Potężny, ale elegancki kompilator CSS przywracający przyjemność z CSS
Name:		ruby-%{pkgname}
Version:	3.4.22
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	857f0bc182b254271e3f03654ed5d2ab
Patch0:		version.patch
URL:		https://github.com/sass/sass
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby >= 1.8.7
BuildRequires:	sed >= 4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sass makes CSS fun again. Sass is an extension of CSS, adding nested
rules, variables, mixins, selector inheritance, and more. It's
translated to well-formatted, standard CSS using the command line tool
or a web-framework plugin.

%description -l pl.UTF-8
Sass czyni CSS z powrotem przyjemnym. Sass jest rozszerzeniem CSS,
dodającym zagnieżdżone reguły, zmienne, domieszki, dziedziczenie
selektorów itd. Jest tłumaczony na dobrze sformatowany, standardowy
XML przy użyciu narzędzia linii poleceń lub wtyczki do szkieletu WWW.

%package rdoc
Summary:	HTML documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla modułu %{pkgname} języka Ruby
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for Ruby %{pkgname} module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla modułu %{pkgname} języka Ruby.

%package ri
Summary:	ri documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu %{pkgname} języka Ruby
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for Ruby %{pkgname} module.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla modułu %{pkgname} języka Ruby.

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

%if %{with doc}
rdoc --ri --op ri lib
rdoc --op rdoc lib
%{__rm} -r ri/ActionController
%{__rm} -r ri/Merb
%{__rm} -r ri/OrderedHash
%{__rm} ri/cache.ri
%{__rm} ri/created.rid
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_ridir},%{ruby_rdocdir},%{_bindir}}

cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}

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
%{ruby_vendorlibdir}/sass
%{ruby_vendorlibdir}/sass.rb
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Sass
%endif
