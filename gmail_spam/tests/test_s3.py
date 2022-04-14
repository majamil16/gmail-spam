
from ..src.s3 import S3Client
import os
import unittest
import tempfile

class S3TestCase(unittest.TestCase):
    def setUp(self):
        self.client = S3Client()
        self.client.get_bucket()

  
    def test_put_and_read(self):
      """
      Test writing to bucket
      """
      # create a temporary file and write some data to it
      with tempfile.TemporaryFile() as fp:
        fp.write(b'Hello world!')
        self.client.put(key='test/temp.txt', file=fp, filetype='obj')

    def test_del(self):
      """
      Test removing from bucket
      """
      pass
    

    # def test_read(self):
    #   """
    #   Test reading from a bucket
    #   """




    def test_list_objs(self):
      self.client.list_obj()
    #   for k, v in sorted(os.environ.items()):
    #     print(k+':', v)
    #   event = {
    #     "event" : "TEST"
    #   }
    #   os.environ['IS_TEST'] = 'true'
    #   lambda_handler(event, None)

def main():
  print("test_lambda_handler")
if __name__ == "__main__":
  unittest.main()


# if __name__ == "__main__":
#   main()