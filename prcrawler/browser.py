# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 01:30:27 2019

@author: T430
"""

import sys, time
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl


class WebpageClient(QWebEnginePage):
    
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        print(' on load pausing 10...')
        time.sleep(10)
        print(' done pausing.')
        self.html = self.toHtml(self.Callable)
        print(self)
        print(' [Load finished]')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


#def main():
#    url = 'https://mediaroom.sanofi.com/en/press-releases/'
##    pr_list_class = 'osw-pagelist-container-content-middle'
##    pr_item_class = 'osw-pagelist-icon osw-pagelist-icon-circle osw-pagelist-icon-download'
#    page = WebpageClient(url)
#    soup = bs.BeautifulSoup(page.html, 'html.parser')
##    js_test = soup.find('a')
#    js_test = soup.select('a[aria-label="Download"]')
#    hrefs = [x.attrs['href'] for x in js_test]
#    response = requests.get(hrefs[0])
#    response.content
##    print(js_test)
#    print([x.attrs['href'] for x in js_test])


#if __name__ == '__main__': main()

