#
# Conditional build:
%bcond_with	tests		# perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Mail
%define		pnam	SpamAssassin
Summary:	A spam filter for email which can be invoked from mail delivery agents
Summary(pl):	Filtr antyspamowy, przeznaczony dla programów dostarczaj±cych pocztê (MDA)
Name:		spamassassin
Version:	3.1.0
Release:	3
License:	Apache Software License v2
Group:		Applications/Mail
Source0:	http://www.apache.org/dist/spamassassin/source/%{pdir}-%{pnam}-%{version}.tar.bz2
# Source0-md5:	d28bd7e83d01b234144e336bbfde0caa
Source1:	%{name}.sysconfig
Source2:	%{name}-spamd.init
Patch0:		%{name}-bug-4619.patch
URL:		http://spamassassin.apache.org/
BuildRequires:	openssl-devel >= 0.9.6m
BuildRequires:	perl-devel >= 1:5.6.1
BuildRequires:	perl-Archive-Tar
BuildRequires:	perl-DB_File
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Mail-SPF-Query
BuildRequires:	perl-IP-Country
BuildRequires:	perl-Net-Ident
BuildRequires:	perl-IO-Socket-INET6 >= 2.51
BuildRequires:	perl-IO-Socket-SSL
BuildRequires:	perl-IO-Zlib
BuildRequires:	perl-DBI
BuildRequires:	perl-Digest-SHA1 >= 2.10
BuildRequires:	perl-HTML-Parser >= 3
#BuildRequires:	perl-Razor2
BuildRequires:	perl-libwww
%if %{with tests}
# are these really needed?
BuildRequires:	perl-MailTools
BuildRequires:	perl-MIME-Base64
BuildRequires:	perl-MIME-tools
%endif
BuildRequires:	rpm-perlprov >= 4.0.2-112.1
Requires:	perl-IO-Socket-INET6 >= 2.51
Requires:	perl-Mail-SpamAssassin = %{version}-%{release}
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

%description -l pl
SpamAssassin daje mo¿liwo¶æ zredukowania, je¶li nie kompletnego
wyeliminowania niezamawianej komercyjnej poczty (Unsolicited
Commercial Email, spamu) z poczty. Mo¿e byæ wywo³ywany z MDA, np.
Sendmaila czy Postfiksa, lub z pliku ~/.forward itp. U¿ywa ogólnego
algorytmu oceniania w celu identyfikacji wiadomo¶ci, które wygl±daj±
na SPAM, po czym dodaje nag³ówki do wiadomo¶ci, umo¿liwiaj±c
filtrowanie przez oprogramowanie u¿ytkownika. Ta dystrybucja zawiera
programy spamd/spamc, umo¿liwiaj±ce uruchomienie serwera, co znacznie
przyspieszy proces przetwarzania poczty.

%package tools
Summary:	Miscleanous tools for SpamAssassin
Summary(pl):	Przeró¿ne narzêdzia zwi±zane z SpamAssassin
Group:		Applications/Mail
Obsoletes:	SpamAssassin-tools

%description tools
Miscleanous tools from various authors, distributed with SpamAssassin.
See /usr/share/doc/spamassassin-tools-*/.

%description tools -l pl
Przeró¿ne narzêdzia, dystrybuowane razem ze SpamAssassinem. Wiêcej
informacji w /usr/share/doc/spamassassin-tools-*/.

%package spamd
Summary:	spamd - daemonized version of spamassassin
Summary(pl):	spamd - spamassassin w postaci demona
Group:		Applications/Mail
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	perl-Mail-SpamAssassin = %{version}-%{release}

%description spamd
The purpose of this program is to provide a daemonized version of the
spamassassin executable. The goal is improving throughput performance
for automated mail checking.

This is intended to be used alongside "spamc", a fast, low-overhead C
client program.

%description spamd -l pl
Spamd jest "demoniczn±" wersj± spamassassina. Jego zadaniem jest
poprawa wydajno¶ci automatycznego sprawdzania poczty.

Spamd powinien byæ u¿ywany wespó³ ze "spamc", który jest szybkim i
wydajnym programem klienckim.

%package spamc
Summary:	spamc - client for spamd
Summary(pl):	spamc - klient dla spamd
Group:		Applications/Mail

%description spamc
Spamc is the client half of the spamc/spamd pair. It should be used in
place of "spamassassin" in scripts to process mail. It will read the
mail from STDIN, and spool it to its connection to spamd, then read
the result back and print it to STDOUT. Spamc has extremely low
overhead in loading, so it should be much faster to load than the
whole spamassassin program.

%description spamc -l pl
Spamc powinien byæ u¿ywany zamiast "spamassassina" w skryptach
przetwarzaj±cych pocztê. Zczytuje pocztê ze STDIN, kolejkuje j± a
nastêpnie przekazuje spamdowi, odczytuje wynik i podaje go na STDOUT.
Spamc stara siê nie obci±¿aæ zbytnio procesora podczas ³adowania,
dziêki czemu powinien dzia³aæ szybciej ni¿ sam spamassassin.

%package -n perl-Mail-SpamAssassin
Summary:	Mail::SpamAssassin - SpamAssassin e-mail filter libraries
Summary(pl):	Mail::SpamAssassin - biblioteki filtra poczty SpamAssassin
Group:		Development/Languages/Perl
Requires:	perl-HTML-Parser >= 3
Requires:	perl-Cache-DB_File >= 0.2
Requires:	perl-Sys-Hostname-Long
Requires:	perl-Mail-SPF-Query
Conflicts:	perl-Net-DNS < 0.50
Conflicts:	perl-IO-Socket-INET6 < 2.51

%description -n perl-Mail-SpamAssassin
Mail::SpamAssassin is a Mail::Audit plugin to identify spam using text
analysis and several internet-based realtime blacklists. Using its
rule base, it uses a wide range of heuristic tests on mail headers and
body text to identify ``spam'', also known as unsolicited commercial
email. Once identified, the mail can then be optionally tagged as spam
for later filtering using the user's own mail user-agent application.

%description -n perl-Mail-SpamAssassin -l pl
Mail::SpamAssassin jest pluginem dla Mail::Audit, s³u¿±cym do
identyfikacji spamu przy u¿yciu analizy zawarto¶ci i/lub internetowych
czarnych list. Do zidentyfikowania jako ,,spam'' stosuje szeroki
zakres testów heurystycznych na nag³ówkach i tre¶ci, posi³kuj±c siê
stworzon± wcze¶niej baz± regu³. Po zidentyfikowaniu, poczta mo¿e byæ
oznaczona jako spam w celu pó¼niejszego wyfiltrowania, np. przy u¿yciu
aplikacji do czytania poczty.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p0

%build
%{__perl} Makefile.PL \
	PREFIX=%{_prefix} \
	SYSCONFDIR=%{_sysconfdir} \
	ENABLE_SSL=yes \
	CONTACT_ADDRESS="postmaster@localhost" \
	PERL_BIN=%{__perl} < /dev/null
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_sysconfdir}/mail/spamassassin}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	SYSCONFDIR=$RPM_BUILD_ROOT%{_sysconfdir} \
	INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/spamassassin

# shouldn't this script be called `spamd' instead?
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/spamassassin

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
%doc procmailrc.example
%attr(755,root,root) %{_bindir}/sa-learn
%attr(755,root,root) %{_bindir}/sa-update
%attr(755,root,root) %{_bindir}/spamassassin
%{_mandir}/man1/sa-learn*
%{_mandir}/man1/sa-update*
%{_mandir}/man1/spamassassin*

%files tools
%defattr(644,root,root,755)
%doc sql ldap tools masses contrib

%files spamd
%defattr(644,root,root,755)
%doc spamd/README*
%attr(754,root,root) /etc/rc.d/init.d/spamassassin
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/spamassassin
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
%{perl_sitelib}/Mail/*
%{_mandir}/man3/*
