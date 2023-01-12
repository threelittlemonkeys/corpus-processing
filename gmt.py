import os
import sys
import re
import time
import urllib
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo dpkg -i google-chrome-stable_current_amd64.deb
# sudo apt-get install -f
# pip install selenium
# pip install webdriver-manager

if len(sys.argv) != 3:
    sys.exit("Usage: %s src_lang tgt_lang < text" % sys.argv[0])

sl = sys.argv[1]
tl = sys.argv[2]

path = (os.path.dirname(__file__) or ".") + "/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--single-process")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

def translate(text):

    global num_reqs
    global num_lines
    global sum_intervals

    q = urllib.parse.quote(text)
    driver.get(f"https://translate.google.com/?sl={sl}&tl={tl}&text={q}&op=translate")

    interval = random.uniform(5, 9)
    time.sleep(interval)

    out = driver.find_element(By.CLASS_NAME,'HwtZe').text

    srcs = text.split("\n")
    tgts = out.split("\n")

    for src, tgt in zip(srcs, tgts):
        tgt = re.sub("\s+", " ", tgt).strip()
        print(src, tgt, sep = "\t")

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

    if len(text) + len(line) < 4500:
        if text:
            text += "\n"
        text += line
        continue

    translate(text)
    text = line

if text:
    translate(text)
