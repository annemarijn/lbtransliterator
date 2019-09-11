from flask import Flask, render_template, redirect, request, session

import requests

app = Flask(__name__)

# Credit to this person for inspiration https://stackoverflow.com/questions/14173421/use-string-translate-in-python-to-transliterate-cyrillic
# Transliteration function
def translit(text, lang):
    if lang == "rus":
        symbols = str.maketrans(u"абвгдеёжзийклмнопрстуѹфцчшъыьѣэѳѵѡАБВГДЕЁЖЗИЙКЛМНОПРСТУѸФЦЧШЪЫЬѢЭѲѴѠ«»",
                               u"abvgdeëžzijklmnoprstuufcčšʺyʹěėfiôABVGDEËŽZIJKLMNOPRSTUUFCČŠʺYʹĚĖFIÔ“”")
        sequence = {
            u'х':'ch',
            u'щ':'šč',
            u'ю':'ju',
            u'я':'ja',
            u'Х':'Ch',
            u'Щ':'Šč',
            u'Ю':'Ju',
            u'Я':'Ja'
        }

    if lang == "ukr":
        symbols = str.maketrans(u"абвгґдежзиійклмнопрстуфцчшь’ѳѵАБВГҐДЕЖЗИІЙКЛМНОПРСТУФЦЧШЬѲѴ«»",
                               u"abvhgdežzyijklmnoprstufcčšʹʼfiABVHGDEŽZYIJKLMNOPRSTUFCČŠʹFI“”")
        sequence = {
            u'є':'je',
            u'ї':'ji',
            u'х':'ch',
            u'щ':'šč',
            u'ю':'ju',
            u'я':'ja',
            u'Є':'Je',
            u'Ї':'Ji',
            u'Х':'Ch',
            u'Щ':'Šč',
            u'Ю':'Ju',
            u'Я':'Ja'
        }

    if lang == "aze":
        symbols = str.maketrans(u"абвгґдежзиыјклмноөпрстуүфхһчҹш’АБВГҒДЕЖЗИЫЈКЛМНОӨПРСТУҮФХҺЧҸШ«»",
                                u"abvgġdežziyǰklmnoôprstuùfhḥčĉšʼABVGĠDEŽZIYJKLMNOÔPRSTUÙFHḤČĈŠ“”")

        sequence = {
            u'':'XXX'
        }

    if lang == "bru":
        symbols = str.maketrans(u"абвгґдеёжзиійклмнопрстуўфцчшыэьѳѵАБВГҐДЕЁЖЗИІЙКЛМНОПРСТУЎФЦЧШЫЬЭѲѴ«»",
                               u"abvhgdeëžziijklmnoprstuŭfcčšyėʼfiABVHGDEËŽZIIJKLMNOPRSTUŬFCČŠYʹĖFI“”")
        sequence = {
            u'х':'ch',
            u'щ':'šč',
            u'ю':'ju',
            u'я':'ja',
            u'Х':'Ch',
            u'Щ':'Šč',
            u'Ю':'Ju',
            u'Я':'Ja'
        }

    if lang == "bul":
        symbols = str.maketrans(u"абвгдежзийклмнопрстуфцчшъьѣѫАБВГДЕЖЗИЙКЛМНОПРСТУФЦЧШЪЬѢѪ«»",
                               u"abvgdežzijklmnoprstufcčšăʹěŭABVGDEŽZIJKLMNOPRSTUFCČŠĂʹĚŬ“”")
        sequence = {
            u'х':'ch',
            u'щ':'št',
            u'ю':'ju',
            u'я':'ja',
            u'Х':'Ch',
            u'Щ':'Št',
            u'Ю':'Ju',
            u'Я':'Ja'
        }

    if lang == "mac":
        symbols = str.maketrans(u"абвгѓдежзијкќлмнопрстуфхцчшАБВГЃДЕЖЗИЈКЌЛМНОПРСТУФХЦЧШ«»",
                               u"abvgǵdežzijkḱlmnoprstufhcčšABVGǴDEŽZIJKḰLMNOPRSTUFHCČŠ“”")
        sequence = {
            u'ѕ':'dz',
            u'љ':'lj',
            u'њ':'nj',
            u'џ':'dž',
            u'Ѕ':'Dz',
            u'Љ':'Lj',
            u'Њ':'Nj',
            u'Џ':'Dž',
        }

    if lang == "scr":
        symbols = str.maketrans(u"абвгдђежзијклмнопрстћуфхцчшАБВГДЂЕЖЗИЈКЛМНОПРСТЋУФХЦЧШ«»",
                               u"abvgdđežzijklmnoprstćufhcčšABVGDĐEŽZIJKLMNOPRSTĆUFHCČŠ“”")
        sequence = {
            u'љ':'lj',
            u'њ':'nj',
            u'џ':'dž',
            u'Љ':'Lj',
            u'Њ':'Nj',
            u'Џ':'Dž',
        }

    if lang == "mon":
        symbols = str.maketrans(u"абвгдеёжзийклмноөпрстуүфцчшъыьэАБВГДЕЁЖЗИЙКЛМНОӨПРСТУҮФЦЧШЪЫЬЭ«»",
                        u"abvgdeёžzijklmnoöprstuüfcčšʺyʹėABVGDEËŽZIJKLMNOÖPRSTUÜFCČŠʺYʹĖ“”")
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

    if lang == "geo":
        symbols = str.maketrans(u"აბგდევზჱთილმნჲოჟრსჳუფქღშჩცხჴჰჵჶჷჸ«»„“",
                        u"abgdevzētilmnjožrswupkǧščcxqhōfəɂ“”“”")
        sequence = {
            u'კ':'k’',
            u'პ':'p’',
            u'ტ':'t’',
            u'ყ':'q’',
            u'ძ':'dz',
            u'წ':'c’',
            u'ჭ':'č’',
            u'ჯ':'dž'
        }

    if lang == "geoblokt":
        symbols = str.maketrans(u"abgdevzჱTiklmnჲopჟrstჳufqGKSCcZwWxჴjhჵჶ`~JRy",
                        u"აბგდევზჱთიკლმნჲოპჟრსტჳუფქღყშჩცძწჭხჴჯჰჵჶ„“ჷჟღყ")

        sequence = {
            u'':'XXX'
        }

    for char in sequence.keys():
        text = text.replace(char, sequence[char])

    return text.translate(symbols)


# Main (index) page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        origtext = request.form.get("origtext")
        language = request.form.get("language")

        transliteration = translit(origtext, language)

        return render_template("index.html", transliteration=transliteration, origtext=origtext)

    else:
       return render_template("index.html")
