import threading

from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.message = message
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.message, bcc=self.recipient_list)
        msg.content_subtype = "html"
        msg.send()