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
            u'고':'ko', u'곡':'kok', u'곤':'kon', u'곧':'kot', u'골':'kol', u'곪':'kolm', u'곬':'kols', u'곯':'kolh', u'곰':'kom', u'곱':'kop',
            u'곳':'kos', u'공':'kong', u'곶':'koc', u'과':'kwa', u'곽':'kwak', u'관':'kwan', u'괄':'kwal', u'괆':'kwalm', u'계':'kyey',
            u'곈':'kyeyn', u'곌':'kyeyl', u'곕':'kyeyp', u'곗':'kyeys',

            u'괌':'kwam', u'괍':'kwap', u'괏':'kwas', u'광':'kwang', u'괘':'kway', u'괜':'kwayn', u'괠':'kwayl', u'괩':'kwayp', u'괬':'kwayss',
            u'괭':'kwayng', u'괴':'koy', u'괵':'koyk', u'괸':'koyn', u'괼':'koyl', u'굄':'koym', u'굅':'koyp', u'굇':'koys', u'굉':'koyng',
            u'교':'kyo', u'굔':'kyon', u'굘':'kyol', u'굡':'kyop', u'굣':'kyos', u'구':'kwu', u'국':'kwuk', u'군':'kwun', u'굳':'kwut',
            u'굴':'kwul', u'굵':'kwulk', u'굶':'kwulm', u'굻':'kwulh', u'굼':'kwum', u'굽':'kwup', u'굿':'kwus', u'궁':'kwung', u'궂':'kwuc',
            u'궈':'kwe', u'궉':'kwek', u'권':'kwen', u'궐':'kwel', u'궜':'kwess', u'궝':'kweng', u'궤':'kwey', u'궷':'kweys', u'귀':'kwi',
            u'귁':'kwik', u'귄':'kwin', u'귈':'kwil', u'귐':'kwim', u'귑':'kwip', u'귓':'kwis', u'규':'kyu', u'균':'kyun', u'귤':'kyul',
            u'그':'ku', u'극':'kuk', u'근':'kun', u'귿':'kut', u'글':'kul', u'긁':'kulk', u'금':'kum', u'급':'kup', u'긋':'kus', u'긍':'kung',
            u'긔':'kuy', u'기':'ki', u'긱':'kik', u'긴':'kin', u'긷':'kit', u'길':'kil', u'긺':'kilm', u'김':'kim', u'깁':'kip', u'깃':'kis',
            u'깅':'king', u'깆':'kic', u'깊':'kiph', u'까':'kka', u'깍':'kkak', u'깎':'kkakk', u'깐':'kkan', u'깔':'kkal', u'깖':'kkalm',
            u'깜':'kkam', u'깝':'kkap', u'깟':'kkas', u'깠':'kkass', u'깡':'kkang', u'깥':'kkath', u'깨':'kkay', u'깩':'kkayk',
            u'깬':'kkayn', u'깰':'kkayl', u'깸':'kkaym',

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

            u'뇟':'noys', u'뇨':'nyo', u'뇩':'nyok', u'뇬':'nyon', u'뇰':'nyol', u'뇹':'nyop', u'뇻':'nyos', u'뇽':'nyong', u'누':'nwu',
            u'눅':'nwuk', u'눈':'nwun', u'눋':'nwut', u'눌':'nwul', u'눔':'nwum', u'눕':'nwup', u'눗':'nwus', u'눙':'nwung', u'눠':'nwe',
            u'눴':'nwess', u'눼':'nwey', u'뉘':'nwi', u'뉜':'nwin', u'뉠':'nwil', u'뉨':'nwim', u'뉩':'nwip', u'뉴':'nyu', u'뉵':'nyuk', u'뉼':'nyul',
            u'늄':'nyum', u'늅':'nyup', u'늉':'nyung', u'느':'nu', u'늑':'nuk', u'는':'nun', u'늘':'nul', u'늙':'nulk', u'늚':'nulm', u'늠':'num',
            u'늡':'nup', u'늣':'nus', u'능':'nung', u'늦':'nuc', u'늪':'nuph', u'늬':'nuy', u'늰':'nuyn', u'늴':'nuyl', u'니':'ni', u'닉':'nik',
            u'닌':'nin', u'닐':'nil', u'닒':'nilm', u'님':'nim', u'닙':'nip', u'닛':'nis', u'닝':'ning', u'닢':'niph', u'다':'ta', u'닥':'tak',
            u'닦':'takk', u'단':'tan', u'닫':'tat', u'달':'tal', u'닭':'talk', u'닮':'talm', u'닯':'talp', u'닳':'talh', u'담':'tam', u'답':'tap',
            u'닷':'tas', u'닸':'tass', u'당':'tang', u'닺':'tac', u'닻':'tach', u'닿':'tah', u'대':'tay', u'댁':'tayk', u'댄':'tayn', u'댈':'tayl',
            u'댐':'taym', u'댑':'tayp', u'댓':'tays', u'댔':'tayss', u'댕':'tayng', u'댜':'tya', u'더':'te', u'덕':'tek', u'덖':'tekk', u'던':'ten',
            u'덛':'tet', u'덜':'tel', u'덞':'telm', u'덟':'telp', u'덤':'tem', u'덥':'tep',

            u'덧':'tes', u'덩':'teng', u'덫':'tech', u'덮':'teph', u'데':'tey', u'덱':'teyk', u'덴':'teyn', u'델':'teyl', u'뎀':'teym',
            u'뎁':'teyp', u'뎃':'teys', u'뎄':'teyss', u'뎅':'teyng', u'뎌':'tye', u'뎐':'tyen', u'뎔':'tyel', u'뎠':'tyess', u'뎡':'tyeng',
            u'뎨':'tyey', u'뎬':'tyeyn', u'도':'to', u'독':'tok', u'돈':'ton', u'돋':'tot', u'돌':'tol', u'돎':'tolm', u'돐':'tols',
            u'돔':'tom', u'돕':'top', u'돗':'tos', u'동':'tong', u'돛':'toch', u'돝':'toth', u'돠':'twa', u'돤':'twan', u'돨':'twal',
            u'돼':'tway', u'됐':'twayss', u'되':'toy', u'된':'toyn', u'될':'toyl', u'됨':'toym', u'됩':'toyp', u'됫':'toys', u'됴':'tyo',
            u'두':'twu', u'둑':'twuk', u'둔':'twun', u'둘':'twul', u'둠':'twum', u'둡':'twup', u'둣':'twus', u'둥':'twung', u'둬':'twe',
            u'뒀':'twess', u'뒈':'twey', u'뒝':'tweyng', u'뒤':'twi', u'뒨':'twin', u'뒬':'twil', u'뒵':'twip', u'뒷':'twis', u'뒹':'twing',
            u'듀':'tyu', u'듄':'tyun', u'듈':'tyul', u'듐':'tyum', u'듕':'tyung', u'드':'tu', u'득':'tuk', u'든':'tun', u'듣':'tut', u'들':'tul',
            u'듦':'tulm', u'듬':'tum', u'듭':'tup', u'듯':'tus', u'등':'tung', u'듸':'tuy', u'디':'ti', u'딕':'tik', u'딘':'tin', u'딛':'tit',
            u'딜':'til', u'딤':'tim', u'딥':'tip', u'딧':'tis', u'딨':'tiss', u'딩':'ting', u'딪':'tic', u'따':'tta', u'딱':'ttak', u'딴':'ttan',
            u'딸':'ttal',

            u'땀':'ttam', u'땁':'ttap', u'땃':'ttas', u'땄':'ttass', u'땅':'ttang', u'땋':'ttah', u'때':'ttay', u'땍':'ttayk', u'땐':'ttayn',
            u'땔':'ttayl', u'땜':'ttaym', u'땝':'ttayp', u'땟':'ttays', u'땠':'ttayss', u'땡':'ttayng', u'떠':'tte', u'떡':'ttek', u'떤':'tten',
            u'떨':'ttel', u'떪':'ttelm', u'떫':'ttelp', u'떰':'ttem', u'떱':'ttep', u'떳':'ttes', u'떴':'ttess', u'떵':'tteng', u'떻':'tteh',
            u'떼':'ttey', u'떽':'tteyk', u'뗀':'tteyn', u'뗄':'tteyl', u'뗌':'tteym', u'뗍':'tteyp', u'뗏':'tteys', u'뗐':'tteyss',
            u'뗑':'tteyng', u'뗘':'ttye', u'뗬':'ttyess', u'또':'tto', u'똑':'ttok', u'똔':'tton', u'똘':'ttol', u'똥':'ttong', u'똬':'ttwa',
            u'똴':'ttwal', u'뙈':'ttway', u'뙤':'ttoy', u'뙨':'ttoyn', u'뚜':'ttwu', u'뚝':'twuk', u'뚠':'ttwun', u'뚤':'ttwul', u'뚫':'ttwulh',
            u'뚬':'ttwum', u'뚱':'ttwung', u'뛔':'ttwey', u'뛰':'ttwi', u'뛴':'twin', u'뛸':'ttwil', u'뜀':'ttwim', u'뜁':'ttwip', u'뜅':'ttwing',
            u'뜨':'ttu', u'뜩':'ttuk', u'뜬':'ttun', u'뜯':'ttut', u'뜰':'ttul', u'뜸':'ttum', u'뜹':'ttup', u'뜻':'ttus', u'띄':'ttuy',
            u'띈':'ttuyn', u'띌':'ttuyl', u'띔':'ttuym', u'띕':'ttuyp', u'띠':'tti', u'띤':'ttin', u'띨':'ttil', u'띰':'ttim', u'띱':'ttip',
            u'띳':'ttis', u'띵':'tting', u'라':'la', u'락':'lak', u'란':'lan', u'랄':'lal', u'람':'lam', u'랍':'lap', u'랏':'las', u'랐':'lass',
            u'랑':'lang', u'랒':'lac', u'랖':'laph', u'랗':'lwang',

            u'래':'lay', u'랙':'layk', u'랜':'layn', u'랠':'layl', u'램':'laym', u'랩':'layp', u'랫':'lays', u'랬':'layss', u'랭':'layng',
            u'랴':'lya', u'략':'lyak', u'랸':'lyan', u'럇':'lyas', u'량':'lyang', u'러':'le', u'럭':'lek', u'런':'len', u'럴':'lel',
            u'럼':'lem', u'럽':'lep', u'럿':'les', u'렀':'less', u'렁':'leng', u'렇':'leh', u'레':'ley', u'렉':'leyk', u'렌':'leyn', u'렐':'leyl',
            u'렘':'leym', u'렙':'leyp', u'렛':'leys', u'렝':'leyng', u'려':'lye', u'력':'lyek', u'련':'lyen', u'렬':'lyel', u'렴':'lyem',
            u'렵':'lyep', u'렷':'lyes', u'렸':'lyess', u'령':'lyeng', u'례':'lyey', u'롄':'lyeyn', u'롑':'lyeyp', u'롓':'lyeys', u'로':'lo',
            u'록':'lok', u'론':'lon', u'롤':'lol', u'롬':'lom', u'롭':'lop', u'롯':'los', u'롱':'long', u'롸':'lwa', u'롼':'lwan', u'뢍':'lwang',
            u'뢨':'lwayss', u'뢰':'loy', u'뢴':'loyn', u'뢸':'loyl', u'룀':'loym', u'룁':'loyp', u'룃':'loys', u'룅':'loyng', u'료':'lyo',
            u'룐':'lyon', u'룔':'lyol', u'룝':'lyop', u'룟':'lyos', u'룡':'lyong', u'루':'lwu', u'룩':'lwuk', u'룬':'lwun', u'룰':'lwul',
            u'룸':'lwum', u'룹':'lwup', u'룻':'lwus', u'룽':'lwung', u'뤄':'lwe', u'뤘':'lwess', u'뤠':'lwey', u'뤼':'lwi', u'뤽':'lwik',
            u'륀':'lwin', u'륄':'lwil', u'륌':'lwim', u'륏':'lwis', u'륑':'lwing', u'류':'lyu', u'륙':'lyuk', u'륜':'lyun', u'률':'lyul',
            u'륨':'lyum', u'륩':'lyup',

            u'륫':'lyus', u'륭':'lyung', u'르':'lu', u'륵':'luk', u'른':'lun', u'를':'lul', u'름':'lum', u'릅':'lup', u'릇':'lus', u'릉':'lung',
            u'릊':'luc', u'릍':'luth', u'릎':'luph', u'리':'li', u'릭':'lik', u'린':'lin', u'릴':'lil', u'림':'lim', u'립':'lip', u'릿':'lis',
            u'링':'ling', u'마':'ma', u'막':'mak', u'만':'man', u'많':'manh', u'맏':'mat', u'말':'mal', u'맑':'malk', u'맒':'malm', u'맘':'mam',
            u'맙':'map', u'맛':'mas', u'망':'mang', u'맞':'mac', u'맡':'math', u'맣':'mah', u'매':'may', u'맥':'mayk', u'맨':'mayn', u'맬':'mayl',
            u'맴':'maym', u'맵':'mayp', u'맷':'mays', u'맸':'mayss', u'맹':'mayng', u'맺':'mayc', u'먀':'mya', u'먁':'myak', u'먈':'myal',
            u'먕':'myang', u'머':'me',
            u'먹':'mek', u'먼':'men', u'멀':'mel', u'멂':'melm', u'멈':'mem', u'멉':'mep', u'멋':'mes', u'멍':'meng', u'멎':'mec', u'멓':'meh',
            u'메':'mey', u'멕':'meyk', u'멘':'meyn', u'멜':'meyl', u'멤':'meym', u'멥':'meyp', u'멧':'meys', u'멨':'meyss', u'멩':'meyng',
            u'며':'mye', u'멱':'myek', u'면':'myen', u'멸':'myel', u'몃':'myes', u'몄':'myess', u'명':'myeng', u'몇':'myech', u'몌':'myey',
            u'모':'mo', u'목':'mok', u'몫':'moks', u'몬':'mon', u'몰':'mol', u'몲':'molm', u'몸':'mom', u'몹':'mop', u'못':'mos', u'몽':'mong',
            u'뫄':'mwa', u'뫈':'mwan', u'뫘':'mwass', u'뫙':'mwang', u'뫼':'moy',

            u'묀':'moyn', u'묄':'moyl', u'묍':'moyp', u'묏':'moys', u'묑':'moyng', u'묘':'myo', u'묜':'myon', u'묠':'myol', u'묩':'myop',
            u'묫':'myos', u'무':'mu', u'묵':'muk', u'묶':'mukk', u'문':'mun', u'묻':'mut', u'물':'mul', u'묽':'mulk', u'묾':'mulm', u'뭄':'mum',
            u'뭅':'mup', u'뭇':'mus', u'뭉':'mung', u'뭍':'muth', u'뭏':'muh', u'뭐':'mwe', u'뭔':'mwen', u'뭘':'mwel', u'뭡':'mwep', u'뭣':'mwes',
            u'뭬':'mwey', u'뮈':'mwi', u'뮌':'mwin', u'뮐':'mwil', u'뮤':'myu', u'뮨':'myun', u'뮬':'myul', u'뮴':'myum', u'뮷':'myus',
            u'므':'mu', u'믄':'mun', u'믈':'mul', u'믐':'mum', u'믓':'mus', u'미':'mi', u'믹':'mik', u'민':'min', u'믿':'mit', u'밀':'mil',
            u'밂':'milm', u'밈':'mim', u'밉':'mip', u'밋':'mis', u'밌':'miss', u'밍':'ming', u'및':'mich', u'밑':'mith', u'바':'pa', u'박':'pak',
            u'밖':'pakk', u'밗':'paks', u'반':'pan', u'받':'pat', u'발':'pal', u'밝':'palk', u'밞':'palm', u'밟':'palp', u'밤':'pam', u'밥':'pap',
            u'밧':'pas', u'방':'pang', u'밭':'path', u'배':'pay', u'백':'payk', u'밴':'payn', u'밸':'payl', u'뱀':'paym', u'뱁':'payp',
            u'뱃':'pays', u'뱄':'payss', u'뱅':'payng', u'뱉':'payth', u'뱌':'pya', u'뱍':'pyak', u'뱐':'pyan', u'뱝':'pyap', u'버':'pe',
            u'벅':'pek', u'번':'pen', u'벋':'pet', u'벌':'pel', u'벎':'pelm', u'범':'pem', u'법':'pep', u'벗':'pes',

            u'벙':'peng', u'벚':'pec', u'베':'pey', u'벡':'peyk', u'벤':'peyn', u'벧':'peyt', u'벨':'peyl', u'벰':'peym', u'벱':'peyp',
            u'벳':'peys', u'벴':'peyss', u'벵':'peyng', u'벼':'pye', u'벽':'pyek', u'변':'pyen', u'별':'pyel', u'볍':'pyep', u'볏':'pyes',
            u'볐':'pyess', u'병':'pyeng', u'볕':'pyeth', u'볘':'pyey', u'볜':'pyeyn', u'보':'po', u'복':'pok', u'볶':'pokk', u'본':'pon',
            u'볼':'pol', u'봄':'pom', u'봅':'pop', u'봇':'pos', u'봉':'pong', u'봐':'pwa', u'봔':'pwan', u'봤':'pwass', u'봬':'pway', u'뵀':'pwayss',
            u'뵈':'poy', u'뵉':'poyk', u'뵌':'poyn', u'뵐':'poyl', u'뵘':'poym', u'뵙':'poyp', u'뵤':'pyo', u'뵨':'pyon', u'부':'pu', u'북':'puk',
            u'분':'pun', u'붇':'put', u'불':'pul', u'붉':'pulk', u'붊':'pulm', u'붐':'pum', u'붑':'pup', u'붓':'pus', u'붕':'pung', u'붙':'puth',
            u'붚':'puph', u'붜':'pwe', u'붤':'pwel', u'붰':'pwess', u'붸':'pwey', u'뷔':'pwi', u'뷕':'pwik', u'뷘':'pwin', u'뷜':'pwil',
            u'뷩':'pwing', u'뷰':'pyu', u'뷴':'pyun', u'뷸':'pyul', u'븀':'pyum', u'븃':'pyus', u'븅':'pyung', u'브':'pu', u'븍':'puk',
            u'븐':'pun', u'블':'pul', u'븜':'pum', u'븝':'pup', u'븟':'pus', u'비':'pi', u'빅':'pik', u'빈':'pin', u'빌':'pil',
            u'빎':'pilm', u'빔':'pim', u'빕':'pip', u'빗':'pis', u'빙':'ping', u'빚':'pic', u'빛':'pich', u'빠':'ppa', u'빡':'ppak', u'빤':'ppan',

            u'빨':'ppal', u'빪':'ppalm', u'빰':'ppam', u'빱':'ppap', u'빳':'ppas', u'빴':'ppass', u'빵':'ppang', u'빻':'ppah', u'빼':'ppay',
            u'빽':'ppayk', u'뺀':'ppayn', u'뺄':'ppayl', u'뺌':'ppaym', u'뺍':'ppayp', u'뺏':'ppays', u'뺐':'ppayss', u'뺑':'ppayng',
            u'뺘':'ppya', u'뺙':'ppyak', u'뺨':'ppyam', u'뻐':'ppe', u'뻑':'ppek', u'뻔':'ppen', u'뻗':'ppet', u'뻘':'ppel', u'뻠':'ppem',
            u'뻣':'ppes', u'뻤':'ppess', u'뻥':'ppeng', u'뻬':'ppey', u'뼁':'ppeyng', u'뼈':'ppye', u'뼉':'ppyek', u'뼘':'ppyem', u'뼙':'ppyep',
            u'뼛':'ppyes', u'뼜':'ppyeyss', u'뼝':'ppyeyng', u'뽀':'ppo', u'뽁':'ppok', u'뽄':'ppon', u'뽈':'ppol', u'뽐':'ppom', u'뽑':'ppop',
            u'뽕':'ppong', u'뾔':'ppoy', u'뾰':'ppyo', u'뿅':'ppyong', u'뿌':'ppu', u'뿍':'ppuk', u'뿐':'ppun', u'뿔':'ppul', u'뿜':'ppum',
            u'뿟':'ppus', u'뿡':'ppung', u'쀼':'ppyu', u'쁑':'ppyung', u'쁘':'ppu', u'쁜':'ppun', u'쁠':'ppul', u'쁨':'ppum', u'쁩':'ppup',
            u'삐':'ppi', u'삑':'ppik', u'삔':'ppin', u'삘':'ppil', u'삠':'ppim', u'삡':'ppip', u'삣':'ppis', u'삥':'pping', u'사':'sa', u'삭':'sak',
            u'삯':'saks', u'산':'san', u'삳':'sat', u'살':'sal', u'삵':'salk', u'삶':'salm', u'삼':'sam', u'삽':'sap', u'삿':'sas', u'샀':'sass',
            u'상':'sang', u'샅':'sath', u'새':'say', u'색':'sayk', u'샌':'sayn', u'샐':'sayl', u'샘':'saym', u'샙':'sayp', u'샛':'says',
            u'샜':'sayss', u'생':'sayng', u'샤':'sya',

            u'샥':'syak', u'샨':'syan', u'샬':'syal', u'샴':'syam', u'샵':'syap', u'샷':'syas', u'샹':'syang', u'섀':'syay', u'섄':'syayn',
            u'섈':'syayl', u'섐':'syaym', u'섕':'syayng', u'서':'se', u'석':'sek', u'섞':'sekk', u'섟':'seks', u'선':'sen', u'섣':'set',
            u'설':'sel', u'섦':'selm', u'섧':'selp', u'섬':'sem', u'섭':'sep', u'섯':'ses', u'섰':'sess', u'성':'seng', u'섶':'seph', u'세':'sey',
            u'섹':'seyk', u'센':'seyn', u'셀':'seyl', u'셈':'seym', u'셉':'seyp', u'셋':'seys', u'셌':'seyss', u'셍':'seyng', u'셔':'sye',
            u'셕':'syek', u'션':'syen', u'셜':'syel', u'셤':'syem', u'셥':'syep', u'셧':'syes', u'셨':'syess', u'셩':'syeng', u'셰':'syey',
            u'셴':'syeyn', u'셸':'syeyl', u'솅':'syeyng', u'소':'so', u'속':'sok', u'솎':'sokk', u'손':'son', u'솔':'sol', u'솖':'solm',
            u'솜':'som', u'솝':'sop', u'솟':'sos', u'송':'song', u'솥':'soth', u'솨':'swa', u'솩':'swak', u'솬':'swan', u'솰':'swal', u'솽':'swang',
            u'쇄':'sway', u'쇈':'swayn', u'쇌':'swayl', u'쇔':'swaym', u'쇗':'sways', u'쇘':'swayss', u'쇠':'soy', u'쇤':'soyn', u'쇨':'soyl',
            u'쇰':'soym', u'쇱':'soyp', u'쇳':'soys', u'쇼':'syo', u'쇽':'syok', u'숀':'syon', u'숄':'syol', u'숌':'syom', u'숍':'syop',
            u'숏':'syos', u'숑':'syong', u'수':'swu', u'숙':'swuk', u'순':'swun', u'숟':'swut', u'술':'swul', u'숨':'swum', u'숩':'swup',
            u'숫':'swus', u'숭':'swung',

            u'숯':'swuc', u'숱':'swuth', u'숲':'swuph', u'숴':'swe', u'쉈':'swess', u'쉐':'swey', u'쉑':'sweyk', u'쉔':'sweyn', u'쉘':'sweyl',
            u'쉠':'sweym', u'쉥':'sweyng', u'쉬':'swi', u'쉭':'swik', u'쉰':'swin', u'쉴':'swil', u'쉼':'swim', u'쉽':'swip', u'쉿':'swis',
            u'슁':'swing', u'슈':'syu', u'슉':'syuk', u'슐':'syul', u'슘':'syum', u'슛':'syus', u'슝':'syung', u'스':'su', u'슥':'suk', u'슨':'sun',
            u'슬':'sul', u'슭':'sulk', u'슴':'sum', u'습':'sup', u'슷':'sus', u'승':'sung', u'시':'si', u'식':'sik', u'신':'sin', u'싣':'sit',
            u'실':'sil', u'싫':'silh', u'심':'sim', u'십':'sip', u'싯':'sis', u'싱':'sing', u'싶':'siph', u'싸':'ssa', u'싹':'ssak', u'싻':'ssaks',
            u'싼':'ssan', u'쌀':'ssal', u'쌈':'ssam', u'쌉':'ssap', u'쌌':'ssass', u'쌍':'ssang', u'쌓':'ssah', u'쌔':'ssay', u'쌕':'ssayk',
            u'쌘':'ssayn', u'쌜':'ssayl', u'쌤':'ssaym', u'쌥':'ssayp', u'쌨':'ssayss', u'쌩':'ssayng', u'썅':'ssyang', u'써':'sse', u'썩':'ssek',
            u'썬':'ssen', u'썰':'ssel', u'썲':'sselm', u'썸':'ssem', u'썹':'ssep', u'썼':'ssess', u'썽':'sseng', u'쎄':'ssey', u'쎈':'sseyn',
            u'쎌':'sseyl', u'쏀':'ssyeyn', u'쏘':'sso', u'쏙':'ssok', u'쏜':'sson', u'쏟':'ssot', u'쏠':'ssol', u'쏢':'ssolm', u'쏨':'ssom',
            u'쏩':'ssop', u'쏭':'ssong', u'쏴':'sswa', u'쏵':'sswak', u'쏸':'sswan', u'쐈':'sswass', u'쐐':'ssway', u'쐤':'sswayss',
            u'쐬':'ssoy', u'쐰':'ssoyn',

            u'쐴':'ssoyl', u'쐼':'ssoym', u'쐽':'ssoyp', u'쑈':'ssyo', u'쑤':'sswu', u'쑥':'sswuk', u'쑨':'sswun', u'쑬':'sswul', u'쑴':'sswum',
            u'쑵':'sswup', u'쑹':'sswung', u'쒀':'sswe', u'쒔':'sswess', u'쒜':'sswey', u'쒸':'sswi', u'쒼':'sswin', u'쓩':'ssyung', u'쓰':'ssu',
            u'쓱':'ssuk', u'쓴':'ssun', u'쓸':'ssul', u'쓺':'ssulm', u'쓿':'ssulh', u'씀':'ssum', u'씁':'ssup', u'씌':'ssuy', u'씐':'ssuyn',
            u'씔':'ssuyl', u'씜':'ssuym', u'씨':'ssi', u'씩':'ssik', u'씬':'ssin', u'씰':'ssil', u'씸':'ssim', u'씹':'ssip', u'씻':'ssis',
            u'씽':'ssing', u'아':'a', u'악':'ak', u'안':'an', u'앉':'anc', u'않':'anh', u'알':'al', u'앍':'alk', u'앎':'alm', u'앓':'alh',
            u'암':'am', u'압':'ap', u'앗':'as', u'았':'ass', u'앙':'ang', u'앝':'ath', u'앞':'aph', u'애':'ay', u'액':'ayk', u'앤':'ayn',
            u'앨':'ayl', u'앰':'aym', u'앱':'ayp', u'앳':'ays', u'앴':'ayss', u'앵':'ayng', u'야':'ya', u'약':'yak', u'얀':'yan', u'얄':'yal',
            u'얇':'yalp', u'얌':'yam', u'얍':'yap', u'얏':'yas', u'양':'yang', u'얕':'yath', u'얗':'yah', u'얘':'yay', u'얜':'yayn', u'얠':'yayl',
            u'얩':'yayp', u'어':'e', u'억':'ek', u'언':'en', u'얹':'enc', u'얻':'et', u'얼':'el', u'얽':'elk', u'얾':'elm', u'엄':'em',
            u'업':'ep', u'없':'eps', u'엇':'es', u'었':'ess', u'엉':'eng', u'엊':'ec', u'엌':'ekh', u'엎':'eph',

            u'에':'ey', u'엑':'eyk', u'엔':'eyn', u'엘':'eyl', u'엠':'eym', u'엡':'eyp', u'엣':'eys', u'엥':'eyng', u'여':'ye', u'역':'yek',
            u'엮':'yekk', u'연':'yen', u'열':'yel', u'엶':'yelm', u'엷':'yelp', u'염':'yem', u'엽':'yep', u'엾':'yeps', u'엿':'yes', u'였':'yess',
            u'영':'yeng', u'옅':'yeth', u'옆':'yeph', u'옇':'yeh', u'예':'yey', u'옌':'yeyn', u'옐':'yeyl', u'옘':'yeym', u'옙':'yeyp', u'옛':'yeys',
            u'옜':'yeyss', u'오':'o', u'옥':'ok', u'온':'on', u'올':'ol', u'옭':'olk', u'옮':'olm', u'옰':'ols', u'옳':'olh', u'옴':'om', u'옵':'op',
            u'옷':'os', u'옹':'ong', u'옻':'och', u'와':'wa', u'왁':'wak', u'완':'wan', u'왈':'wal', u'왐':'wam', u'왑':'wap', u'왓':'was', u'왔':'wass',
            u'왕':'wang', u'왜':'way', u'왝':'wayk', u'왠':'wayn', u'왬':'waym', u'왯':'ways', u'왱':'wayng', u'외':'oy', u'왹':'oyk', u'왼':'oyn',
            u'욀':'oyl', u'욈':'oym', u'욉':'oyp', u'욋':'oys', u'욍':'oyng', u'요':'yo', u'욕':'yok', u'욘':'yon', u'욜':'yol', u'욤':'yom', u'욥':'yop',
            u'욧':'yos', u'용':'yong', u'우':'wu', u'욱':'wuk', u'운':'wun', u'울':'wul', u'욹':'wulk', u'욺':'wulm', u'움':'wum', u'웁':'wup',
            u'웃':'wus', u'웅':'wung', u'워':'we', u'웍':'wek', u'원':'wen', u'월':'wel', u'웜':'wem', u'웝':'wep', u'웠':'wess', u'웡':'weng',
            u'웨':'wey',

            u'웩':'weyk', u'웬':'weyn', u'웰':'weyl', u'웸':'weym', u'웹':'weyp', u'웽':'weyng', u'위':'wi', u'윅':'wik', u'윈':'win',
            u'윌':'wil', u'윔':'wim', u'윕':'wip', u'윗':'wis', u'윙':'wing', u'유':'yu', u'육':'yuk', u'윤':'yun', u'율':'yul', u'윰':'yum',
            u'윱':'yup', u'윳':'yus', u'융':'yung', u'윷':'yuch', u'으':'u', u'윽':'uk', u'은':'un', u'을':'ul', u'읊':'ulph', u'음':'um',
            u'읍':'up', u'읏':'us', u'응':'ung', u'읒':'uc', u'읓':'uch', u'읔':'ukh', u'읕':'uth', u'읖':'uph', u'읗':'uh', u'의':'uy',
            u'읜':'uyn', u'읠':'uyl', u'읨':'uym', u'읫':'uys', u'이':'i', u'익':'ik', u'인':'in', u'일':'il', u'읽':'ilk', u'읾':'ilm',
            u'잃':'ilh', u'임':'im', u'입':'ip', u'잇':'is', u'있':'iss', u'잉':'ing', u'잊':'ic', u'잎':'iph', u'자':'ca', u'작':'cak',
            u'잔':'can', u'잖':'canh', u'잗':'cat', u'잘':'cal', u'잚':'calm', u'잠':'cam', u'잡':'cap', u'잣':'cas', u'잤':'cass', u'장':'cang',
            u'잦':'cac', u'재':'cay', u'잭':'cayk', u'잰':'cayn', u'잴':'cayl', u'잼':'caym', u'잽':'cayp', u'잿':'cays', u'쟀':'cayss',
            u'쟁':'cayng', u'쟈':'cya', u'쟉':'cyak', u'쟌':'cyan', u'쟎':'cyanh', u'쟐':'cyal', u'쟘':'cyam', u'쟝':'cyang', u'쟤':'cyay',
            u'쟨':'cyayn', u'쟬':'cyayl', u'저':'ce', u'적':'cek', u'전':'cen', u'절':'cel', u'젊':'celm',

            u'점':'cem', u'접':'cep', u'젓':'ces', u'정':'ceng', u'젖':'cec', u'제':'cey', u'젝':'ceyk', u'젠':'ceyn', u'젤':'ceyl', u'젬':'ceym',
            u'젭':'ceyp', u'젯':'ceys', u'젱':'ceyng', u'져':'cye', u'젼':'cyen', u'졀':'cyel', u'졈':'cyem', u'졉':'cyep', u'졌':'cyess',
            u'졍':'cyeng', u'졔':'cyey', u'조':'co', u'족':'cok', u'존':'con', u'졸':'col', u'졺':'colm', u'좀':'com', u'좁':'cop', u'좃':'cos',
            u'종':'cong', u'좆':'coc', u'좇':'coch', u'좋':'coh', u'좌':'cwa', u'좍':'cwak', u'좔':'cwal', u'좝':'cwap', u'좟':'cwas', u'좡':'cwang',
            u'좨':'cway', u'좼':'cwayss', u'좽':'cwayng', u'죄':'coy', u'죈':'coyn', u'죌':'coyl', u'죔':'coym', u'죕':'coyp', u'죗':'coys',
            u'죙':'coyng', u'죠':'cyo', u'죡':'cyok', u'죤':'cyon', u'죵':'cyong', u'주':'cwu', u'죽':'cwuk', u'준':'cwun', u'줄':'cwul', u'줅':'cwulk',
            u'줆':'cwulm', u'줌':'cwum', u'줍':'cwup', u'줏':'cwus', u'중':'cwung', u'줘':'cwe', u'줬':'cwess', u'줴':'cwey', u'쥐':'cwi',
            u'쥑':'cwik', u'쥔':'cwin', u'쥘':'cwil', u'쥠':'cwim', u'쥡':'cwip', u'쥣':'cwis', u'쥬':'cyu', u'쥰':'cyun', u'쥴':'cyul', u'쥼':'cyum',
            u'즈':'cu', u'즉':'cuk', u'즌':'cun', u'즐':'cul', u'즘':'cum', u'즙':'cup', u'즛':'cus', u'증':'cung', u'지':'ci', u'직':'cik',
            u'진':'cin', u'짇':'cit', u'질':'cil', u'짊':'cilm', u'짐':'cim', u'집':'cip', u'짓':'cis'







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
