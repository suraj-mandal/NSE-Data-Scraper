from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def extract_row_data(row):
    row_contents = []
    for content in row:
        if content.findChildren(['a']):
            href_content = content.findChildren(['a'])[0]
            if href_content.findChildren(['b']):
                href_content = href_content.findChildren(['b'])[0]
            row_contents.append(href_content.decode_contents().strip())
        else:
            row_contents.append(content.decode_contents().strip())
    return row_contents

def extract_data(nse_webpage : BeautifulSoup):
    table = nse_webpage.find(lambda tag : tag.name=='table' and tag.has_attr('id') and tag['id']=='octable')
    if table:
        columns = table.findAllNext(lambda tag: tag.name=='th' and tag.has_attr('title'))
        columns = [column.decode_contents().replace('<br/>', ' ') for column in columns][1:-1]
        # now the next task is to retrieve the rows
        row_data = table.findChildren(['tr'])[2:-1]
        stock_df = pd.DataFrame(columns=columns)
        for idx, row in enumerate(row_data):
            stock_df.loc[idx] = extract_row_data(row.findChildren(['td'])[1:-1])
        stock_df.to_csv('results.csv', index=False)
    else:
        print('No columns available')


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe')

    url = 'https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=-10006&symbol=NIFTY&symbol=NIFTY&instrument=-&date=-&segmentLink=17&symbolCount=2&segmentLink=17'

    driver.get(url)
    results = driver.page_source
    soup = BeautifulSoup(results, 'html.parser')
    extract_data(soup)


    driver.close()



