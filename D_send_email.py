import yagmail
import cred
from C_DA import name_export_xl

def main_send_email():
    ''' Function to send email with attachement'''
    try:
        yag = yagmail.SMTP('testthatcode2023@gmail.com', cred.password)

        recipient = 'testthatcode2023@gmail.com'
        subject = 'List of live Goods tender'

        html_content = '''
        <html>
            <body>
                <p>HI,</p>
                <p>Please find attached the list of <b>Goods tender</b> which are <b>Live</b> today for your reference. The data is scrapped, cleaned and emailed using Python. The data source is www.egp.gov.bt.</p>
            </body>
        </html>
        '''
        attachment = name_export_xl()
        yag.send(to=recipient, subject=subject, contents=html_content, attachments=attachment)
    except:
        print('Sending email failed!!!')