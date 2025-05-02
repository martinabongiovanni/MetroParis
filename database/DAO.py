from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def hasConnessione(u: Fermata, v:Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM connessione c
                WHERE c.id_stazP = &s and c.id_stazA = %s"""

        cursor.execute(query, (u.id_fermata, v.id_fermata))

        for row in cursor:
            result.append(Fermata(**row))
            # ho ottenuto così una lista di oggetti di tipo Fermata

        cursor.close()
        conn.close()
        # mi interessa restituire solo la lunghezza della lista, quindi non faccio return result, ma faccio:
        return len(result) > 0 # mi restituisce un booleano!

    @staticmethod
    def getVicini(u: Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT * 
                FROM connessione c
                WHERE c.id_stazP = &s """

        cursor.execute(query, (u.id_fermata, ))

        for row in cursor:
            result.append(Connessione(**row))
            # ho ottenuto così una lista di oggetti di tipo Connessione

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT * 
                    FROM connessione c"""

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
            # ho ottenuto così una lista di oggetti di tipo Connessione, sono tutti gli archi possibili

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesPesati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT id_stazP, id_stazA, COUNT(*) as n 
                    FROM connessione c
                    GROUP BY id_stazP, id_stazA
                    order by n desc
                    """

        cursor.execute(query)

        for row in cursor:
            result.append((row["id_stazP"], row["id_stazA"], row["n"]))
            # ho ottenuto così una tupla di nodo di partenza, di arrivo e peso dell'arco

        cursor.close()
        conn.close()
        return result