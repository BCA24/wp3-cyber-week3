# werkplaats-3-inhaalopdracht-actiontypes
Template voor de WP3 inhaalopdracht "action types"

Deze repository bevat de volgende bestanden:
- De opdrachtomschrijving: [casus.md](casus)
- Een openapi specificatie voor het ontwerp van de API: [openapi.yaml](openapi.yaml)
- Een lijst met action types: [actiontype_statements.json](actiontype_statements.json)
- Een lijst met initiële studenten: [studenten.json](studenten.json)

Je mag dit document leegmaken en gebruiken voor documentatie van jouw uitwerking. 

# werkplaats-3-inhaalopdracht-actiontypes
Template voor de WP3 inhaalopdracht "action types"

“Myers-Briggs persoonlijkheidstypes"
--------------------------------------------------------------------------------------------
**Uitleg over hoe te starten in een virtual environment**

Voor Windows:
1. Open een nieuw venster voor commando's: Druk op de Windows-toets en de letter `R` tegelijkertijd, typ `cmd` in het vak dat verschijnt en druk op Enter.
2. Ga naar de map waar je wilt werken: Gebruik het commando `cd` om naar de map te gaan waar je aan je project wilt werken.
3. Maak een nieuwe map voor je project: Typ `mkdir myproject` en druk op Enter.
4. Ga naar je nieuwe map: Typ `cd myproject` en druk op Enter.
5. Maak een nieuwe virtuele omgeving: Typ `python -m venv venv` en druk op Enter.
6. Activeer je virtuele omgeving: Typ `venv\Scripts\activate` en druk op Enter. Je ziet nu `(venv)` in je commando-venster.

Voor macOS:
1. Open de Terminal: Ga naar de map `Applications` > `Utilities` > `Terminal` in Finder en dubbelklik erop.
2. Ga naar de map waar je wilt werken: Gebruik het commando `cd` om naar de map te gaan waar je aan je project wilt werken.
3. Maak een nieuwe map voor je project: Typ `mkdir myproject` en druk op Enter.
4. Ga naar je nieuwe map: Typ `cd myproject` en druk op Enter.
5. Maak een nieuwe virtuele omgeving: Typ `python3 -m venv venv` en druk op Enter.
6. Activeer je virtuele omgeving: Typ `source venv/bin/activate` en druk op Enter. Je ziet nu `(venv)` in je Terminal-venster.

**Opdracht**

We maken een persoonlijkheids test voor studenten om een action type te vinden die bij hun past door statements te kiezen. Zo kunnen we zien wie bij wie hoort.

Ook:
    mag ieder student het 1 keer doen zolang de result bestaat
    admins mogen docenten maken en admin geven
    admins mogen studenten maken, deleten, resetten en details bekijken van gekozen statements
    Werkende inlog

Daarbij:
    Via REST API de statements erbij gehaald via JSON file
    AJAX JQUERY om vragen website constant te houden
    FLASK voor funcites op te roepen
    Class models om SQL te bewerken

**personaliteit typen**

Er zijn verschillende types die tegen elkaar in gaan:
    Nadenken T tegen op gevoel F
    Extravert E tegen Introvert I
    zien begrijpen S tegen intuïtie N
    oordelen J tegen waarnemen P

**login**

Voor de login:
    Admin:
        name: admin
        passw: admin
    Student: 
        name: Bryan Kremer
        nmr: 2317948

        name: Mette Ansems
        nmr: 2603543

**Bronnen**

https://www.youtube.com/watch?v=FLeLlm51Lp4&pp=ygUUYWx0ZXIgdGFibGVzIHNxbGxpdGU%3D modify table sqllite, May 21 2020, MainlyWebStuff


https://www.youtube.com/watch?v=tNKD0kfel6o&pp=ygUWYWpheCBqcXVlcnkgamF2YXNjcmlwdA%3D%3D noob javascript met ajax, Apr 19 2017, Dani Krossing 


https://www.youtube.com/watch?v=MG9itGX1hD0&pp=ygUWYWpheCBqcXVlcnkgamF2YXNjcmlwdA%3D%3D post get html, flask, ajax, Apr 27 2017, Dani Krossing


https://www.youtube.com/watch?v=fEYx8dQr_cQ&pp=ygUWYWpheCBqcXVlcnkgamF2YXNjcmlwdA%3D%3D noob ajax api, jqeury, Jun 18 2014, LearnCode.academy


https://www.youtube.com/watch?v=Oage6H4GX2o&pp=ygUZcmVhZCBqc29uIGZpbGUgamF2YXNjcmlwdA%3D%3D voor leren van json naar html door java en api. Jul 13, 2022, ByteGra