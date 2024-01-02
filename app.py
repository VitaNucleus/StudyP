from flask import Flask, request, render_template
import json
import os


app = Flask(__name__)


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
            except:
                records_dict = {}
                records_dict['1'] = {'e-mail': e_mail,
                                     'text': text}

                json_write = open('cache/main.json', 'w')
                json.dump(records_dict, json_write, indent=4)

    return render_template('main.html')


if __name__ == '__main__':
    app.run()