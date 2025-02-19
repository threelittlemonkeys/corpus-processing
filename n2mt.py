import sys
import re
import time

import requests
import hmac
import base64

import random
import fake_headers

requests.packages.urllib3.disable_warnings()

URL = "https://papago.naver.com/apis/n2mt/translate"
VERSION = "v1.8.9_a5c5d7faee" # main.[a-z0-9]+.chunk.js

LANGS = {
    "en", "ja", "ko", "zh-CN", "zh-TW",
    "ar", "id", "th", "vi",
    "de", "es", "fr", "it", "pt", "ru",
    "fa", "hi", "mm"
}

UUID = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k = 32))
UUID = "%s-%s-%s-%s-%s" % (UUID[:8], UUID[8:12], UUID[12:16], UUID[16:20], UUID[20:32])

logger = {
    "num_reqs": 0,
    "num_srcs": 0,
    "num_tgts": 0,
    "total_time": 0
}

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
        print(res, file = sys.stderr)
        exit()

def translate(src_lang, tgt_lang, xs):

    global num_reqs
    global num_lines
    global sum_intervals

    interval = random.uniform(5, 9)
    time.sleep(interval)

    ys = [
        re.sub("\\s+", " ", y).strip()
        for y in n2mt(src_lang, tgt_lang, "\n".join(xs)).strip().split("\n")
    ]

    logger["num_reqs"] += 1
    logger["num_srcs"] += len(xs)
    logger["num_tgts"] += len(ys)
    logger["total_time"] += interval

    print("[%d] %d chars %d/%d lines -> %d chars %d/%d lines (%.4f/%.4f secs)" % (
        logger["num_reqs"],
        sum(map(len, xs)), len(xs), logger["num_srcs"],
        sum(map(len, ys)), len(ys), logger["num_tgts"],
        interval,
        logger["total_time"]
    ), file = sys.stderr)

    return ys

if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.exit("Usage: %s src_lang tgt_lang filename" % sys.argv[0])

    src_lang, tgt_lang, filename = sys.argv[1:]
    text_size = 1000

    assert src_lang in LANGS
    assert tgt_lang in LANGS

    fin = open(filename, "r")
    fout = open(filename + ".n2mt", "w")

    xs = [
        re.sub("\\s+", " ", x).strip()
        for x in fin.read().strip().split("\n")
    ][::-1]

    z, _xs = 0, []

    while xs or _xs:

        if xs and z < text_size:
            _xs.append(xs.pop())
            z += len(_xs[-1])
            continue

        ys = translate(src_lang, tgt_lang, _xs)
        print("\n".join(ys), file = fout, flush = True)
        z, _xs = 0, []

    fin.close()
    fout.close()
