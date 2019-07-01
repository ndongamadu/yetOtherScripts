import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
country = 'mozambique'
#somalia = "http://www.ipcinfo.org/ipc-country-analysis/details-map/en/c/1151962/"
moz = "http://www.ipcinfo.org/ipc-country-analysis/details-map/en/c/1151806/"
#drc = "http://www.ipcinfo.org/ipc-country-analysis/details-map/en/c/1151753/"
#caf = "http://www.ipcinfo.org/ipc-country-analysis/details-map/en/c/1151724/"
#yem = "http://www.ipcinfo.org/ipc-country-analysis/details-map/en/c/1151858/"

drv = "/Users/amadu/.wdm/chromedriver/74.0.3729.6/mac64/chromedriver"
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(drv)
driver.get(moz)
driver.find_element_by_id('poestab').click()
# time.sleep(10)
# driver.switch_to.frame(driver.findElements(By.tagName("iframe"))).get(0)
driver.switch_to.frame(2)
page_source = driver.page_source
soupe = BeautifulSoup(page_source, 'lxml')
tab = soupe.find('table', id='population_data_3')

rows = tab.findAll('tr')
nbRows = 0

with open('%s-ipcData.csv' % country, 'w') as file:
    writer = csv.writer(file, delimiter=',')
    for r in rows:
        currentCell = r.findAll('td')
        data = []
        for c in currentCell:
            print("nouvelle ligne")
            print(c)
            print("====")
            data.append(c.get_text())

        if nbRows == 0:
            # writer.writerow(data)
            nbRows += 1
            # add hxl tags
        else:
            writer.writerow(data)
print("====table content===")
# print(tab)
