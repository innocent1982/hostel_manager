from datetime import datetime 
from dateutil.relativedelta import relativedelta

now = datetime.now()
month = now + relativedelta(months=5)
print(month)
