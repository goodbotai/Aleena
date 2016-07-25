from flask import Flask, request
from urlparse import urlparse
from urlparse import parse_qs, urlparse
import urllib
import json
import requests
from collections import defaultdict
time = " 11:55"
vaccination_due = 0
health_dict = dict()
found = [0]
sender = []

app = Flask(__name__)
"""
lata = {"name": "Marks",
    "groups": [
               "Vaccinationdue"],
        "urns": [
                  "telegram" + ":" + number],

    "fields": {
        "my_date": "05-06-2016 11:45",

        "nick-name" : msg
        
    }
}


message = {
    "urns": [
             "telegram:" + number],
        "text": msg
}"""

def bulk_send():
    for x in sender:
        hey = requests.get('http://demotest:Admin123@46.101.51.199:8080/opensrp/rest/rapid/client/c?id=' + x)
        number = json.loads(hey.content)["client"]["phoneNo"]
        msg =  "Hi! you got this message because you have one or more vaccination due. Please consult a health worker to get the vaccines." + "\n" + "penta1 = " + json.loads(hey.content)["vaccineCard"]["penta1"] + "\n" + "penta2 = " + json.loads(hey.content)["vaccineCard"]["penta2"]+ "\n" +"penta3 = " + json.loads(hey.content)["vaccineCard"]["penta3"]+ "\n" + "pcv1  = " + json.loads(hey.content)["vaccineCard"]["pcv1"]+ "\n" +"pcv2 = " + json.loads(hey.content)["vaccineCard"]["pcv2"]+ "\n" + "pcv3   = " + json.loads(hey.content)["vaccineCard"]["pcv3"]+ "\n" + "opv1 = " + json.loads(hey.content)["vaccineCard"]["opv1"]+ "\n" + "opv2  = " + json.loads(hey.content)["vaccineCard"]["opv2"]+ "\n" + "opv3 = " + json.loads(hey.content)["vaccineCard"]["opv3"]+ "\n" + "measles1 = " + json.loads(hey.content)["vaccineCard"]["measles1"]+ "\n" + "measles2 = " +json.loads(hey.content)["vaccineCard"]["measles2"] + "\n" + "bcg  =  " + json.loads(hey.content)["vaccineCard"]["bcg"]
        
        message = {
            "urns": [
            "telegram:" + number,
                     "tel:+254710616572"],
            "text": msg
        }
            
        for j in json.loads(hey.content)["vaccineCard"]:
            if (json.loads(hey.content)["vaccineCard"][j] == "due"):
                vaccination_due = 1
        if (vaccination_due == 1):
            send = requests.post('https://rapidpro.ona.io/api/v1/broadcasts.json',json=message, headers={'Authorization': 'Token 6269bcaa1c78de11a12a52b2f280386439bff016'})
            vacination_due = 0
def bulk(x):
    hey = requests.get('http://demotest:Admin123@46.101.51.199:8080/opensrp/rest/rapid/client/c?id=' + x)
    number = json.loads(hey.content)["client"]["phoneNo"]
    msg =  "Hi! Here is your Vaccination details." + "\n" + "penta1 = " + json.loads(hey.content)["vaccineCard"]["penta1"] + "\n" + "penta2 = " + json.loads(hey.content)["vaccineCard"]["penta2"]+ "\n" +"penta3 = " + json.loads(hey.content)["vaccineCard"]["penta3"]+ "\n" + "pcv1  = " + json.loads(hey.content)["vaccineCard"]["pcv1"]+ "\n" +"pcv2 = " + json.loads(hey.content)["vaccineCard"]["pcv2"]+ "\n" + "pcv3   = " + json.loads(hey.content)["vaccineCard"]["pcv3"]+ "\n" + "opv1 = " + json.loads(hey.content)["vaccineCard"]["opv1"]+ "\n" + "opv2  = " + json.loads(hey.content)["vaccineCard"]["opv2"]+ "\n" + "opv3 = " + json.loads(hey.content)["vaccineCard"]["opv3"]+ "\n" + "measles1 = " + json.loads(hey.content)["vaccineCard"]["measles1"]+ "\n" + "measles2 = " +json.loads(hey.content)["vaccineCard"]["measles2"] + "\n" + "bcg  =  " + json.loads(hey.content)["vaccineCard"]["bcg"]
        
    message = {
            "urns": [
                     "telegram:" + number
                     ],
            "text": msg
    }
    return json.dumps({"valuee":msg})

@app.route('/rapidpro', methods=['POST'])
def record_id():
    import ipdb
    ipdb.set_trace()
    data = request.form
    length = len(eval(request.form["values"]))
    val = (eval(request.form["values"])[length-1]["value"])
    phone = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['phone'][0]
    name = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['name'][0]
    id = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['identifier'][0]
    birth = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['birth'][0]
    sender.append(id)
    lata = {"name": name + "s",
    "groups": [
               "Vaccinationdue"],
        "urns": [
                 "telegram" + ":" + phone],

"fields": {
    "my_date": birth + time,
     "penta1":"due",
     "penta2":"due",
     "penta3":"due",
     "measles1":"due",
     "measles2":"due",
     "bcg":"due",
     "penta1date":birth + time,
     "penta2date":birth + time,
     "penta3date":birth + time,
     "measles1date":birth + time,
     "measles2date":birth + time,
     "bcgdate":birth + time

     }
   }
    
    Run = request.form["run"]
    send = requests.post('https://rapidpro.ona.io/api/v1/contacts.json',json=lata, headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
    response = requests.get('https://rapidpro.ona.io/api/v1/messages.json?run={}'.format(Run), headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
    ID = json.loads(response.content)["results"][0]["urn"].split(":", 1)[1]
    print sender
    print ID
    for key in health_dict:
        if (ID == key):
            health_dict[ID].append(id)
            found[0] = 1
    if (found[0] ==1):
        found[0] = 0
    else:
        health_dict[ID] = []
        health_dict[ID].append(id)
    print health_dict
    return "ok"
@app.route('/send', methods=['POST'])
def send_messages():
    """bulk_send()"""
    Run = request.form["run"]
    response = requests.get('https://rapidpro.ona.io/api/v1/messages.json?run={}'.format(Run), headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
    ID = json.loads(response.content)["results"][0]["urn"].split(":", 1)[1]
    for key in health_dict:
        if (key==ID):
            for x in health_dict[ID]:
                hey = requests.get('http://demotest:Admin123@46.101.51.199:8080/opensrp/rest/rapid/client/c?id=' + x )
                number = json.loads(hey.content)["client"]["phoneNo"]
                msg =  "Hi! you got this message because you have one or more vaccination due. Please consult a health worker to get the vaccines." + "\n" + "penta1 = " + json.loads(hey.content)["vaccineCard"]["penta1"] + "\n" + "penta2 = " + json.loads(hey.content)["vaccineCard"]["penta2"]+ "\n" +"penta3 = " + json.loads(hey.content)["vaccineCard"]["penta3"]+ "\n" + "pcv1  = " + json.loads(hey.content)["vaccineCard"]["pcv1"]+ "\n" +"pcv2 = " + json.loads(hey.content)["vaccineCard"]["pcv2"]+ "\n" + "pcv3   = " + json.loads(hey.content)["vaccineCard"]["pcv3"]+ "\n" + "opv1 = " + json.loads(hey.content)["vaccineCard"]["opv1"]+ "\n" + "opv2  = " + json.loads(hey.content)["vaccineCard"]["opv2"]+ "\n" + "opv3 = " + json.loads(hey.content)["vaccineCard"]["opv3"]+ "\n" + "measles1 = " + json.loads(hey.content)["vaccineCard"]["measles1"]+ "\n" + "measles2 = " +json.loads(hey.content)["vaccineCard"]["measles2"] + "\n" + "bcg  =  " + json.loads(hey.content)["vaccineCard"]["bcg"]
        
                message = {
            "urns": [
                     "telegram:" + number,
                     "tel:+254710616572"],
            "text": msg
                      }
        
                for j in json.loads(hey.content)["vaccineCard"]:
                    if (json.loads(hey.content)["vaccineCard"][j] == "due"):
                        vaccination_due = 1
                if (vaccination_due == 1):
                    send = requests.post('https://rapidpro.ona.io/api/v1/broadcasts.json',json=message, headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
                    vacination_due = 0
    return "ok"

@app.route('/rapidpros', methods=['POST'])
def record_ids():
    data = request.form
    length = len(eval(request.form["values"]))
    val = (eval(request.form["values"])[length-1]["value"])
    
    return bulk(val)
"""result = requests.post('https://rapidpro.ona.io/api/v1/contacts.json',json=lata, headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
import ipdb
ipdb.set_trace()
print result"""
print id

@app.route('/penta1', methods=['POST'])
def vaccinate_penta1():
    name = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['name'][0]
    penta1date = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['date'][0]
    id = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['clientId'][0]
    hey = requests.get('http://demotest:Admin123@46.101.51.199:8080/opensrp/rest/rapid/client/c?id=' + id)
    number = json.loads(hey.content)["client"]["phoneNo"]
    lata = {"name": name,
    "groups": [
               "Vaccinationdue"],
        "urns": [
                 "telegram" + ":" + number],

"fields": {
    "penta1date": "01-01-2000" + time,
    "penta1": penta1date
    
    }
        }

    send = requests.post('https://rapidpro.ona.io/api/v1/contacts.json',json=lata, headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
    return "ok"

@app.route('/penta2', methods=['POST'])
def vaccinate_penta2():
    name = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['name'][0]
    penta2date = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['date'][0]
    id = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['clientId'][0]
    hey = requests.get('http://demotest:Admin123@46.101.51.199:8080/opensrp/rest/rapid/client/c?id=' + id)
    number = json.loads(hey.content)["client"]["phoneNo"]
    lata = {"name": name,
    "groups": [
               "Vaccinationdue"],
        "urns": [
                 "telegram" + ":" + number],

"fields": {
    "penta2date": "01-01-2000" + " 10:25",
    "penta2": penta2date
    
    }
    }
    
    send = requests.post('https://rapidpro.ona.io/api/v1/contacts.json',json=lata, headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
    return "ok"

@app.route('/penta3', methods=['POST'])
def vaccinate_penta3():
    name = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['name'][0]
    penta3date = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['date'][0]
    id = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['clientId'][0]
    hey = requests.get('http://demotest:Admin123@46.101.51.199:8080/opensrp/rest/rapid/client/c?id=' + id)
    number = json.loads(hey.content)["client"]["phoneNo"]
    lata = {"name": name,
    "groups": [
               "Vaccinationdue"],
        "urns": [
                 "telegram" + ":" + number],

"fields": {
    "penta3date": "01-01-2000" + " 10:25",
    "penta3": penta3date
    
    }
    }
    
    send = requests.post('https://rapidpro.ona.io/api/v1/contacts.json',json=lata, headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
    return "ok"

@app.route('/bcg', methods=['POST'])
def vaccinate_bcg():
    name = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['name'][0]
    bcgdate = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['date'][0]
    id = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['clientId'][0]
    hey = requests.get('http://demotest:Admin123@46.101.51.199:8080/opensrp/rest/rapid/client/c?id=' + id)
    number = json.loads(hey.content)["client"]["phoneNo"]
    lata = {"name": name,
    "groups": [
               "Vaccinationdue"],
        "urns": [
                 "telegram" + ":" + number],

"fields": {
    "bcgdate": "01-01-2000" + " 10:25",
    "bcg": bcgdate
    
    }
    }
    
    send = requests.post('https://rapidpro.ona.io/api/v1/contacts.json',json=lata, headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
    return "ok"

@app.route('/measles1', methods=['POST'])
def vaccinate_measles1():
    name = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['name'][0]
    measles1date = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['date'][0]
    id = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['clientId'][0]
    hey = requests.get('http://demotest:Admin123@46.101.51.199:8080/opensrp/rest/rapid/client/c?id=' + id)
    number = json.loads(hey.content)["client"]["phoneNo"]
    lata = {"name": name,
    "groups": [
               "Vaccinationdue"],
        "urns": [
                 "telegram" + ":" + number],

"fields": {
    "measles1date": "01-01-2000" + " 10:25",
    "measles1": measles1date
    
    }
    }
    
    send = requests.post('https://rapidpro.ona.io/api/v1/contacts.json',json=lata, headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
    return "ok"
@app.route('/measles2', methods=['POST'])
def vaccinate_measles2():
    name = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['name'][0]
    measles2date = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['date'][0]
    id = parse_qs(urlparse('/?'+request.query_string).query,keep_blank_values=True)['clientId'][0]
    hey = requests.get('http://demotest:Admin123@46.101.51.199:8080/opensrp/rest/rapid/client/c?id=' + id)
    number = json.loads(hey.content)["client"]["phoneNo"]
    lata = {"name": name,
    "groups": [
               "Vaccinationdue"],
        "urns": [
                 "telegram" + ":" + number],

"fields": {
    "measles2date": "01-01-2000" + " 10:25",
    "measles2": measles2date
    
    }
    
    }
    
    send = requests.post('https://rapidpro.ona.io/api/v1/contacts.json',json=lata, headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})
    return "ok"

@app.route('/message', methods=['POST'])
def specific_message():
    length = len(eval(request.form["values"]))
    val = (eval(request.form["values"])[length-1]["value"])
    print val
    for x in sender:
        hey = requests.get('http://demotest:Admin123@46.101.51.199:8080/opensrp/rest/rapid/client/c?id=' + x)
        number = json.loads(hey.content)["client"]["phoneNo"]
        msg =  val
        
        message = {
            "urns": [
                     "telegram:" + number,
                     "tel:+254710616572"],
            "text": msg
        }
        send = requests.post('https://rapidpro.ona.io/api/v1/broadcasts.json',json=message, headers={'Authorization': 'Token c40134bced79d90b50a9579572ebae620846add9'})

    
    return "ok"
@app.route('/locate', methods=['POST'])
def locate():
    lengt = len(eval(request.form["values"]))
    val = (eval(request.form["values"])[lengt-1]["value"])
    da = {"query": val, "key":"AIzaSyD2y6sRKMVLiBD5atdDCNoYzAKABDFKCsk" }
    print da
    post =requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json',params=da)
    lat = eval(post.content)['results'][0]['geometry']['location']['lat']
    long = eval(post.content)['results'][0]['geometry']['location']['lng']
    du= {"query": "hospitals",
    "key":"AIzaSyD2y6sRKMVLiBD5atdDCNoYzAKABDFKCsk",
    "location" : str(lat) +"," + str(long) ,
    "radius" : "5000"}
    posts =requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json',params=du)
    length =  len(eval(posts.content)['results'])
    if (length ==1):
        va = eval(posts.content)['results'][0]['name']
        dict = {"valuees":"choose! Is this the place " + va }
    else:
        va = eval(posts.content)['results'][0]['name']
        van = eval(posts.content)['results'][1]['name']
        dict = {"valuees":"choose! Which one is familiar " + va +" or " + van}
    return json.dumps(dict)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
"""print response.form"""
