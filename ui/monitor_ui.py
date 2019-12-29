import sys,requests,time,json
from PyQt5.QtWidgets import QApplication,QMainWindow
from monitor import Ui_mainWin
from visualization import *
from threading import Thread
from multiprocessing import Process
from mat_visual import test_visual,show_visual,draw_individual

class MyMainWindow(QMainWindow,Ui_mainWin):
    def __init__(self,parent=None,rest_url=None,datapath=None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.rest_url=rest_url
        self.datapath=datapath
        self.Data=Data(rest_url)
        self.textBrowsers=[]
        self.overall_result=[]
        for i in range(5):
            self.textBrowsers.append(eval('self.textBrowser_'+str(i+1)))
        #self.Data.update()
        #time.sleep(1)
        # self.update_data()
        # self.show_1.clicked.connect(self.show_factory(0))
        # self.show_2.clicked.connect(self.show_factory(1))
        # self.show_3.clicked.connect(self.show_factory(2))
        # self.show_4.clicked.connect(self.show_factory(3))
        # self.show_5.clicked.connect(self.show_factory(4))
        self.connect.clicked.connect(self.update_data)

    def show_factory(self,d_index):
        index=d_index
        ds=json.loads(self.Data.data)
        #print(ds[index])
        d=ds[index]
        def test():
            return draw_individual(d,450)
        
        return test

    def update_data(self):
        self.Data.update()
        d=json.loads(self.Data.data)
        print(self.Data.overall)
        ad=json.loads(self.Data.overall)

        for i in range(5):
            print(d[i])
            t=''
            for key,value in d[i].items():
                tmp=';    ' if key !='fitness' else '\n'
                t+="{k}:{v}{tmp}".format(k=key,v=value,tmp=tmp)
            self.textBrowsers[i].setHtml(t)
            #cursor = self.textBrowsers[i].textCursor()
            #self.textBrowsers[i].moveCursor(cursor.Start)
        print("AD",ad)
        self.totaltimecost.setText(str(ad['ttc']))
        self.population.setText(str(ad['popu']))
        self.bestfitness.setText(str(ad['best']))
        self.bestsolution.setText(str(ad['bestsolution']))
        
        self.show_1.clicked.connect(self.show_factory(0))
        self.show_2.clicked.connect(self.show_factory(1))
        self.show_3.clicked.connect(self.show_factory(2))
        self.show_4.clicked.connect(self.show_factory(3))
        self.show_5.clicked.connect(self.show_factory(4))
        #self.update()
        #self.processEvents()
        self.totaltimecost.resize(0,0)
        self.population.resize(0,0)
        self.bestfitness.resize(0,0)
        self.bestsolution.resize(0,0)
        

class UI_server:
    def __init__(self,rest_url):
        self.window=MyMainWindow(rest_url=rest_url)


class Data:
    def __init__(self,url):
        self.url=url
        self.data=[]
        self.overall=[]
    
    def update(self):
        query_api='query'
        overall_api='overall'
        self.data=requests.get(self.url+query_api).text
        self.overall=requests.get(self.url+overall_api).text
        #print(self.data)
        #print(self.data)
        return


if __name__ == '__main__':
    app=QApplication(sys.argv)
    myWin=MyMainWindow(rest_url='http://127.0.0.1:5000/')
    myWin.show()
    sys.exit(app.exec_())
