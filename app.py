from flask import Flask, request, render_template, redirect, url_for
from email.message import EmailMessage
import schedule
import smtplib
import json
import os
import time


app = Flask(__name__)


def send_mail():
    with open('cache/main.json', 'r') as file:
        json_dict = json.load(file)

        keys = list(json_dict.keys())
        host_email = 'AbiturientSynergy@yandex.ru'
        host_pass = 'qkomeaarhceuawun'
        server = smtplib.SMTP_SSL('smtp.yandex.com', 465)
        server.login(host_email, host_pass)
        for key in keys:
            dest_email = json_dict[key]['e-mail']
            subject = "Акты проверки нарушений качества теплоснабжения"

            msg = EmailMessage()
            msg["From"] = host_email  # Прозвище, учетная запись почтового ящика отправителя
            msg["To"] = dest_email  # Прозвище, учетная запись почтового ящика получателя
            msg["Subject"] = subject  # Тема письма
            msg['Text'] = json_dict[key]['text']

            server.send_message(msg)
        server.quit()
@app.route('/sended')
def every_day():
    schedule.every().minute.do(send_mail)
    while True:
        schedule.run_pending()
        time.sleep(1)

    return render_template('sended.html')

@app.route("/", methods=['GET', 'POST'])
def make_record_in_json():
    if not os.path.exists('cache'):
        os.mkdir('cache')
    if not os.path.exists('cache/main.json'):
        open('cache/main.json', 'w')
    if request.method == 'POST':
        e_mail = request.form.get("e-mail")
        text = request.form.get("text")

        with open('cache/main.json', 'r') as json_read:
            try:
                json_dict = json.load(json_read)
                last_key = list(json_dict.keys())[-1]

                if int(last_key) != 10:
                    last_key = int(last_key) + 1
                    json_dict[f'{last_key}'] = {'e-mail': e_mail,
                                                'text': text}

                    json_write = open('cache/main.json', 'w')
                    json.dump(json_dict, json_write, indent=4)

                    redirect(url_for('every_day'))
                else:
                    keys = list(json_dict.keys())

                    new_dict = {}
                    for key in keys:
                        if int(key) != 1:
                            new_dict[f'{int(key) - 1}'] = json_dict[key]
                    new_dict['10'] = {'e-mail': e_mail,
                                     'text': text}

                    json_write = open('cache/main.json', 'w')
                    json.dump(new_dict, json_write, indent=4)

                    redirect(url_for('every_day'))
            except:
                records_dict = {}
                records_dict['1'] = {'e-mail': e_mail,
                                     'text': text}

                json_write = open('cache/main.json', 'w')
                json.dump(records_dict, json_write, indent=4)

                redirect(url_for('every_day'))

    return render_template('main.html')


if __name__ == '__main__':
    app.run()
