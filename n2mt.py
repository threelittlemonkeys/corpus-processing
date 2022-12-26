import sys
import re
import time

import requests
import hmac
import base64

import random
import fake_headers

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

if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.exit("Usage: %s src_lang tgt_lang all|tgt < text" % sys.argv[0])

    idxs = []
    text = ""

    num_reqs = 0
    num_lines = 0

    src_lang = sys.argv[1]
    tgt_lang = sys.argv[2]
    option = sys.argv[3]

    assert src_lang in LANGS
    assert tgt_lang in LANGS

    def translate(idxs, text):

        global num_reqs
        global num_lines

        interval = random.uniform(5, 9)
        time.sleep(interval)

        srcs = text.split("\n")
        tgts = n2mt(src_lang, tgt_lang, text).split("\n")

        for idx, src, tgt in zip(idxs, srcs, tgts):
            tgt = re.sub("\s+", " ", tgt).strip()
            print(*([*idx, src] if option == "all" else []), tgt, sep = "\t")

        num_reqs += 1
        num_lines += len(srcs)

        print(
            "[%d] %d chars %d/%d lines (%.4f secs)"
            % (num_reqs, len(text), len(srcs), num_lines, interval),
            file = sys.stderr
        )

    for line in sys.stdin:
        *idx, src = [re.sub("\s+", " ", x).strip() for x in line.split("\t")]

        if not src:
            continue

        if len(text) + len(src)  < 4000:
            idxs.append(idx)
            if text:
                text += "\n"
            text += src
            continue

        translate(idxs, text)
        idxs = [idx]
        text = src

    if text:
        translate(idxs, text)
