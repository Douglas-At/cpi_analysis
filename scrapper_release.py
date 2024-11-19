import pandas as pd
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.bls.gov/news.release/cpi.htm")
html = driver.page_source
df = pd.read_html(html,attrs = {'id': 'cpipress2'})[0].iloc[:-1,:]
df.to_excel('CPI_NEWS_RELEASE.xlsx')

