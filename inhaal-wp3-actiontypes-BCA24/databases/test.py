import sqlite3
import json

# Connect to your sqlite DB
conn = sqlite3.connect('databases/studentInfo.db')

# Open a cursor to perform database operations
cur = conn.cursor()



with open('actiontype_statements.json', 'r') as file:
    data = json.load(file)

for item in data:
    stelling_nummer = item['statement_number']
    for choice in item['statement_choices']:
        keuze_tekst = choice['choice_text']
        keuze_nummer = choice['choice_number']
        keuze_resultaat = choice['choice_result']
        
        # Execute a query
        cur.execute(
            "INSERT INTO Stellingen (stelling_nummer, keuze_tekst, keuze_nummer, keuze_resultaat) VALUES (?, ?, ?, ?)",
            (stelling_nummer, keuze_tekst, keuze_nummer, keuze_resultaat)
        )

# Commit the transaction
conn.commit()

# Close the connection
cur.close()
conn.close()