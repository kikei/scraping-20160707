from selenium import webdriver
import urllib
import os
import re

CHROME_DRIVER_PATH = os.path.join(os.path.dirname(__file__), 'chromedriver')
TOP_PAGE = 'http://example.com'
SAVE_DIR = 'download'

browser = webdriver.Chrome(CHROME_DRIVER_PATH)
browser.get(TOP_PAGE)

imgs = browser.find_elements_by_tag_name('img')
srcs = map(to_src, imgs)
srcs = filter(is_jpg, srcs)
for src in srcs: download_to(src, SAVE_DIR)

links = browser.find_elements_by_tag_name('a')
refs = list_href(links)

pickups = list(filter(lambda r: r.find('pickup') > -1, refs))
sumples = list(filter(lambda r: r.find('sumple') > -1, refs))

for pickup in pickups:
    download_pickup(browser, pickup)

for sumple in sumples: download_sumple(browser, sumple)

def download_sumple(browser, sumple):
    browser.get(sumple)
    imgs = browser.find_elements_by_tag_name('img')
    srcs = map(to_src, imgs)
    srcs = filter(is_jpg, srcs)
    for src in srcs: download_to(src, SAVE_DIR)
    
    links = browser.find_elements_by_tag_name('a')
    refs = list_href(links)
    sumpleis = list(filter(is_sumple_link, refs))
    for sumplei in sumpleis: download_pickup(browser, sumplei)

def is_sumple_link(r):
    return re.search('sumple\d_\d.htm', r) is not None

def download_pickup(browser, pickup):
    browser.get(pickup)
    imgs = browser.find_elements_by_tag_name('img')
    srcs = map(to_src, imgs)
    srcs = filter(is_jpg, srcs)
    for src in srcs: download_to(src, SAVE_DIR)

def list_href(es):
    refs = map(to_href, es)
    return list(filter(lambda r: r is not None, refs))

def to_href(e):
    return e.get_attribute('href')

def to_src(e):
    return e.get_attribute('src')

def is_jpg(p):
    return p.find('.jpg') > -1 or p.find('.jpeg') > -1

def is_not_jpg(p):
    return not is_jpg(p)

def mkdir_p(d):
    if not os.path.isdir(d):
        os.mkdir(d)
        if not os.path.isdir(d):
            raise Error("failed to make directory")
        
def download_to(url, d):
    mkdir_p(d)
    to = d + "/" + os.path.basename(url)
    print("Downloading " + url + "...")
    urllib.request.urlretrieve(url, to)
