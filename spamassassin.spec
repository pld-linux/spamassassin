#
# Conditional build:
%bcond_with  tests	# perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	Mail
%define	pnam	SpamAssassin
Summary:	A spam filter for email which can be invoked from mail delivery agents
Summary(pl.UTF-8):   Filtr antyspamowy, przeznaczony dla programów dostarczających pocztę (MDA)
Name:		spamassassin
Version:	3.0.1
Release:	1
License:	Apache Software License v2
Group:		Applications/Mail
Source0:	http://www.apache.org/dist/spamassassin/%{pdir}-%{pnam}-%{version}.tar.bz2
# Source0-md5:	83f60f97c823d9b8df19309247fe33eb
Source1:	%{name}.sysconfig
Source2:	%{name}-spamd.init
URL:		http://spamassassin.apache.org/
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.16
BuildRequires:	perl(Digest::SHA1) >= 2.10
%if %{with tests}
BuildRequires:	perl-HTML-Parser >= 3
# are these really needed?
BuildRequires:	perl-MailTools
BuildRequires:	perl-MIME-Base64
BuildRequires:	perl-MIME-tools
%endif
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	perl-Mail-SpamAssassin >= %{version}
Obsoletes:	SpamAssassin
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl.UTF-8
SpamAssassin udostępnia Ci możliwość zredukowania, jeśli nie
kompletnego wyeliminowania Niezamawianej Komercyjnej Poczty
(Unsolicited Commercial Email, spamu) z Twojej poczty. Może być
wywoływany z MDA, np. Sendmaila czy Postfixa, lub z pliku ~/.forward
itp. Używa ogólnego algorytmu oceniania w celu identyfikacji
wiadomości, które wyglądają na SPAM, po czym dodaje nagłówki do
wiadomości, umożliwiając filtrowanie przez oprogramowanie użytkownika.
Ta dystrybucja zawiera programy spamd/spamc, umożliwiające
uruchomienie serwera, co znacznie przyspieszy proces przetwarzania
poczty.

%package tools
Summary:	Miscleanous tools for SpamAssassin
Summary(pl.UTF-8):   Przeróżne narzędzia związane z SpamAssassin
Group:		Applications/Mail
Obsoletes:	SpamAssassin-tools

%description tools
Miscleanous tools from various authors, distributed with SpamAssassin.
See /usr/share/doc/spamassassin-tools-*/.

%description tools -l pl.UTF-8
Przeróżne narzędzia, dystrybuowane razem z SpamAssassin. Zobacz
/usr/share/doc/spamassassin-tools-*/.

%package spamd
Summary:	spamd - daemonized version of spamassassin
Summary(pl.UTF-8):   spamd - spamassassin w postaci demona
Group:		Applications/Mail
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig

%description spamd
The purpose of this program is to provide a daemonized version of the
spamassassin executable. The goal is improving throughput performance
for automated mail checking.

This is intended to be used alongside "spamc", a fast, low-overhead C
client program.

%description spamd -l pl.UTF-8
Spamd jest "demoniczną" wersją spamassassina. Jego zadaniem jest
poprawa wydajności automatycznego sprawdzania poczty.

Spamd powinien być używany wespół ze "spamc", który jest szybkim i
wydajnym programem klienckim.

%package spamc
Summary:	spamc - client for spamd
Summary(pl.UTF-8):   spamc - klient dla spamd
Group:		Applications/Mail

%description spamc
Spamc is the client half of the spamc/spamd pair. It should be used in
place of "spamassassin" in scripts to process mail. It will read the
mail from STDIN, and spool it to its connection to spamd, then read
the result back and print it to STDOUT. Spamc has extremely low
overhead in loading, so it should be much faster to load than the
whole spamassassin program.

%description spamc -l pl.UTF-8
Spamc powinien być używany zamiast "spamassassina" w skryptach
przetwarzających pocztę. Zczytuje pocztę ze STDIN, kolejkuje ją a
następnie przekazuje spamd'owi, odczytuje wynik i podaje go na STDOUT.
Spamc stara się nie obciążać zbytnio procesora podczas ładowania,
dzięki czemu powinien działać szybciej niż sam spamassassin.

%package -n perl-Mail-SpamAssassin
Summary:	Mail::SpamAssassin - SpamAssassin e-mail filter libraries
Summary(pl.UTF-8):   Mail::SpamAssassin - biblioteki filtra poczty SpamAssassin
Group:		Development/Languages/Perl
Requires:	perl-HTML-Parser >= 3
Requires:	perl-Cache-DB_File >= 0.2

%description -n perl-Mail-SpamAssassin
Mail::SpamAssassin is a Mail::Audit plugin to identify spam using text
analysis and several internet-based realtime blacklists. Using its
rule base, it uses a wide range of heuristic tests on mail headers and
body text to identify ``spam'', also known as unsolicited commercial
email. Once identified, the mail can then be optionally tagged as spam
for later filtering using the user's own mail user-agent application.

%description -n perl-Mail-SpamAssassin -l pl.UTF-8
Mail::SpamAssassin jest pluginem dla Mail::Audit, służącym do
identyfikacji spamu przy użyciu analizy zawartości i/lub internetowych
czarnych list. Do zidentyfikowania jako ,,spam'' stosuje szeroki
zakres testów heurystycznych na nagłówkach i treści, posiłkując się
stworzoną wcześniej bazą reguł. Po zidentyfikowaniu, poczta może być
oznaczona jako spam w celu późniejszego wyfiltrowania, np. przy użyciu
aplikacji do czytania poczty.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
echo "postmaster@localhost" | \
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	PREFIX=%{_prefix} \
	SYSCONFDIR=%{_sysconfdir} \
	ENABLE_SSL=yes \
	RUN_NET_TESTS=0 \
	PERL_BIN=%{__perl}
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_sysconfdir}/mail/spamassassin}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/spamassassin

# shouldn't this script be called `spamd' instead?
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/spamassassin

rm -f spamd/{*.sh,*.conf,spam*} contrib/snp.tar.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post spamd
/sbin/chkconfig --add spamassassin
if [ -f /var/lock/subsys/spamd ]; then
	/etc/rc.d/init.d/spamassassin restart 1>&2
else
	echo 'Run "/etc/rc.d/init.d/spamassassin start" to start the spamd daemon.'
fi

%preun spamd
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/spamd ]; then
		/etc/rc.d/init.d/spamassassin stop 1>&2
	fi
	/sbin/chkconfig --del spamassassin
fi

%files
%defattr(644,root,root,755)
%doc BUGS CREDITS Changes INSTALL README STATUS TRADEMARK UPGRADE USAGE
%doc procmailrc.example sample*.txt
%attr(755,root,root) %{_bindir}/sa-learn
%attr(755,root,root) %{_bindir}/spamassassin
%{_mandir}/man1/sa-learn*
%{_mandir}/man1/spamassassin*

%files tools
%defattr(644,root,root,755)
%doc sql tools masses contrib

%files spamd
%defattr(644,root,root,755)
%doc spamd/README*
%attr(754,root,root) /etc/rc.d/init.d/spamassassin
%attr(600,root,root) %config(noreplace) /etc/sysconfig/spamassassin
%attr(755,root,root) %{_bindir}/spamd
%{_mandir}/man1/spamd*

%files spamc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/spamc
%{_mandir}/man1/spamc*

%files -n perl-Mail-SpamAssassin
%defattr(644,root,root,755)
%doc sample-nonspam.txt sample-spam.txt
%dir %{_sysconfdir}/mail/spamassassin
%config(noreplace) %{_sysconfdir}/mail/spamassassin/*
%dir %{_datadir}/spamassassin
%config(noreplace) %{_datadir}/spamassassin/*
%{perl_vendorlib}/Mail/*
%{_mandir}/man3/*
