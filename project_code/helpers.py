import smtplib

def send_email(recipient_email, message):
    sender_email = 'ntwaribruce647@gmail.com'
    # App password 
    sender_password = 'dnxu aqek mess tcke'
    
    # Set up the SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)
    
    # The message
    subject = 'Property visit Appointment'
    body = f'Thank you for your interest in our services. To schedule a property with Id "{message}", Kindly reply to this email with the date and time you wish to visit.'
    message = f'Subject: {subject}\n\n{body}'

    # Send the message
    smtp_server.sendmail(sender_email, recipient_email, message)
    smtp_server.quit()