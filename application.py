from flask import Flask, render_template, redirect, request, session

import requests

app = Flask(__name__)

# Credit to this person for inspiration https://stackoverflow.com/questions/14173421/use-string-translate-in-python-to-transliterate-cyrillic
#Russian
def translitrus(text):
    symbols = str.maketrans(u"абвгдеёжзийклмнопрстуѹфцчшъыьѣэѳѵѡАБВГДЕЁЖЗИЙКЛМНОПРСТУѸФЦЧШЪЫЬѢЭѲѴѠ«»",
                               u"abvgdeёžzijklmnoprstuufcčšʺyʹěėfiôABVGDEËŽZIJKLMNOPRSTUUFCČŠʺYʹĚĖFIÔ“”")
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

# Ukrainian
def translitukr(text):
    symbols = str.maketrans(u"абвгґдежзийклмнопрстуфцчшь’ѳѵАБВГҐДЕЖЗИЙКЛМНОПРСТУФЦЧШЬѲѴ«»",
                               u"abvhgdežzyjklmnoprstufcčšʹʼfiABVHGDEŽZYJKLMNOPRSTUFCČŠʹFI“”")
    sequence = {
        u'є':'je',
        u'ї':'ji',
        u'х':'ch',
        u'щ':'šč',
        u'ю':'ju',
        u'я':'ja',
        u'Є':'Je',
        u'Ї':'Ji',
        u'X':'Ch',
        u'Щ':'Šč',
        u'Ю':'Ju',
        u'Я':'Ja'
    }

    for char in sequence.keys():
        text = text.replace(char, sequence[char])

    return text.translate(symbols)

# Belarusan
def translitbru(text):
    symbols = str.maketrans(u"абвгґдеëжзийклмнопрстуўфцчшыьэѳѵАБВГҐДЕЁЖЗИЙКЛМНОПРСТУЎФЦЧШЫЬЭѲѴ«»",
                               u"abvhgdeëžzyjklmnoprstuŭfcčšyėʼfiABVHGDEЁŽZYJKLMNOPRSTUŬFCČŠYʹĖFI“”")
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

# Bulgarian
def translitbul(text):
    symbols = str.maketrans(u"абвгдежзийклмнопрстуфцчшъьѣѫАБВГДЕЖЗИЙКЛМНОПРСТУФЦЧШЪЬѢѪ«»",
                               u"abvgdežzijklmnoprstufcčšăʹěŭABVGDEŽZIJKLMNOPRSTUFCČŠĂʹĚŬ“”")
    sequence = {
        u'х':'ch',
        u'щ':'št',
        u'ю':'ju',
        u'я':'ja',
        u'X':'Ch',
        u'Щ':'Št',
        u'Ю':'Ju',
        u'Я':'Ja'
    }

    for char in sequence.keys():
        text = text.replace(char, sequence[char])

    return text.translate(symbols)

# Macedonian
def translitmac(text):
    symbols = str.maketrans(u"абвгѓдежзиjкќлмнопрстуфхцчшАБВГЃДЕЖЗИJКЌЛМНОПРСТУФXЦЧШ«»",
                               u"abvgǵdežzijkḱlmnoprstufhcčšABVGǴDEŽZIJKḰLMNOPRSTUFHCČŠ“”")
    sequence = {
        u's':'dz',
        u'љ':'lj',
        u'њ':'nj',
        u'џ':'dž',
        u'S':'Dz',
        u'Љ':'Lj',
        u'Њ':'Nj',
        u'Џ':'Dž',
    }

    for char in sequence.keys():
        text = text.replace(char, sequence[char])

    return text.translate(symbols)

# Serbian/Montenegrin
def translitscr(text):
    symbols = str.maketrans(u"абвгдђежзиjклмнопрстћуфхцчшАБВГДЕЖЗИJКЛМНОПРСТЋУФХЦЧШ«»",
                               u"abvgdđežzijklmnoprstćufhcčšABVGDEŽZIJKLMNOPRSTĆUFHCČŠ“”")
    sequence = {
        u'љ':'lj',
        u'њ':'nj',
        u'џ':'dž',
        u'Љ':'Lj',
        u'Њ':'Nj',
        u'Џ':'Dž',
    }

    for char in sequence.keys():
        text = text.replace(char, sequence[char])

    return text.translate(symbols)

# Georgian
def translitgeo(text):
    symbols = str.maketrans(u"აბგდევზჱთილმნჲოჟრსჳუფქღშჩცხჴჰჵჶჷჸ",
                        u"abgdevzētilmnjožrswupkǧščcxqhōfəɂ")
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

    for char in sequence.keys():
        text = text.replace(char, sequence[char])

    return text.translate(symbols)



# Main (index) page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        origtext = request.form.get("origtext")
        language = request.form.get("language")

        if language == "rus":
            transliteration = translitrus(origtext)
        if language == "ukr":
            transliteration = translitukr(origtext)
        if language == "bru":
            transliteration = translitbru(origtext)
        if language == "bul":
            transliteration = translitbul(origtext)
        if language == "mac":
            transliteration = translitmac(origtext)
        if language == "scr":
            transliteration = translitscr(origtext)
        if language == "geo":
            transliteration = translitgeo(origtext)

        return render_template("index.html", transliteration=transliteration, origtext=origtext)

    else:
       return render_template("index.html")
