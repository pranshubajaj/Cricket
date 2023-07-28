from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests 
from bs4 import BeautifulSoup
from termcolor import colored


# retrieves the heading of the match
def overview():
    URL = "https://www.cricbuzz.com"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find_all('li', attrs = {'class': 'cb-view-all-ga cb-match-card cb-bg-white'})
    # replace this with the team initials eg. IND for India
    pref = 'SL'
    
    for li in table:
        match = li.text.strip()
        if(match.count(pref)>0):
            print(colored(match, 'green'))
            link = li.find('a', attrs = {'title': 'Sri Lanka v Pakistan - 2nd Test'})
            print('\n')
            return link['href'], match


# retrieves the scorecard of the same match
def fetch_details(link):
    URL = link
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    stats = soup.find('div', attrs = {'class': 'cb-col-67 cb-col'})
    scores = stats.find_all('div')
    table = []
    cnt = 0
    row = {}
    for s in scores:
        if(cnt%6==0 and len(row)):
            table.append(row)
            row = {}
        if(len(s.find_all('div'))==0):
            cnt+=1
            row[(cnt-1)%6]=s.text.strip()
    table.append(row)
    return table



# sends the message to the contact via WhatsApp
def send_message(name, mes, driver):
    try:     
    # Find Whom to message     
    # user = driver.find_element("x_path",'//span[@title = "{}"]'.format(name))
    # user.click()
        user = driver.find_element(By.XPATH,'//span[@title = "{}"]'.format(name))
        user.click()

        msg_bar = driver.find_element(By.CLASS_NAME,'_3Uu1_')
        msgs = mes.split('\n')
        for m in msgs:
            msg_bar.send_keys(m)
            msg_bar.send_keys(Keys.SHIFT + Keys.ENTER)
            msg_bar.send_keys(Keys.SHIFT + Keys.ENTER)
        msg_bar.send_keys(Keys.ENTER)
        return 'Scorecard Sent Successfully'
    except Exception as e:
        print('Error: ', e)
        return 'Error While Sending Scorecard'
    


# replace this with the location of your driver
browser = webdriver.Chrome(executable_path="chromedriver")

URL = 'https://web.whatsapp.com/'
browser.get(URL)
time.sleep(20)
batter = False
while(1):
    message = ''
    det, scores = overview()
    message += scores
    table = fetch_details('https://www.cricbuzz.com' + det)
    for row in table:
        if(row[0]=='Batsman' or row[0]=='Bowler'):
            print(colored("{:<24} {:<8} {:<8} {:<8} {:<8} {:<8}".format(row[0], row[1], row[2], row[3], row[4], row[5]), 'cyan', attrs=['bold']))
            batter = not batter
        else:
            print(colored("{:<24} {:<8} {:<8} {:<8} {:<8} {:<8}".format(row[0], row[1], row[2], row[3], row[4], row[5]), 'white'))
            if(batter):
                msg = '\n'+row[0]+':  '+row[1]+'('+row[2]+')'+'  '+'S.R. '+row[5]
                message += msg
            else:
                msg = '\n'+row[0]+':  '+row[1]+'-'+row[2]+'-'+row[3]+'-'+row[4]
                message += msg

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    message += ('\nThis is the latest score updated at: ' + current_time)
    print(colored("\nTime Stamp: " + current_time + "\n", 'red'))
    time.sleep(30)
    # replace this with the name of the contact you want to send the scorecard to
    send_message('S', message, browser)

    # time.sleep(30)




# batter = False
# message = ''
# det, scores = overview()
# message += scores
# table = fetch_details('https://www.cricbuzz.com' + det)
# for row in table:
#     if(row[0]=='Batter' or row[0]=='Bowler'):
#         print(colored("{:<24} {:<8} {:<8} {:<8} {:<8} {:<8}".format(row[0], row[1], row[2], row[3], row[4], row[5]), 'cyan', attrs=['bold']))
#         batter = not batter
#     else:
#         print(colored("{:<24} {:<8} {:<8} {:<8} {:<8} {:<8}".format(row[0], row[1], row[2], row[3], row[4], row[5]), 'white'))
#         if(batter):
#             msg = '\n'+row[0]+':  '+row[1]+'('+row[2]+')'+'  '+'S.R. '+row[5]
#             message += msg
#         else:
#             msg = '\n'+row[0]+':  '+row[1]+'-'+row[2]+'-'+row[3]+'-'+row[4]
#             message += msg





