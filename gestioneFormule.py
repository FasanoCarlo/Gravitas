import gravitasXML as gxml

def formula_geometrica(forma, tipo, dati):
    forma = forma.capitalize()
    tipo = tipo.capitalize()
    try:
        testoFormula = fileXML.trovaFormule_FormaTipo(forma,tipo)
        testoFormula = testoFormula[0]
        return testoFormula
    except:
        return {'procedura' : "Errore Sconosciuto", 'risultato' : "Errore"}

file_da_Modificare = 'formule'
fileXML = gxml.FileXML("formule_geometriche.xml")
if file_da_Modificare == 'formule':
    if input("Vuoi Inserire [i] o Provare [v] formule? ") == 'i':
        # Inserimento Formule
        while True:
            tipo = input("Tipo (es. Area): ")
            if tipo == 'stoop':
                break
            forma = input("Forma (es. Rettangolo): ")
            dimensioni = input("Dimensioni (es. 2D): ")
            datiNecessari = input("Dati Necessari (es. Base,Altezza): ")
            testoFormula = input("Testo Formula (es. base*altezza): ")
            if testoFormula != 'stoop':
                fileXML.inserisciFormula(tipo, forma, dimensioni, datiNecessari, testoFormula)
            print()
    else:
        # Prova Formule
        tipo = input("Tipo: ")
        forma = input("Forma: ")
        print(tipo + " " + forma)
        dati = {}
        while True:
            key = input("Key: ")
            if key == 'stoop':
                break
            value = float(input("valore: "))
            dati.update({key:value})
        risultato = formula_geometrica(forma, tipo, dati)
        #print("Procedura:", risultato['procedura'])
        #print()
        #print("Risultato:", risultato['risultato'])
        print("Formula:", risultato)
        print("---")
elif file_da_Modificare == 'costanti':
    pass
