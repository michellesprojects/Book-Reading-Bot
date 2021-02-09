import smtplib
from email.mime.text import MIMEText

import schedule
import time 

#global variables

from_email = "throwaway-gmail-account-here@gmail.com"
email_password = "password-here" #password of throwaway account
to_email = "recipient-email-account-here@gmail.com"
email_subject = "Daily Reading!"

lines_per_email = 3 #amount of lines to include per email reading
bookmarked_line = 0 #last read line
book_complete = False #when this is True, terminate program
book = "testbook.txt"

#open the book and save the lines into an array
with open(book, "r") as file:
	book_lines = file.readlines()

#this function will return a string containing the lines for the
#user's next reading
def get_reading():

	global bookmarked_line, book_complete
	email_body = ""

	try: 

		for i in range(lines_per_email):

			line = book_lines[bookmarked_line] #next line

			#check first line of reading for a disjoint sentence
			if bookmarked_line != 0 and i == 0 and "." in line:
			#bookmarked_line != 0, if first line of text, dont worry about it being disjoint, it wont be
			#i == 0 and "." in line, if first line of this reading block, check if there is a period, if there is one assume it is a disjoint sentence and only take second half
				email_body += line.split(".")[1].strip()
				bookmarked_line+=1

			elif i == lines_per_email - 1: #last line

				if "." not in line:

					#keep going till we find a period, so we can end the reading gracefully
					while "." not in line:
						email_body += line
						bookmarked_line += 1
						line = book_lines[bookmarked_line]

					#when we have a line with a period, assume that is two sentences and don't read past first period
					email_body += line.split(".")[0] + "."
				else:
					email_body += line

			else:

				email_body += line
				bookmarked_line +=1 


	except IndexError as exception: #if we try to read an index that does not exist (past the last index), we are done with the book
		book_complete = True 
		return email_body 

	return email_body

#send ourselves the email 
def send_email():

	email = MIMEText(get_reading())
	email['From'] = from_email
	email['To'] = to_email
	email['Subject'] = email_subject

	session = smtplib.SMTP('smtp.gmail.com', 587)
	session.starttls()
	session.login(from_email, email_password)
	text = email.as_string()
	session.sendmail(from_email, to_email, text)
	session.quit()
	print("Mail sent")

	#if this was the last reading, terminate the program
	book_complete and exit()
	

#schedule the email to send automatically, everyday 6:26am 

schedule.every().day.at("06:26").do(send_email)

while True:
	schedule.run_pending()
	time.sleep(1)















