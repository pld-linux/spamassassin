%include	/usr/lib/rpm/macros.perl
%define	pdir	Mail
%define	pnam	SpamAssassin
Summary:	%{pdir}::%{pnam} -- SpamAssassin e-mail filter Perl modules.
Summary(pl):	%{pdir}::%{pnam} -- modu³y Perla filtru poczty SpamAssassin.
Name:		perl-%{pdir}-%{pnam}
Version:	2.31
Release:	2
License:	GPL/Artistic
Group:		Development/Languages/Perl
URL:		http://spamassassin.org/
Source0:	http://spamassassin.org/released/%{pdir}-%{pnam}-%{version}.tar.gz
Patch0:		findbin.patch
Patch1:		spamassassin-makefile.patch
Patch2:		spamassassin-rc-script.patch
BuildRequires:	perl >= 5.6
BuildRequires:	rpm-perlprov >= 3.0.3-16
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
#BuildArch:	noarch # perl-mail-spamassassin is noarch, but SpamAssassin is not...

%define		_noautoreq	'perl(Razor::Agent)' 'perl(Razor::Client)' 'perl(Net::SMTP::Server)' 'perl(Net::SMTP::Client)'

%description
Mail::SpamAssassin is a Mail::Audit plugin to identify spam using text
analysis and several internet-based realtime blacklists. Using its
rule base, it uses a wide range of heuristic tests on mail headers and
body text to identify ``spam'', also known as unsolicited commercial
email. Once identified, the mail can then be optionally tagged as spam
for later filtering using the user's own mail user-agent application.

%description -l pl
Mail::SpamAssassin jest pluginem dla Mail::Audit, s³u¿±cym do
identyfikacji spamu przy u¿yciu analizy zawarto¶ci i/lub internetowych
czarnych list. Do zidentyfikowania jako ,,spam'' stosuje szeroki
zakres testów heurystycznych na nag³ówkach i tre¶ci, posi³kuj±c siê
stworzon± wcze¶niej baz± regu³. Po zidentyfikowaniu, poczta mo¿e byæ
oznaczona jako spam w celu pó¼niejszego wyfiltrowania, np. przy u¿yciu
aplikacji do czytania poczty.

%package -n spamassassin
Summary:	A spam filter for email which can be invoked from mail delivery agents.
Summary(pl):	Filtr antyspamowy, przeznaczony dla programów dostarczaj±cych pocztê (MDA).
Group:		Applications/Mail
Obsoletes:	SpamAssassin
Prereq:		/sbin/chkconfig

%description -n spamassassin
SpamAssassin provides you with a way to reduce if not completely
eliminate Unsolicited Commercial Email (SPAM) from your incoming
email. It can be invoked by a MDA such as sendmail or postfix, or can
be called from a procmail script, .forward file, etc. It uses a
genetic-algorithm evolved scoring system to identify messages which
look spammy, then adds headers to the message so they can be filtered
by the user's mail reading software. This distribution includes the
spamd/spamc components which create a server that considerably speeds
processing of mail.

%description -n spamassassin -l pl
SpamAssassin udostêpnia Ci mo¿liwo¶æ zredukowania, je¶li nie
kompletnego wyeliminowania Niezamawianej Komercyjnej Poczty
(Unsolicited Commercial Email, spamu) z Twojej poczty. Mo¿e byæ
wywo³ywany z MDA, np. Sendmaila czy Postfixa, lub z pliku ~/.forward
itp. U¿ywa ogólnego algorytmu oceniania w celu identyfikacji
wiadomo¶ci, które wygl±daj± na SPAM, po czym dodaje nag³ówki do
wiadomo¶ci, umo¿liwiaj±c filtrowanie przez oprogramowanie u¿ytkownika.
Ta dystrybucja zawiera programy spamd/spamc, umo¿liwiaj±ce
uruchomienie serwera, co znacznie przyspieszy proces przetwarzania
poczty.

%package -n spamassassin-tools
Summary:	Miscleanous tools for SpamAssassin.
Summary(pl):	Przeró¿ne narzêdzia zwi±zane z SpamAssassin.
Group:		Applications/Mail
Obsoletes:	SpamAssassin-tools
#BuildArch:	noarch

%description -n spamassassin-tools
Miscleanous tools from various authors, distributed with SpamAssassin.
See /usr/share/doc/SpamAssassin-tools-*/.

%description -n spamassassin-tools -l pl
Przeró¿ne narzêdzia, dystrybuowane razem z SpamAssassin. Zobacz
/usr/share/doc/SpamAssassin-tools-*/.

%prep -q
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1
%patch1 -p0
%patch2 -p1

%build
%{__perl} Makefile.PL PREFIX=%{_prefix}
%{__make} OPTIMIZE="%{rpmcflags}" PREFIX=%{_prefix}
#%make test

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
# shouldn't this script be called `spamd' instead?
install -m 0755 spamd/pld-rc-script.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/spamassassin

install -d $RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin

rm -f spamd/{*.sh,*.conf,spam*} spamproxy/spamproxyd*

%post -n spamassassin
if [ $1 = 1 ]; then
	/sbin/chkconfig --add spamassassin
fi
if [ -f /var/lock/subsys/spamassassin ]; then
	/etc/rc.d/init.d/spamassassin restart 1>&2
else
	echo 'Run "/etc/rc.d/init.d/spamassassin start" to start the spamd daemon.'
fi

%preun -n spamassassin
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
%{perl_sitelib}/Mail/*
%{perl_sitelib}/auto/Mail/*

%doc
%{_mandir}/man3/*

%files -n spamassassin
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%config(noreplace) %attr(755,root,root) %{_sysconfdir}/rc.d/init.d/spamassassin
%config(noreplace) %{_sysconfdir}/mail/spamassassin
%config(noreplace) %{_datadir}/spamassassin

%doc Changes README TODO sample-nonspam.txt sample-spam.txt spamd spamproxy
%{_mandir}/man1/*

%files -n spamassassin-tools
%defattr(644,root,root,755)
%doc sql tools masses contrib
