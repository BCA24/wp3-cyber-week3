from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from databases.users import NoteModel


from threading import Lock
import json, sqlite3

conn = sqlite3.connect('databases/studentInfo.db', check_same_thread=False)
cursor = conn.cursor()
thread_lock = Lock()

app = Flask(__name__)
print("meh")
app.secret_key = "mysecretkey"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        user_model = NoteModel()
        user = None      
        if role == "docent":
            gebruikersnaam = request.form.get("username")
            wachtwoord = request.form.get("password")
            user = user_model.get_docent_login('databases/studentInfo.db', gebruikersnaam, wachtwoord)
        if role == "student":	
            studentnummer = request.form.get("studentnummer")
            studentnaam = request.form.get("studentnaam")
            user = user_model.get_student('databases/studentInfo.db', studentnummer, studentnaam)
        if user :
            # print("In user lus")
            # session['user_role'] = 'user'
            # session["user"] = user['Gebruikersnaam']  
            # session["is_ingelogd"] = True
            if role == "docent":
                if user['is_admin'] == 1:
                    session['user_role'] = 'admin'
                    return redirect(url_for("docent"))
                else:  
                    session['user_role'] = 'docent'
                    return redirect(url_for("overzicht"))
            if role == "student":
                session['studentnummer'] = studentnummer
                session['user_role'] = 'student'
                return redirect(url_for("vragen"))
        else:
            flash("Invalid username or password")
            return redirect(url_for("login"))

            
            
    return render_template("login.html")

@app.route("/agenda", methods=["GET", "POST"])
def agenda():
    if session.get("is_ingelogd"):
        print("agendaroute1")
        # flash("You are now logged in")
        return 'ingelogd'
    else:
        print("agendaroute2")
        return 'niet ingelogd...'

@app.route("/Welkom/Docent")
def docent():
    user_role = session.get("user_role")
    if user_role == 'admin' or user_role == 'docent':
        return render_template("docentMain.html")
    else:
        flash("You are not authorized to view this page")
        return redirect(url_for("login"))


@app.route('/overzicht', methods=['GET', 'POST'])
def overzicht():
    if request.method == 'POST':
        studentnaam = request.form.get('studentnaam')
        action = request.form.get('action')


        connection = sqlite3.connect('databases\studentInfo.db')
        cursor = connection.cursor()

        if action == 'reset':
            cursor.execute("UPDATE Studenten SET Action_type = NULL, test_gedaan = 0, tijdstip_af = NULL WHERE studentnummer = ?", (studentnaam,))
        elif action == 'delete':
            cursor.execute("DELETE FROM Studenten WHERE studentnummer = ?", (studentnaam,))

        connection.commit()

        connection.close()

    user_role = session.get("user_role")
    if user_role == 'admin' or user_role == 'docent':
        model = NoteModel()
        students = model.get_student_info('databases/studentInfo.db')

        return render_template("overzicht.html",  students = students)
    else:
        flash("You are not authorized to view this page")
        return redirect(url_for("login"))


@app.route('/details/<studentnaam>')
def details(studentnaam):
    connection = sqlite3.connect('databases\studentInfo.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Stellingen WHERE keuze_nummer = ?", (studentnaam,))
    Stellingen = cursor.fetchall()

    connection.close()

    return render_template('details.html', Stellingen=Stellingen)


@app.route('/reset/<studentnaam>', methods=['POST'])
def reset(studentnaam):
    print(f"Reset route hit with studentnaam: {studentnaam}")

    connection = sqlite3.connect('databases\studentInfo.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE Studenten SET Action_type = NULL, test_gedaan = 0, tijdstip_af = NULL WHERE studentnummer = ?", (studentnaam,))
    print(f"Rows updated: {cursor.rowcount}")

    connection.commit()

    connection.close()

    return redirect(url_for('overzicht'))


    
@app.route("/create_student", methods=["GET", "POST"])
def create_student():
    if request.method == "POST":
        studentnummer = request.form.get("studentnummer")
        studentnaam = request.form.get("studentnaam")
        studentklas = request.form.get("studentklas")


        student = NoteModel.create_student('databases/studentInfo.db', studentnummer, studentnaam, studentklas)
        flash("Student created successfully")
        return redirect(url_for("overzicht"))

    return render_template("createStudent.html")

@app.route("/create_docent", methods=["GET", "POST"])
def create_docent():
    if request.method == "POST":
        Docentnaam = request.form.get("Docentnaam")
        Gebruikersnaam = request.form.get("Gebruikersnaam")
        Wachtwoord = request.form.get("Wachtwoord")
        is_admin = request.form.get("is_admin")

        print(f"Docentnaam: {Docentnaam}")
        print(f"Gebruikersnaam: {Gebruikersnaam}")
        print(f"Wachtwoord: {Wachtwoord}")
        print(f"is_admin: {is_admin}")

        docent = NoteModel.create_docent('databases/studentInfo.db', Docentnaam, Gebruikersnaam, Wachtwoord, is_admin)
        flash("Docent created successfully")
        return redirect(url_for("overzicht"))

    return render_template("createDocent.html")

@app.route("/vragen", methods=['GET', 'POST'])
def vragen():
    if 'current_statement' not in session:
        session['current_statement'] = 0  

    with open('actiontype_statements.json', 'r', encoding='utf-8') as f:
        statements = json.load(f)

    if session['current_statement'] < len(statements):
        current_statement = statements[session['current_statement']]
        session['current_statement'] += 1  
    else:
        current_statement = None  

    student_id = session.get('studentnummer')
    connection = sqlite3.connect('databases\studentInfo.db')
    cursor = connection.cursor()
    cursor.execute("SELECT test_gedaan FROM Studenten WHERE studentnummer = ? AND test_gedaan = 0", (student_id,))
    connection.close()

  

    return render_template("vragen.html", statement=current_statement)

@app.route("/vragen/progress")
def vragen_progress():
    with open('actiontype_statements.json', 'r', encoding='utf-8') as f:
        statements = json.load(f)
    total_statements = len(statements)
    current_statement = session.get('current_statement', 0)
    progress = (current_statement / total_statements) * 100  

    return jsonify({'progress': progress})
@app.route("/previous_statement", methods=['POST'])
def previous_statement():
    if 'current_statement' not in session or session['current_statement'] <= 1:
        return jsonify(None)  

    with open('actiontype_statements.json', 'r', encoding='utf-8') as f:
        statements = json.load(f)

    session['current_statement'] -= 2  
    current_statement = statements[session['current_statement']]
    session['current_statement'] += 1 

    return jsonify(current_statement)

@app.route("/next_statement", methods=['POST'])
def next_statement():
    if 'current_statement' not in session:
        session['current_statement'] = 0  

    with open('actiontype_statements.json', 'r', encoding='utf-8') as f:
        statements = json.load(f)

    if session['current_statement'] < len(statements):
        current_statement = statements[session['current_statement']]
        session['current_statement'] += 1  
    else:
        current_statement = None  

    return jsonify(current_statement)

# @app.route("/resultaat", methods=['GET', 'POST'])
# def resultaat():
#     if request.method == 'POST':
#         result = request.form.get('result')  
        
#         session['result'] = result  
#         return jsonify({'status': 'success'})

#     result = session.get('result')  
#     return render_template("resultaat.html", result=result)

@app.route('/resultaat', methods=['POST'])
def handle_result():
    questionnaire_results = request.form['result']
    student_id =  session['studentnummer']
    

    action_choices = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    for letter in questionnaire_results:
        if letter in action_choices:
            action_choices[letter] += 1

    action_type = ""
    action_type += "E" if action_choices["E"] > action_choices["I"] else "I"
    action_type += "S" if action_choices["S"] > action_choices["N"] else "N"
    action_type += "T" if action_choices["T"] > action_choices["F"] else "F"
    action_type += "J" if action_choices["J"] > action_choices["P"] else "P"

    session['result'] = action_type

    connection = sqlite3.connect('databases\studentInfo.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE Studenten SET Action_type = ?, test_gedaan = 1, tijdstip_af = CURRENT_TIMESTAMP WHERE studentnummer = ?", (action_type, student_id))
    connection.commit()
    connection.close()

    return redirect('/resultaat')

@app.route('/resultaat')
def show_result():
        
    result = session.get('result', '')
    return render_template('resultaat.html', result=result)

if __name__ == "__main__":
    app.run(port=5001, debug=True)