from ..src.lambda_fn import lambda_handler, get_gmail, get_inbox_gen, get_spam,extract_msg_contents
import os
import unittest

class lambdaTestCase(unittest.TestCase):
    def setUp(self):
      os.environ['IS_TEST'] = 'true'
      mail = get_gmail()
      self.inbox_gen = get_inbox_gen(mail, verbose=True)
      # self.spam = get_spam(mail)
      self.mail = mail
      print(self.mail)

    def test_extract_msg_contents_inbox(self):
      """
      Test extracting the message contents of inbox
      """
      # batches = [x for x in self.inbox_gen ]
      for b in self.inbox_gen:
        messages = extract_msg_contents(b, 'inbox')
      self.assertEqual(len(messages), 10)

    def test_lambda_handler(self):
      for k, v in sorted(os.environ.items()):
        print(k+':', v)
      event = {
        "env" : "TEST"
      }
      lambda_handler(event, None)

# def main():
#   print("test_lambda_handler")
#   test_lambda_handler()


if __name__ == "__main__":
  unittest.main()
