# Script to validate PZSS license status
# Check is done in 5 min intervals
# When License will be avaiable there will be email notification

import time
from datetime import datetime
import yagmail
import requests
import pandas as pd
from bs4 import BeautifulSoup

# User input to pass credentials and logins

login = input("Please enter login to PZSS portal: ")
password = input("Please enter password to PZSS portal: ")
email = input("Please enter your email adress: ")
email_pass = input("Please enter your email password: ")
website = 'https://portal.pzss.org.pl'
website_2 = "https://portal.pzss.org.pl/Player/Applications"


# Static variables to be used within functions
initial_subject = "Initial PZSS license status"
update_subject = "New PZSS license status"

# Function to retrieve license status from website


def license_status():
    s = requests.session()

    r = s.post(url=website, json={"Login": login, "Password": password})

    r2 = s.get(url=website_2)

    p1 = BeautifulSoup(r2.text, 'lxml').prettify()
    p2 = pd.read_html(p1, header=0, index_col=None)[0]
    return p2.iat[0, 3]


# Function to send email with any update to the license status
def send_email(contents, email_subject):
    yag = yagmail.SMTP(email, email_pass)
    yag.send(
        to=email,
        subject=email_subject,
        contents=contents,
    )


# Creating session on PZSS website and checking initial status of the license
# send the email with current status of the license
# Print initial license status in console with timestamp

result_initial = license_status()
result = result_initial
mail_subject = initial_subject
content = str(datetime.now())+": "+result
send_email(content, mail_subject)
print(str(datetime.now())+" Initial PZSS license status: "+result)


# continuously loop with request to the portal in search for a change of license status in 5 min intervals

while result_initial == result:
    result = license_status()

# Penultimate status is "Zatwierdzony przez WZSS  oczekiwanie na decyzję PZSS"
# when reaching penultimate status
# send email update,print status into console, exit loop and enter final loop in search of final status change
    if result == "Zatwierdzony przez WZSS  oczekiwanie na decyzję PZSS":
        content = str(datetime.now()) + ": " + result
        mail_subject = update_subject
        send_email(content, mail_subject)
        print(str(datetime.now()) + " Current license status: " + result)
        time.sleep(300)
        result_initial = result
        break

# should there be a change with the status, send the email with new status and search for further status change
    if result_initial != result:
        result_initial = result
        content = str(datetime.now()) + ": " + result
        mail_subject = update_subject
        send_email(content, mail_subject)
        print(str(datetime.now()) + " Current license status: " + result)
        time.sleep(300)
        continue


# Final loop to break when final status change will happen
while result_initial == result:
    result = license_status()
    if result != "Zatwierdzony przez WZSS  oczekiwanie na decyzję PZSS":
        break
    print(str(datetime.now())+" Current license status: "+result)
    time.sleep(300)

# After final status change on website code to send final email update and exit
content = str(datetime.now())+": "+result
mail_subject = update_subject
send_email(content, mail_subject)
print(str(datetime.now()) + " Current license status: " + result)
