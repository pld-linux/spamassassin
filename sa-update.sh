#!/bin/sh

umask 022
OPT=""

[ -f /etc/mail/spamassassin/channels ] && OPT="$OPT --channelfile /etc/mail/spamassassin/channels"

# Only restart spamd if sa-update returns 0, meaning it updated the rules
/usr/bin/sa-update $OPT || exit $?

if [ -x /usr/bin/sa-compile ]; then
	out=$(/usr/bin/sa-compile 2>&1)
	rc=$?
	if [ $rc -gt 0 ]; then
		echo >&2 "$out"
		exit $rc
	fi
fi

if [ -x /etc/rc.d/init.d/spamd -a -e /var/lock/subsys/spamd ]; then
	/sbin/service spamd restart > /dev/null
fi
