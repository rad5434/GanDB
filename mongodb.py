from flask import Flask,render_template, request, jsonify
import json,ast
from flask_pymongo import PyMongo
from random import *
from pymongo import MongoClient

app=Flask(__name__)
@app.route('/')
def hello():
    return "This is database ec2 instance"

#waaa has the results data
#baaaa has 100 gan sketches
app.config['MONGO_DBNAME'] = 'caaaa'
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = 27017

app.config['MONGO2_DBNAME'] = 'zaaaa'
app.config['MONGO2_HOST'] = '127.0.0.1'
app.config['MONGO2_PORT'] = 27017

#app.config['MONGO2_DBNAME'] = '3dData'
#app.config['MONGO2_HOST'] = '127.0.0.1'
#app.config['MONGO2_PORT'] = 27017

mongo = PyMongo(app, config_prefix='MONGO')
mongo2 = PyMongo(app, config_prefix='MONGO2')

@app.route('/data', methods=['GET'])
def get_all_datas():
    data = mongo.db.data
    output = []
    for s in data.find():
        print s
        output.append(s['vector'])
    output = json.dumps(output)
    output = json.loads(output)
    return jsonify({"results":output})

@app.route('/data/<int:count>', methods=['GET'])
def get_all_data(count):
    data = mongo.db.data
    output = []
    mycount=0
    for s in data.find():
	if mycount==count:
		output.append(s['vector'])
		output = json.dumps(output)
    		output = json.loads(output)
		return jsonify(output[0])
	else:
		mycount+=1


@app.route('/Hdata', methods=['GET'])
def get_all_datas_human():
    data = mongo2.db.data
    output = []
    for s in data.find():
        output.append(s['vector'])
    output = json.dumps(output)
    output = json.loads(output)
    return jsonify({"results":output})

@app.route('/Hdata/<int:count>', methods=['GET'])
def get_all_data_human(count):
    data = mongo2.db.data
    #if count is 0:
    myoutput = []
    num=0
    output=[]
    for s in data.find():
	if num == count:
        	output.append(s['vector'])
       		output = json.dumps(output)
    		output = json.loads(output)	
		return jsonify(output[0])
	else:
		num+=1	

@app.route('/random', methods=['GET'])  #returns one boat per request
def get_ramdom_one():
    data = mongo.db.data
    output = []
    for s in data.find():
        print s
        output.append(s['vector'])
    output = json.dumps(output)
    output = json.loads(output)
    mylen = len(output)
    myrand = randint(0,mylen-1)
    return jsonify(output[myrand])


@app.route('/random/<int:count>', methods=['GET'])  #returns count number of boats per request
def get_ramdom_count(count):
    data = mongo.db.data
    output = []
    for s in data.find():
        print s
        output.append(s['vector'])
    output = json.dumps(output)
    output = json.loads(output)
    mylen = len(output)
    finalList=[]
    for i in range(count):
        myrand = randint(0,mylen-1)
        finalList.append(output[myrand])
        output.pop(myrand)
        mylen=mylen - 1

    newlist = sorted(finalList, key=lambda k: k['id']) 

    return jsonify(newlist)


@app.route('/emptyDB', methods=['GET'])
def empty_sketches():
    data = mongo.db.data
    data.remove({})
    return jsonify("done")


@app.route('/Hdata', methods=['POST'])
def add_data_human():
    data = mongo2.db.data
    reqdata = json.loads(request.data)
    vector = reqdata['data']
    postall_id = data.insert({'vector': vector})
    new_postall = data.find_one({'_id': postall_id })
    output = {'vector': new_postall['vector']}
    return jsonify(output)

@app.route('/Hdata/<int:count>', methods=['POST'])
def change_data_human(count):
    print "Posting in post"
    data = mongo2.db.data
    reqdata = json.loads(request.data)
    print type(reqdata)
    if reqdata:
        print "Python"
        reqdata = json.loads(request.data)
        vector = reqdata['data']
        postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
        print postall_id.matched_count
        new_postall = data.find_one({'_id': vector['id']})
        print new_postall
        output = {'vector': new_postall['vector']}
        print "Posting " + str(output)
        return jsonify({'data': output})
    else:
        print "Unity"
        reqdata = dict(request.form)
        print "req data"
        print reqdata
        vector = reqdata['data']
        print "vector"
        vector = json.loads(vector[0])
        print vector
        postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
        print postall_id.matched_count
        new_postall = data.find_one({'_id': vector['id']})
        print new_postall
        output = {'vector': new_postall['vector']}
        print "Posting " + str(output)
        return jsonify({'data': output})

@app.route('/data/<int:count>', methods=['POST'])
def change_data(count):
    print "Posting in post"
    data = mongo.db.data
    reqdata = request.data
    print type(reqdata)
    if reqdata:
        print "Python"
        reqdata = json.loads(request.data)
        vector = reqdata['data']
        postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
        print postall_id.matched_count
        new_postall = data.find_one({'_id': vector['id']})
        print new_postall
        output = {'vector': new_postall['vector']}
        print "Posting " + str(output)
        return jsonify({'data': output})
    else:
        print "Unity"
        reqdata = dict(request.form)
        print "req data"
        print reqdata
        vector = reqdata['data']
        print "vector"
        # vector=dict(vector[0])
        vector = json.loads(vector[0])
        print vector
        postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
        print postall_id.matched_count
        new_postall = data.find_one({'_id': vector['id']})
        print new_postall
        output = {'vector': new_postall['vector']}
        print "Posting " + str(output)
        return jsonify({'data': output})


@app.route('/data', methods=['POST'])
def add_sketches():
    data = mongo.db.data
    data.remove({})
    reqdata = json.loads(request.data)
    print reqdata
    vector = reqdata['results']
    print "\n\n\nhere we go\n\n\n"
    print vector
    print "\n\n\nthere we go\n\n\n"
    print type(vector)
    index=0
    datastored=[]
    while index < len(vector):
        print "my Vector \n\n\n" + str(vector[index]) + "\n\n\n"
        print vector[index]['id']
        postall_id = data.insert({'vector':vector[index]})
        print postall_id
        index+=1
    return jsonify(len(vector))


#------------------ 3D PART BEGINS --------------------------------------------------------

app.config['MONGO2_DBNAME'] = '3dData'
app.config['MONGO2_HOST'] = '127.0.0.1'
app.config['MONGO2_PORT'] = 27017

mongo3 = PyMongo(app, config_prefix='MONGO3')

@app.route('/3dData', methods=['POST'])
def add_3d_data():
    data = mongo3.db.data
    reqdata = json.loads(request.data)
    vector = reqdata['data']
    postall_id = data.insert({"_id":vector['id'],'data': vector})
    #postall_id = vector['id']
    new_postall = data.find_one({'_id': postall_id })
    output = {'data': new_postall['data']}
    return jsonify(output)

@app.route('/3dData/<int:count>', methods=['GET']) #returns based on how much the user asks. It will return based on random order
def get_3d_data(count):
    data = mongo3.db.data
    maxi = mongo3.db.count()-1
    output = []
    randnums=[]
    for i in range(count):
        myrand = random.randint(0,maxi)
        if myrand not in randnums:
            randnums.append(myrand)
            output.append(data.find(myrand))
        else:
            count+=1
    
    output = json.dumps(output)
    output = json.loads(output)
    return jsonify({"results":output})


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=80)

