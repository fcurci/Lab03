import csv
import operator

class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice_strumento=codice
        self.tipo_strumento=tipo
        self.marca_strumento=marca
        self.anno_acquisto_strumento=int(anno_acquisto)
        self.valore_strumento=float(valore)
    def __str__(self):
        return f"{self.codice_strumento}, {self.tipo_strumento}, {self.marca_strumento}, {self.anno_acquisto_strumento}, {self.valore_strumento}"

class Prestito:
    def __init__(self, codice_p, data, id_strumento, cognome_allievo):
        self.codice_prestito=codice_p
        self.data_prestito=data
        self.codice_strumento_prestito=id_strumento
        self.studente_prestito=cognome_allievo

    def __str__(self):
        return f"{self.codice_prestito}, {self.data_prestito}, {self.codice_strumento_prestito}, {self.studente_prestito}"



class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self.nome_deposito=nome
        self.responsabile_deposito=responsabile
        self.strumenti_deposito=[]
        self.prestiti_deposito=[]

    def carica_file_strumenti(self, file_path):
        try:
            f=open(file_path,"r",encoding="utf-8")
            reader=csv.DictReader(f,fieldnames=["codice","tipo","marca","anno_acquisto","valore"])

            for line in reader:
                nuovo=Strumento(line["codice"], line["tipo"], line["marca"], line["anno_acquisto"], line["valore"])
                self.strumenti_deposito.append(nuovo)

            f.close()
        except FileNotFoundError:
            raise Exception("File non valido")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):

        if len(self.strumenti_deposito)==0:
            codice="S1"
        else:
            ultimo_codice=self.strumenti_deposito[-1].codice_strumento
            numero=int(ultimo_codice[1:])+1
            codice="S"+str(numero)

        nuovo=Strumento(codice, tipo, marca, anno_acquisto, valore)
        self.strumenti_deposito.append(nuovo)

        return nuovo

    def strumenti_ordinati_per_marca(self):
        return sorted(self.strumenti_deposito,key=operator.attrgetter("marca_strumento"))


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        if len(self.prestiti_deposito)==0:
            codice="P1"
        else:
            ultimo_codice=self.prestiti_deposito[-1].codice_prestito
            numero=int(ultimo_codice[1:])+1
            codice="P"+str(numero)

        controllo_presenza=0
        controllo_prestito=0

        for strumento in self.strumenti_deposito:
            if id_strumento==strumento.codice_strumento:
                controllo_presenza=1

        for prestito in self.prestiti_deposito:
            if id_strumento==prestito.codice_strumento_prestito:
                controllo_prestito=1

        if controllo_presenza==1 and controllo_prestito==0:
            nuovo=Prestito(codice, data, id_strumento, cognome_allievo)
            self.prestiti_deposito.append(nuovo)
            return nuovo
        if controllo_presenza==0:
            raise Exception("Strumento inesistente")
        if controllo_prestito==1:
            raise Exception("Strumento già in prestito")

    def termina_prestito(self, id_prestito):

        esistenza=0

        for prestito in self.prestiti_deposito:
            if id_prestito==prestito.codice_prestito:
                self.prestiti_deposito.remove(prestito)
                esistenza=1

        if esistenza==1:
            return id_prestito
        else:
            raise Exception("Prestito non trovato")