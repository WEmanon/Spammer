import smtplib
import pandas as pd

class Spammer:
    def __init__(self, email_sender, sender_password, receivers):
        self.email_sender = email_sender
        self.sender_password = sender_password
        self.receivers = receivers

        self.smtp_server = smtplib.SMTP('smtp.gmail.com', 587)

    def run(self, message):
        self.smtp_server.starttls()
        self.smtp_server.login(self.email_sender, self.sender_password)
        self.smtp_server.sendmail(self.email_sender, self.receivers, message.as_string())

    