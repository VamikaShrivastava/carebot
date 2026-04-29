

from flask import Flask,request,render_template,g,url_for
from pymongo import *
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


def init_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    db =client['user']
    collection = db["userI"]
    db1 = client['doctor']
    db2 = client['Sess']
    db3 = client['Feedback']
    return db,db1,db2,db3

@app.before_request
def before_request():
    g.db ,g.db1,g.db2,g.db3 = init_db()
    

@app.route('/df',methods = ['POST'])
def handleWebhook1():

    req = request.get_json()

    responseText = ""
    intent = req["queryResult"]["intent"]["displayName"]
    sessionId = req["session"].split("/")[-1]
    sessionFull = req["session"]

    if intent == "TypeofDoc":
        valueE = req["queryResult"]["parameters"]["DoctorType"]
        responseText = Responses(intent,valueE)
        res = {"fulfillmentMessages": responseText}
    elif intent == "NewAppointment":
        kuser=g.db.posts.find_one(sort=[("UserId", -1)])

        userID = kuser["UserId"] + 1

        res1 = Responses(intent,0)
        UserIdS =  int(req["queryResult"]["parameters"]["UserId"])
        posts = g.db2.posts
        g.db2.posts.update_one({'Session':sessionId},{'$set': {"UserId": UserIdS}}, 
                                upsert=True)
        
        
        if int(req["queryResult"]["parameters"]["UserId"]) in range(1111 ,userID):
            

            res = {"fulfillmentMessages": res1,"sessionEntityTypes":[
    {
      "name":sessionFull+"/entityTypes/UserData",
      "entities":[
        
        {
          "value":"Apple_Key",
          "synonyms":[
            UserIdS
          ]

        
        }
      ],
      "entityOverrideMode":"ENTITY_OVERRIDE_MODE_OVERRIDE"
    }
  ]}
        else:
            res = {"fulfillmentMessages": [{"text": {"text": ["No such user"]}}]}

    elif intent == "numberDoctor":
        valueF = int(req["queryResult"]["parameters"]["number"])

        myquery = { "Session": sessionId}


        mydoc = g.db2.posts.find_one(myquery)

        if mydoc:
            value1 = int(mydoc["UserId"])
            value2 = UserBooked(value1)
            
            if value2 == "No":
      
                myquery = { "Did": str(valueF)}
                mydoc = g.db1.posts.find_one(myquery)
                date = str(datetime.datetime.today().day) +"/"+ str(datetime.datetime.today().month)
                g.db.posts.update_one({"UserId": value1}, {"$push": {"Appoint":{"Did":str(valueF),"Name":mydoc["Name"],"Date":date}}})
                res = {"fulfillmentMessages": [{"text": {"text": ["We have successfully booked your appointment with Dr. {}".format(mydoc["Name"])]}}]}

            else:
                responseText = Responses("NoIntent",value2)
                res = {"fulfillmentMessages": responseText}
        
        else:
            res = {"fulfillmentMessages": [{"text": {"text": ["Sorry We do not have your User Id information."]}}]}
    
    
    
    elif intent == "ViewAppoint":
        myquery = { "Session": sessionId}
        mydoc = g.db2.posts.find_one(myquery)
            
        if mydoc:
            value1 = int(mydoc["UserId"])
            myquery1 = { "UserId": value1}
            mydoc1 = g.db.posts.find_one(myquery1)
            if "Appoint" in mydoc1 and len(mydoc1["Appoint"]):
                responseText = Responses(intent,mydoc1["Appoint"])
                res = {"fulfillmentMessages": responseText}
            else:
                res = {"fulfillmentMessages": [{"text": {"text": ["You do not have past or upcoming booking details"]}}]}
                
                
        
        else:
            res = {"fulfillmentMessages": [{"text": {"text": ["Sorry We do not have your User Id information.Kindly enter your Unique User Id"]}}]}

    elif intent == "numberUser":
        valueI = int(req["queryResult"]["parameters"]["number"])
        g.db2.posts.update_one({'Session':sessionId},{'$set': {"UserId": valueI}}, 
                                upsert=True)
        myquery1 = { "UserId": valueI}
        mydoc1 = g.db.posts.find_one(myquery1)
        if "Appoint" in mydoc1 and len(mydoc1["Appoint"]):
            responseText = Responses("ViewAppoint",mydoc1["Appoint"])
            res = {"fulfillmentMessages": responseText}
        else:
            res = {"fulfillmentMessages": [{"text": {"text": ["You do not have past or upcoming booking details"]}}]}
                
    elif intent == "Yes":
        docv = str(int(req["alternativeQueryResults"][0]["outputContexts"][0]["parameters"]["number"]))
        print(docv)
        myquery = { "Session": sessionId}
        mydoc = g.db2.posts.find_one(myquery)

        if mydoc:
            value1 = int(mydoc["UserId"])
            date =   str(datetime.datetime.today().day)+"/"+ str(datetime.datetime.today().month)
            myquery = { "Did": docv }
            mydoc4 = g.db1.posts.find_one(myquery)
            g.db.posts.update_one({"UserId":value1},{"$pull": {"Appoint":{"Date":date}}})
            g.db.posts.update_one({"UserId":value1},{"$push": {"Appoint":{"Date":date,"Did":docv,"Name":mydoc4["Name"]}}})
            res = {"fulfillmentMessages": [{"text": {"text": ["We have successfully booked your appointment with Dr. {}".format(mydoc4["Name"])]}}]}
            
        else:
            res = {"fulfillmentMessages": [{"text": {"text": ["You have not given the Unique User Id"]} }]} 
   
    else:
        responseText = f"There are no fulfillment responses defined for Intent {intent}"

    
        res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}


    return res


@app.route('/action1',methods = ['GET'])
def handleWebhook2():


    return render_template('formt.html')


@app.route('/action2',methods = ['POST'])
def handleWebhook3():

    result = request.form
    name = result["first_name"] + " " + result["Last_name"]
    email = result["email_address"]
    gender = result["gender"]
    medical = result["Medical"]
    bloodG = result["blood_group"]

    kuser=g.db.posts.find_one(sort=[("UserId", -1)])

    userID = kuser["UserId"] + 1

    post = {"Name": name , "Email": email, "Gender":gender,"BloodG":bloodG,"medical":medical,"UserId":userID}
    posts = g.db.posts
    result = posts.insert_one(post)

    return render_template('info.html',dictV=post)

@app.route('/')
def root():
    

    return render_template('base.html')


@app.route('/feedback1',methods = ['GET'])
def feedback():


    return render_template('abc.html')


@app.route('/feedback2',methods = ['POST'])
def feedbackresponse():

    result = request.form
    post = {"Email": result["mailid"], "Feedback":result["subject"]}
    g.db3.posts.insert_one(post)
  

    return str("We have successfully logged your feedback")


def Responses(intentT,valueE):
    
    if intentT == "NewAppointment":
        
        response = [
      {
        "payload": {
          "facebook": {
            "attachment": {
              "payload": {
                "template_type": "generic",
                "elements": [
                  {
                    "subtitle": "We have the right doctor for everyone.",
                    "title": "Welcome!",
                    "buttons": [
                      {
                        "type": "postback",
                        "title": "Psychiatrist",
                        "payload": "Psychiatrist"
                      },
                      {
                        "type": "postback",
                        "title": "Neurologist",
                        "payload": "Neurologist"
                      },
                      
                      {
                        "type": "postback",
                        "title": "Therapist",
                        "payload": "Therapist"
                      }
                    ]
                  }
                ]
              },
              "type": "template"
            }
          }
        },
        "platform": "FACEBOOK"
      },
      {
        "text": {
          "text": [
            ""
          ]
        }
      }
    ]
  

    if intentT == "TypeofDoc":
        
        url = {"1265":url_for('static', filename='doctor_1.png'),"2347":url_for('static', filename='doctor_2.png')}

        response = [
      {
        "payload": {
          "facebook": {
            "attachment": {
              "payload": {
                "template_type": "generic",
                "elements": [
               
                ]
              },
              "type": "template"
            }
          }
        },
        "platform": "FACEBOOK"
      },
      {
        "text": {
          "text": [
            ""
          ]
        }
      }
    ]
        myquery = { "desc": valueE}
        mydoc = list(g.db1.posts.find(myquery))
        for i in mydoc:
            dict1 = {
            "title": "Dr. " + i["Name"],
            "image_url": os.getenv("BASE_URL") + url[i["Did"]],
            "subtitle":"Dr.{} has a total experience of {} in {} field. Available on weekdays and timings are {}".format(i["Name"],i["exp"],i["desc"],i["timings"]),
            
            "buttons":[
              {
                "type":"postback",
                "title":"Book",
                "payload": i["Did"]
              }              
            ]      
          }
            response[0]["payload"]["facebook"]["attachment"]["payload"]["elements"].append(dict1)

    if intentT == "ViewAppoint":
        
        response = [
      {
        "payload": {
          "facebook": {
            "attachment": {
              "payload": {
                "template_type": "generic",
                "elements": [
               
                ]
              },
              "type": "template"
            }
          }
        },
        "platform": "FACEBOOK"
      },
      {
        "text": {
          "text": [
            ""
          ]
        }
      }
    ]
        for i in valueE:
            a = i["Date"]
            x ,y = a.split("/")
            appointed = "Upcoming"

            m,n = datetime.datetime.today().day , datetime.datetime.today().month

            if (int(n)> int(y)):
                appointed = "Past"
            elif(int(m) > int(x) and int(n)==int(y)):
                appointed = "Past"
                

            b=1
            dict1 = {
            "title": "Appointment with Dr. " + i["Name"],
            
            "subtitle":"{} appointment -  {}/23".format(appointed,a)
            
                  
          }
            response[0]["payload"]["facebook"]["attachment"]["payload"]["elements"].append(dict1)


    if intentT == "NoIntent":
        
        response = [
      {
        "payload": {
          "facebook": {
            "attachment": {
              "payload": {
                "template_type":"button",
                "text":"You already have one booking with Dr. {} Do you want to update?".format(valueE),
        "buttons":[
          {
            "type": "postback",
            "title": "Yes I like to update",
            "payload": "Yes"
          },
          {
            "type": "postback",
            "title": "No I am fine with current booking",
            "payload": "No"
          }
        ]
              },
              "type": "template"
            }
          }
        },
        "platform": "FACEBOOK"
      },
      {
        "text": {
          "text": [
            ""
          ]
        }
      }
    ]       
    return response

def UserBooked(userId):
    
    myquery1 = { "UserId": userId}
    mydoc1 = g.db.posts.find_one(myquery1)
    if "Appoint" in mydoc1 and len(mydoc1["Appoint"]):
        for i in mydoc1["Appoint"]:
            x= str(datetime.datetime.today().day) + "/" + str(datetime.datetime.today().month)

            if x == i["Date"]:
                return i["Name"]
            
    return "No"


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)
