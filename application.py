from flask import Flask, render_template, redirect, request, session

import requests

app = Flask(__name__)

# Credit to this person for inspiration https://stackoverflow.com/questions/14173421/use-string-translate-in-python-to-transliterate-cyrillic
def translit(text):

    if language="rus":

        symbols = str.maketrans(u"абвгдеёжзийклмнопрстуѹфцчшъыьѣэѳѵѡАБВГДЕЁЖЗИЙКЛМНОПРСТУѸФЦЧЪЫЬѢЭѲѴѠ",
                               u"abvgdeёžzijklmnoprstuufcčšʺyʹěėfiôABVGDEËŽZIJKLMNOPRSTUUFCČʺYʹĚĖFIÔ")
        sequence = {
            u'х':'ch',
            u'щ':'šč',
            u'ю':'ju',
            u'я':'ja',
            u'X':'Ch',
            u'Щ':'Šč',
            u'Ю':'Ju',
            u'Я':'Ja'
        }

        for char in sequence.keys():
            text = text.replace(char, sequence[char])




    return text.translate(symbols)


# Main (index) page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cyrillic = request.form.get("cyrillic")
        language = request.form.get("language")
        transliteration = translit(cyrillic)

        return render_template("index.html", transliteration=transliteration, cyrillic=cyrillic)

    else:
       return render_template("index.html")
