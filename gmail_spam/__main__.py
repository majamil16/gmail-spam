"""
To run as `python -m gmail_spam module_name`
"""
import sys
module_name = sys.argv[1] if len(sys.argv) >= 2 else ''
if module_name == 'lambda' : 
  from .src import lambda_fn
  lambda_fn.main()
elif module_name == 's3' : 
  from .src import s3
  s3.main()

