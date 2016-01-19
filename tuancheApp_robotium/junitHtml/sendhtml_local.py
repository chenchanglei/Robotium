# coding=utf-8
'''
Created on 2014-01-13

@author: HuangHongTian
'''
import email,sys,codecs
import thread
from xml.dom.minidom import parse,parseString
import xml.etree.ElementTree as ET
from datetime import date,timedelta,datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP
from pyh import *
import MySQLdb
from datetime import date,timedelta,datetime


if sys.platform == "win32":
    localdir=r'D:\getapks\jUnitHtml\\'
else: 
    localdir='/xqa/junitHtml/'

#localdir='/xqa/junitHtml/'
#localdir='./'
vdate=date.today()
datestr=vdate.strftime('%Y-%m-%d')



def xml(xmf):
    allresult=[]
    
    #f=file('report3.xml')
    f=codecs.open(xmf,'r','utf-8')
    #dom1=parse('report.xml')
    tree=ET.parse(f)
    root=tree.getroot()
    
    for child in root:
        ts=[]
        #for tc in child.iter('testcase'): # only for python 2.7
        for tc in child.getiterator('testcase'):
            tcclass=tc.get('classname')
            tcname=tc.get('name')
            print tcclass
            print tcname
            print len(tc)
            if len(tc)==1:
                #print tc.find('failure').get('message')
                tr='failed'
            else:
                tr='passed'
            tc_result={'testcase':tcname,
                       'testclass':tcclass,
                       'testresult':tr
                       }
            ts.append(tc_result) #追加每个tc的结果到当前ts
        #print ts
        allresult.append(ts)#追加每个ts的结果到总的结果中
        
    #print allresult
    #print allresult[0]
    #print len(allresult)
    
    f.close()
    return allresult

def classlist(ts):
    clist=[]
    for i in range(len(ts)):
        clist.append(ts[i]['testclass'])
    
    cl=list(set(clist))
    
    #print cl
    return cl

def classstat(ts,testclass):
    passcount=0
    failcount=0
    for i in range(len(ts)):
        if ts[i]['testclass']==testclass:
            #统计passed和failed
            if ts[i]['testresult']=='passed':
                passcount+=1
            else:
                failcount+=1
    #print (passcount,failcount)
    cs={'total':str(passcount+failcount),
        'passcount':str(passcount),
        'failcount':str(failcount)
        }
    
    return cs
    
def resultstat(xmf):
    statrun={}
    
    Tresult=xml(xmf)
    #print tr
    Tpass=0
    Tfail=0
    tslen=len(Tresult)
    for i in range(tslen):
        for j in range(len(Tresult[i])):  
            #算总数
            if Tresult[i][j]['testresult']=='passed':
                Tpass+=1
            else:
                Tfail+=1

    statrun['passcount']=Tpass
    statrun['failcount']=Tfail
    statrun['total']=Tpass+Tfail
    statrun['ratio']=str(float(Tpass)/(Tpass+Tfail)*100)[:5]
    
    return statrun


def insert_autodb(xmf,job,product):
    lock = thread.allocate_lock()
    conn = MySQLdb.connect(host="192.168.36.55",user="xqa",
             passwd="xqa2014",db="dailyfb",charset="utf8")
    conn.ping(True)#保持数据库连接
    cursor = conn.cursor()
    conn.select_db('dailyfb')
    
    sql = "insert daily_autorun_stat (date,product,job,runtotal,passcount,failcount,ratio) values (%s,%s,%s,%s,%s,%s,%s)"
    stat=resultstat(xmf)
    param=(datestr,
           product,
           job,
           stat['total'],
           stat['passcount'],
           stat['failcount'],
           stat['ratio']
           )
    
    
    lock.acquire() #
    cursor.execute(sql,param)
    conn.commit()
    result=cursor.fetchall()
    lock.release()
    
    cursor.close()
    conn.close()
    

def createHTML():
    Tresult=xml(xmf)
    #print tr
    Tpass=0
    Tfail=0
    tslen=len(Tresult)
    for i in range(tslen):
        for j in range(len(Tresult[i])):  
            #算总数
            if Tresult[i][j]['testresult']=='passed':
                Tpass+=1
            else:
                Tfail+=1
    
    passratio=str(float(Tpass)/(Tpass+Tfail)*100)[:5]+'%'           
    page=PyH(projectjob+u"Robotium Daily Test Report")
    headfile=open(localdir+'head.txt','r')
    head=headfile.read()
    page << head
    div1= page<< div(cl='heading',id='div1')
    div1<<h1(projectjob+u' Daily Robotium Test Report')+p('<strong>Start Time:</strong> %s' %date.today())+p('<strong>Status:</strong> PASS %s Failed %s PASS Ratio: %s'  %(str(Tpass),str(Tfail),passratio))
    div1<<p('<strong>Details view:</strong> %s' %(buildlink))
    
    table1=page<< table(id='result_table')
    headtr=table1<< tr(id='head_row',bgcolor='#8B7D7B')
    headtr<< td('Test Group/Test case')+td('Total')+td('Passed')+td('Failed')
    totaltr=table1<< tr(id='totsl_row',bgcolor='#87CEEB')
    totaltr<< td('<strong>Summary </strong>')+td('%s'%str(Tpass+Tfail))+td('%s'%str(Tpass))+td('%s'%str(Tfail))

    for i in range(tslen):
        #print Tresult[i]
        clist=classlist(Tresult[i])
        
        for testclass in clist: #每个测试测试类
            classtr= table1 << tr(id='failclass',bgcolor='#FFE4B5')
            classtr<<td('%s' %testclass)
            cstat=classstat(Tresult[i],testclass)
            #print cstat
            
            classtr<<td('%s' %cstat['total'])      
            classtr<<td('%s' %cstat['passcount'])
            classtr<<td('%s' %cstat['failcount'])
            
            for j in range(len(Tresult[i])):
                if Tresult[i][j]['testclass']==testclass:
                     ##显示testcase名和测试结果
                    tctr=classtr<<tr(id='pt1.1',bgcolor='#ADD8E6')
                    tctr<<ul(id='testcase')
                    tctr<<td(id='none')<<div(id='testcase')<<p('%s' %Tresult[i][j]['testcase'])
                    tctr<<td(id='none',colspan='5',align='center')<<div(id='testcase')<<p('%s' %Tresult[i][j]['testresult'])
                
    #page.printOut()
    
    return page
     
    
def sendmail(maillist):
    
    SMTPserver = 'smtp.gmail.com'
    sender =     'QA_NqmsFeedBack@nq.com'
    destination =maillist.split(',')
    #destination = ['huanghongtian@nq.com']
    #destination = ['huanghongtian@nq.com','jiakui@nq.com','liujia@nq.com','xiangmingxin@nq.com','weixia@nq.com','zhaojie@nq.com','zhaolei@nq.com','leixin@nq.com','yehang@nq.com','heyongliang@nq.com','chengping@nq.com','wangwei@nq.com','liangtao@nq.com','wangxiaolan@nq.com','taoli@nq.com','zhaozheng@nq.com','chenglin@nq.com']
    USERNAME = "QA_NqmsFeedBack@nq.com"
    PASSWORD = "AVNQtypx33"
    
    # typical values for text_subtype are plain, html, xml
    
    #text_subtype = 'plain'
    text_subtype = 'html'
    
    #line1=PyH('my page')
    
    page=createHTML()
    page.printOut(temphtml)
    
    #page.printOut()
    
    print "OKo"
    f=open(temphtml,'rb')
    content=f.read()
    subject=projectjob+u'每日自动化测试报告'+datestr
    f.close()

    try:
        #msg=MIMEText(content, 'html', 'utf-8')
        msg = MIMEText(content, text_subtype,'utf-8')
        msg['Subject']=subject
        msg['From']=sender # some SMTP servers will do this automatically, not all
        msg['To']=','.join(destination)
        
        conn = SMTP(SMTPserver,'465')
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        
        try:
            #pass
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.close()
    except Exception, exc:
        print exc

        
if __name__ == "__main__":

    xmf='report.xml'
    try:
        xml(xmf)
    except Exception,e:
        print e
    
    
    print "testdone"
    #xml()
    #createHTML()