# -*- coding: utf-8 -*-
"""
Created on Wed May  1 14:20:49 2024

@author: timwi
"""

import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
connection = sqlite3.connect('prg_python_database')

# Cursor-Objekt erstellen
cursor = connection.cursor()

# SQL-Befehl ausführen, um Daten aus der Datenbank abzurufen
cursor.execute('SELECT * FROM tabelle_3_Test_Daten')

# Ergebnis abrufen
result = cursor.fetchall()

# Ergebnis anzeigen
for row in result:
    print(row)

# Verbindung schließen
connection.close()