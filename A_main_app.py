import time

time.sleep(1)
from B_scrapper import main_scrapper
main_scrapper()

time.sleep(1)
from C_DA import main_DA
main_DA()

time.sleep(1)
from D_send_email import main_send_email
main_send_email()