import sys
import requests
from bs4 import BeautifulSoup
import re

if len(sys.argv)!=3:
  raise Exception("Usage: python simhash.py <URL1> <URL2>")

url1=sys.argv[1]
url2=sys.argv[2]

def get_body_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup.body:
        return soup.body.get_text()
    else:
        return ""

def get_words(text):
    words = re.findall(r'\w+', text)
    return words

def get_freq(words):
    freq = {}
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    return freq

def get_hash(word):
    p = 53
    m = 2**64
    hash_value = 0
    power = 1
    for ch in word:
        hash_value = (hash_value + ord(ch) * power) % m
        power = (power * p) % m
    return hash_value

def get_simhash(freq):
    vector = [0]*64
    for word, frequency in freq.items():
        hash_value = get_hash(word)
        for i in range(64):
            bit = (hash_value>>i) & 1
            if bit==1:
                vector[i] += frequency
            else:
                vector[i] -= frequency
    simhash = 0
    for i in range(64):
        if vector[i] >= 0:
            simhash |= (1<<i)
    return simhash

def main():
    text1 = get_body_content(url1)
    text2 = get_body_content(url2)

    words1 = get_words(text1)
    words2 = get_words(text2)

    freq1 = get_freq(words1)
    freq2 = get_freq(words2)

    sim1 = get_simhash(freq1)
    sim2 = get_simhash(freq2)

    xorfunc = sim1 ^ sim2
    dif = 0

    while xorfunc > 0:
        if xorfunc % 2 == 1:
            dif += 1
        xorfunc = xorfunc // 2

    common = 64 - dif

    print("Simhash 1:", sim1)
    print("Simhash 2:", sim2)
    print("Common bits:", common)

main()
