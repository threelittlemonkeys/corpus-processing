import sys
import re

import requests
import time
import hmac
import base64

import random
import fake_headers

URL = "https://papago.naver.com/apis/n2mt/translate"
VERSION = "v1.6.9_0f9c783dcc"

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
    headers.update({"Authorization": authorization, "Timestamp": timestamp})

    data = {
        "source": src_lang,
        "target": tgt_lang,
        "text": query,
        "honorific": "false"
    }

    res = requests.post(URL, headers = headers, data = data)

    try:
        res = res.json()
    except:
        print(res)
        exit()

    return res["translatedText"]

if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.exit("Usage: %s src_lang tgt_lang both|tgt < text" % sys.argv[0])

    num_reqs = 0
    num_lines = 0
    text = ""

    src_lang = sys.argv[1]
    tgt_lang = sys.argv[2]
    option = sys.argv[3]

    def translate(text):

        global num_lines

        srcs = text.split("\n")
        tgts = n2mt(src_lang, tgt_lang, text).split("\n")

        for src, tgt in zip(srcs, tgts):
            tgt = re.sub("\s+", " ", tgt).strip()
            result = [src] if option = "both" else []
            result += [tgt]
            print(*result, sep = "\t")

        num_lines += len(srcs)
        interval = random.uniform(5, 9)
        time.sleep(interval)

        print(
            "[%d] %d chars %d/%d lines (%.4f secs)"
            % (num_reqs, len(text), len(srcs), num_lines, interval),
            file = sys.stderr
        )

    for line in sys.stdin:
        line = re.sub("\s+", " ", line).strip()

        if len(text) + len(line)  < 4000:
            if text:
                text += "\n"
            text += line
            continue

        translate(text)

        text = ""
        num_reqs += 1

    if text:
        translate(text)
