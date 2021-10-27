# in this project we will be scrapping data from a website using beautifulSoap and then create and email and sent the informationn out . this can be like finding some news that you want to receive from a website but you
# you dont want the whole page or the template newsletter email they currently have.

from bs4 import BeautifulSoup
# library for sending email
import smtplib
# library for making HTTP requests
import requests
# library for working with date and time
import datetime
# library for email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from requests.api import head

# create a variable for email content
email_content = ''


def extract_data_from_website(url):
    print("Extracting Hacker News Stories .... ")
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'}
    cnt = ''
    cnt += ('<b>HN Top Stories:</b>\n'+'<b>'+'-'*50+'<br>')
    pageContent = ''
    response = requests.get(url, headers=headers)
    pageContent = response.content
    soup = BeautifulSoup(pageContent, 'html.parser')
    for i, tag in enumerate(soup.findall('td', attrs={'class': 'title', 'valign': ''})):
        cnt += ((str(i+1)+' :: '+tag.text+"\n"+'<br>')
                if tag.text != 'More' else '')
    return cnt


cnt = ''
now = datetime.datetime.now()
#cnt = extract_data_from_website('https://news.ycombinator.com')
email_content += cnt
email_content += ('<br>--------------</br>')
email_content += ('<br><br> End of Message')
print(email_content)

# sending email
print("Composing Emai...")
SERVER = 'smtp.gmail.com'
PORT = 465  # 587
FROM = ''  # from email address
TO = ''  # to email address
PASS = ''
msg = MIMEMultipart()
msg['Subject'] = f"Top News From Hacker News [Automated Email] {now.day}/{now.month}/{now.year}"
msg['From'] = FROM
msg['To'] = TO
msg.attach(MIMEText(email_content, 'html'))
print("Initializing Server...")
server = smtplib.SMTP_SSL(SERVER, PORT)
server.set_debuglevel(1)
try:

    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string)
    print("email sent...")
    server.quit()
except:
    print("somthing went wrong...")
    server.quit()
