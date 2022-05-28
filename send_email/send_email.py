from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email(temporary_directory, to_addr):
    gmail = "cmapbuildcompletion@gmail.com"
    gmail_pw = "fy6472395**jsf2"
    to = [to_addr]

    message = MIMEMultipart()

    message.attach(MIMEText("Contents of the email", "plain"))
    all_files = os.listdir(f"{temporary_directory}")

    for file in all_files:
        attach_file_name = f"{temporary_directory}/{file}"
        attach_file = open(attach_file_name, "rb")
        payload = MIMEBase("application", "octate-stream")
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)
        payload.add_header("Content-Disposition", "attachment", filename=file)
        message.attach(payload)
        attach_file.close()

    text = message.as_string()

    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=gmail, password=gmail_pw)
        # msg = f"Subject:File Sending Test\n\nContent"
        connection.sendmail(gmail, to, text)
        print("Email Has Been Sent.")
        connection.quit()