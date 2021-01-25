from bs4 import BeautifulSoup
from selenium import webdriver
import time
from module_v2 import solve_nonogram as s_n

hint = [[], []]

url = input("url : ")
# url = 'http://nemonemologic.com/play_logic.php?quid=8952&page=0&size=-1'
driver = webdriver.Chrome('D:/temp/chromedriver.exe')
driver.get(url)
time.sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 세로 힌트 추출
col_hints = soup.find(class_="nemo-v-hint")
for i in col_hints:
    col_hint = i.find_all(class_="hint-num")
    temp = []
    for j in col_hint:
        temp.append(int(j.text))
    hint[0].append(temp)
del hint[0][0]

# 가로 힌트 추출
row_hints = soup.find_all(
        class_="nemo-h-hint nemo-box-r-guard nemo-curlineable")
for i in row_hints:
    row_hint = i.find_all(class_='hint-num')
    temp = []
    for j in row_hint:
        temp.append(int(j.text))
    hint[1].append(temp)

# driver.close()

# 길이 파악
N = len(hint[0])

# nonogram Solve
board, cnt = s_n(N, hint, url)

# 다 풀면 클릭
for i in range(N):
    for j in range(N):
        if board[i][j] == 1:
            click = driver.find_element_by_xpath(
                                    "//td[@id='nemo-box-{}']".format(i*N+j))
            click.click()

if cnt < 101:
    if N == 5:
        f = open("./hints/5x5.txt", 'a')
        f.write(str(hint)+'\n')
        f.close
    elif N == 10:
        f = open("./hints/10x10.txt", 'a')
        f.write(str(hint)+'\n')
        f.close
    elif N == 15:
        f = open("./hints/15x15.txt", 'a')
        f.write(str(hint)+'\n')
        f.close
    elif N == 20:
        f = open("./hints/20x20.txt", 'a')
        f.write(str(hint)+'\n')
        f.close
    elif N == 25:
        f = open("./hints/25x25.txt", 'a')
        f.write(str(hint)+'\n')
        f.close
    elif N == 30:
        f = open("./hints/30x30.txt", 'a')
        f.write(str(hint)+'\n')
        f.close
