from flask import Flask, render_template, redirect, request, session

import requests

app = Flask(__name__)

# Credit to this person for inspiration https://stackoverflow.com/questions/14173421/use-string-translate-in-python-to-transliterate-cyrillic
# Transliteration function
def translit(text, lang):
    if lang == "kor":
        symbols = str.maketrans(u"『』「」",
                               u"“”“”")

        sequence = {
            u'가':'ka', u'각':'kak', u'갂':'kakk', u'갃':'kaks', u'간':'kan', u'갅':'kanc', u'갆':'kanh', u'갇':'kat', u'갈':'kal',
            u'갉':'kalk', u'갊':'kalm', u'갋':'kalp', u'갌':'kals', u'갍':'kalth', u'갎':'kalph', u'갏':'kalh', u'감':'kam', u'갑':'kap',
            u'값':'kaps', u'갓':'kas', u'갔':'kass', u'강':'kang', u'갖':'kac', u'갗':'kach', u'갘':'kakh', u'같':'kath', u'갚':'kaph',
            u'갛':'kah', u'개':'kay', u'객':'kayk', u'갞':'kaykk', u'갟':'kayks', u'갠':'kayn', u'갡':'kaync', u'갢':'kaynh', u'갣':'kayt',
            u'갤':'kayl', u'갥':'kaylk', u'갦':'kaylm', u'갧':'kaylp', u'갨':'kayls', u'갩':'kaylth', u'갪':'kaylph', u'갫':'kaylh',
            u'갬':'kaym', u'갭':'kayp', u'갮':'kayps', u'갯':'kays', u'갰':'kayss', u'갱':'kayng', u'갲':'kayc', u'갳':'kaych', u'갴':'kaykh',
            u'갵':'kayth', u'갶':'kayph', u'갷':'kayh', u'갸':'kya', u'갹':'kyak', u'갺':'kyakk', u'갻':'kyaks', u'갼':'kyan', u'갽':'kyanc',
            u'갾':'kyanh', u'갿':'kyat', u'걀':'kyal', u'걁':'kyalk', u'걂':'kyalm', u'걃':'kyalp', u'걄':'kyals', u'걅':'kyalth', u'걆':'kyalph',
            u'걇':'kyalh', u'걈':'kyam', u'걉':'kyap', u'걊':'kyaps', u'걋':'kyas', u'걌':'kyass', u'걍':'kyang', u'걎':'kyac', u'걏':'kyach',
            u'걐':'kyakh', u'걑':'kyath', u'걒':'kyaph', u'걓':'kyah', u'걔':'kyay', u'걕':'kyayk', u'걖':'kyaykk', u'걗':'kyayks', u'걘':'kyayn',
            u'걙':'kyaync', u'걚':'kyaynh', u'걛':'kyayt', u'걜':'kyayl', u'걝':'kyaylk', u'걞':'kyaylm', u'걟':'kyaylp', u'걠':'kyayls',
            u'걡':'kyaylth', u'걢':'kyaylph', u'걣':'kyaylh', u'걤':'kyaym', u'걥':'kyayp', u'걦':'kyayps', u'걧':'kyays', u'걨':'kyayss',
            u'걩':'kyayng', u'걪':'kyayc', u'걫':'kyaych', u'걬':'kyaykh', u'걭':'kyayth', u'걮':'kyayph', u'걯':'kyayh', u'거':'ke', u'걱':'kek',
            u'걲':'kekk', u'걳':'keks', u'건':'ken', u'걵':'kenc', u'걶':'kenh', u'걷':'ket', u'걸':'kel', u'걹':'kelk', u'걺':'kelm',u'걻':'kelp',
            u'걼':'kels', u'걽':'kelth', u'걾':'kelph', u'걿':'kelh', u'검':'kem', u'겁':'kep', u'겂':'keps', u'것':'kes', u'겄':'kess',
            u'겅':'keng', u'겆':'kec', u'겇':'kech', u'겈':'kekh', u'겉':'keth', u'겊':'keph', u'겋':'keh', u'게':'key', u'겍':'keyk', u'겎':'keykk',
            u'겏':'keyks', u'겐':'keyn', u'겑':'keync', u'겒':'keynh', u'겓':'keyt', u'겔':'keyl', u'겕':'keylk', u'겖':'keylm', u'겗':'keylp',
            u'겘':'keyls', u'겙':'keylth', u'겚':'keylph', u'겛':'keylh', u'겜':'keym', u'겝':'keyp', u'겞':'keyps', u'겟':'keys', u'겠':'keyss',
            u'겡':'keyng', u'겢':'keyc', u'겣':'keych', u'겤':'keykh', u'겥':'keyth', u'겦':'keyph', u'겧':'keyh', u'겨':'kye', u'격':'kyek',
            u'겪':'kyekk', u'겫':'kyeks', u'견':'kyen', u'겭':'kyenc', u'겮':'kyenh', u'겯':'kyet', u'결':'kyel', u'겱':'kyelk', u'겲':'kyelm',
            u'겳':'kyelp', u'겴':'kyels', u'겵':'kyelth', u'겶':'kyelph', u'겷':'kyelh', u'겸':'kyem', u'겹':'kyep', u'겺':'kyeps', u'겻':'kyes',
            u'겼':'kyess', u'경':'kyeng', u'겾':'kyec', u'겿':'kyech', u'곀':'kyekh', u'곁':'kyeth', u'곂':'kyeph', u'곃':'kyeh',
            u'고':'ko', u'곡':'kok', u'곤':'kon', u'곧':'kot', u'골':'kol', u'곪':'kolm', u'곬':'kols', u'곯':'kolh', u'곰':'kom',
            u'곳':'kos', u'공':'kong', u'곶':'koc', u'과':'kwa', u'곽':'kwak', u'관':'kwan', u'괄':'kwal', u'괆':'kwalm',

            u'괌':'kwam', u'괍':'kwap', u'괏':'kwas', u'광':'kwang', u'괘':'kway', u'괜':'kwayn', u'괠':'kwayl', u'괩':'kwayp', u'괬':'kwayss',
            u'괭':'kwayng', u'괴':'koy', u'괵':'koyk', u'괸':'koyn', u'괼':'koyl', u'굄':'koym', u'굅':'koyp', u'굇':'koys', u'굉':'koyng',
            u'교':'kyo', u'굔':'kyon', u'굘':'kyol', u'굡':'kyop', u'굣':'kyos', u'구':'kwu', u'국':'kwuk', u'군':'kwun', u'굳':'kwut',
            u'굴':'kwul', u'굵':'kwulk', u'굶':'kwulm', u'굻':'kwulh', u'굼':'kwum', u'굽':'kwup', u'굿':'kwus', u'궁':'kwung', u'궂':'kwuc',
            u'궈':'kwe', u'궉':'kwek', u'권':'kwen', u'궐':'kwel', u'궜':'kwess', u'궝':'kweng', u'궤':'kwey', u'궷':'kweys', u'귀':'kwi',
            u'귁':'kwik', u'귄':'kwin', u'귈':'kwil', u'귐':'kwim', u'귑':'kwip', u'귓':'kwis', u'규':'kyu', u'균':'kyun', u'귤':'kyul',
            u'그':'ku', u'극':'kuk', u'근':'kun', u'귿':'kut', u'글':'kul', u'긁':'kulk', u'금':'kum', u'급':'kup', u'긋':'kus', u'긍':'kung',
            u'긔':'kuy', u'기':'ki', u'긱':'kik', u'긴':'kin', u'긷':'kit', u'길':'kil', u'긺':'kilm', u'김':'kim', u'깁':'kip', u'깃':'kis',
            u'깅':'king', u'깆':'kic', u'깊':'kiph', u'까':'kka', u'깍':'kkak', u'깎':'kkakk', u'깐':'kkan', u'깔':'kkal', u'깖':'kkalm',
            u'깠':'kkass', u'깡':'kkang', u'깥':'kkath', u'깨':'kkay', u'깩':'kkayk', u'깬':'kkayn', u'깰':'kkayl', u'깸':'kkaym',

            u'깹':'kkayp', u'깻':'kkays', u'깼':'kkayss', u'깽':'kkayng', u'꺄':'kkya', u'꺅':'kkyak', u'꺌':'kkyal', u'꺼':'kke', u'꺽':'kkek',
            u'꺾':'kkekk', u'껀':'kken', u'껄':'kkel', u'껌':'kkem', u'껍':'kkep', u'껏':'kkes', u'껐':'kkess', u'껑':'kkeng', u'께':'kkey',
            u'껙':'kkeyk', u'껜':'kkeyn', u'껨':'kkeym', u'껫':'kkeys', u'껭':'kkeyng', u'껴':'kkye', u'껸':'kkyen', u'껼':'kkyel', u'꼇':'kkyes',
            u'꼈':'kkyess', u'꼍':'kkyeth', u'꼐':'kkyey', u'꼬':'kko', u'꼭':'kkok', u'꼰':'kkon', u'꼲':'kkonh', u'꼴':'kkol', u'꼼':'kkom',
            u'꼽':'kkop', u'꼿':'kkos', u'꽁':'kkong', u'꽂':'kkoc', u'꽃':'kkoch', u'꽈':'kkwa', u'꽉':'kkwak', u'꽐':'kkwal', u'꽜':'kkwass',
            u'꽝':'kkwang', u'꽤':'kkway', u'꽥':'kkwayk', u'꽹':'kkwayng', u'꾀':'kkoy', u'꾄':'kkoyn', u'꾈':'kkoyl', u'꾐':'kkoym', u'꾑':'kkoyp',
            u'꾕':'kkoyng', u'꾜':'kkyo', u'꾸':'kkwu', u'꾹':'kkwuk', u'꾼':'kkwun', u'꿀':'kkwul', u'꿇':'kkwulh', u'꿈':'kkwum', u'꿉':'kkwup',
            u'꿋':'kkwus', u'꿍':'kkwung', u'꿎':'kkwuc', u'꿔':'kkwe', u'꿜':'kkwel', u'꿨':'kkwess', u'꿩':'kkweng', u'꿰':'kkwey', u'꿱':'kkweyk',
            u'꿴':'kkweyn', u'꿸':'kkweyl', u'뀀':'kkweym', u'뀁':'kkweyp', u'뀄':'kkweyss', u'뀌':'kkwi', u'뀐':'kkwin', u'뀔':'kkwil', u'뀜':'kkwim',
            u'뀝':'kkwip', u'뀨':'kkyu', u'끄':'kku', u'끅':'kkuk', u'끈':'kkun', u'끊':'kkunh', u'끌':'kkul', u'끎':'kkulm', u'끓':'kkulh',
            u'끔':'kkum', u'끕':'kkup', u'끗':'kkus', u'끙':'kkung',

            u'끝':'kkuth', u'끼':'kki', u'끽':'kkik', u'낀':'kkin', u'낄':'kkil', u'낌':'kkim', u'낍':'kkip', u'낏':'kkis', u'낑':'kking',
            u'나':'na', u'낙':'nak', u'낚':'nakk', u'난':'nan', u'낟':'nat', u'날':'nal', u'낡':'nalk', u'낢':'nalm', u'남':'nam', u'납':'nap',
            u'낫':'nas', u'났':'nass', u'낭':'nang', u'낮':'nac', u'낯':'nach', u'낱':'nath', u'낳':'nah', u'내':'nay', u'낵':'nayk', u'낸':'nayn',
            u'낼':'nayl', u'냄':'naym', u'냅':'nayp', u'냇':'nays', u'냈':'nayss', u'냉':'nayng', u'냐':'nya', u'냑':'nyak', u'냔':'nyan',
            u'냘':'nyal', u'냠':'nyam', u'냥':'nyang', u'너':'ne', u'넉':'nek', u'넋':'neks', u'넌':'nen', u'널':'nel', u'넒':'nelm', u'넓':'nelp',
            u'넘':'nem', u'넙':'nep', u'넛':'nes', u'넜':'ness', u'넝':'neng', u'넣':'neh', u'네':'ney', u'넥':'neyk', u'넨':'neyn', u'넬':'neyl',
            u'넴':'neym', u'넵':'neyp', u'넷':'neys', u'넸':'neyss', u'넹':'neyng', u'녀':'nye', u'녁':'nyek', u'년':'nyen', u'녈':'nyel',
            u'념':'nyem', u'녑':'nyep', u'녔':'nyess', u'녕':'nyeng', u'녘':'nyekk', u'녜':'nyey', u'녠':'nyeyn', u'노':'no', u'녹':'nok', u'논':'non',
            u'놀':'nol', u'놂':'nolm', u'놈':'nom', u'놉':'nop', u'놋':'nos', u'농':'nong', u'높':'noph', u'놓':'noh', u'놔':'nwa', u'놘':'nwan',
            u'놜':'nwal', u'놨':'nwass', u'뇌':'noy', u'뇐':'noyn', u'뇔':'noyl', u'뇜':'noym', u'뇝':'noyp',



        }



    if lang == "rus":
        symbols = str.maketrans(u"абвгдеёжзийклмнопрстуѹфцчшъыьѣэѳѵѡАБВГДЕЁЖЗИЙКЛМНОПРСТУѸФЦЧШЪЫЬѢЭѲѴѠ«»„”",
                               u"abvgdeëžzijklmnoprstuufcčšʺyʹěėfiôABVGDEËŽZIJKLMNOPRSTUUFCČŠʺYʹĚĖFIÔ“”\"\"")
        sequence = {
            u'х':'ch',
            u'щ':'šč',
            u'ю':'ju',
            u'я':'ja',
            u'Х':'Ch',
            u'Щ':'Šč',
            u'Ю':'Ju',
            u'Я':'Ja',
            u'№':'No.'
        }

    if lang == "ukr":
        symbols = str.maketrans(u"абвгґдежзиійклмнопрстуфцчшь’ѳѵАБВГҐДЕЖЗИІЙКЛМНОПРСТУФЦЧШЬѲѴ«»„”",
                               u"abvhgdežzyijklmnoprstufcčšʹʼfiABVHGDEŽZYIJKLMNOPRSTUFCČŠʹFI“”\"\"")
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
            u'Я':'Ja',
            u'№':'No.'
        }

    if lang == "iso9":
        symbols = str.maketrans(u"абвгѓғҕдђеёєжзӡѕийіїыјкќлмнԋоөҩпҧрстћҭуӯўүфхһцчҹшщъьэюяѣѫѵ’АБВГЃҒҔДЂЕЁЄЖЗӠЅИЙІЇЫЈКЌЛМНԊОӨҨПҦРСТЋҬУӮЎҮФХҺЦЧҸШЩЪЬЭЮЯѢѪѴӀ«»„”",
                                u"abvgǵġğdđeëêžzźẑijìïyǰkḱlmnǹoôòpṕrstćțuūŭùfhḥcčĉšŝʺʹèûâěǎỳʼABVGǴĠĞDĐEËÊŽZŹẐIJÌÏYJKḰLMNǸOÔÒPṔRSTĆȚUŪŬÙFHḤCČĈŠŜʺʹÈÛÂĚǍỲ‡“”\"\"")

        sequence = {
            u'':'XXX',
            u'Ҟ':'K̄',
            u'ҟ':'k̄',
            u'Қ':'K̦',
            u'Ҝ':'K̂',
            u'ҝ':'k̂',
            u'қ':'k̦',
            u'Љ':'L̂',
            u'љ':'l̂',
            u'Њ':'N̂',
            u'њ':'n̂',
            u'Ң':'N̦',
            u'ң':'n̦',
            u'Ұ':'U̇',
            u'ұ':'u̇',
            u'Ҳ':'H̦',
            u'ҳ':'h̦',
            u'Ҵ':'C̄',
            u'ҵ':'c̄',
            u'Џ':'D̂',
            u'џ':'d̂',
            u'Ҷ':'C̦',
            u'ҷ':'c̦',
            u'Ҽ':'C̆',
            u'ҽ':'c̆',
            u'Ҿ':'C̨̆',
            u'ҿ':'c̨̆',
            u'Ә':'A̋',
            u'ә':'a̋',
            u'Ґ':'G̀',
            u'ґ':'g̀',
            u'Ѳ':'F̀',
            u'ѳ':'f̀',
            u'Җ':'Ž̦',
            u'җ':'ž̦',
            u'№':'No.'
        }

    if lang == "bru":
        symbols = str.maketrans(u"абвгґдеёжзиійклмнопрстуўфцчшыэьѳѵАБВГҐДЕЁЖЗИІЙКЛМНОПРСТУЎФЦЧШЫЬЭѲѴ«»„”",
                               u"abvhgdeëžziijklmnoprstuŭfcčšyėʼfiABVHGDEËŽZIIJKLMNOPRSTUŬFCČŠYʹĖFI“”\"\"")
        sequence = {
            u'х':'ch',
            u'щ':'šč',
            u'ю':'ju',
            u'я':'ja',
            u'Х':'Ch',
            u'Щ':'Šč',
            u'Ю':'Ju',
            u'Я':'Ja',
            u'№':'No.'
        }

    if lang == "bul":
        symbols = str.maketrans(u"абвгдежзийклмнопрстуфцчшъьѣѫАБВГДЕЖЗИЙКЛМНОПРСТУФЦЧШЪЬѢѪ«»„”",
                               u"abvgdežzijklmnoprstufcčšăʹěŭABVGDEŽZIJKLMNOPRSTUFCČŠĂʹĚŬ“”\"\"")
        sequence = {
            u'х':'ch',
            u'щ':'št',
            u'ю':'ju',
            u'я':'ja',
            u'Х':'Ch',
            u'Щ':'Št',
            u'Ю':'Ju',
            u'Я':'Ja',
            u'№':'No.'
        }

    if lang == "mac":
        symbols = str.maketrans(u"абвгѓдежзијкќлмнопрстуфхцчшАБВГЃДЕЖЗИЈКЌЛМНОПРСТУФХЦЧШ«»„”",
                               u"abvgǵdežzijkḱlmnoprstufhcčšABVGǴDEŽZIJKḰLMNOPRSTUFHCČŠ“”\"\"")
        sequence = {
            u'ѕ':'dz',
            u'љ':'lj',
            u'њ':'nj',
            u'џ':'dž',
            u'Ѕ':'Dz',
            u'Љ':'Lj',
            u'Њ':'Nj',
            u'Џ':'Dž',
            u'№':'No.'
        }

    if lang == "scr":
        symbols = str.maketrans(u"абвгдђежзијклмнопрстћуфхцчшАБВГДЂЕЖЗИЈКЛМНОПРСТЋУФХЦЧШ«»„”",
                               u"abvgdđežzijklmnoprstćufhcčšABVGDĐEŽZIJKLMNOPRSTĆUFHCČŠ“”\"\"")
        sequence = {
            u'љ':'lj',
            u'њ':'nj',
            u'џ':'dž',
            u'Љ':'Lj',
            u'Њ':'Nj',
            u'Џ':'Dž',
            u'№':'No.'
        }

    if lang == "mon":
        symbols = str.maketrans(u"абвгдеёжзийклмноөпрстуүфцчшъыьэАБВГДЕЁЖЗИЙКЛМНОӨПРСТУҮФЦЧШЪЫЬЭ«»„”",
                        u"abvgdeëžzijklmnoöprstuüfcčšʺyʹėABVGDEËŽZIJKLMNOÖPRSTUÜFCČŠʺYʹĖ“”\"\"")
        sequence = {
            u'х':'ch',
            u'щ':'šč',
            u'ю':'ju',
            u'я':'ja',
            u'X':'Ch',
            u'Щ':'Šč',
            u'Ю':'Ju',
            u'Я':'Ja',
            u'№':'No.'
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
            u'ჯ':'dž',
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
