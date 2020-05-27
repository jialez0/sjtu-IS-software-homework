# -*- coding: utf-8 -*-
import uuid
from flask import Flask, jsonify, request
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask import Flask
#from flask_cors import CORS
import json
from flask_cors import *
import pymysql
import datetime
from sqlalchemy import func


def getday_in_int():
    current_time = datetime.datetime.now()
    day = current_time.strftime("%Y%m%d")
    return day

def gettime_in_int():
    current_time = datetime.datetime.now()
    time = current_time.strftime("%H%M")
    return time



BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

app.config['SECRET_KEY'] ='123456'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123456@127.0.0.1:3306/managesystem'
#设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
#实例化
db = SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

import contextlib
#定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', passwd='123456', db='managesystem',charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset,autocommit=True)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
    cursor.close()
    conn.close()

class RegInfo(db.Model):
    __tablename__ = 'registration_information'
    ID_person = db.Column(db.Integer, primary_key=True,nullable=False)
    name = db.Column(db.String(50))
    status = db.Column(db.String(50))
    age = db.Column(db.Integer)
    date_register = db.Column(db.Integer)
    time_register = db.Column(db.Integer)
    password = db.Column(db.String(50))
    def __repr__(self):
        return '<RegInfo {}>'.format(self.ID_person)


class LocCurr(db.Model):
    __tablename__ = 'location_current'
    ID_visit = db.Column(db.Integer, primary_key=True,nullable=False)
    ID_person = db.Column(db.Integer, db.ForeignKey(RegInfo.ID_person))
    longitude_current = db.Column(db.Float)
    latitude_current = db.Column(db.Float)
    date_current = db.Column(db.Integer)
    time_current = db.Column(db.Integer)
    date_start = db.Column(db.Integer)
    time_start = db.Column(db.Integer)
    time_stay = db.Column(db.Integer)
    def __repr__(self):
        return '<RegInfo {}>'.format(self.ID_visit)

class LocHist(db.Model):
    __tablename__ = 'location_history'
    ID_history = db.Column(db.Integer, primary_key=True,nullable=False)
    ID_visit = db.Column(db.Integer, db.ForeignKey(LocCurr.ID_visit))
    ID_person = db.Column(db.Integer, db.ForeignKey(RegInfo.ID_person))
    longitude_history = db.Column(db.Float)
    latitude_history = db.Column(db.Float)
    date_history = db.Column(db.Integer)
    time_history = db.Column(db.Integer)
    flag = db.Column(db.String(20))
    def __repr__(self):
        return '<RegInfo {}>'.format(self.ID_history)


class TimeAlloc(db.Model):
    __tablename__ = 'time_allocation'
    ID_time = db.Column(db.Integer, primary_key=True,nullable=False)
    ID_visit = db.Column(db.Integer, db.ForeignKey(LocCurr.ID_visit))
    time_stay = db.Column(db.Integer)
    date_time = db.Column(db.Integer)
    def __repr__(self):
        return '<RegInfo {}>'.format(self.ID_time)



def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })



        #conn = pymysql.connect(host='127.0.0.1', port=3306,user='root', passwd='123456', db='managesystem',charset='utf8')
        #cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        #sql = "INSERT INTO managesystem.time_allocation (ID_time, ID_visit, time_stay, date_time) VALUES (9,1,1,20000000)"
        #try:
        #    row_counts=cursor.execute(sql)
        #except:
        #    print("add item fail")
        #conn.commit()
        #cursor.close()
        #conn.close()

        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


def register(name,status,age,password,date_register=getday_in_int(),time_register=gettime_in_int()):
    if (RegInfo.query.filter_by(name=name).count()>0):
        return (False,"name already registered")
    new_user = RegInfo(name=name,status=status,age=age,date_register=date_register,time_register=time_register,password=password)
    try:
        db.session.add_all([new_user])
        db.session.commit()
        return (True,new_user)
    except:
        return (False,"register failed")

def checkUser(name):
    if (RegInfo.query.filter_by(name=name).count()>1):
        print("alert! more than 1 users match this name, choose the first one")
    if (RegInfo.query.filter_by(name=name).count()==0):
        return(False,"no this user")
    user = RegInfo.query.filter_by(name=name).first()
    return (True, user)

def login(name,status='访客',age=0,password='123456'):
    res1=checkUser(name)
    if (res1[0]==False):#用户不存在
        res = register(name,status=status,age=age,password=password)
        if (res[0] == True):
            return (True,res[1].ID_person)
        else:
            return (False,"login error")
    else:
        a = (password == res1[1].password)
        b = (status == res1[1].status)
        if a and b:
            return (True,res1[1].ID_person)
        elif (not a):
            return (False,"password error")
        else:
            return (False,"status error")

def endVisitByName(name,longitude_current=121.426365,\
                   latitude_current=31.01966,date_current=getday_in_int(),time_current=gettime_in_int()):
    if(RegInfo.query.filter_by(name=name).count()!=1):
        return (False,"no such name")
    thisID = RegInfo.query.filter_by(name=name).first().ID_person
    return(endVisit(thisID,longitude_current=longitude_current,latitude_current=latitude_current,\
                    date_current=date_current,time_current=time_current))

def endVisit(ID_person,longitude_current=121.426365,\
                   latitude_current=31.01966,date_current=getday_in_int(),time_current=gettime_in_int()):
    if(RegInfo.query.filter_by(ID_person=ID_person).count()!=1):
        return (False,"no visit now")
    if (RegInfo.query.filter_by(ID_person=ID_person).first().status!='访客'):
        return (False,"this is not a visitor")
    try:
        ID_visit = LocCurr.query.filter_by(ID_person=ID_person).first().ID_visit
        time = LocCurr.query.filter_by(ID_person=ID_person).first().time_stay
        res = LocCurr.query.filter_by(ID_person=ID_person).delete()
        db.session.commit()
        res2 = recordVisit(ID_visit=ID_visit,ID_person=ID_person,longitude_current=longitude_current,latitude_current=latitude_current,\
                    date_current=date_current,time_current=time_current,flag='离开')
        res3 = (showTimeStay(ID_visit)[-1] > time)
        if (res==1 and res2[0] == True):
            if (res3):
                return (True,"delete success, but stay longer than allocation")
            else:
                return (True,"delete success")
        else:
            return (False,"delete failed")
    except:
        return(False,"no such ID_person")

def startVisitByName(name,longitude_current=121.426365,\
                   latitude_current=31.01966,time_stay=300,date_current=getday_in_int(),time_current=gettime_in_int(),\
               date_start=getday_in_int(),time_start=gettime_in_int()):
    if(RegInfo.query.filter_by(name=name).count()!=1):
        return (False,"no such name")
    thisID = RegInfo.query.filter_by(name=name).first().ID_person
    return startVisit(thisID,longitude_current,latitude_current,time_stay,date_current,time_current,date_start,time_start)


def startVisit(ID_person,longitude_current='121.426365',\
                   latitude_current='31.01966',time_stay=300,date_current=getday_in_int(),time_current=gettime_in_int(),\
               date_start=getday_in_int(),time_start=gettime_in_int()):
    '''
    默认是思源门地址，3h
    '''

    if(LocCurr.query.filter_by(ID_person=ID_person).count()>0):
        return (False,"this ID is still in visit time")
    else:
        res = RegInfo.query.filter_by(ID_person=ID_person).first()
        if(res.status!='访客'):
            return(False,"this is not a visitor")
        new_user = LocCurr(ID_person=ID_person,longitude_current=longitude_current,\
                   latitude_current=latitude_current,date_current=date_current,time_current=time_current,\
               date_start=date_start,time_start=time_start,time_stay=time_stay)
        #try:
        db.session.add_all([new_user])
        db.session.commit()
        res = recordVisit(ID_visit=new_user.ID_visit,ID_person=ID_person,longitude_current=longitude_current,\
            latitude_current=latitude_current,date_current=date_current,time_current=time_current,flag='进入')
        res2 = newTimeAlloc(ID_visit=new_user.ID_visit,time_stay=time_stay,date_time=date_current)
        if (res[0] == True and res2[0] == True):
            return (True,"new visit start")
        else:
            return (False,"record failed")
        #except:
            #return (False,"start new visit failed")

def updateVisitLocation(ID_person,longitude_current=121.426365,\
                   latitude_current=31.01966,date_current=getday_in_int(),time_current=gettime_in_int()):
    if(LocCurr.query.filter_by(ID_person=ID_person).count()!=1):
        return (False,"no visit now")
    currentuser = LocCurr.query.filter_by(ID_person=ID_person).first()
    currentuser.longitude_current=longitude_current
    currentuser.latitude_current=latitude_current
    currentuser.date_current=date_current
    currentuser.time_current=time_current
    fulltime = int(currentuser.time_stay/100)*60+currentuser.time_stay%100
    minnow = int(int(time_current)/100)*60+int(time_current)%100
    minin = int(currentuser.time_start/100)*60+currentuser.time_start%100
    minleft = fulltime - (minnow-minin)
    '''
    if(TimeAlloc.query.filter_by(ID_visit=currentuser.ID_visit).count()!=1):
        return (False,"no time allocation")
    fulltime = str(TimeAlloc.query.filter_by(ID_visit=currentuser.ID_visit).first().time_stay)
    fulltime = datetime.datetime.strptime(fulltime,"%H%M")
    ds = str(currentuser.date_start) +' ' + str(currentuser.time_start)
    ds = datetime.datetime.strptime(ds,"%Y%m%d %H%M")
    dn = str(date_current) + ' ' + str(time_current)
    dn = datetime.datetime.strptime(dn,"%Y%m%d %H%M")
    timeused = dn-ds
    timeleft = fulltime - timeused
    flag = timeleft.strftime("d")
    currentuser.time_stay = timeleft.strftime("%H%M")
    if(flag>1):
        currentuser.time_stay = 0
        '''
    try:
        db.session.commit()
        res = recordVisit(ID_visit=currentuser.ID_visit,ID_person=ID_person,longitude_current=longitude_current,latitude_current=latitude_current,\
                    date_current=date_current,time_current=time_current,flag='逗留')
        if (res[0] == True ):#and flag==0
            return(True,"update successfully",minleft)
        #elif (flag>1):
        #    return(True,"but time is running out")
        else:
            return(False,"record failed")
    except:
        return(False,"update failed")

def recordVisit(ID_visit,ID_person,longitude_current='121.426365',\
                   latitude_current='31.01966',date_current=getday_in_int(),time_current=gettime_in_int(),flag='逗留'):
    #if(LocCurr.query.filter_by(ID_person=ID_person).count()!=1):
    #    return(False,"no this visitor")
    #visitid = LocCurr.query.filter_by(ID_person=ID_person).first().ID_visit
    loc = LocHist(ID_visit=ID_visit,ID_person=ID_person,longitude_history=longitude_current,latitude_history=latitude_current,\
            date_history=date_current,time_history=time_current,flag=flag)
    #try:
    db.session.add_all([loc])
    db.session.commit()
    return (True,"record success")
    #except:
    #    return (False,"record failed")

def newTimeAlloc(ID_visit,time_stay=300,date_time=getday_in_int()):
    if (TimeAlloc.query.filter_by(ID_visit=ID_visit).count()>0):
        return (False,"already allocate time")
    ta = TimeAlloc(ID_visit=ID_visit,time_stay=time_stay,date_time=date_time)
    try:
        db.session.add_all([ta])
        db.session.commit()
        return (True,"new time allocation successfully")
    except:
        return (False,"new time allocation  failed")

def addTimeAlloc(ID_visit,time_add=300):
    if (TimeAlloc.query.filter_by(ID_visit=ID_visit).count()!=1):
        return (False,"no value")
    ta = TimeAlloc.query.filter_by(ID_visit=ID_visit).first()
    hours = int(time_add/100) + int(ta.time_stay/100)
    minutes = time_add%100 + ta.time_stay%100
    if(minutes>=60):
        hours=hours+1
        minutes=minutes-60
    ta.time_stay = hours*100+minutes
    tv = LocCurr.query.filter_by(ID_visit=ID_visit).first()
    tv.time_stay = ta.time_stay

    try:
        db.session.commit()
        return (True,"update successfully")
    except:
        return (False,"update time allocation failed")

def addTimeAllocByID(ID_person,time_add=300):
    idvisit=LocCurr.query.filter_by(ID_person=ID_person).first().ID_visit
    return (addTimeAlloc(idvisit,time_add))

def showVisitorNow():
    return LocCurr.query.all()

def showCountToday():
    sql = 'SELECT count(*) FROM managesystem.location_history where date_history='+getday_in_int()+' group by ID_visit'
    cursor = db.session.execute(sql)
    result = cursor.fetchall()
    return len(result)

def showCountInOnePlaceNow(longitude_low,longitude_high,latitude_low,latitude_high):
    return LocCurr.query.filter(and_(LocCurr.longitude_current.between(longitude_low,longitude_high),\
                                   LocCurr.latitude_current.between(latitude_low,latitude_high))).count()

def showCountInOnePlace(longitude_low,longitude_high,latitude_low,latitude_high,date=getday_in_int()):
    sql = 'SELECT count(*) FROM managesystem.location_history where date_history='+date\
          +' and longitude_history between '+str(longitude_low)+' and '+str(longitude_high)+' and latitude_history between '\
          +str(latitude_low)+' and '+str(latitude_high)+' group by ID_visit'
    cursor = db.session.execute(sql)
    result = cursor.fetchall()
    return len(result)

def showTimeStay(ID_visit,date=getday_in_int()):
    getins = LocHist.query.filter(and_(LocHist.date_history==date,LocHist.flag=='进入',LocHist.ID_visit==ID_visit)).all()
    getouts = LocHist.query.filter(and_(LocHist.date_history==date,LocHist.flag=='离开',LocHist.ID_visit==ID_visit)).all()
    ts=[]
    for i in range(len(getouts)):
        intime = str(getins[i].time_history)
        outtime = str(getouts[i].time_history)
        timestay = datetime.datetime.strptime(outtime,"%H%M")-datetime.datetime.strptime(intime,"%H%M")
        seconds=timestay.total_seconds()
        minutes = int(seconds/60)
        hours = int(minutes/60)
        mins = minutes%60
        ts.append(hours*100+mins)
    return(ts)

def showTimeAlloc(date=getday_in_int()):
    return TimeAlloc.query.filter(TimeAlloc.date_time==date).all()

if __name__ == '__main__':
    print(getday_in_int())
    print(gettime_in_int())
    '''
    print(login(name='梁力佳',status='保卫处',password='123456'))
    print(login('张家乐',status='保卫处',password='123456'))
    print(login('张西珩',status='门卫',password='123456'))
    print(login('魏上清'))
    print(login('陆天和'))
    print(login('谢禹翀'))
    print(login('访客甲'))
    print(login('访客乙'))
    print(login('门卫甲',status='门卫',password='123456'))
    print(login('访客丙',password='123456'))
    '''


    #print(showCountInOnePlace(120,130,20,40))
    #print(showCountInOnePlace(120,130,20,33))
    #print(showCountInOnePlaceNow(120,130,20,33))
    #print(endVisit(6))
    #print(updateVisitLocation(5,121.4271,31.0144))
    #print(updateVisitLocation(6,121.4217,31.0349))
    #print(startVisit(5,121.4405,31.0249,100))
    #print(startVisitByName('谢禹翀',121.4405,31.0249,130))
    #print(startVisit('4','121.42078','31.030427',time_stay='400'))
    #print(endVisit('5',time_current=2100))

    #print(endVisit('4'))
    #print(endVisit('5'))
    #print((endVisitByName('魏上清')))
    #print(addTimeAllocByID(4,40))


    #app.run()
