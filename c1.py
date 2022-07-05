from bs4 import BeautifulSoup
import requests, lxml, time, reprlib
from datetime import datetime, timedelta

re = reprlib.Repr()
re.maxstring = 20    # max characters displayed for strings

def midReturn(val, s, e):
    if s in val:
        val = val[val.find(s)+len(s):]
        if e in val: val = val[:val.find(e)]
    return val

taskdone = False
trial = 0

# 탐색 날짜 범위 (ex. days=1 : 1일 이내, 0:측정 시작순간 이후)
# 설정 날짜의 딱 자정으로 설정됩니다 (ex. 8.18 1:45AM -> 8.18 00:00AM)
drange = int('1')

fontpath='font.otf'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

# 갤러리ID
gid = 'baseball_new11'
filename = 'bb_new11_06'
start = '0'

if (start==''): i=0
else: i=int(start)


# 갤러리 링크
link = 'https://gall.dcinside.com/board/lists/?id=' + gid


ystday = (datetime.now() - timedelta(days=drange)).replace(hour=0, minute=0, second=0, microsecond=0)
print(ystday, '이후의 게시글을 수집합니다.')
        
taskdone = False
trial = 0

prev_num = 0

while not taskdone and trial < 10:

    # 마이너, 정식갤러리 판별
    r = requests.get('https://gall.dcinside.com/board/lists/?id=' + gid, headers = headers).text
    print('갤러리 형식:', end=' ')

    # 마이너 갤러리일 경우
    if 'location.replace' in r:
        link = link.replace('board/','mgallery/board/')    
        print('마이너')
    else:
        print('정식')

    data = 'Post ID\tTitle\tNickname(IP)\tDate\tViewcount\tUpvoteCount\n'
    fin = False
    r = None

    while not fin:
        time.sleep(0.5)
        
        i += 1
        print('===== 페이지 읽는 중... [{}번째...] ====='.format(i))#, end='\r')
        titleok = False

        while not titleok:
            r = requests.get(link + '&page=' + str(i), headers = headers).text
            bs = BeautifulSoup(r, 'lxml')

            posts = bs.find_all('tr', class_='ub-content us-post')

            for p in posts:
                title = p.find('td', class_='gall_tit ub-word')

                # 공지 제외 (볼드태그 찾을때 str 처리 해줘야 찾기가능)
                if not '<b>' in str(title):
                    titleok = True
                    pid = p.find("td", {"class", "gall_num"}).text.strip()
                    title = midReturn(str(title), '</em>', '</a>')
                    nick = p.find("td", {"class", "gall_writer ub-writer"}).text.strip()
                    date = datetime.strptime(p.find('td', class_='gall_date').get('title'), "%Y-%m-%d %H:%M:%S")
                   

                    # 이전 넘버링보다 현재 넘버링이 적을 경우에만 읽기
                    if prev_num > int(pid) or prev_num == 0:
                        
                        #초 단위까지는 안 가도록 함
                        if date >= ystday:
                            data += pid + "\t" + title + "\t" + nick  + "\n"
                        else:
                            ask = input('중지하시겠습니까? [Y/n]: ')
                            if ask == 'y' or ask == 'Y':
                                print('[NO]' + title)
                                print('기간 초과:', date)
                                fin = True
                                date = ystday
                                break
                            else:
                                data += pid + "\t" + title + "\t" + nick + "\n"

                        prev_num = int(pid)
                        
                    else:
                        print(pid + '\t올바르지 않은 글 넘버 - 무시하고 계속 읽습니다.')
                    
            if not titleok:
                print('게시글 크롤링 실패. 5초 후 다시 시도해 봅니다.')
                #i -= 1
                time.sleep(5)
                     

    print('저장 완료')
    taskdone = True


print("파일 쓰는 중...")
open(filename + '.tsv', 'w', encoding='utf-8-sig').write(data)
print("쓰기 완료.")