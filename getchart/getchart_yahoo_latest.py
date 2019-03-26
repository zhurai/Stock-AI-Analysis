import requests
import datetime
import sys
sys.path.insert(0, '..')
import config
import utils

# If Yahoo Changes Setup, Then This Breaks
today=datetime.datetime.combine(datetime.date.today(),datetime.datetime.min.time())
date1=1225872000
date2=int(today.timestamp())
localconfig=config.config['EXTERNAL']
localconfig2=config.config['EXTERNALYAHOO']

urlbase="https://query1.finance.yahoo.com/v7/finance/download/"
urlpart1="?period1="
urlpart2="?period2="
urlother="&interval=1d&events=history&crumb="
# https://query1.finance.yahoo.com/v7/finance/download/SPXS?period1=1227081600&period2=1553497200&interval=1d&events=history&crumb=Wp35b.GBLT4
# https://query1.finance.yahoo.com/v7/finance/download/SPXS?period1=1225872000?period2=1553497200&interval=1d&events=history&crumb=Wp35b.GBLT4
stocks=[]
# get list of stocks
for item in localconfig2:
    stocks.append(item.upper())

# get their filenames
for item in stocks:
    # download the file
    print(urlbase+item+urlpart1+str(date1)+urlpart2+str(date2)+urlother+crumb)
    r=requests.get(urlbase+item+urlpart1+str(date1)+urlpart2+str(date2)+urlother+crumb)

    # save it into input
    with open(utils.getroot()+localconfig['localfolder']+item+".csv",'w') as f:
        for line in f:
            f.write(line)


# DOES NOT CURRENTLY WORK
# GET COOKIE ID
# GET CRUMB ID

'''
>>> r2=requests.get("https://finance.yahoo.com/quote/AAPL/history?period1=1503558000&period2=1535094000&interval=1wk&filter=history&frequency=1wk")
>>> r2.text

>>> r2.cookie
Traceback (most recent call last):
  File "<pyshell#50>", line 1, in <module>
    r2.cookie
AttributeError: 'Response' object has no attribute 'cookie'
>>> r2.cookies
<RequestsCookieJar[Cookie(version=0, name='B', value='26iujd1e9hv1q&b=3&s=14', port=None, port_specified=False, domain='.yahoo.com', domain_specified=True, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=1585065914, discard=False, comment=None, comment_url=None, rest={}, rfc2109=False)]>
>>> r2.text['crumb']
Traceback (most recent call last):
  File "<pyshell#52>", line 1, in <module>
    r2.text['crumb']
TypeError: string indices must be integers
>>> r2.text.json()
Traceback (most recent call last):
  File "<pyshell#53>", line 1, in <module>
    r2.text.json()
AttributeError: 'str' object has no attribute 'json'
>>> r2.json()
Traceback (most recent call last):
  File "<pyshell#54>", line 1, in <module>
    r2.json()
  File "C:\Personal\Programs\Python\3.7.0\lib\site-packages\requests\models.py", line 897, in json
    return complexjson.loads(self.text, **kwargs)
  File "C:\Personal\Programs\Python\3.7.0\lib\json\__init__.py", line 348, in loads
    return _default_decoder.decode(s)
  File "C:\Personal\Programs\Python\3.7.0\lib\json\decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "C:\Personal\Programs\Python\3.7.0\lib\json\decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
>>> r2.text.contains("crumb")
Traceback (most recent call last):
  File "<pyshell#55>", line 1, in <module>
    r2.text.contains("crumb")
AttributeError: 'str' object has no attribute 'contains'
>>> r2.text.find("crumb")
134229
>>> r2.text[:134229]

>>> r2.text[134229:134230]
'c'
>>> r2.text[134229:134300]
'crumb":"{crumb}","format":"json","q":"SELECT decos.counts.unseen FROM y'
>>> r2.text.find("\"crumb\"")
134228
>>> r2.text.find("\"crumb\"",) crumb
KeyboardInterrupt
>>> for x in range(0,18)
SyntaxError: invalid syntax
>>> r2.text.find("CrumbStore")
404575
>>> r2.text[r2.text.find("CrumbStore"):r2.text.find("CrumbStore")+50]
'CrumbStore":{"crumb":"65mJ9eMMT0k"},"StreamStore":'
>>> r2.text[r2.text.find("CrumbStore"):r2.text.find("CrumbStore")+19]
'CrumbStore":{"crumb'
>>> r2.text[r2.text.find("CrumbStore")+19:r2.text.find("\"",beg=r2.text.find("CrumbStore")+19]

SyntaxError: invalid syntax
>>> r2.text[r2.text.find("CrumbStore")+19:r2.text.find("\"",beg=]

SyntaxError: invalid syntax
>>> r2.text.find("CrumbStore")+19

404594
>>> r2.text[r2.text.find("CrumbStore")+19:r2.text.find("\"",beg=404594]

SyntaxError: invalid syntax
>>> r2.text[r2.text.find("CrumbStore")+19:r2.text.find("\"",404594)]

''
>>> r2.text[r2.text.find("CrumbStore")+19:r2.text.find("\"",404594)]

''
>>> r2.text.find("CrumbStore")+19

404594
>>> r2.text.find("\"",404594)

404594
>>> r2.text.find("\"",404595)

404596
>>> r2.text.find("\"",404594+1)

404596
>>> r2.text[r2.text.find("CrumbStore")+19:r2.text.find("\"",404594+1)]

'":'
>>> r2.text[r2.text.find("CrumbStore")+19:r2.text.find("\"",404594+2)]

'":'
>>> r2.text[r2.text.find("CrumbStore")+19:r2.text.find("\"",404594+3)]

'":"65mJ9eMMT0k'
>>> r2.text[r2.text.find("CrumbStore")+20:r2.text.find("\"",404594+3)]

':"65mJ9eMMT0k'
>>> r2.text[r2.text.find("CrumbStore")+23:r2.text.find("\"",404594+3)]

'5mJ9eMMT0k'
>>> r2.text[r2.text.find("CrumbStore")+22:r2.text.find("\"",404594+3)]

'65mJ9eMMT0k'
>>>
'''
