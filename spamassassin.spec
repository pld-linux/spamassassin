#
# Conditional build:
# _without_tests - do not perform "make test"
%include	/usr/lib/rpm/macros.perl
%define	pdir	Mail
%define	pnam	SpamAssassin
Summary:	A spam filter for email which can be invoked from mail delivery agents
Summary(pl):	Filtr antyspamowy, przeznaczony dla program�w dostarczaj�cych poczt� (MDA)
Group:		Applications/Mail
Version:	2.41
Release:	2
Name:		spamassassin
License:	Artistic
Source0:	http://spamassassin.org/released/%{pdir}-%{pnam}-%{version}.tar.gz
Patch0:		spamassassin-rc-script.patch
URL:		http://spamassassin.org/
BuildRequires:	perl >= 5.6
BuildRequires:	rpm-perlprov >= 3.0.3-16
%if %{?_without_tests:0}%{!?_without_tests:1}
BuildRequires:	perl-HTML-Parser >= 3
# are these really needed?
BuildRequires:	perl-MailTools
BuildRequires:	perl-MIME-Base64
BuildRequires:	perl-MIME-tools
%endif
Prereq:		/sbin/chkconfig
Requires:	perl-Mail-SpamAssassin >= %{version}
Obsoletes:	SpamAssassin
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(Razor2::Client::Agent)' 'perl(Razor::Agent)' 'perl(Razor::Client)' 'perl(DBI)'

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
See /usr/share/doc/spamassassin-tools-*/.

%description tools -l pl
Przer�ne narz�dzia, dystrybuowane razem z SpamAssassin. Zobacz
/usr/share/doc/spamassassin-tools-*/.

%package -n perl-Mail-SpamAssassin
Summary:	%{pdir}::%{pnam} -- SpamAssassin e-mail filter Perl modules
Summary(pl):	%{pdir}::%{pnam} -- modu�y Perla filtru poczty SpamAssassin
Group:		Development/Languages/Perl
Requires:	perl-HTML-Parser >= 3


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

%define		sa_confdir	$RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin

%prep -q
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p0

%build
%{__perl} Makefile.PL PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir}
%{__make} OPTIMIZE="%{rpmcflags}" PREFIX=%{_prefix}

%{!?_without_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{sa_confdir},/etc/rc.d/init.d}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
	LOCAL_RULES_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin

install rules/local.cf $RPM_BUILD_ROOT%{sa_confdir}

# shouldn't this script be called `spamd' instead?
install spamd/pld-rc-script.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/spamassassin

rm -f spamd/{*.sh,*.conf,spam*} contrib/snp.tar.gz

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
%doc BUGS Changes COPYRIGHT INSTALL README TRADEMARK
%doc sample-nonspam.txt sample-spam.txt spamd procmailrc.example
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/spamassassin
%dir %{_sysconfdir}/mail/spamassassin
%config(noreplace) %{_sysconfdir}/mail/spamassassin/*
%dir %{_datadir}/spamassassin
%config(noreplace) %{_datadir}/spamassassin/*
%{_mandir}/man1/*

%files tools
%defattr(644,root,root,755)
%doc sql tools masses contrib

%files -n perl-Mail-SpamAssassin
%defattr(644,root,root,755)
%{perl_sitelib}/Mail/*
%{_mandir}/man3/*
