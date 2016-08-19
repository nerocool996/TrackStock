from flask import Flask, render_template, request, redirect, url_for,flash, jsonify
app = Flask(__name__)
from flask import session as login_session
import random,string
from sqlalchemy import create_engine,desc,func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Stock, User
import datetime
import httplib2,urllib
import json
from flask import make_response
import requests

##CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']

engine = create_engine('sqlite:///stock.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def main():
    	if 'username' not in login_session:
         	user = None
        else:
            user = session.query(User).filter_by(name = login_session['username']).one()
	return render_template('main.html')

@app.route('/getData')
def getData():
    lables = [];
    for i in range(0, 20):
        lables.append(str(datetime.date.today()-datetime.timedelta(i)))
    data = {"data":{}}
    stocks = session.query(Stock).all()
    stockLst = []
    for i in stocks:
        stockLst.append(i.name)
        res = []
        parm = {'api_key':'mEthQomHfHJQ_bTJ6w7U'}
    	url = "https://www.quandl.com/api/v3/datasets/WIKI/"+i.name+".json?"+ urllib.urlencode(parm)
    	print url
    	h = httplib2.Http()
   	result = h.request(url,'GET')[1]
   	result = json.loads(result)
    	try:
        	for j in result["dataset"]["data"][0:20]:
        		res.append(j[1])
        	data["data"][i.name] = res
        	print (res,lables)

    	except:
        	return "<h1><center>Stock code dosent exist</center></h1>"
    data["lables"] = lables
    data["stocks"] = stockLst
    return json.dumps(data)

@app.route('/add/', methods=['POST'])
def add():
    	print (request.data)
     	count = session.query(Stock).filter_by(name=request.data).count()
     	if count>0:
        	return "Stock Already exits"
     	parm = {'api_key':'Your key here'}
    	url = "https://www.quandl.com/api/v3/datasets/WIKI/"+request.data+".json?"+ urllib.urlencode(parm)
    	print url
    	h = httplib2.Http()
   	result = h.request(url,'GET')[1]
   	result = json.loads(result)
    	if "quandl_error" in result:
        	return "Stock code dosen't exits"
	else:
     		newStock = Stock(name = request.data)
     		session.add(newStock)
       		session.commit()
	return request.data

@app.route('/remove/',methods=['POST'])
def remove():
    	lable = request.data
    	print lable;
    	rem = session.query(Stock).filter_by(name = lable).one()
     	session.delete(rem)
      	session.commit()
	return request.data

#if __name__ == '__main__':
app.secret_key = 'super_secret_key'
app.debug = True
#app.run(host = '0.0.0.0', port = 5000)
