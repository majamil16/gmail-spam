from operator import imod


print("hi")

import sys
module_name = sys.argv[1] if len(sys.argv) >= 2 else ''
if module_name == 'lambda' : 

  from .src import lambda_fn
  lambda_fn.main()

  # print(f'Found student: {search_students(student_name)}')
