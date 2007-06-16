# TODO
# - build lib{,ssl}spamc.so (if there is a point)
# - kill "update" subpackage and move it to perl-Mail-SpamAssassin?
#   it's `strongly recommended' in 3.2.0 (instead of `optional').
# - is it possible to package compiled results in -compile or the result is
#   site/machine dependant?
#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Mail
%define		pnam	SpamAssassin
%define		sa_version %(printf %d.%03d%03d $(echo %{version} | tr '.' ' '))
Summary:	A spam filter for email which can be invoked from mail delivery agents
Summary(pl.UTF-8):	Filtr antyspamowy, przeznaczony dla programów dostarczających pocztę (MDA)
Name:		spamassassin
Version:	3.2.1
Release:	3
License:	Apache Software License v2
Group:		Applications/Mail
Source0:	http://www.apache.net.pl/spamassassin/source/%{pdir}-%{pnam}-%{version}.tar.bz2
# Source0-md5:	7b2fdbcdca5e9a181d4bb1b17663c138
Source1:	%{name}.sysconfig
Source2:	%{name}-spamd.init
Source3:	%{name}-default.rc
Source4:	%{name}-spamc.rc
URL:		http://spamassassin.apache.org/
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.16
BuildRequires:	perl-Archive-Tar
BuildRequires:	perl-DBI
BuildRequires:	perl-DB_File
BuildRequires:	perl-Digest-SHA1 >= 2.10
BuildRequires:	perl-HTML-Parser >= 3
BuildRequires:	perl-IO-Socket-INET6 >= 2.51
BuildRequires:	perl-IO-Socket-SSL
BuildRequires:	perl-IO-Zlib
BuildRequires:	perl-IP-Country
BuildRequires:	perl-Mail-SPF-Query
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Net-Ident
#BuildRequires:	perl-Razor2
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	perl-libwww
BuildRequires:	re2c
BuildRequires:	rpmbuild(macros) >= 1.310
%if %{with tests}
# are these really needed?
BuildRequires:	perl-Encode-Detect
BuildRequires:	perl-MIME-Base64
BuildRequires:	perl-MIME-tools
BuildRequires:	perl-Mail-DKIM
BuildRequires:	perl-Mail-DomainKeys
BuildRequires:	perl-Mail-SPF
BuildRequires:	perl-MailTools
BuildRequires:	perl-Razor > 2.61
BUildRequires:	perl-Compress-Zlib
%endif
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	perl-Mail-SpamAssassin = %{version}-%{release}
Obsoletes:	SpamAssassin
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(Razor2::Client::Agent)' 'perl(Razor::Agent)' 'perl(Razor::Client)' 'perl(DBI)' 'perl(Net::Ident)'

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

To enable spamassassin, if you are receiving mail locally, simply add
this line to your ~/.procmailrc:
INCLUDERC=/etc/mail/spamassassin/spamassassin-default.rc

To filter spam for all users, add that line to /etc/procmailrc
(creating if necessary).

%description -l pl.UTF-8
SpamAssassin daje możliwość zredukowania, jeśli nie kompletnego
wyeliminowania niezamawianej komercyjnej poczty (Unsolicited
Commercial Email, spamu) z poczty. Może być wywoływany z MDA, np.
Sendmaila czy Postfiksa, lub z pliku ~/.forward itp. Używa ogólnego
algorytmu oceniania w celu identyfikacji wiadomości, które wyglądają
na SPAM, po czym dodaje nagłówki do wiadomości, umożliwiając
filtrowanie przez oprogramowanie użytkownika. Ta dystrybucja zawiera
programy spamd/spamc, umożliwiające uruchomienie serwera, co znacznie
przyspieszy proces przetwarzania poczty.

%package tools
Summary:	Miscleanous tools for SpamAssassin
Summary(pl.UTF-8):	Przeróżne narzędzia związane z SpamAssassin
Group:		Applications/Mail
Obsoletes:	SpamAssassin-tools

%description tools
Miscleanous tools from various authors, distributed with SpamAssassin.
See /usr/share/doc/spamassassin-tools-*/.

%description tools -l pl.UTF-8
Przeróżne narzędzia, dystrybuowane razem ze SpamAssassinem. Więcej
informacji w /usr/share/doc/spamassassin-tools-*/.

%package spamd
Summary:	spamd - daemonized version of spamassassin
Summary(pl.UTF-8):	spamd - spamassassin w postaci demona
Group:		Applications/Mail
Requires(post,preun):	/sbin/chkconfig
Requires:	perl-Mail-SpamAssassin = %{version}-%{release}
Requires:	rc-scripts

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
Summary(pl.UTF-8):	spamc - klient dla spamd
Group:		Applications/Mail

%description spamc
Spamc is the client half of the spamc/spamd pair. It should be used in
place of "spamassassin" in scripts to process mail. It will read the
mail from STDIN, and spool it to its connection to spamd, then read
the result back and print it to STDOUT. Spamc has extremely low
overhead in loading, so it should be much faster to load than the
whole spamassassin program.

To enable spamassassin, if you are receiving mail locally, simply add
this line to your ~/.procmailrc:
INCLUDERC=/etc/mail/spamassassin/spamassassin-spamc.rc

To filter spam for all users, add that line to /etc/procmailrc
(creating if necessary).

%description spamc -l pl.UTF-8
Spamc powinien być używany zamiast "spamassassina" w skryptach
przetwarzających pocztę. Zczytuje pocztę ze STDIN, kolejkuje ją a
następnie przekazuje spamdowi, odczytuje wynik i podaje go na STDOUT.
Spamc stara się nie obciążać zbytnio procesora podczas ładowania,
dzięki czemu powinien działać szybciej niż sam spamassassin.

%package compile
Summary:	sa-compile - compile SpamAssassin ruleset into native code
Group:		Applications/Mail
Requires:	gcc
Requires:	glibc-devel
Requires:	make
Requires:	perl(ExtUtils::MakeMaker)
Requires:	perl-Mail-SpamAssassin = %{version}-%{release}
Requires:	perl-devel
Requires:	re2c >= 0.10

%description compile
sa-compile uses "re2c" to compile the SpamAssassin ruleset. This is
then used by the "Mail::SpamAssassin::Plugin::Rule2XSBody" plugin to
speed up SpamAssassin's operation, where possible, and when that
plugin is loaded.

%package update
Summary:	sa-update - automate SpamAssassin rule updates
Summary(pl.UTF-8):	sa-update - automatyczne uaktualnianie regułek SpamAssassina
Group:		Applications/Mail
Requires:	gnupg
Requires:	perl-Archive-Tar
Requires:	perl-Mail-SpamAssassin = %{version}-%{release}
Requires:	perl-libwww

%description update
sa-update automates the process of downloading and installing new
rules and configuration, based on channels. The default channel is
updates.spamassassin.org, which has updated rules since the previous
release.

Update archives are verified by default using SHA1 hashes and GPG
signatures.

%description update -l pl.UTF-8
sa-update automatyzuje proces ściągania i instalowania nowych regułek
i konfiguracji w oparciu o kanały. Domyślny kanał to
updates.spamassassin.org, który ma uaktualnione regułki od czasu
poprzedniego wydania.

Archiwa uaktualnień są sprawdzane domyślnie przy użyciu skrótów SHA1 i
podpisów GPG.

%package -n perl-Mail-SpamAssassin
Summary:	Mail::SpamAssassin - SpamAssassin e-mail filter libraries
Summary(pl.UTF-8):	Mail::SpamAssassin - biblioteki filtra poczty SpamAssassin
Group:		Development/Languages/Perl
Requires:	perl-Cache-DB_File >= 0.2
Requires:	perl-HTML-Parser >= 3
Requires:	perl-IO-Socket-INET6 >= 2.51
Requires:	perl-Mail-SPF-Query
Requires:	perl-Sys-Hostname-Long
Conflicts:	perl-Net-DNS < 0.50

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
# for spamc/configure
export CFLAGS="%{rpmcflags}"
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	PREFIX=%{_prefix} \
	SYSCONFDIR=%{_sysconfdir} \
	ENABLE_SSL=yes \
	CONTACT_ADDRESS="postmaster@localhost" \
	PERL_BIN=%{__perl} < /dev/null
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{__sed} -e "s,@@LOCAL_STATE_DIR@@,$(pwd)," sa-compile.raw > sa-compile.pl
%{__perl} -T sa-compile.pl --siteconfigpath=rules
rm -f compiled/%{sa_version}/auto/Mail/SpamAssassin/CompiledRegexps/body_0/.packlist

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_sysconfdir}/mail/spamassassin}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/spamd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/spamd
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin

# sa-update, sa-compile
install -d $RPM_BUILD_ROOT/var/lib/spamassassin/{%{sa_version},compiled/%{sa_version}}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin/sa-update-keys
touch $RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin/sa-update-keys/{pubring,secring,trustdb}.gpg
cp -a compiled/%{sa_version} $RPM_BUILD_ROOT/var/lib/spamassassin/compiled

rm -f $RPM_BUILD_ROOT{%{perl_archlib}/perllocal.pod,%{perl_vendorarch}/auto/Mail/SpamAssassin/.packlist,%{_mandir}/man3/spamassassin-run.*}

%clean
rm -rf $RPM_BUILD_ROOT

%post spamd
/sbin/chkconfig --add spamd
%service spamd restart

%preun spamd
if [ "$1" = "0" ]; then
	%service spamd stop
	/sbin/chkconfig --del spamd
fi

%triggerpostun spamd -- spamassassin-spamd < 3.1.0-5.3
# temp hack, should we care of the dead link?
ln -s spamd /etc/rc.d/init.d/spamassassin
/sbin/chkconfig --del spamassassin
rm -f /etc/rc.d/init.d/spamassassin
if [ -f /etc/sysconfig/spamassassin.rpmsave ]; then
	mv -f /etc/sysconfig/spamassassin.rpmsave /etc/sysconfig/spamd
fi

%files
%defattr(644,root,root,755)
%doc CREDITS Changes INSTALL README TRADEMARK UPGRADE USAGE
%doc procmailrc.example
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/spamassassin/spamassassin-default.rc
%attr(755,root,root) %{_bindir}/sa-learn
%attr(755,root,root) %{_bindir}/spamassassin

# It's needed for help of spamassassin command.
%{perl_vendorlib}/spamassassin-run.pod
%{_mandir}/man1/sa-learn*
%{_mandir}/man1/spamassassin*

%files tools
%defattr(644,root,root,755)
%doc sql ldap

%files spamd
%defattr(644,root,root,755)
%doc spamd/README*
%attr(754,root,root) /etc/rc.d/init.d/spamd
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/spamd
%attr(755,root,root) %{_bindir}/spamd
%{_mandir}/man1/spamd*

%files spamc
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/spamassassin/spamassassin-spamc.rc
%attr(755,root,root) %{_bindir}/spamc
%{_mandir}/man1/spamc*

%files compile
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sa-compile
%{_mandir}/man1/sa-compile*
%dir /var/lib/spamassassin/compiled
%dir /var/lib/spamassassin/compiled/%{sa_version}

# maybe include these in main package?
%dir /var/lib/spamassassin/compiled/%{sa_version}/auto
%dir /var/lib/spamassassin/compiled/%{sa_version}/auto/Mail
%dir /var/lib/spamassassin/compiled/%{sa_version}/auto/Mail/SpamAssassin/CompiledRegexps
%dir /var/lib/spamassassin/compiled/%{sa_version}/auto/Mail/SpamAssassin/CompiledRegexps/body_0
%config(noreplace) %verify(not md5 mtime size) %attr(755,root,root) /var/lib/spamassassin/compiled/%{sa_version}/auto/Mail/SpamAssassin/CompiledRegexps/body_0/body_0.so
%config(noreplace) %verify(not md5 mtime size) /var/lib/spamassassin/compiled/%{sa_version}/auto/Mail/SpamAssassin/CompiledRegexps/body_0/body_0.bs
%dir /var/lib/spamassassin/compiled/%{sa_version}/Mail
%dir /var/lib/spamassassin/compiled/%{sa_version}/Mail/SpamAssassin
%dir /var/lib/spamassassin/compiled/%{sa_version}/Mail/SpamAssassin/CompiledRegexps
%config(noreplace) %verify(not md5 mtime size) /var/lib/spamassassin/compiled/%{sa_version}/Mail/SpamAssassin/CompiledRegexps/body_0.pm
%config(noreplace) %verify(not md5 mtime size) /var/lib/spamassassin/compiled/%{sa_version}/bases_body_0.pl

%files update
%defattr(644,root,root,755)
%attr(700,root,root) %dir %{_sysconfdir}/mail/spamassassin/sa-update-keys
%attr(700,root,root) %ghost %{_sysconfdir}/mail/spamassassin/sa-update-keys/*
%attr(755,root,root) %{_bindir}/sa-update
%{_datadir}/spamassassin/sa-update-pubkey.txt
%dir /var/lib/spamassassin/%{sa_version}
%{_mandir}/man1/sa-update*

%files -n perl-Mail-SpamAssassin
%defattr(644,root,root,755)
%doc sample-nonspam.txt sample-spam.txt
%dir %{_sysconfdir}/mail/spamassassin
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/spamassassin/*.pre
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mail/spamassassin/*.cf
%exclude %{_sysconfdir}/mail/spamassassin/sa-update-keys

%dir %{_datadir}/spamassassin
%config(noreplace) %{_datadir}/spamassassin/*
%exclude %{_datadir}/spamassassin/sa-update-pubkey.txt

%dir /var/lib/spamassassin

%{perl_vendorlib}/Mail/*
%{_mandir}/man3/*
