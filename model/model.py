from database.distributore_DAO import DistributoreDAO
from database.prezzo_DAO import PrezzoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1 #nessun costo è ancora stato salvato

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        prezzo_medio = PrezzoDAO.get_prezzo_medio_mese(mese)
        return prezzo_medio

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        if giorno == 8: #condizione di terminazione: quando arrivo al giorno 8 mi fermo
            #controlla se è il primo tentativo in assoluto oppure se ho trovato un costo totale inferiore rispetto al record precedente
            if self.__costo_ottimo ==-1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale) #copia la lista dei distributori convenienti

        else:
            #scorro tutti i distributori disponibili
            for distributore in prezzi_settimana:
                prezzo_litro = prezzi_settimana[distributore][giorno - 1] #estraggo i relativi prezzi al litro giornaliero
                costo_variabile = prezzo_litro * 100
                costo_spostamento = 0
                if ultimo_distributore is not None and distributore != ultimo_distributore: #controllo che non sia il primo giorno
                    costo_spostamento = 5

                costo_totale = costo_corrente + costo_variabile + costo_spostamento

                sequenza_parziale.append(distributore) #aggiungo temporaneamente il distributore alla sequenza parziale
                self.__ricorsione(sequenza_parziale, giorno+1, distributore, costo_totale, prezzi_settimana)
                sequenza_parziale.pop() #backtracking, utile per esplorare tutte le strade e capire la migliore


    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        prezzi_prima_settimana = PrezzoDAO.get_prezzi_primaSettimana(mese)
        diz_prezzi  = {}

        for riga in prezzi_prima_settimana:
            id_distributore = riga[0]
            prezzo = riga[2]
            if id_distributore not in diz_prezzi:
                diz_prezzi[id_distributore] = []

            #aggiungo il prezzo alla lista di quel distributore
            diz_prezzi[id_distributore].append(prezzo)

        return diz_prezzi