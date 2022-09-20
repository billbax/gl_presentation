import os
import tempfile
from zipfile import ZipFile
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_email(temporary_directory, to_addr, client):
    # Create a zip file containing all the files created
    zip_file = save_files_to_zip(temporary_directory=temporary_directory)

    to = ["bill.baxter@cmap-software.com", to_addr]

    # Create a message template for the email
    message = MIMEMultipart()
    message["Subject"] = f"Import sheets for {client}"
    message.attach(MIMEText("Attached zip file contains all data ready for import\n\nBill", "plain"))
    # Attach zip_file to the email
    with open(zip_file, "rb") as file:
        message.attach(MIMEApplication(file.read(), Name="Files.zip"))
        file.close()

    # Login and send email
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=os.environ["GMAIL"], password=os.environ["GMAIL_PW"])
        # msg = f"Subject:File Sending Test\n\nContent"
        connection.sendmail(os.environ["GMAIL"], to, message.as_string())
        print("Email Has Been Sent.")
        connection.quit()


def save_files_to_zip(temporary_directory):
    all_files = os.listdir(temporary_directory)

    zip_temp_dir = tempfile.TemporaryDirectory()
    zip_temp_dir_name = zip_temp_dir.name

    zip_obj = ZipFile(f"{zip_temp_dir_name}/Files.zip", "w")
    for file in all_files:
        zip_obj.write(filename=f"{temporary_directory}/{file}", arcname=file)

    return f"{zip_temp_dir_name}/Files.zip"
