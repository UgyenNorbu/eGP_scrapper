import yagmail

yag = yagmail.SMTP('testthatcode2023@gmail.com', 'Iamadeveloper@2023')
contents = ["This is the email body"]
yag.send('testthatcode2023@gmail.com', 'Test email', contents)

# TODO: wrap inside a main function