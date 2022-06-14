import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os


def send_mail(params, email, password):

    print(params['name'])
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Alert! Device changed for {params['rollno']}"
    msg['From'] = email
    msg['To'] = email

    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html lang="en">
      <body>
        <p>Dear Admin<p>
        </br>
        <p>The following student """ + params['name'] + ", roll number: " + params['rollno'] + """ has registered using a different device, please verify.</p>
        <p>The old device ID is """ + params['old_device'] + ", new device ID: " + params['new_device'] + """ </p>

        <p>Thanks and Regards,</p>
        <p>Attendance Admin</p>
        <p>IIIT Vadodara</p>
        </br>

      </body>
    </html>

    """

    # Record the MIME types of both parts - text/plain and text/html.
    part = MIMEText(html, 'html')

    msg.attach(part)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(email, password)
    mail.sendmail(email, email, msg.as_string())
    mail.quit()
