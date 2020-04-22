from .decode import Decode
import smtplib



class Email:

    def sendEmail(self):
        from . import views
        global email
        obj=Decode()
        pwd=obj.funcDecode(b'gAAAAABeoB9uq_d034uIFobubo5MPJnQBZy5AqznBIDRAPiWPlpILxnWbIJP8LPUEaVkeftDWwTEDqkTlUDTCaeIXMb8TlOKIQ==')
        sender = 'myemailservertest@gmail.com'
        message = """\
        Subject: Regestration Successful

        Your Account is successfully created.."""
        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com',587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.login(sender, pwd)
            smtpObj.sendmail(sender, views.email, message)
            print("Successfully sent email")
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print(e)