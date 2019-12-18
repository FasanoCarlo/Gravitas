# Questo è un file secondario che andrà a contenere tutte le funzioni legate alla gestione (lettura/scrittura) dei file XML
import xml.etree.ElementTree as et
import os

class FileXML:
    path = None
    nomeFile = None
    tree = None
    root = None
    errore_inizializzazione = False

    def __init__(self, nomeFile):
        try:
            self.path = os.path.dirname(os.path.realpath(__file__))
            self.nomeFile = os.path.join(self.path, nomeFile)
            self.tree = et.parse(self.nomeFile)
            self.root = self.tree.getroot()
        except et.ParseError:
            print("!!! Errore durante la lettura di " + nomeFile + " !!!")
            self.errore_inizializzazione = True

    def minuscolo(self, stringa):
        return str(stringa).lower()

    def confermaRiuscitaOperazione(self):
        print("Path: " + self.path)
        print("Nome File: " + self.nomeFile)
        return {'path':self.path, 'nomeFile':self.nomeFile}


    def listaTestiFormule(self):
        ritorno = []
        for child in self.root:
            for element in child:
                if element.tag == 'testoFormula':
                    ritorno.append(element.text)
        return ritorno

    def trovaFormule_Par1Par2(self, par1 = '00', par2 = '00', par3 = '00'):
        array_finale = []
        par1 = self.minuscolo(par1)
        par2 = self.minuscolo(par2)
        par3 = self.minuscolo(par3)
        for child in self.root:
            if self.minuscolo(child.attrib['par1']) == par1 and self.minuscolo(child.attrib['par2']) == par2 and self.minuscolo(child.attrib['par3']) == par3:
                for element in child:
                    if element.tag == 'testoFormula':
                        array_finale.append(element.text)
        return array_finale

    def trovaParametri_Par1Par2(self, par1 = '00', par2 = '00', par3 = '00'):
        array_finale = []
        par1 = self.minuscolo(par1)
        par2 = self.minuscolo(par2)
        par3 = self.minuscolo(par3)
        for child in self.root:
            if self.minuscolo(child.attrib['par1']) == par1 and self.minuscolo(child.attrib['par2']) == par2 and self.minuscolo(child.attrib['par3']) == par3:
                for element in child:
                    if element.tag == 'datiNecessari':
                        for datoNecessario in element:
                            print(datoNecessario.text)
                            array_finale.append(datoNecessario.text)
        return array_finale

    def ultimoID(self):
        return int(self.root[len(self.root)-1].attrib['id'])

    def inserisciFormula(self, tipo, forma, dimensioni, datiNecessari, testoFormula):
        id = str(self.ultimoID() + 1)
        nuova_formula = et.SubElement(self.root, 'formula', attrib={'id':id, 'par2':tipo, 'par1':forma, 'dimensioni':dimensioni})
        nuova_serie_dati_necessari = et.SubElement(nuova_formula, "datiNecessari")
        nuovo_dato_necessario = et.SubElement(nuova_serie_dati_necessari, "datoNecessario")
        testo_formula = et.SubElement(nuova_formula, "testoFormula")
        nuovo_dato_necessario.text = datiNecessari
        testo_formula.text = testoFormula
        self.tree.write(self.nomeFile)

    def ottieniInformazioni(self):
        return {'versione' : self.root.attrib['versione'], 'data' : self.root.attrib['data'], 'commenti' : self.root.attrib['commenti']}

    def ottieniCostanti(self):
        ritorno = {}
        key = None
        value = None
        for child in self.root:
            for element in child:
                if element.tag == 'paroleChiave':
                    key = element.text
                elif element.tag == 'valore':
                    value = element.text
            ritorno.update({key:value})
        return ritorno

    def listaFormuleGeometria(self):
        testo = "Formule di Geometria Gravitas:"
        for child in self.root:
            testo += "\n" + "ID: " + child.attrib['id']
            testo += "\n" + "Forma: " + child.attrib['par1']
            testo += "\n" + "Tipo: " + child.attrib['par2']
            testo += "\n" + "Dimensioni: " + child.attrib['dimensioni']
            for element in child:
                if element.tag == 'datineccesari':
                    for nec in element:
                        testo += "\n" + "Dato Necessario: " + nec.text
                if element.tag == 'testoFormula':
                    testo += "\n" + "Testo Formula: " + element.text
            testo += "\n---------------------"
        return testo

    def listaFormuleFisica(self):
        testo = "Formule di Fisica Gravitas:"
        for child in self.root:
            #testo += "\n" + "ID: " + child.attrib['id']
            testo += "\n" + "Argomento: " + child.attrib['par1']
            testo += "\n" + "Valore: " + child.attrib['par2']
            for element in child:
                if element.tag == 'datineccesari':
                    for nec in element:
                        testo += "\n" + "Dato Necessario: " + nec.text
                if element.tag == 'testoFormula':
                    testo += "\n" + "Testo Formula: " + element.text
            testo += "\n---------------------"
        return testo

    
    # Scale e Conversioni

    def ottieniSI_utente(self, tipo_grandezza):
        for child in self.root:
            if child.attrib['tipo'] == tipo_grandezza:
                return child.attrib['si'] +  " (" + child.attrib['si_abb'] +  ")"
        return "Tipo grandezza non valido"

    def ottieniSI_sis(self, tipo_grandezza):
        for child in self.root:
            if child.attrib['tipo'] == tipo_grandezza:
                return child.attrib['si_abb']
        return "NonValido"

    def ottieni_multipli_sottomultipli(self, tipo_grandezza):
        array_finale = [{'nome' : "Chilogrammi", 'abbreviazione' : "Kg"},
                        {'nome': "Ettogrammi", 'abbreviazione': "hg"}] # Esempio
        array_finale = []

        for child in self.root:
            if child.attrib['tipo'] == tipo_grandezza:
                for element in child:
                    array_finale.append({'nome' : element.attrib['nome'],
                                         'abbreviazione' : element.text})

        print(array_finale)
        return array_finale

    def ottieniK_A(self, tipo_grandezza, partenza):
        # La partenza è l'unità del SI
        for child in self.root:
            print("Child:", child.attrib['tipo'])
            if child.attrib['tipo'] == tipo_grandezza:
                for element in child:
                    print("Element:", '-' + element.text + '-', '-' + partenza + '-')
                    if element.text == partenza:
                        return int(element.attrib['esponente'])
        print("Errore gravitasXML")
        return 8

    def ottieniK_B(self, tipo_grandezza, arrivo):
        # La partenza NON è un'unità del SI
        for child in self.root:
            #print("Child:", child.attrib['tipo'])
            if child.attrib['tipo'] == tipo_grandezza:
                for element in child:
                    #print("Element:", '-' + element.text + '-', '-' + arrivo + '-')
                    if element.text == arrivo:
                        return int(element.attrib['esponente']) * (-1)
        print("Errore gravitasXML")
        return 8
        