#imports
import sqlite3
import sys
import os
import hashlib
import time
from random import randint
#prepaing clear command
clear = lambda: os.system('cls')
clear()
#global variables
logged_in = False
active_user = ""
#Establishing SQLite Connection
connection = sqlite3.connect("bankdata.db")
cursor = connection.cursor()
def register():
        newname = input("BITTE NAMEN EINTRAGEN (FORMAT: maxmustermann)")
        commane1 = """
        SELECT inhaber FROM Konten WHERE inhaber=\"""" + newname + "\""
        cursor.execute(commane1)
        
        soos = cursor.fetchall()
        
        if soos == []:
            print("BITTE PASSWORT FESTLEGEN:")
            newpassword = input()
            passwordhash = get_hash(newpassword)
            
            saas= "INSERT INTO Konten (inhaber, kontonummer, kontostand, passwort) VALUES (\"" + newname + "\"" + "," + str(randint(0, 1000)) + "," + "0,\"" + passwordhash  + "\");"
            
            
            
            cursor.execute(saas)

            connection.commit()
            clear()
            
            print("REGISTRIERUNG ERFOLGREICH!")
            print("WILLKOMMEN " + newname)
            introscreen()
            
        else:
            print("FEHLER")


def get_hash(pass1):
    
    lol = hashlib.sha256()
    lol.update(pass1.encode())
    hash1 = lol.hexdigest()
    return hash1



def anzahl_konten():

    cursor.execute("SELECT COUNT(*) FROM Konten")
    return cursor.fetchall()[0][0]

def get_password(user):
    command1 = """
    SELECT passwort FROM Konten WHERE inhaber=\"""" + user + "\""
    
    
    
    
    cursor.execute(command1)
    
    return cursor.fetchall()[0][0]



def anmelden():
    clear()
    global logged_in
    global active_user
    username = input("BENUTZERNAME:")
    password = input("PASSWORT:")
    pass2 = get_password(username)
    
    if get_hash(password) == pass2:
        print("ERFOLGREICH ANGEMELDET!")
        logged_in = True
        active_user = username
        mainmenu()
    else:
        clear()
        print("!FALSCHE ANMELDEDATEN!")
        print("PROGRAMM WIRD BEENDET")
        time.sleep(2.5)
        clear()
        print("3")
        time.sleep(1)
        clear()
        print("2")
        time.sleep(1)
        clear()
        print("1")
        time.sleep(1)
        clear()
        print("BIS BALD!")
        time.sleep(1)
        sys.exit()

      
def get_kontostand(username1):
    saas = "SELECT kontostand FROM Konten WHERE inhaber=\"" + username1 + "\""
    cursor.execute(saas)
    
    return cursor.fetchall()[0][0]

def introscreen():
    clear()
    print("***************************")
    print("CheapBank-OnlineBanking")
    print("WIR GENIEßEN DAS VERTRAUEN VON " + str(anzahl_konten()) + " NUTZERN")
    print("***************************")
    
    if logged_in == False:
        print("STATUS: NICHT ANGEMELDET")
    if logged_in == True:
        print("ANGEMELDET ALS " + active_user)
    
    print("***************************\n")
    
    print("HAUPTMENÜ:")
    print("1: ANMELDEN")
    print("2: REGISTRIEREN")
    print("3: PROGRAMM BEENDEN")
    wahl = int(input("EINGABE:"))
    if wahl == 1:
        anmelden()
    if wahl == 2:
        register()
    if wahl == 3:
        sys.exit()
def get_information(user1):
    clear()
    saas = "SELECT kontonummer,kontostand FROM Konten WHERE inhaber=\"" + user1 + "\""
    cursor.execute(saas)
    
    info1 = cursor.fetchall()
    
    print("Kontoinhaber: " + active_user)
    print("Kontonummer: " + str(info1[0][0]))
    print("Kontostand: " + str(info1[0][1]))
    print("ENTER FÜR ZURÜCK")
    lool = input()
    mainmenu()    


def mainmenu():
    global logged_in
    global active_user
    clear()
    print("***************************")
    print("CheapBank-OnlineBanking")
    print("WIR GENIEßEN DAS VERTRAUEN VON " + str(anzahl_konten()) + " NUTZERN")
    print("***************************")
    
    if logged_in == False:
        print("FEHLER: NICHT ANGEMELDET")
        time.sleep(2)
        clear()
        print("3")
        time.sleep(0.5)
        clear()
        print("2")
        time.sleep(0.5)
        clear()
        print("1")
        time.sleep(0.5)
        clear()
        print("UMLEITUNG ZUR ANMELDUNG")
        time.sleep(0.5)
        introscreen()
    if logged_in == True:
        print("ANGEMELDET ALS " + active_user)
    
    print("***************************\n")
    print("IHR AKTUELLER KONTOSTAND BETRÄGT " + str(get_kontostand(active_user)) + "€")
    print("HAUPTMENÜ:")
    print("1: Ein/Auszahlungen")
    print("2: Überweisungen")
    print("3: Kontoinformationen")
    print("4: Ausloggen/Beenden")
    
    wahl = int(input())
    if wahl == 1:
        ein_auszahlung()
    if wahl == 2:
        ueberweisung()
    if wahl == 3:
        get_information(active_user)
    if wahl == 4:
        logged_in = False
        active_user = ""
        clear()
        print("SIE WERDEN IN 3 SEKUNDEN AUSGELOGGT")
        time.sleep(1)
        clear()
        print("SIE WERDEN IN 2 SEKUNDEN AUSGELOGGT")
        time.sleep(1)
        clear()
        print("SIE WERDEN IN 1 SEKUNDEN AUSGELOGGT")
        time.sleep(1)
        clear()
        print("SIE WERDEN IN 0 SEKUNDEN AUSGELOGGT")
        time.sleep(1)
        clear()
        mainmenu()

def ein_auszahlung():
    clear()
    print("1: GELD EINZAHLEN")
    print("2: GELD AUSZAHLEN")
    print("3: ZURÜCK")
    wahl = int(input())
    if wahl == 1:
        einzahlung_menu()
    if wahl == 2:
        auszahlung_menu()

def einzahlung_menu():
    print("WIEVIEL GELD MÖCHTEN SIE EINZAHLEN?")
    betrag1 = int(input())
    saas = "SELECT kontostand FROM Konten WHERE inhaber=\"" + active_user + "\""
    cursor.execute(saas)
    kontostand1 = cursor.fetchall()[0][0]
    neukontostand = kontostand1 + betrag1
    saas = "UPDATE Konten SET kontostand=\"" + str(neukontostand) + "\"" + " WHERE inhaber=" + "\"" + active_user + "\""
    cursor.execute(saas)
    connection.commit()
    mainmenu()

def auszahlung_menu():
    print("WIEVIEL GELD MÖCHTEN SIE AUSZAHLEN?")
    betrag1 = int(input())
    saas = "SELECT kontostand FROM Konten WHERE inhaber=\"" + active_user + "\""
    cursor.execute(saas)
    kontostand1 = cursor.fetchall()[0][0]
    neukontostand = kontostand1 - betrag1
    saas = "UPDATE Konten SET kontostand=\"" + str(neukontostand) + "\"" + " WHERE inhaber=" + "\"" + active_user + "\""
    cursor.execute(saas)
    connection.commit()
    mainmenu()

def ueberweisung():
    clear()
    print("1: KONTONUMMERVERZEICHNIS")
    print("2: ÜBERWEISUNG AUFGEBEN")
    print("3: ZURÜCK")
    wahl123 = int(input())
    if wahl123 == 1:
        clear()
        saas = "SELECT inhaber, kontonummer FROM Konten"
        cursor.execute(saas)
        info = cursor.fetchall()
        
        for i in info:
            for a in i:
                print(a)
            print("------")
                
        print("ENTER FÜR ZURÜCK")
        ss = input()
        ueberweisung()
    if wahl123 == 2:
        print("BITTE KONTONUMMER EINGEBEN")
        address = int(input())
        print("BITTE BETRAG EINGEBEN")
        betrag = int(input())
        saas = "SELECT kontostand FROM Konten WHERE kontonummer=" + str(address)
        cursor.execute(saas)
        info = cursor.fetchall()[0][0]
        
        
        
        if info == None:
            print("KONTONUMMER NICHT VERGEBEN")
            print("ENTER FÜR WEITER")
            ss = input()
            ueberweisung()
        neukontostand1 = info + betrag

        saas = "UPDATE Konten SET kontostand=" + str(neukontostand1) + " WHERE kontonummer=" + str(address) + ";"
        cursor.execute(saas)
        connection.commit()
        print("ÜBERWEISUNG ERFOLGREICH!")
        print("ENTER FÜR HAUPTMENÜ")
        ss = input()
        mainmenu()
    if wahl123 == 3:
        mainmenu()


introscreen()



