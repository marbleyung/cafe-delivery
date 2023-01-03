from datetime import datetime, timedelta

now = datetime.now()
print(now)
x = now - timedelta(minutes=30)
data = datetime(2023, 1, 3, 13, 25, 10)
data1 = datetime(2023, 1, 3, 13, 55, 10)
print(data.timestamp() - data1.timestamp())
print(datetime.now().timestamp())