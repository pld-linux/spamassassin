#!/bin/sh

umask 022
OPT=""

# sa-update must create keyring
if [ ! -d /etc/mail/spamassassin/sa-update-keys ]; then
	sa-update
fi

# Initialize Channels and Keys
CHANNELLIST=""
KEYLIST=""
# Process each channel defined in /etc/mail/spamassassin/channel.d/
for file in /etc/mail/spamassassin/channel.d/*.conf; do
    [ ! -f "$file" ] && continue
    # Validate config file
    PREFIXES="CHANNELURL KEYID BEGIN"
    for prefix in $PREFIXES; do
        if ! grep -q "$prefix" $file; then
            echo "ERROR: $file missing $prefix"
            exit 255
        fi
    done
    . "$file"
    #echo "CHANNELURL=$CHANNELURL"
    #echo "KEYID=$KEYID"
    CHANNELLIST="$CHANNELLIST $CHANNELURL"
    KEYLIST="$KEYLIST $KEYID"
    sa-update --import "$file"
done

[ -f /etc/mail/spamassassin/channels ] && OPT="$OPT --channelfile /etc/mail/spamassassin/channels"

# Run sa-update on each channel, restart spam daemon if success
for channel in $CHANNELLIST; do
    OPT="$OPT --channel $channel"
done
for keyid in $KEYLIST; do
    OPT="$OPT --gpgkey $keyid"
done

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
