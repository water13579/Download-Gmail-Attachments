#!/usr/bin/env python
#
# Very basic example of using Python 3 and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# This script is example code from this blog post:
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
# This is an updated version of the original -- modified to work with Python 3.4.
#
import os
import sys
import re
import imaplib
import getpass
import email
import email.header
import datetime
import pprint
from email.header import decode_header
import base64


os.system('chcp 65001')

EMAIL_ACCOUNT = input('Username: ')

# Use 'INBOX' to read inbox.  Note that whatever folder is specified, 
# after successfully running this script all emails in that folder 
# will be marked as read.
EMAIL_FOLDER = "INBOX"
print('29')

def get_attachments(msg):
    for part in msg.walk():

        ##if part.get_content_maintype() == 'multipart':
        ##    continue

        if part.get('Content-Disposition') is None:
            continue

        fileName = msg['From']
        print('fileName = ', fileName)
        filename = decode_header(part.get_filename())
        print('filename = ', filename)
        try:
            filename = str(*filename[0])
        except:
            filename = filename[0][0]
        print(filename)
            # if decode_header(filename)[0][1] is not None:
            # 	filename = decode_header(filename)[0][0].decode(decode_header(filename)[0][1])
        # print('filename = ', fileName)
        if filename:
            dirname = re.findall(r'<(.*?)@', msg['From'], flags=0)[0]            
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            print('file name = ', repr(fileName))
            filePath = os.path.join(dirname, filename)
            with open(filePath, 'wb') as f:
                payload = part.get_payload(decode=True)
                    # pprint.pprint(part.get_content_type())
                f.write(payload)


def process_mailbox(M):
    """
   Do something with emails messages in the folder.
   For the sake of this example, print some headers.
   """

    rv, data = M.search(None, "FLAGGED")
    if rv != 'OK':
        print("No messages found!")
        return
    print(data)
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])

        get_attachments(msg)


M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    print('92')
    passwd = getpass.getpass()
    rv, data = M.login(EMAIL_ACCOUNT, passwd)
except imaplib.IMAP4.error:
    print("LOGIN FAILED!!! ")
    sys.exit(1)

print(rv, data)

rv, mailboxes = M.list()
if rv == 'OK':
    print("Mailboxes:")
    print(mailboxes)

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print("Processing mailbox...\n")
    process_mailbox(M)
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

M.logout()
