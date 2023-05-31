from selenium import  webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import datetime
import time
import json
def pachong():
    crossTime=2
    data= {}
    buildingList={2:"文萃楼",3:"综合教学楼A",7:"综合教学楼B",10:"理科教学楼"}
    buildingIndex=[2,3,7,10]
    ID="1120201961"
    passWord="LPJssd!hhd!LACc0"
    for index in buildingIndex:#选择教室
        #设置虚拟浏览器属性
        browser = webdriver.Chrome()
        browser.get('http://jxzxehallapp.bit.edu.cn/jwapp/sys/kxjas/*default/index.do?t_s=1684396131471&amp_sec_version_=1&gid_=cTFUaVliWGltaU9UYWxVenFSR0JHMTg5OXZxL3lQSGVUUiswSFlxS2djcDNldWtWR2FSSnQyMVlmOU9sQ3ozU09UOXpOK2svM05lOTVqUUtlUlpXdlE9PQ&EMAP_LANG=zh&THEME=cherry#/kxjas')
        #登陆
        name=browser.find_element(By.ID,'username')
        password=browser.find_element(By.ID,'password')
        loginButton=browser.find_element(By.ID,'login_submit')
        name.send_keys(ID)
        password.send_keys(passWord)
        loginButton.click()
        browser.implicitly_wait(11)
        time.sleep(5)
        #选择良乡校区
        chose_school=browser.find_element(By.CSS_SELECTOR,"#kxjas-index-search > div.bh-advancedQuery.bh-mb-16 > div.bh-advancedQuery-quick > div.bh-advancedQuery-form > div > div > div.bh-clearfix.bh-advancedQuery-groupList.bh-label-radio-group > div > div:nth-child(4)")
        chose_school.click()
        time.sleep(0.5)
        data={}
        data[index]= {}
        selector="#kxjas-index-card > div > div.bh-emapCard-card-list > div > div:nth-child(" + str(index) + ") > div.sc-panel-user-1-container.bh-animate-all.bh-animate-fast > div.sc-panel-user-1-operate.bh-animate-bottom.bh-animate-fast > span"
        buildings=browser.find_element(By.CSS_SELECTOR,selector)
        ActionChains(browser).move_to_element(buildings).perform()
        time.sleep(0.2)
        buildings.click()
        date = datetime.date.today()  # 现在的时间
        for add_time in range(0, crossTime):#遍历cross_time的课表

            dateSelectionObject=browser.find_element(By.CSS_SELECTOR, "#inputselectDate")
            dateSelectionObject.clear()

            searchTime=str(date + datetime.timedelta(days=+add_time))
            print(searchTime)
            dateSelectionObject.send_keys(searchTime)
            searchButton=browser.find_element(By.CSS_SELECTOR, "#kxjasxqcx")
            searchButton.click()
            browser.implicitly_wait(11)

            data[index][searchTime]={}

            #获得一些基本的信息
            #页数
            objectOfPages=browser.find_element(By.CSS_SELECTOR, "#toppager > div > div > div.bh-pull-left > span.bh-pager-no")
            numberOfPages=int(objectOfPages.get_attribute('innerHTML').split(' ')[-1])
            #总教室数
            objectOfNumberOfClassrooms=browser.find_element(By.CSS_SELECTOR, "#pagerkxjascx-index-table > div > div > div.bh-pull-left > span.bh-pager-num")
            totalNumberOfClassrooms=int(objectOfNumberOfClassrooms.get_attribute('innerHTML').split(' ')[-1])

            print(searchTime)
            #遍历每一栋教学楼的教室
            for j in range(1,numberOfPages+1):
                #等待加载
                time.sleep(1.5)

                for indexOfPage in range(0, 10):

                    totalNumberOfClassrooms-=1  #遍历教室数
                    if totalNumberOfClassrooms<0:
                        browser.implicitly_wait(11)
                        continue

                    classroomParameters= "#row" + str(indexOfPage) + "kxjascx-index-table"
                    classroomOccupancyObject=browser.find_element(By.CSS_SELECTOR, classroomParameters)
                    basicClassroomInformation=classroomOccupancyObject.text.split(" ")#教室所在位置，教室容纳人数，教室类型
                    className=basicClassroomInformation[0]
                    data[index][searchTime][className]=[]
                    for i in basicClassroomInformation:
                        data[index][searchTime][className].append(str(i))
                    print("get "+className)
                    classTime=5
                    while classTime<10:
                        selector="#row"+str(indexOfPage)+"kxjascx-index-table > td:nth-child("+str(classTime)+")"
                        try:
                            courseOccupancyObject= browser.find_element(By.CSS_SELECTOR,selector)
                            classTime+=1
                            if courseOccupancyObject.get_attribute("innerHTML") == '<span></span>' or courseOccupancyObject.get_attribute("innerHTML") == '':
                                data[index][searchTime][basicClassroomInformation[0]].append("free")
                            else:
                                data[index][searchTime][basicClassroomInformation[0]].append("occupied")
                        except StaleElementReferenceException:
                            classTime-=1

                desPage = browser.find_element(By.CSS_SELECTOR,"#pagerkxjascx-index-table > div > div > div.bh-pull-left > a:nth-child(3) > i")
                desPage.click()
                browser.implicitly_wait(11)

            time.sleep(1)

        jsons=json.dumps(data, ensure_ascii=False, indent=2)
        f2 = open(buildingList[index]+'.json', 'w')
        f2.write(jsons)
        f2.close()
        browser.close()
