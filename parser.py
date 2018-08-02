# CODE WRITTED BY KotRik

import io
import random
import re
import requests
import shutil
from urllib.parse import unquote
import os
import time
from lxml import html

headers = "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko"

sess = requests.Session()
sess.headers['user-agent'] = headers

regex = r"https:\/\/.*\/(.*)"
small_names = False

def generate_random_name():
    alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(alphabet)
    return f"{''.join(random.sample(alphabet, 4))}.jpg"

def download_image(url, folder_name):
    result = re.match(regex, unquote(url))
    name = None
    if small_names or not result:
        name = generate_random_name()
    else:
        name = result.group(1)
    
    img_bytes = requests.get(url, stream=True)
    try:
        if not os.path.exists(f"output/{folder_name}/"):
            os.makedirs(f"output/{folder_name}/")

        with open(f"output/{folder_name}/{name}", 'wb') as f:
            img_bytes.raw.decode_content = True
            shutil.copyfileobj(img_bytes.raw, f) 
    except Exception as e:
        print(f"ERROR: {e}")
        return None

    return name

def main(name, page_count):
    urls_of_images = []
    while page_count >= 1:
        params = dict(
            tags=name,
            page=page_count,
            commit="Search"
        )
        
        fs_paged = sess.get(f"https://yande.re/post", params=params)
        fs_paged_res = html.fromstring(fs_paged.text)

        images = fs_paged_res.cssselect('ul#post-list-posts>li>a.directlink')

        if not images:
            return print("Program not found arts, sorry about that(")
        
        for x in images:
            urls_of_images.append(x.attrib["href"])

        page_count-=1
        time.sleep(0.5)
    
    print(f"Found {len(urls_of_images)} arts, start download")
    picnum = 1
    for x in urls_of_images:
        number = download_image(x, name)
        if not number:
            print(f"[{picnum}/{len(urls_of_images)}] Error while loading image")
        else:
            print(f"[{picnum}/{len(urls_of_images)}] Final download image {number}")
        picnum+=1
        time.sleep(0.5)


if __name__ == "__main__":
    name_of_character = input("Enter Tag (Ex. minami_kotori): ")
    if not name_of_character:
        print("Please enter tag OwO")
        exit()

    page_count = input("How page with content parse?(Ex. 4): ")
    if not page_count.isdigit():
        print("Count need to be int!")
        exit()

    need_adult = input("Download R-18? Type yes/no (default no) (That may not work): ")
    if not need_adult or need_adult == "no":
        sess.cookies.set("country", "RU")
        sess.cookies.set("vote", "1")
    
    use_small_names = input("Use small names like Ilfj.jpg? Type yes/no (default no): ")
    if not use_small_names or use_small_names == "no":
        pass
    else:
        small_names = True
    
    page_count = int(page_count)
    main(name_of_character, page_count)

    print("Program success exited! Thanks for using")
