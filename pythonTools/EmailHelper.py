import smtplib


class EmailHelper: 

    helper_email_address = "mwspencerpythonhelper@gmail.com"
    helper_password = "gteltlobsiapehdu"


    def __init__(self, subject, message, reciever):
        self.subject = subject
        self.message = message
        self.reciever = reciever

    def send_message(self):
        
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            #encrypt traffic
            smtp.starttls()
            smtp.ehlo()

            smtp.login(self.helper_email_address, self.helper_password) 

            msg = f'Subject: {self.subject} \n\n{self.message}'

            smtp.sendmail(self.helper_email_address, self.reciever, msg) 



         

 