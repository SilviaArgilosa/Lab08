from database.DB_connect import DBConnect
from model.prezzo_DTO import Prezzo

"""
    PREZZO DAO
    Gestisce le operazioni di accesso alla tabella prezzo.
"""

class PrezzoDAO:
    @staticmethod
    def get_prezzi(id_distributore) -> list[Prezzo] | None:
        """
        Restituisce tutti i prezzi di un distributore
        :return: lista di tutti i Prezzi di un certo distributore
        """
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM prezzo WHERE id_distributore = %s"""
        try:
            cursor.execute(query, (id_distributore,))
            for row in cursor:
                prezzo = Prezzo(
                    data=row["data"],
                    prezzo_litro=float(row["prezzo_litro"]),
                    id_distributore=row["id_distributore"],
                )
                result.append(prezzo)
        except Exception as e:
            print(f"Errore durante la query get_prezzi: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    def get_prezzo_medio_mese(mese):
        cnx = DBConnect.get_connection()
        prezzo_medio = []
        cursor = cnx.cursor()

        query = """select d.nome, AVG(p.prezzo_litro)
                   from distributore d, prezzo p
                   where d.id = p.id_distributore and MONTH(p.data) = %s
                   group by d.id, d.nome"""

        try:
            cursor.execute(query, (mese,)) #ogni riga del cursore è già una tupla
            for row in cursor:
                prezzo_medio.append(row)

        except Exception as e:
            print(f"Errore durante la query get_prezzi: {e}")
            prezzo_medio = None
        finally:
            cursor.close()
            cnx.close()

        return prezzo_medio


    def get_prezzi_primaSettimana(mese):
        cnx = DBConnect.get_connection()
        prezzi_Primasettimana = []
        cursor = cnx.cursor()

        query = """select d.id, d.nome, p.prezzo_litro
                   from distributore d, prezzo p
                   where d.id = p.id_distributore and MONTH(p.data)= %s and DAY(p.data) <= 7"""

        try:
            cursor.execute(query, (mese,))
            for row in cursor:
                prezzi_Primasettimana.append(row)

        except Exception as e:
            print(f"Errore durante la query get_prezzi: {e}")
            prezzi_Primasettimana = None
        finally:
            cursor.close()
            cnx.close()

        return prezzi_Primasettimana
