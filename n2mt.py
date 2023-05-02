import sys
import re
import time

import requests
import hmac
import base64

import random
import fake_headers

requests.packages.urllib3.disable_warnings()

if len(sys.argv) != 3:
    sys.exit("Usage: %s src_lang tgt_lang < text" % sys.argv[0])

URL = "https://papago.naver.com/apis/n2mt/translate"
VERSION = "v1.7.2_9d7a38d925"

LANGS = {
    "en", "ja", "ko", "zh-CN", "zh-TW",
    "ar", "id", "th", "vi",
    "de", "es", "fr", "it", "pt", "ru",
    "fa", "hi", "mm"
}

UUID = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k = 32))
UUID = "%s-%s-%s-%s-%s" % (UUID[:8], UUID[8:12], UUID[12:16], UUID[16:20], UUID[20:32])

src_lang = sys.argv[1]
tgt_lang = sys.argv[2]

assert src_lang in LANGS
assert tgt_lang in LANGS

_headers = fake_headers.Headers()

def hmacmd5(key, passphrase):
    md5 = hmac.digest(passphrase.encode("UTF-8"), key.encode("UTF-8"), "MD5")
    return base64.b64encode(md5).decode("UTF-8")

def n2mt(src_lang, tgt_lang, query):
    timestamp = str(int(time.time() * 1000))
    key = hmacmd5(f"{UUID}\n{URL}\n{timestamp}", VERSION)
    authorization = f"PPG {UUID}:{key}"

    headers = _headers.generate()
    headers.update({
        "Authorization": authorization,
        "Timestamp": timestamp
    })

    data = {
        "source": src_lang,
        "target": tgt_lang,
        "text": query,
        "honorific": "false"
    }

    res = requests.post(URL, headers = headers, data = data, verify = False)

    try:
        return res.json()["translatedText"]
    except:
        print(res)
        exit()

def translate(text):

    global num_reqs
    global num_lines
    global sum_intervals

    interval = random.uniform(5, 9)
    time.sleep(interval)

    srcs = text.split("\n")
    tgts = n2mt(src_lang, tgt_lang, text).split("\n")

    for src, tgt in zip(srcs, tgts):
        tgt = re.sub("\s+", " ", tgt).strip()
        print(tgt)

    num_reqs += 1
    num_lines += len(srcs)
    sum_intervals += interval

    print(
        "[%d] %d chars %d/%d lines (%.4f/%.4f secs)"
        % (num_reqs, len(text), len(srcs), num_lines, interval, sum_intervals),
        file = sys.stderr
    )

text = ""
num_reqs = 0
num_lines = 0
sum_intervals = 0

for line in sys.stdin:

    line = re.sub("\s+", " ", line).strip()

    if not line:
        continue

    if len(text) + len(line) < 4000:
        if text:
            text += "\n"
        text += line
        continue

    translate(text)
    text = line

if text:
    translate(text)
