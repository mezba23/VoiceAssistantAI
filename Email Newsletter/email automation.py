import schedule
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import requests
from dotenv import load_dotenv
load_dotenv()


send_mail=str(input("enter sender email:"))
send_pass=str(input("enter sender password:"))
Email=str(input("enter subscriber email:"))
Content=str(input("enter content:"))
Time=str(input("enter content time:"))
Subject=str(input("enter subject:"))


AIRTABLE_BASE_ID=os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY=os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME=os.environ.get("AIRTABLE_TABLE_NAME")

endpoint=f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'


def add_to_airtable(Email=None, Subject="",Content="",Time=""):
    if Email is None:
        return
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
    "records": [
            {
            "fields": {
                "Email": Email,
				"Subject":Subject,
				"Content":Content,
				"Time":Time
                }
            }
        ]
    }
    r = requests.post(endpoint, json=data, headers=headers)
    return r.status_code == 200




# send our email message 'msg' to our boss
def message(subject=Subject,
			text="", img=None, attachment=None):
	
	# build message contents
	msg = MIMEMultipart()
	
	# Add Subject
	msg['Subject'] = subject
	
	# Add text contents
	msg.attach(MIMEText(text))

	# Check if we have anything
	# given in the img parameter
	if img is not None:

		# Check whether we have the
		# lists of images or not!
		if type(img) is not list:
			
			# if it isn't a list, make it one
			img = [img]

		# Now iterate through our list
		for one_img in img:
			
			# read the image binary data
			img_data = open(one_img, 'rb').read()
			
			# Attach the image data to MIMEMultipart
			# using MIMEImage,
			# we add the given filename use os.basename
			msg.attach(MIMEImage(img_data,
								name=os.path.basename(one_img)))

	# We do the same for attachments
	# as we did for images
	if attachment is not None:

		# Check whether we have the
		# lists of attachments or not!
		if type(attachment) is not list:
			
			# if it isn't a list, make it one
			attachment = [attachment]

		for one_attachment in attachment:

			with open(one_attachment, 'rb') as f:
				
				# Read in the attachment using MIMEApplication
				file = MIMEApplication(
					f.read(),
					name=os.path.basename(one_attachment)
				)
			file['Content-Disposition'] = f'attachment;\
			filename="{os.path.basename(one_attachment)}"'
			
			# At last, Add the attachment to our message object
			msg.attach(file)
	return msg


def mail():
	
	# initialize connection to our email server,
	# we will use gmail here
	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.ehlo()
	smtp.starttls()
	
	# Login with your email and password
	smtp.login(send_mail,send_pass)

	# Call the message function
	msg = message(Content)
	
	# Make a list of emails, where you wanna send mail
	to = [Email]

	# Provide some data to the sendmail function!
	smtp.sendmail(from_addr=send_mail,
				to_addrs=to, msg=msg.as_string())
	
	# Finally, don't forget to close the connection
	smtp.quit()

add_to_airtable(Email,Subject,Content,Time)


schedule.every(2).seconds.do(mail)
schedule.every(10).minutes.do(mail)
schedule.every().hour.do(mail)
schedule.every().day.at("10:30").do(mail)
schedule.every(5).to(10).minutes.do(mail)
schedule.every().monday.do(mail)
schedule.every().wednesday.at("13:15").do(mail)
schedule.every().minute.at(":17").do(mail)

while True:
	schedule.run_pending()
	time.sleep(1)
