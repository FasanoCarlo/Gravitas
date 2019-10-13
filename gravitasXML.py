# Questo è un file secondario che andrà a contenere tutte le funzioni legate alla gestione (lettura/scrittura) dei file XML
import xml.etree.ElementTree as et
import os

class FileXML:
    path = None
    nomeFile = None
    tree = None
    root = None
    def __init__(self, nomeFile):  
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.nomeFile = os.path.join(self.path, nomeFile)
        self.tree = et.parse(self.nomeFile)
        self.root = self.tree.getroot()

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

    def trovaFormule_Par1Par2(self, forma, tipo):
        array_finale = []
        for child in self.root:
            if child.attrib['par1'] == forma and child.attrib['par2'] == tipo:
                for element in child:
                    if element.tag == 'testoFormula':
                        array_finale.append(element.text)
        return array_finale

    def trovaParametri_Par1Par2(self, forma, tipo):
        array_finale = []
        for child in self.root:
            if child.attrib['par1'] == forma and child.attrib['par2'] == tipo:
                for element in child:
                    if element.tag == 'datiNecessari':
                        for datoNecessario in element:
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