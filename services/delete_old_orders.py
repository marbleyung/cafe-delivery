from order_process import delete_old_orders
import time

while True:
    delete_old_orders()
    time.sleep(1800)