import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jobs import job_loop, date_today, timedelta

load_dotenv()
def send_email(subject, to_email):
    job_df = job_loop()
    # Set up the sender's email and password
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    # Set up the email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Attach the email body
    # message.attach(MIMEText(body, "plain"))
    # Create the plain-text and HTML version of your message
    html = f"""\
    <html>
      <body>
        <p>Hi Dave,<br>
           Hier sind die neusten Jobangebote für heute den {date_today} von der<br>
           <a href="https://www.arbeitsagentur.de/jobsuche/">Jobbörse</a> 
           bei der Agentur für Arbeit.
           Eine Datei mit den Stellenanzeigen findest du auch in {os.getcwd()}/01_data
           {job_df.to_html()}
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)

    # Set up the SMTP server
    smtp_server = "smtp.web.de"
    smtp_port = 587

    # Start the SMTP server connection
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Upgrade the connection to a secure TLS connection
        server.login(sender_email, sender_password)  # Log in to the email account
        server.sendmail(sender_email, to_email, message.as_string())  # Send the email

    print(f"Email sent successfully to {to_email}")

if __name__ == "__main__":
    subject = f"Neue Stellenanzeigen von der Jobbörse für den {date_today - timedelta(1)}"
    recipient_email = "dave.williams@web.de"

    send_email(subject, recipient_email)
