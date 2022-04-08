from gmail_spam.utils.get_logger import get_logger
from gmail_spam.constants import LOG_DIR
# for AWS
import boto3
from botocore.exceptions import ClientError

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

# init logger
lgr = get_logger( LOG_DIR, 'gmail_spam.lambda') # logger name is  meaning root

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
  # select the Inbox mailbox
  mail.select('Inbox')
  _, inbox_msgnums  = mail.search(None, 'ALL')
  
  inbox_emails = []

  i=0 # fr testing only
  for num in inbox_msgnums[0].split() : 
    _, data = mail.fetch(num, '(RFC822)')
    print(f"{len(inbox_msgnums[0].split())} Inbox messages retrieved")
    if verbose : 
      lgr.info('Message %s\n%s\n' % (num, data[0][1]))

    inbox_emails.append(data)
    i += 1
    if i >=10 and os.getenv('IS_TEST').upper() =='TRUE': 
      break

  return inbox_emails

  

def get_spam(mail, verbose=False):
  # select the Spam mailbox
  mail.select('[Gmail]/Spam')
  _, spam_msgnums  = mail.search(None, 'ALL')
  
  spam_emails = []

  i=0 # fr testing only
  for num in spam_msgnums[0].split() : 
    # for num in data[0].split():
    _, data = mail.fetch(num, '(RFC822)')
    if verbose : 
      lgr.info('Message %s\n%s\n' % (num, data[0][1]))

    spam_emails.append(data)
    i += 1
    if i >=16 and os.getenv('IS_TEST').upper() =='TRUE': 
      break

  return spam_emails

def extract_msg_contents(messages, label, verbose=False,  format='batch'):
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
          'sender_name' : sender_name,
          'label' : label
        }

        msg_id = str(uuid.uuid4())
        if format == 'dynamo':
          ddb_msg_obj = {
           k: {"S": v} for k, v in msg_obj.items()
          }
          ddb_msg_obj['id'] = {'S':msg_id}
          print(ddb_msg_obj)
          msg_objs.append(ddb_msg_obj)
        elif format=='batch':
          msg_obj['id'] = msg_id
          print(msg_obj)
          msg_objs.append(msg_obj)

  return msg_objs


def insert_dynamodb(dynamodb, messages):
  try : 
    table = dynamodb.Table(os.getenv('TABLE'))
    with table.batch_writer() as batch:
      for item in messages:
          batch.put_item(
              Item=item)
    lgr.info("Loaded data into table %s.", table.name)
  except ClientError:
        lgr.exception("Couldn't load data into table %s.", table.name)
        raise


def lambda_handler(event, context):
  """
  Run our lambda code. This lambda will mainly be invoked manually, not via trigger. 
  Need to configure a test Event
  """
  print(f"In test: {os.getenv('IS_TEST').upper() =='TRUE'}" ) 
  mail = get_gmail()
  spam = get_spam(mail)
  inbox = get_inbox(mail)
  
  print("Getting spam")
  spam_messages = extract_msg_contents(spam, label='spam', verbose=True)
  print("Inserting spam")
  insert_dynamodb(dynamodb, spam_messages)
  print("Inserted spam")
  
  print("Getting inbox")
  inbox_messages = extract_msg_contents(inbox, label='inbox')
  print("Inserting inbox")
  insert_dynamodb(dynamodb, inbox_messages)
  print("Inserted inbox")

def main():
  # event = {
  #   'first_name' : "Test",
  #   'last_name' : "Event"
  # }
  lambda_handler(None, None)

if __name__ == '__main__':
  main()
