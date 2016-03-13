from selenium import webdriver
path = 'C:/Users/tho/Desktop/Python/Web Scraping/phantomjs-2.0.0-windows/bin/phantomjs.exe'

#browser = webdriver.PhantomJS(executable_path= path)
browser = webdriver.Chrome()
browser.get('http://localhost:8000')

assert 'Django' in browser.title