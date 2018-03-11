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

mongo = PyMongo(app, config_prefix='MONGO')
mongo2 = PyMongo(app, config_prefix='MONGO2')


count=0
lastdatasent=0
myoutput=[]
#cdbb actual data is stored
@app.route('/data', methods=['GET'])
def get_all_datas():
    data = mongo.db.data
    output = []
    for s in data.find():
        #s.pop('_id')
        print s
        output.append(s['vector'])
        #{'vector' : s['vector']}
    #output=output.encode("ascii", "replace")
    output = json.dumps(output)
    output = json.loads(output)
    #type(loaded_r)  # Output dict
    print "Getting " + str({'data':output})
    #print "Type: "+ str(type(output))
    return jsonify({'results':output})

@app.route('/data/<int:count>', methods=['GET'])
def get_all_data(count):
    data = mongo.db.data
    output = []
    for s in data.find():
        # s.pop('_id')
        output.append(s['vector'])

    #output={'results': output}
    output = json.dumps(output)
    output = json.loads(output)
    print "Getting " + str(output)
    #print "The first one:" + str(output[0])
    return jsonify(output[count])


@app.route('/Hdata', methods=['GET'])
def get_all_datas_human():
    data = mongo2.db.data
    output = []
    for s in data.find():
        #s.pop('_id')
        print s
        output.append(s['vector'])
        #{'vector' : s['vector']}
    #output=output.encode("ascii", "replace")
    output = json.dumps(output)
    output = json.loads(output)
    #type(loaded_r)  # Output dict
    print "Getting " + str({'data':output})
    #print "Type: "+ str(type(output))
    return jsonify({'results':output})

@app.route('/Hdata/<int:count>', methods=['GET'])
def get_all_data_human(count):
    data = mongo2.db.data
    #if count is 0:
    myoutput = []
    num=0
    for s in data.find():
        #s.pop('_id')
        myoutput.append(s['vector'])
       
    myoutput = json.dumps(myoutput)
    myoutput = json.loads(myoutput)

    return jsonify(myoutput[count])	


@app.route('/random', methods=['GET'])  #returns one boat per request
def get_ramdom_one():
    data = mongo.db.data
    output = []
    for s in data.find():
        #s.pop('_id')
        print s
        output.append(s['vector'])
        #{'vector' : s['vector']}
    #output=output.encode("ascii", "replace")
    output = json.dumps(output)
    output = json.loads(output)
    #type(loaded_r)  # Output dict
    #print "Getting " + str({'data':output})
    mylen = len(output)
    myrand = randint(0,mylen-1)
    #print "Type: "+ str(type(output))
    return jsonify(output[myrand])


@app.route('/random/<int:count>', methods=['GET'])  #returns count number of boats per request
def get_ramdom_count(count):
    data = mongo.db.data
    output = []
    for s in data.find():
        #s.pop('_id')
        print s
        output.append(s['vector'])
        #{'vector' : s['vector']}
    #output=output.encode("ascii", "replace")
    output = json.dumps(output)
    output = json.loads(output)
    #type(loaded_r)  # Output dict
    #print "Getting " + str({'data':output})
    mylen = len(output)
    finalList=[]
    for i in range(count):
        myrand = randint(0,mylen-1)
        finalList.append(output[myrand])
        output.pop(myrand)
        mylen=mylen - 1

    #finalList.sort(key=id)
    newlist = sorted(finalList, key=lambda k: k['id']) 

    return jsonify(newlist)


@app.route('/emptyDB', methods=['GET'])
def empty_sketches():
    data = mongo.db.data
    data.remove({})
    #print "Type: "+ str(type(output))
    return jsonify("done")




'''@app.route('/data/<int:count>', methods=['GET'])
def get_one_data(count):
    data = mongo.db.data
    output=[]
    for s in data.find():
        # s.pop('_id')
        output.append(s['vector'])
    #print output
    print data.find_one({"vector":{"id":count}})
    s = data.find_one({'_id':count})
    if s:
        output = { 'check': s['check'],'id': s['id'],'x_data': s['x_data'],'y_data': s['y_data']}
    else:
        output = "No such name"
    return jsonify({'data': output})'''


'''@app.route('/data/<int:count>', methods=['DELETE'])
def do_delete(count):
    data = mongo.db.data
    output = []
    for s in data.find():
        output.append(s['vector'])
        print (s['vector']['check'])

    output.remove(output[count])
    return jsonify(output)

@app.route('/data/<int:count>', methods=['PUT'])
def update_task(count):
    data = mongo.db.data
    reqdata = json.loads(request.data)
    vector = reqdata
    postall_id = data.insert({'vector': vector})
    new_postall = data.find_one({'_id': postall_id})
    output = {'vector': new_postall['vector']}
    print "Posting " + str(output)
    return jsonify({'results': output})
    #data = mongo.db.data
    output = []
    for s in mongo.db.data.find():
        if s['vector']['id']==count:
            s['vector']['check']=1
            output.append(s['vector'])

    #print output[count]
    return jsonify(output)'''

@app.route('/Hdata', methods=['POST'])   #"""HUMAN DATA"""
def add_data_human():
    data = mongo2.db.data
    #data.remove({})
    reqdata = json.loads(request.data)
    vector = reqdata['data']
    #myaxis=vector['axis']
    print vector['id']
    postall_id = data.insert({'_id':vector['id'],'vector': vector})
    print postall_id
    new_postall = data.find_one({'_id': postall_id })
    print new_postall
    output = {'vector': new_postall['vector']}
    print "Posting " + str(output)
    return jsonify({'data': output})

@app.route('/Hdata/<int:count>', methods=['POST'])
def change_data_human(count):
    print "Posting in post"
    data = mongo2.db.data
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
        # print myDict
        # reqdata = json.loads(request.form)
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
def add_data():
    data = mongo.db.data
    #data.remove({})
    reqdata = json.loads(request.data)
    vector = reqdata['data']
    #myaxis=vector['axis']
    print vector['id']
    postall_id = data.insert({'_id':vector['id'],'vector': vector})
    print postall_id
    new_postall = data.find_one({'_id': postall_id })
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
        # print myDict
        # reqdata = json.loads(request.form)
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

'''@app.route('/data/<int:count>', methods=['POST'])
def change_data(count):
    data = mongo.db.data
    reqdata = json.loads(request.data)
    vector = reqdata['data']
    postall_id = data.update_one({'_id': vector['id']}, {'$set': {'vector': vector}})
    print postall_id.matched_count
    new_postall = data.find_one({'_id': vector['id']})
    print new_postall
    output = {'vector': new_postall['vector']}
    print "Posting " + str(output)
    return jsonify({'data': output})'''



'''@app.route('/data', methods=['POST'])
def add_data(name):
    data = mongo.db.data
    vector = request.json['results']
    name = randint(1,100)
    #print "Hello World" + str(vector)
    lists=[]
    #for s in vector:
        #print s
        #lists.append(s)
    #print "List: "+str(lists)
    #print "Vector: " + str(vector)
    postall_id = data.insert({'vector': vector,'name':name})
    new_postall = data.find_one({'_id': postall_id })
    output = {'vector': new_postall['vector'],'name':new_postall['name']}
    print "Posting " + str(output)
    return jsonify(output)'''

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=80)

