%include	/usr/lib/rpm/macros.perl
%define	pdir	Mail
%define	pnam	SpamAssassin
Summary:	A spam filter for email which can be invoked from mail delivery agents
Summary(pl):	Filtr antyspamowy, przeznaczony dla program�w dostarczaj�cych poczt� (MDA)
Group:		Applications/Mail
Version:	2.31
Release:	5
Name:		spamassassin
License:	GPL/Artistic
Source0:	http://spamassassin.org/released/%{pdir}-%{pnam}-%{version}.tar.gz
Patch0:		spamassassin-makefile.patch
Patch1:		spamassassin-rc-script.patch
URL:		http://spamassassin.org/
BuildRequires:	perl >= 5.6
BuildRequires:	rpm-perlprov >= 3.0.3-16
Prereq:		/sbin/chkconfig
Obsoletes:	SpamAssassin
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(Razor::Agent)' 'perl(Razor::Client)'

%description
SpamAssassin provides you with a way to reduce if not completely
eliminate Unsolicited Commercial Email (SPAM) from your incoming
email. It can be invoked by a MDA such as sendmail or postfix, or can
be called from a procmail script, .forward file, etc. It uses a
genetic-algorithm evolved scoring system to identify messages which
look spammy, then adds headers to the message so they can be filtered
by the user's mail reading software. This distribution includes the
spamd/spamc components which create a server that considerably speeds
processing of mail.

%description -l pl
SpamAssassin udost�pnia Ci mo�liwo�� zredukowania, je�li nie
kompletnego wyeliminowania Niezamawianej Komercyjnej Poczty
(Unsolicited Commercial Email, spamu) z Twojej poczty. Mo�e by�
wywo�ywany z MDA, np. Sendmaila czy Postfixa, lub z pliku ~/.forward
itp. U�ywa og�lnego algorytmu oceniania w celu identyfikacji
wiadomo�ci, kt�re wygl�daj� na SPAM, po czym dodaje nag��wki do
wiadomo�ci, umo�liwiaj�c filtrowanie przez oprogramowanie u�ytkownika.
Ta dystrybucja zawiera programy spamd/spamc, umo�liwiaj�ce
uruchomienie serwera, co znacznie przyspieszy proces przetwarzania
poczty.

%package tools
Summary:	Miscleanous tools for SpamAssassin
Summary(pl):	Przer�ne narz�dzia zwi�zane z SpamAssassin
Group:		Applications/Mail
Obsoletes:	SpamAssassin-tools

%description tools
Miscleanous tools from various authors, distributed with SpamAssassin.
See /usr/share/doc/SpamAssassin-tools-*/.

%description tools -l pl
Przer�ne narz�dzia, dystrybuowane razem z SpamAssassin. Zobacz
/usr/share/doc/SpamAssassin-tools-*/.


%package -n perl-Mail-SpamAssassin
Summary:	%{pdir}::%{pnam} -- SpamAssassin e-mail filter Perl modules
Summary(pl):	%{pdir}::%{pnam} -- modu�y Perla filtru poczty SpamAssassin
Group:		Development/Languages/Perl

%description -n perl-Mail-SpamAssassin
Mail::SpamAssassin is a Mail::Audit plugin to identify spam using text
analysis and several internet-based realtime blacklists. Using its
rule base, it uses a wide range of heuristic tests on mail headers and
body text to identify ``spam'', also known as unsolicited commercial
email. Once identified, the mail can then be optionally tagged as spam
for later filtering using the user's own mail user-agent application.

%description -n perl-Mail-SpamAssassin -l pl
Mail::SpamAssassin jest pluginem dla Mail::Audit, s�u��cym do
identyfikacji spamu przy u�yciu analizy zawarto�ci i/lub internetowych
czarnych list. Do zidentyfikowania jako ,,spam'' stosuje szeroki
zakres test�w heurystycznych na nag��wkach i tre�ci, posi�kuj�c si�
stworzon� wcze�niej baz� regu�. Po zidentyfikowaniu, poczta mo�e by�
oznaczona jako spam w celu p�niejszego wyfiltrowania, np. przy u�yciu
aplikacji do czytania poczty.


%prep -q
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p0
%patch1 -p1

%build
%{__perl} Makefile.PL PREFIX=%{_prefix}
%{__make} OPTIMIZE="%{rpmcflags}" PREFIX=%{_prefix}
#%make test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/mail/spamassassin,/etc/rc.d/init.d}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

# shouldn't this script be called `spamd' instead?
install spamd/pld-rc-script.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/spamassassin

rm -f spamd/{*.sh,*.conf,spam*} spamproxy/spamproxyd*

%post
if [ $1 = 1 ]; then
	/sbin/chkconfig --add spamassassin
fi
if [ -f /var/lock/subsys/spamassassin ]; then
	/etc/rc.d/init.d/spamassassin restart 1>&2
else
	echo 'Run "/etc/rc.d/init.d/spamassassin start" to start the spamd daemon.'
fi

%preun
if [ $1 = 0 ]; then
	if [ -f /var/lock/subsys/spamassassin ]; then
		/etc/rc.d/init.d/spamassassin stop 1>&2
	fi
	/sbin/chkconfig --del spamassassin
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README TODO sample-nonspam.txt sample-spam.txt spamd spamproxy
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/spamassassin
%config(noreplace) %{_sysconfdir}/mail/spamassassin
%config(noreplace) %{_datadir}/spamassassin
%{_mandir}/man1/*

%files tools
%defattr(644,root,root,755)
%doc sql tools masses contrib

%files -n perl-Mail-SpamAssassin
%defattr(644,root,root,755)
%{perl_sitelib}/Mail/*
%{perl_sitelib}/auto/Mail/*
%{_mandir}/man3/*
