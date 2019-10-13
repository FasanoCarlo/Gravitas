# Gravitas 2019

# Importazione Librerie
import math
from datetime import datetime
import gravitasXML as gxml
import os
import platform

# Operazioni Preliminari
geoXML = gxml.FileXML("xml/formule_geometriche.xml")
fisXML = gxml.FileXML("xml/formule_fisiche.xml")
variabili_utente = {}
costanti = gxml.FileXML("xml/costanti.xml").ottieniCostanti()
nomeFile_Predefinito = None
dataOraAttuale = datetime.now()


# Matematica e Logica di Base
def null(var):
    if var == None or var == '' or var == 0:
        return True
    else:
        return False

def elevazione_potenza(numero_originale, esponente):
    numero = numero_originale
    if esponente == 0:
        return 1
    elif esponente == 1:
        return numero
    for i in range(esponente-1):
        numero = numero * numero_originale
        i = i
    return numero

def cos(x):
    return math.cos(math.radians(x)) # Coseno (Gradi)

def moltiplica_tutto(dati): # Array dati
    i = 1
    for n in dati:
        i = i * n
    return i

def radice_quadrata(x):
    return math.sqrt(x)

def teorema_pitagora(ipotenusa, cateto1, cateto2):
    print("catet1 alla 2", elevazione_potenza(cateto1, 2))
    if ipotenusa == 0:
        return {'risultato': radice_quadrata(elevazione_potenza(cateto1, 2) + elevazione_potenza(cateto2, 2)), 'procedura': "VV " +  str(cateto1) + "^2 + " + str(cateto2) + "^2 VV = " + str(radice_quadrata(elevazione_potenza(cateto1, 2) + elevazione_potenza(cateto2, 2)))}
    elif cateto1 == 0:
        return {'risultato': radice_quadrata(elevazione_potenza(ipotenusa, 2) - elevazione_potenza(cateto2, 2)), 'procedura': "VV " + str(ipotenusa) + "^2 - " + str(cateto2) + "^2 VV = " + str(radice_quadrata(elevazione_potenza(ipotenusa, 2) - elevazione_potenza(cateto2, 2)))}
    elif cateto2 == 0:
        return {'risultato': radice_quadrata(elevazione_potenza(ipotenusa, 2) - elevazione_potenza(cateto1, 2)), 'procedura': "VV " + str(ipotenusa) + "^2 - " + str(cateto1) + "^2 = " + str(radice_quadrata(elevazione_potenza(ipotenusa, 2) - elevazione_potenza(cateto1, 2)))}

def formula_finale(formula, array_dati):
    for dato in array_dati:
        formula = formula.replace(dato, str(array_dati[dato]))
    return formula

def calcolatrice_libera(loop): # Bool loop (eseguire in loop la calcolatrice?)
    if loop == True:
        while True:
            operazione_str = input("+-> ")
            print(eval(operazione_str))
            if operazione_str == '' or operazione_str == 'esci' or operazione_str == 'stoop' or operazione_str == 'exit':
                break
        return
    else:
        operazione_str = input("+-> ")
        risultato = eval(operazione_str)
        print(risultato)
        return risultato

def calcolatrice_scientifica(a, dati, considerareVariabiliUtente):
    # Immissione dati
    for dato in dati:
        a = a.replace(dato, str(dati[dato]))
    # Immissione Variabili Utente
    if considerareVariabiliUtente == True:
        for var in variabili_utente:
            a = a.replace(var, str(variabili_utente[var]['risultato']))
    # Immissioni Costanti
    for final in costanti:
        chiavi = final.split(',')
        for chiave in chiavi:
            a = a.replace(chiave, str(costanti[final]))
    datiMessi = a
    # Risoluzione Potenze
    if "^" in a:
        array_pezzi = a.split(" ")
        for stringa in array_pezzi:
            if "^" in stringa:
                array_pezzi_potenza = stringa.split("^")
                numero_finale = elevazione_potenza(float(array_pezzi_potenza[0]), int(array_pezzi_potenza[1]))
                a = a.replace(stringa, str(numero_finale))
    # Risoluzione Radici Quadrate
    if "VV" in a:
        radici = a.split("VV")
        for i in range(len(radici)):
            if i % 2 != 0 and i != 0:
                radice = radice_quadrata(eval(radici[i]))
                a = a.replace("VV" + radici[i] + "VV", str(radice))
            else:
                pass
    # Risoluzione Coseno
    if "CC" in a:
        coseni = a.split("CC")
        for i in range(len(coseni)):
            if i % 2 != 0 and i != 0:
                coseno = cos(eval(coseni[i]))
                a = a.replace("CC" + coseni[i] + "CC", str(coseno))
            else:
                pass
    # Fine
    return {'procedura' : datiMessi, 'risultato' : eval(a)}


# Funzioni Geometriche

def formula(par1, par2, dati, file_XML):
    Parametro1 = par1.capitalize()
    Parametro2 = par2.capitalize()
    try:
        testoFormula = file_XML.trovaFormule_Par1Par2(Parametro1,Parametro2)
        testoFormula = testoFormula[0]
        return calcolatrice_scientifica(testoFormula, dati, False)
    except:
        return {'procedura' : "Errore Sconosciuto", 'risultato' : "Errore"}


# Funzioni Fisiche

def scomposizione_vettori(dati): # Array dati --> 'vx':Float, 'vy':Float, 'modulo':Float, 'angolo':Float
    vx = 0
    vy = 0
    if null(dati['vx']) and null(dati['vy']):
        #print("caso1")
        # Bisogna usare il coseno
        vx = dati['modulo'] * cos(dati['angolo'])
        vy = dati['modulo'] * cos(90 - dati['angolo'])
        modulo = dati['modulo']
        angolo = dati['angolo']
        formula = formula_finale("Vx = modulo * cos(angolo°) \nVy = modulo * cos(90 - angolo°) \nModulo = modulo", dati)
    elif null(dati['vx']):
        #print("caso2")
        # Teorema di Pitagora
        vy = dati['vy']
        vx = radice_quadrata(elevazione_potenza(dati['modulo'], 2) - elevazione_potenza(dati['vy'], 2))
        modulo = dati['modulo']
        angolo = dati['angolo']
        formula = formula_finale("Vx = VV modulo^2 - vy^2 VV \nVy = vy \nModulo = modulo", dati)
    elif null(dati['vy']):
        #print("caso3")
        # Teorema di Pitagora
        vx = dati['vx']
        vy = radice_quadrata(elevazione_potenza(dati['modulo'], 2) - elevazione_potenza(dati['vx'], 2))
        modulo = dati['modulo']
        angolo = dati['angolo']
        formula = formula_finale("Vx = vx \nVy = VV modulo^2 - vx^2 VV \nModulo = modulo", dati)
    elif null(dati['modulo']):
        #print("caso4")
        # Teorema di Pitagora
        vx = dati['vx']
        vy = dati['vy']
        modulo = radice_quadrata(elevazione_potenza(dati['vx'], 2) + elevazione_potenza(dati['vy'], 2))
        angolo = dati['angolo']
        formula = "Vx = vx \nVy = vy \nModulo = VV vx^2 + vy^2 VV"
    elif null(dati['angolo']):
        pass
    else:
        vx = "Errore"
        vy = "Errore"
        modulo = "Errore"
        angolo = "Errore"
        formula = "Errore"
    
    return {'vx':vx, 'vy':vy, 'modulo':modulo, 'angolo': angolo, 'procedura': formula}

def somma_vettori(vettori): # Array di array vettori. Esempio. vettori = {{'vx':10,'vy':2}, {'vx':11, 'vy':3}}
    return radice_quadrata(elevazione_potenza(vettori[0]['vx'] + vettori[1]['vx'], 2) + elevazione_potenza(vettori[0]['vy'] + vettori[1]['vy'], 2))

# Altre Funzioni
def scrivi(nomeFile, testo, eccezioniSilenziose = False):
    # boolInterno serve a dire alla funzione se è stata chiamata dal programma o dall'utente
    try:
        a = open(nomeFile, "w")
        a.write(testo)
        a.close()
    except FileNotFoundError:
        if eccezioniSilenziose == False:
            # Funzione Chiamata dall'utente. Riporta l'eccezione
            riporta_eccezione("!!! File non esistente !!!")
            print("File non esistente")
    except PermissionError:
        if eccezioniSilenziose == False:
            # Funzione Chiamata dall'utente. Riporta l'eccezione
            riporta_eccezione("!!! Permessi insufficienti !!!")
            print("Permessi Insufficienti")

def riporta_eccezione(STReccezione):
    fileEccezione = open(dataOraAttuale.strftime("%d.%m.%Y_%H.%M.%S_EccezioneGravitas.txt"), "w")
    fileEccezione.write(STReccezione)
    fileEccezione.close()

def leggi(nomeFile, eccezioniSilenziose = False):
    try:
        a = open(nomeFile, "r")
        b = a.read()
        a.close()
        return b
    except FileNotFoundError:
        if eccezioniSilenziose == False:
            # Funzione Chiamata dall'utente. Riporta l'eccezione
            riporta_eccezione("!!! File Insistente !!!")
            print("File Inesistente")
        return ""
    except PermissionError:
        if eccezioniSilenziose == False:
            # Funzione Chiamata dall'utente. Riporta l'eccezione
            riporta_eccezione("!!! Permessi insufficienti !!!")
            print("Permessi insufficienti")
        return ""

def appendi(nomeFile, testo, eccezioniSilenziose = False):
    try:
        a = leggi(nomeFile, True)
    except (FileNotFoundError):
        scrivi(nomeFile, "")
        a = leggi(nomeFile, False)
    try:
        a += "\n" + testo
        scrivi(nomeFile, a)
    except TypeError:
        if eccezioniSilenziose == False:
            riporta_eccezione("!!! Errore di Tipo !!!" + "\n" + "Tipo di testo: " + str(type(testo)) + "\n" + "Testo = " + str(testo))

def enumero(var):
    try:
        float(var)
        return True
    except:
        return False

# Presentazione Programma
print("Gravitas 2019")
print("Programma italiano per la fisica di base")
print()

# Spazio Interazioni...

while True:
    INPUT = input("_ Gravitas >>> ")
    if INPUT == 'stoop' or INPUT == 'STOOP' or INPUT == 'esci':
        exit(0)
    elif INPUT == 'var' or INPUT == 'variabile':
        nomeVariabile = input("Nome Variabile: ")
        while True:
            conferma = None
            valore_variabile = None
            tipo_valore = input("Che tipo di valore vuoi che immettere (guida per ulteriori info): ")
            if tipo_valore == "guida":
                print()
                print("espressione (espressione matematica)")
                print("geo (formula geometrica)")
                print("fisica (formula fisica)")
                print("vettore (scomposizione/composizione vettore)")
                print("pitagora (teorema di pitagora)")
                print("numero (numero)")
                print()

            elif tipo_valore == "espressione":
                valoreVariabile = calcolatrice_scientifica(input("Scrivi l'espressione: "), {}, True)
                valoreVariabile = {'procedura' : nomeVariabile + " = " + valoreVariabile['procedura'] + " = " + str(valoreVariabile['risultato']), 'risultato' : valoreVariabile['risultato']}
            
            elif tipo_valore == "geo":
                tipoGeo = input("Tipo: ")
                formaGeo = input("Forma: ")
                array_parametri = geoXML.trovaParametri_Par1Par2(formaGeo, tipoGeo)
                dizionario_parametri = {}
                for parametro in array_parametri:
                    valore = input( parametro + " = ")
                    dizionario_parametri.update({ parametro.lower():valore })
                valoreVariabile = formula(formaGeo, tipoGeo, dizionario_parametri, geoXML)
                valoreVariabile = {'procedura' : nomeVariabile + " = " + valoreVariabile['procedura'] + " = " + str(valoreVariabile['risultato']), 'risultato' : valoreVariabile['risultato']}
            
            elif tipo_valore == "numero":
                while True:
                    valoreVariabile = str(input("Numero: "))
                    valoreVaraibile = valoreVariabile.replace(",", ".")
                    if enumero(valoreVariabile) == True:
                        valoreVariabile = {'procedura': nomeVariabile + " = " + str(float(valoreVariabile)), 'risultato': float(valoreVariabile)}
                        break
                    else:
                        print("Valore non accettabile. Assegnazione della variabile annullata. Riprova...")

            elif tipo_valore == "fisica":
                print("In caso di dubbi consultare il manuale.")
                argoFis = input("Argomento: ")
                datoFis = input("Valore: ")
                array_parametri = fisXML.trovaParametri_Par1Par2(argoFis, datoFis)
                dizionario_parametri = {}
                for parametro in array_parametri:
                    valore = input( parametro + " = ")
                    dizionario_parametri.update({ parametro.lower() : valore })
                valoreVariabile = formula(argoFis, datoFis, dizionario_parametri, fisXML)
                valoreVariabile = {'procedura' : nomeVariabile + " = " + valoreVariabile['procedura'] + " = " + str(valoreVariabile['risultato']), 'risultato' : valoreVariabile['risultato']}
            
            elif tipo_valore == 'vettore':
                print("Inserisci i dati richiesti. Imposta a zero il dato da ottenere")
                
                # INPUT
                nomeVettore = nomeVariabile
                VettoreX = float(input("Componente X: "))
                VettoreY = float(input("Componente Y: "))
                VettoreModulo = float(input("Modulo: "))
                VettoreAngolo = float(input("Angolo: "))
                
                pacchetto_dati = {'vx' : VettoreX, 'vy' : VettoreY, 'modulo' : VettoreModulo, 'angolo' : VettoreAngolo}
                dati_vettore = scomposizione_vettori(pacchetto_dati)
                
                # Variabili Utente Generate
                variabili_utente.update({nomeVariabile + "X" : {'procedura' : nomeVettore + "X = " + str(dati_vettore['modulo']) + " * cos(" + str(VettoreAngolo) + ") = " + str(dati_vettore['vx']), 'risultato' : dati_vettore['vx']}})
                variabili_utente.update({nomeVariabile + "Y" : {'procedura' : nomeVettore + "Y = " + str(dati_vettore['vy']), 'risultato' : dati_vettore['vy']}})
                variabili_utente.update({nomeVariabile + "Modulo" : {'procedura' : nomeVettore + "Modulo = " + str(dati_vettore['modulo']), 'risultato' : dati_vettore['modulo']}})

                break

            elif tipo_valore == "pitagora":
                print("FUNZIONE ANCORA IN BETA")
                print("Imposta a 0 il valore che desideri conoscere...")
                ipotenusa = float(input("Ipotenusa: "))
                cateto1 = float(input("Primo Cateto: "))
                cateto2 = float(input("Secondo Cateto: "))
                valoreVariabile = teorema_pitagora(ipotenusa, cateto1, cateto2)

            if tipo_valore != "guida" and tipo_valore != "vettore":
                if input("Confermi [S/n] ? ") != "n":
                    variabili_utente.update({nomeVariabile:valoreVariabile})
                else:
                    break
                if input("Scrivere su file [S/n] ? ") != "n":
                    if nomeFile_Predefinito != None:
                        # Esiste il nome file predefinito
                        appendi(nomeFile_Predefinito, variabili_utente[nomeVariabile]['procedura'], True)
                        break
                    else:
                        # Non esiste il nome file predefinito
                        appendi(str(input("Nome file: ")), variabili_utente[nomeVariabile]['procedura'])
                        break
                break


    elif INPUT == "leggi":
        nomeFile = input("Nome File: ")
        print(leggi(nomeFile))
        print()

    elif INPUT == "file":
        nomeFile_Predefinito = input("Nome file predefinito (solo per questa sessione): ")

    elif INPUT == "listavariabili" or INPUT == "listavar":
        if len(variabili_utente) == 0:
            print("Nessuna variabile memorizzata")
        else:
            i = 1
            for var in variabili_utente:
                print(str(i) + ". " + var + " = " + str(variabili_utente[var]['risultato']) + "   Procedura: " + str(variabili_utente[var]['procedura']))
                i += 1

    elif INPUT == "stampa":
        nomeVarStamp = input("Nome variabile: ")
        try:
            print(variabili_utente[nomeVariabile])
        except (NameError):
            print("'" + nomeVarStamp + "' non esiste")

    elif INPUT == "scrivi":
        nomeFile = None
        input_n_var = input("Inserisci il nome della variabile che vuoi scrivere su file: ")
        if nomeFile_Predefinito == None:
            # Non è stato impostanto un nome file. Va chiesto adesso
            nomeFile = input("Nome File: ")
        else:
            nomeFile = nomeFile_Predefinito
        try:
            appendi(nomeFile, variabili_utente[input_n_var])
        except KeyError:
            print("La variabile '" + input_n_var + "' non esiste")
    
    elif INPUT == "tabrasa":
        conf = input("Le variabili che hai memorizzato verrano cancellate. Continuare [S/n]? ")
        if conf == 'S':
            variabili_utente = {}
        else:
            print("Operazione Annullata")

    elif INPUT == "pulisci":
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    elif INPUT == "calcola" or INPUT == "espressione":
        # Guida Calcolatrice
        print(" Guida Calcolatrice Scientfica:")
        print("1. Scrivi la formula da risolvere. Ogni numero, operatore deve essere accompagnato uno spazio:")
        print("   Esempio: 10 + 4 / 2 - 1 * 7")
        print("2. Fa eccezione l'elevazione a potenza che va espressa così: 20^2   ( Base^Esponente )")
        print("3. Usare solo parentesi tonde (). NON usare altri tipi di parente [] {}")
        print("4. La funzione Coseno si indica: CC x CC in cui x è l'angolo in GRADI")
        print("5. La radice quadrata si indica: VV x + y / z VV  dentro le 'VV' va immesso il numero o l'espressione")
        print()

        while True:
            espressione = input("Scrivi l'espressione: ")
            print("Risultato:", calcolatrice_scientifica(espressione, {}, True)['risultato'])
            print()
            if input("Uscire dalla calcolatrice [S/n]? ") != "n":
                break
            else:
                pass

    elif INPUT == "guida":
        print()
        print("---------------------- Guida GRAVITAS ----------------------")
        print("              -   COMANDO   -   FUNZIONE   -                ")
        print("                    stoop   -   Esce da Gravitas            ")
        print("          var - variabile   -   Dichiara una nuova variabile")
        print("                    leggi   -   Legge un file               ")
        print("                     file   -   Imposta il file predefinito per l'output ")
        print("listavariabili - listavar   -   Stampa a video tutte le variabili dichiarate con il loro valore e procedura")
        print("                   stampa   -   Stampa a video una variabile")
        print("                   scrivi   -   Scrive su file una variabile già dichiarata")
        print("                  tabrasa   -   Cancella le varabili memorizzate durante la sessione")
        print("                  pulisci   -   Genera dello spazio vuoto nel terminale")
        print("    calcola - espressione   -   Avvia una calcolatrice scientifica che può usufruire delle variabili già dichiarate")
        print("                    guida   -   Stampa a video questa guida")
        print()


    else:
        print("Comando NON riconosciuto")
        tipo_valore = "guida"
    


if False:
    a = calcolatrice_scientifica("CC 30 CC", {'bcm':3}, True)
    print(a['procedura'])
    print(a['risultato'])