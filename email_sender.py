import smtplib

from email.mime.text import MIMEText

msg = MIMEText('Testing some Mailgun awesomness')
msg['Subject'] = "Hello"
msg['From']    = "julian@jarminowski.de"
msg['To']      = "julian.jarminowski@gmx.de"

s = smtplib.SMTP('smtp.mailgun.org', 587)

s.login('postmaster@mg.jarminowski.de', 'a5a384995426d2caae6aed77ce16b6ae')
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()
