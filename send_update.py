import pathlib
import json
import requests
import bs4
import html5lib
import smtplib
import sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

contentWrapper = '''<div style="background-color:transparent;"><div class="block-grid mixed-two-up no-stack" style="Margin: 0 auto; min-width: 320px; max-width:
800px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #ffffff;"> <div style="width:100% !important;"><div style="
border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px;
padding-bottom:5px; padding-right: 15px; padding-left: 10px;"><div style="color:#6c6c6c;font-family:Ubuntu, Tahoma, Verdana, Segoe, sans-serif;line-height:1.5;
padding-top:0px;padding-right:10px;padding-bottom:5px;padding-left:10px;"><div style="line-height: 1.5; font-size: 12px; color: #6c6c6c; font-family: Ubuntu, 
Tahoma, Verdana, Segoe, sans-serif; mso-line-height-alt: 18px;">CONTENT_TOKEN</div></div></div></div></div></div>'''

splitLine = '''<div style="background-color:transparent;"><div class="block-grid" style="Margin: 0 auto; min-width: 320px; max-width: 800px; overflow-wrap: 
break-word; word-wrap: break-word; word-break: break-word; background-color: #ffffff;"><div style="border-collapse: collapse;display: table;width: 100%;
background-color:#ffffff;"><div class="col num12" style="min-width: 320px; max-width: 800px; display: table-cell; vertical-align: top; width: 600px;">
<div style="width:100% !important;"><div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; 
border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;"><table border="0" cellpadding="0" cellspacing="0"
class="divider" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; 
mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;" valign="top" width="100%"><tbody><tr style="vertical-align: top;"
valign="top"><td class="divider_inner" style="word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 
100%; padding-top: 5px; padding-right: 15px; padding-bottom: 5px; padding-left: 15px;" valign="top"><table align="center" border="0" cellpadding="0" cellspacing="0"
class="divider_content" role="presentation" style="table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt;
mso-table-rspace: 0pt; border-top: 1px solid #1BE4FF; width: 100%;" valign="top" width="100%"><tbody><tr style="vertical-align: top;" valign="top"><td style="
word-break: break-word; vertical-align: top; -ms-text-size-adjus t: 100%; -webkit-text-size-adjust: 100%;" valign="top"><span></span></td></tr></tbody></table>
</td></tr><tbody></table></div></div></div></div></div></div>'''

def fetchIACR(templatePage, keywords):
    payload = {'last' : 7, 'title' : 1}
    linkElems = bs4.BeautifulSoup(requests.get('https://eprint.iacr.org/eprint-bin/search.pl', params = payload).text, 'html5lib').select('dt')

    for item in linkElems:
        rDetail = requests.get("https://eprint.iacr.org" + item.select('a:first-child')[0]['href'])
        rDetailTextBody = bs4.BeautifulSoup(rDetail.text, 'html5lib').body

        if any(keyword in rDetailTextBody.text.lower() for keyword in keywords):
            [s.extract() for s in rDetailTextBody('script')]
            itemDetail = ''.join([str(child).replace('href="/', 'href="https://eprint.iacr.org/') for child in rDetailTextBody.contents[:-5]])
            templatePage = templatePage.replace('<!--TOKEN-END-->', splitLine + contentWrapper.replace('CONTENT_TOKEN', itemDetail) + '<!--TOKEN-END-->')
    
    templatePage = templatePage.replace('<!--KEYWORDS-TOKEN-->', ", ".join(keywords))
    return templatePage

def sendMail(receiver, username, password):
    page = open(root / 'target.html', 'r', encoding='utf-8')

    msg = MIMEMultipart()
    mail_body = MIMEText(page.read(), _subtype='html', _charset='utf-8')
    msg['Subject'] = Header("IACR EPRINT UPDATE", 'utf-8')
    msg['From'] = username
    toclause = receiver.split(',')
    msg['To'] = ",".join(toclause)
    msg.attach(mail_body)

    try:
        smtp = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
        smtp.ehlo()  
        smtp.login(username, password)
        smtp.sendmail(username, toclause, msg.as_string())
    except:
        print("Fail to send email to " + receiver)
    else:
        print("Send email successfully")
    finally:
        smtp.quit()
        page.close()

def main():
    root = pathlib.Path(__file__).parent.resolve()

    with open(root / "users.json",'r') as userJson:
        userInfo = json.load(userJson)

    for user in userInfo:
        print(user)
        templateHTML = open(root / "template.html", "r", encoding='utf-8')
        template = templateHTML.read()

        template = fetchIACR(template, user["keywords"])

        target = open(root / "target.html",'w', encoding='utf-8')
        target.write(template)
        templateHTML.close()
        target.close()

        sendMail(user["receiver"], sys.argv[1], sys.argv[2])
        
if __name__ == "__main__":
    main()
