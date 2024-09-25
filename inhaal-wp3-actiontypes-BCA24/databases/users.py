import sqlite3
import json

class NoteModel :

    def get_docent_login(self, db, gebruikersnaam, wachtwoord):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM Docenten WHERE Gebruikersnaam = ? AND Wachtwoord = ?", (gebruikersnaam, wachtwoord) )
        user = cursor.fetchone()
        return user
    
    def get_user_by_admin(self, db, gebruikersnaam, wachtwoord):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM Docenten WHERE Gebruikersnaam = ? AND Wachtwoord = ? AND is_admin = 1", (gebruikersnaam, wachtwoord) )
        user = cursor.fetchone()
        return user
    
    def get_student(self, db, studentnummer, studentnaam):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM Studenten WHERE studentnaam = ? AND studentnummer = ?", (studentnaam, studentnummer))
        student = cursor.fetchone()
        return student

    def get_student_info (self,db):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM Studenten Limit 100, 150")
        return cursor.fetchall()
    
    def create_student(db_path, studentnummer, studentnaam, studentklas):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Studenten (studentnummer, studentnaam, studentklas) VALUES (?, ?, ?)", (studentnummer, studentnaam, studentklas))
        connection.commit()
        connection.close()
    
    def create_docent(db_path, Docentnaam, Gebruikersnaam, Wachtwoord, is_admin):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Docenten (Docentnaam, Gebruikersnaam, Wachtwoord, is_admin) VALUES (?, ?, ?, ?)", (Docentnaam, Gebruikersnaam, Wachtwoord, is_admin))
        connection.commit()
        connection.close()

    def transform_json():
        with open('actiontype_statements.json', 'r') as f:
            data = json.load(f)

        return data

    def insert_into_db(data):
        conn = sqlite3.connect('studentInfo.db')  
        c = conn.cursor()

        for item in data:
            for choice in item['statement_choices']:
                stelling_nummer = item['statement_number']
                keuze_tekst = choice['choice_text']
                keuze_nummer = choice['choice_number']
                keuze_resultaat = choice['choice_result']

                c.execute("INSERT INTO Stellingen VALUES (?, ?, ?, ?)",
                        (stelling_nummer, keuze_tekst, keuze_nummer, keuze_resultaat))

        conn.commit()  
        conn.close()  



with open('students.json', 'r') as f:
    students = json.load(f)

conn = sqlite3.connect('databases\studentInfo.db')
c = conn.cursor()

for student in students:
    c.execute("INSERT INTO Studenten (studentnummer, studentnaam, studentklas) VALUES (?, ?, ?)",
              (student['student_number'], student['student_name'], student['student_class']))



conn.commit()
conn.close()