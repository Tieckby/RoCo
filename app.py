#Importer les modules necessaires pour l'utilisation de Flask
from flask import (Flask, render_template, request, session, redirect, url_for, g, flash)
from datetime import timedelta

#JSON for json file processing
import json

# import pyttsx3 as pts

# speak = pts.init()
# #set index to 0 for french and 1 for english
# voices = speak.getProperty('voices')
# speak.setProperty('voice', voices[0].id)


#On importe le module RoCo
from ChatBot import RoCo

#Initialisation de RoCo
chatbot = RoCo()

#Initialisation de Flask
app = Flask(__name__)
app.secret_key = 'helloworld@tiemoko'
app.static_folder = 'static'
app.permanent_session_lifetime = timedelta(minutes=1)

#Class User to save login information
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def ___repr__(self):
        return f"User: {self.username}"

users = []
users.append(User(id=1, username='admin', password='admin'))

# ------------------------------------------ Fonction admin section -------------------------------------- #
#Fonction for writing in json file
def write_json(data, filename='Data.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f)

#Fonction add_to_json_file to add item in json file
def add_to_json_file(cat, ques, rep):
    listTags = ["salutationSimple", "salutationQuestion", "auRevoir", "motSimple", "noanswer", "remerciement", "options", "date des examens", "nombre de dette pour avoir sa licence", "blague", "myself"]

    with open("Data.json", "r+") as jsonfile:
        data = json.load(jsonfile)

        for intent in data["data"]:
            if cat not in listTags:
                new_data = {"tags": f"{cat}", "questions": [f"{ques}"], "responses": [f"{rep}"]}
                data["data"].append(new_data)
                flash("Mis a jour faite avec succes")
            elif cat == intent["tags"] and ques in intent["questions"] and rep in intent["responses"]:
                flash("Ces éléments existent déja ! Merci.")
            elif intent["tags"] == cat:
                if ques not in intent["questions"] and rep not in intent["responses"]:
                    intent["questions"].append(ques)
                    intent["responses"].append(rep)
            else:
                flash("Ajout non éffectué !")

        print(data)
    
    write_json(data)

#Fonction delete_to_json_file to del item in json file
def delete_to_json_file(cat, ques, rep):
    listTags = ["salutationSimple", "salutationQuestion", "auRevoir", "motSimple", "noanswer", "remerciement", "options", "date des examens", "nombre de dette pour avoir sa licence", "blague", "myself"]

    with open("Data.json", "r+") as jsonfile:
        data = json.load(jsonfile)

        for intent in data["data"]:
            if cat not in listTags:
                #Alert cat  doesn't exist
                flash(f"La catégorie {cat} n'existe pas dans la base.")
            elif cat == intent["tags"] and ques not in intent["questions"] and rep not in intent["responses"]:
                #Alert Questions and responses don't exist
                flash("Désolé, ces données existent déja dans la base")
            elif cat == intent["tags"] and ques in intent["questions"] and rep in intent["responses"]:
                intent["questions"].remove(ques)
                intent["responses"].remove(rep)
                flash("Données supprimées avec succes.")
            else:
                flash("Suppression non éffectuée !")
    
    write_json(data)

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/run",methods=['GET','POST'])
def getBotResponse():
    userText = request.args['msg']
    print(userText)
    # speak.say(chatbot.get_RoCo_Response(userText))
    # speak.runAndWait()
    # speak.stop()
    return str(chatbot.get_RoCo_Response(userText))

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
#Demarre la page d'accueille
@app.route("/")
def home():
    return render_template("index.html")

#Page de login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username and x.password == password]
        if user:
            session['user_id'] = user[0].id
            return redirect(url_for('admin'))
        
        flash("Mot de pass ou username incorrect...!")
        return redirect(url_for('login'))
    else:
        if g.user:
            return redirect(url_for('admin'))
        
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for('login'))

@app.route("/admin")
def admin():
    if not g.user:
        return redirect(url_for('login'))

    return render_template("admin.html")

@app.route("/add_data", methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        category = request.form['category']
        question = request.form['question']
        answer = request.form['answer']

        if category and question and answer:
            add_to_json_file(category, question, answer)
        else:
            flash("Veuillez saisir tous les champ svp!")

    return render_template("Modify_DB/add_data.html")

@app.route("/delete_data", methods=['GET', 'POST'])
def delete_data():
    if request.method == 'POST':
        category = request.form['category']
        question = request.form['question']
        answer = request.form['answer']

        if category and question and answer:
            delete_to_json_file(category, question, answer)
        else:
            flash("Veuillez saisir tous les champ svp!")

    return render_template("Modify_DB/delete_data.html")

@app.route("/modify_data", methods=['GET', 'POST'])
def modify_data():
    if request.method == 'POST':
        category = request.form['category']
        question = request.form['question']
        answer = request.form['answer']

        if category and question and answer:
            flash("Mis a jour faite a success")
        else:
            flash("Veuillez saisir tous les champ !")

    return render_template("Modify_DB/modify_data.html")

if __name__ == "__main__":
    app.run(debug=False)