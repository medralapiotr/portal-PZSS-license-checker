## Script to validate PZSS license status
## Check is done in 5 min intervals
## When License will be avaiable there will be email notification

import time
from datetime import datetime
import yagmail
import requests
import pandas as pd
from bs4 import BeautifulSoup

## User input to pass credentials and logins

login = input("Please enter login to PZSS portal")
password = input("Please enter password to PZSS portal")
email = input("Please enter your email adress")
emailpass = input("Please enter your email password")
strona = 'https://portal.pzss.org.pl'
strona_2 = "https://portal.pzss.org.pl/Player/Applications"

## Creating session on PZSS website and checking initial status of the license and send the email with current status of the license
s = requests.session()

r = s.post(url=strona, json={"Login": login, "Password": password})

r2 = s.get(url=strona_2)

p1 = BeautifulSoup(r2.text, 'lxml').prettify()
p2 = pd.read_html(p1, header=0, index_col=None)[0]
result_initial = p2.iat[0, 3]
result_initial = result

yag = yagmail.SMTP(email, emailpass)
yag.send(
    to=email,
    subject="Initial PZSS license status",
    contents=(str(datetime.now())+": "result,
)
print(str(datetime.now())+" Initial PZSS license status: "+result)


## continuously loop with request to the portal in search for a change of license status in 5 min intervals

while result_initial == result:
    s = requests.session()
    r = s.post(url=strona,json={"Login": login,"Password": password})
    r2 = s.get(url= strona_2)

    p1 = BeautifulSoup(r2.text, 'lxml').prettify()
    p2 = pd.read_html(p1, header = 0, index_col= None ) [0]
    result = p2.iat[0,3]

## Penultimate status is "Zatwierdzony przez WZSS  oczekiwanie na decyzję PZSS"
## when reaching penultimate status send email update, exit loop and enter final loop in search of final status change
    if result ="Zatwierdzony przez WZSS  oczekiwanie na decyzję PZSS":
        yag.send(
            to=email,
            subject="New PZSS license status,
        contents = (str(datetime.now()) + ": "result,
                    )
        print(str(datetime.now()) + " Current license status: " + result)
        time.sleep(300)
        result_initial = result
        break

## should there be a change with the status, send the email with new status and search for further status change
    if result_initial != result:
        result_initial = result
        yag.send(
            to=email,
            subject="New PZSS license status",
        contents = (str(datetime.now()) + ": "result,
                    )
        continue

    print(str(datetime.now())+" Current license status: "+result)
    time.sleep(300)

##Final loop to break when final status change will happen
while result_initial == result:
    r = s.post(url=strona,json={"Login": login,"Password": password})
    r2 = s.get(url= strona_2)

    p1 = BeautifulSoup(r2.text, 'lxml').prettify()
    p2 = pd.read_html(p1, header = 0, index_col= None ) [0]
    result = p2.iat[0,3]
    if result !="Zatwierdzony przez WZSS  oczekiwanie na decyzję PZSS":
        break
    print(str(datetime.now())+" Current license status: "+result)
    time.sleep(300)

#After final status change on website code to send final email update and exit

yag.send(
    to=email,
    subject="New PZSS license status",
    contents=(str(datetime.now()) + ": "result,
              )

print(str(datetime.now()) + " Current license status: " + result)