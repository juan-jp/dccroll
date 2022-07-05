import requests 
import pandas as pd
from bs4 import BeautifulSoup

DC_URL ="https://gall.dcinside.com/board/lists/"

list_index =['제목', '글쓴이']
list =[]

for num in range(1,10):
    try:
        params ={"id":"baseball_new11", "page":f"{num}"}
        headers ={"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        resp = requests.get(DC_URL, params=params, headers=headers)
        soup =BeautifulSoup(resp.content, "html.parser")
        contents =soup.find('tbody').findall('tr')
        page_size =len(contents)
        
        for i in contents:
            line =[]
            print(i)
            try:
                if not "<b>" in str(i):
                    new_dict={}
                    title_tag = i.find("a")
                    title =title_tag.text
                    line.append(title)
                   
            except:
                continue
        
    except:
        continue
    resp.close
    df =pd.DataFrame(list, columns=list_index)
    df.to_csv('content/out.csv', encoding='utf-8-sig')