#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pyotp
import json
import requests
import getopt


def usage():
    print 'check_guacamole_login.py -u <username> -p <password> -s <totp-secret> -U <url>'
    sys.exit(3)


def main(argv):

   # Commandline handling

    try:
        (opts, args) = getopt.getopt(argv, 'u:p:s:U:', ['username=',
                'password=', 'totpsecret=', 'url='])
    except getopt.GetoptError:
        usage()

    scounter = 0
    ucounter = 0
    pcounter = 0
    Ucounter = 0

    for (opt, arg) in opts:
        if opt == '-h':
            usage()
        elif opt in ('-u', '--username'):
            username = arg
            ucounter += 1
        elif opt in ('-p', '--password'):
            password = arg
            pcounter += 1
        elif opt in ('-U', '--url'):
            url = arg
            Ucounter += 1
        elif opt in ('-s', '--totpsecret'):
            secret = arg
            scounter += 1

    if scounter != 1 or pcounter != 1 or Ucounter != 1 or scounter != 1:
        usage()

    returnValue = 3
    totp = pyotp.TOTP(secret)
    pin = totp.now()

   # Login

    r = requests.post(url + '/api/tokens', data={'username': username,
                      'password': password, 'secret': pin})

    if r.status_code != 200:
        print 'Could not authenticate via ldap (%d,%s):' \
            % (r.status_code, r.reason)
        print r.text
        returnValue = 2
    else:
        print 'Successfully logged in.'
        returnValue = 0
        authToken = json.loads(r.text)['authToken']

      # Logout

        r = requests.delete(url + '/api/tokens/' + authToken)
        if r.status_code != 204:
            print 'Could not log out (%d,%s)' % (r.status_code,
                    r.reason)
            returnValue = 1

    sys.exit(returnValue)


if __name__ == '__main__':
    main(sys.argv[1:])

			