# for AWS
import boto3
# for dealing w/email
import imaplib2 #imaplib - use imaplib2 because imaplib gave an error when trying to retrieve all Inbox messages (too many emails)
# imaplib._MAXLINE = 400000

# for parsing the emails
import email
# from email import policy

from email.header import Header, decode_header, make_header
from email.policy import default
from email.message import EmailMessage

import uuid

# for dealing w/env variables
import os
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
EMAIL, PASSWORD = os.getenv('EMAIL'), os.getenv('GMAIL_APP_PASSWORD')
# Gmail IMAP url
IMAP_URL = 'imap.gmail.com'

# initialize dynamodb object
dynamodb = boto3.resource('dynamodb', 'us-east-1')


def get_gmail(verbose=False):
  # Log into Gmail inbox
  mail = imaplib2.IMAP4_SSL(IMAP_URL)
  mail.login(EMAIL, PASSWORD)
  _, mailboxes = mail.list()
  # print the mailbox names
  if verbose:
    for i in mailboxes:
      l = i.decode().split(' "/" ')
      print(l[0] + " = " + l[1])

  return mail

def get_inbox(mail, verbose=False):
  # select the Spam mailbox
  mail.select('Inbox')
  _, inbox_msgnums  = mail.search(None, 'ALL')
  
  inbox_emails = []

  i=0 # fr testing only
  for num in inbox_msgnums[0].split() : 
    _, data = mail.fetch(num, '(RFC822)')
    if verbose : 
      if verbose: print(num)
      print('Message %s\n%s\n' % (num, data[0][1]))

    inbox_emails.append(data)
    i += 1
    if i >=10 : 
      break

  return inbox_emails

  

def get_spam(mail, verbose=False):
  # select the Spam mailbox
  mail.select('[Gmail]/Spam')
  _, spam_msgnums  = mail.search(None, 'ALL')
  
  spam_emails = []

  i=0 # fr testing only
  for num in spam_msgnums[0].split() : 
    if verbose: print(num)
    # for num in data[0].split():
    _, data = mail.fetch(num, '(RFC822)')
    if verbose : print('Message %s\n%s\n' % (num, data[0][1]))

    spam_emails.append(data)
    i += 1
    if i >=10 : 
      break

  return spam_emails

def extract_msg_contents(messages, verbose=False):
  """
  Extract only the text content of the message.
  
  Pass in the list of spam emails or inbox emails.
  """
  msg_objs = []
  print("MESSAGES:", len(messages))
  for msg in messages[::-1]:  
    for response_part in msg : 
      if type(response_part) is tuple : 
        # continue
        my_msg = email.message_from_bytes((response_part[1]), policy=default)

        print('=====================')
        # subj = make_header(decode_header(my_msg['subject']))
        # sender = make_header(decode_header(my_msg['Sender']))
        # print(f"subj : {subj}")
        # print(f"from : {sender}")
        if verbose: 
          print(f"subj : {my_msg['subject']}, {type(my_msg['subject'])}")
          print(f"from : {my_msg['from']}, {type(my_msg['Sender'])}")
          print("body : ")
        body = ""
        for part in my_msg.walk():
          #print(part.get_content_type())
          if part.get_content_type() == 'text/plain' : 
            # print("payload")
            body = part.get_payload().strip()
            if verbose: print(body)
        
        sender_name, sender_email = my_msg['from'].split('<')
        sender_name = sender_name.strip()
        sender_email = sender_email.strip('>')

        msg_obj = {
          'body' : body,
          'subject' : my_msg['subject'],
          'sender' : sender_email,
          'sender_name' : sender_name
        }


        # formatted for dynamodb
        # ddb_msg_obj = {
        #   "M" : {k: {"S": v} for k, v in msg_obj.items()}
        # }
        msg_id = str(uuid.uuid4())

        ddb_msg_obj = {
         k: {"S": v} for k, v in msg_obj.items()
        }
        ddb_msg_obj['id'] = {'S':msg_id}
        print(ddb_msg_obj)
        msg_objs.append(msg_obj)

  return msg_objs


def insert_dynamodb(dynamodb, messages):
  table = dynamodb.Table(os.getenv('TABLE'))
  with table.batch_writer() as batch:
    for item in messages:
        batch.put_item(
            Item=item)



def lambda_handler(event, context):
  """
  Run our lambda code. This lambda will mainly be invoked manually, not via trigger. 
  Need to configure a test Event
  """
  mail = get_gmail()
  spam = get_spam(mail)
  inbox = get_inbox(mail, verbose=True)

  spam_messages = extract_msg_contents(spam)
  insert_dynamodb(dynamodb, spam_messages)

  inbox_messages = extract_msg_contents(spam)
  insert_dynamodb(dynamodb, inbox_messages)
  
  # message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])  
  # return( { 
  #     'message' : message
  # })



def main():
  # event = {
  #   'first_name' : "Test",
  #   'last_name' : "Event"
  # }
  lambda_handler(None, None)

if __name__ == '__main__':
  main()
