from selenium import webdriver

import csv
import os
from os import path
import pathlib

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

# Funtion to send mail
def send_mail(email_id,password):

    filename = 'csvfile.csv'
    filepath = './csvfile.csv'

    subject = "Google Summer of Code"
    body = "Dear Student, \n\nPlease find the infomation regarding Google Summer of Code in the csv file attached to the mail.\n\nRegards."
    
    msg = MIMEMultipart()
    body_part = MIMEText(body, 'plain')
    msg['Subject'] = subject
    msg['From'] = email_id
    msg['To'] = email_id
    
    msg.attach(body_part)
    
    with open(filepath,'rb') as fileobj:
        msg.attach(MIMEApplication(fileobj.read(), Name=filename))

    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.starttls()
    smtp_obj.login(email_id, password)
    smtp_obj.sendmail(email_id, email_id, msg.as_string())
    smtp_obj.quit()

website_list = []

# 52 North Gmbh
website1 = "https://summerofcode.withgoogle.com/archive/2020/organizations/6309633414660096/"
website_list.append(website1)

#AboutCode.org
website2 = "https://summerofcode.withgoogle.com/archive/2020/organizations/6689005560659968/"
website_list.append(website2)

#Academy Software Foundation (ASWF)
website3 = "https://summerofcode.withgoogle.com/archive/2020/organizations/6043464124334080/"
website_list.append(website3)

#Accord Project
website4 = "https://summerofcode.withgoogle.com/archive/2020/organizations/5947521500708864/"
website_list.append(website4)
  
all_language_list = []
Path = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(Path)
for website in website_list:  
    driver.get(website)

    web_language_ele = driver.find_elements_by_css_selector('li.organization__tag.organization__tag--technology')
    
    web_language_list = []
    for i in range(len(web_language_ele)):
        value = (web_language_ele[i].text)
        web_language_list.append(value)
    
    all_language_list.extend(web_language_list)
driver.quit()

print(set(all_language_list))  # To print unique languages only

email_id = input("Enter your email-id: ")
password = input("Enter password: ")

user_language_list = []
while(True):
    language = input("Enter What you know from the above tech stack: ")

    if language == "exit": break
    user_language_list.append(language)

Path = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(Path)

file = pathlib.Path("csvfile.csv") # To delete csv file if it already exists in the folder
if file.exists ():
    os.remove('csvfile.csv')
else:
    pass

for website in website_list:  # Check the 4 websites for languages
    driver.get(website)

    web_name = driver.title
    index = web_name.index("-")
    website_name = web_name[0:index-1]

    web_language_ele = driver.find_elements_by_css_selector('li.organization__tag.organization__tag--technology')
    
    web_language_list = []
    for i in range(len(web_language_ele)):
        value = (web_language_ele[i].text)
        web_language_list.append(value)

    check =  any(item in web_language_list for item in user_language_list) 

    if check == True:
        # Creating and appending data in csv file
        with open('csvfile.csv', mode='a+') as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            file_writer.writerow([website_name, website, web_language_list])

    else:
        pass

driver.quit()

#Call Funtion to send email
send_mail(email_id,password)
