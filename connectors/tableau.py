from connectors.config import *
import requests as req
import os
import glob
from PyPDF2 import PdfFileWriter, PdfFileReader
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(filename):
    fromaddr = "custom.pdf.export@gmail.com"
    toaddr = get_recipe_config().get('email', None)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = filename
    body = "You export from Dataiku DSS"
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "CornielusFudge")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def merger(output_path, input_paths):
    pdf_writer = PdfFileWriter()

    for path in input_paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)

class Tableau:

    def __init__(self, server_type):

        self.api_url = '{}/api/{}/'.format(API[server_type]['url'], API[server_type]['version'])
        self.api_credentials = TABLEAU_SERVER_CREDENTIALS[server_type]
        self.site = API[server_type]['site']
        self.server_type = server_type

    def connect(self):
            data = dict()
            self.auth_url = '{}/auth/signin'.format(self.api_url)

            payload = {
                "credentials": {
                    "name": self.api_credentials['username'],
                    "password": self.api_credentials['password'],
                    "site": {
                        "contentUrl": self.site
                    }
                }
            }

            headers = {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            }

            r = req.post(self.auth_url, json=payload, headers=headers)

            try:
                if 'error' in [*r.json()]:
                    print(r.json()['error'])
                else:
                    data = r.json()

            except Exception as e:
                print('Error when connecting to Tableau: {}\n{}'.format(e, r.text))

            return data


    def get_views(self):
        views = list()

        url = '{}sites/{}/views/'.format(self.api_url, self.connect()['credentials']['site']['id'])

        params = dict()
        headers = {
            'X-tableau-auth': self.connect()['credentials']['token'],
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        r = req.get(url,headers=headers, params=params,allow_redirects=True)

        try:
            views = r.json()["views"]['view']

        except Exception as e:
            print('Error when connecting to Tableau {}: {}\n{}'.format(self.server_type,e, r.text))

        return views


    def exportPDF(self, view_name, filter_name, values, email):

        view_id = list(filter(lambda view: view["name"] == view_name, self.get_views()))[0].get('id', ' ')

        url = '{}sites/{}/views/{}/pdf'.format(self.api_url,self.connect()['credentials']['site']['id'],view_id)

        headers = {
            'X-tableau-auth': self.connect()['credentials']['token'],
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        params = dict()
        filter_key = 'vf_{}'.format(filter_name)
        for value in values:
            params[filter_key] = value
            r = req.get(url,headers=headers, params=params,allow_redirects=True)
            filename = '{}_{}'.format(view_name, str(value))
            with open('{}.pdf'.format(filename), 'wb') as f:
                f.write(r.content)

        paths = glob.glob('*{}*.pdf'.format(view_name))
        paths.sort()
        merger('[PDF_merged] {}.pdf'.format(view_name), paths)

        send_email(glob.glob('*[PDF_merged]*{}*.pdf'.format(view_name))[0], email)

        for file in paths:
            os.remove(file)

        return paths
