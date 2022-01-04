import json

def write_json(data, filename='hello.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f)


def add_to_json_file(cat, ques, rep):
    listTags = ["salutation", "AuRevoir"]

    with open("hello.json", "r+") as jsonfile:
        data = json.load(jsonfile)
        print(data)
        print("\n")

        for intent in data["data"]:
            print(intent)
            if cat not in listTags:
                new_data = {"tags": f"{cat}", "questions": [f"{ques}"], "responses": [f"{rep}"]}
                data["data"].append(new_data)
            elif cat == intent["tags"] and ques in intent["questions"] and rep in intent["responses"]:
                pass
            elif intent["tags"] == cat:
                if ques not in intent["questions"] and rep not in intent["responses"]:
                    intent["questions"].append(ques)
                    intent["responses"].append(rep)
            else:
                pass
    
    write_json(data)

# def modify_to_json_file(cat, ques, rep):
#     listTags = ["salutation", "AuRevoir"]

#     with open("hello.json", "r+") as jsonfile:
#         data = json.load(jsonfile)
#         print(data)
#         print("\n")

#         for intent in data["data"]:
#             print(intent)
#             if cat not in listTags:
#                 #Alert cat  doesn't exist
#             elif cat:
#                 pass
#             else:
#                 pass
    
#     write_json(data)

def delete_to_json_file(cat, ques, rep):
    listTags = ["salutation", "AuRevoir"]

    with open("hello.json", "r+") as jsonfile:
        data = json.load(jsonfile)
        print(data)
        print("\n")

        for intent in data["data"]:
            if cat not in listTags:
                #Alert cat  doesn't exist
                print("Alert cat  doesn't exist")
            elif cat == intent["tags"] and ques not in intent["questions"] and rep not in intent["responses"]:
                #Alert Questions and responses don't exist
                print("Alert Questions and responses don't exist")
            elif cat == intent["tags"] and ques in intent["questions"] and rep in intent["responses"]:
                intent["questions"].remove(ques)
                intent["responses"].remove(rep)
                print("Données supprimées")
            else:
                pass
        
        print(data)
    
    write_json(data)

delete_to_json_file("AuRevoir", "Bye", "Ok")


"""

import json 
  
  
# function to add to JSON 
def write_json(data, filename='data.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 
      
      
with open('data.json') as json_file: 
    data = json.load(json_file) 
      
    temp = data['emp_details'] 
  
    # python object to be appended 
    y = {"emp_name":'Nikhil', 
         "email": "nikhil@geeksforgeeks.org", 
         "job_profile": "Full Time"
        } 
  
  
    # appending data to emp_details  
    temp.append(y) 
      
write_json(data) 


"""

# def writeToJson(path, filename, data):
#     filenameExit = './'+path+'/'+filename+'.json'
#     with open(filenameExit, 'w') as f:
#         json.dump(data, f)

# path = './'
# filename = 'hello'

# data = {}
# data['test'] = "OK"
# data['hello'] = "Bonjour"

# writeToJson(path, filename, data)