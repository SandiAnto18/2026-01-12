
from database.DB_connect import DBConnect
from model.Constructor import Constructor


class DAO():

    @staticmethod
    def getAllYears():
        # Recupero tutti gli anni disponibili nel database
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct s.year
FROM seasons s
ORDER BY s.year
        """

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getConstructorForYear(da, a):
        # Recupero i costruttori che hanno risultati nel periodo selezionato
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.*
FROM constructors c, results r, races rc
WHERE c.constructorId = r.constructorId
AND rc.raceId = r.raceId
AND rc.year BETWEEN %s AND %s
AND r.`position` IS NOT NULL
        """

        cursor.execute(query, (da, a))

        # Converto ogni riga in un oggetto Constructor
        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getC1C2peso(da, a):
        # Recupero le coppie di costruttori e il numero di piloti condivisi
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.constructorId AS c1,
c2.constructorId AS c2,
COUNT(DISTINCT r.driverId) AS peso
FROM constructors c, results r, races rc,
results r2, constructors c2, races rc2
WHERE c.constructorId = r.constructorId
AND rc.raceId = r.raceId
AND rc.year BETWEEN %s AND %s
AND r.`position` IS NOT NULL
AND r.driverId = r2.driverId
AND c2.constructorId = r2.constructorId
AND rc2.raceId = r2.raceId
AND rc2.year BETWEEN %s AND %s
AND r2.constructorId = c2.constructorId
AND r2.`position` IS NOT NULL
AND c.constructorId < c2.constructorId
GROUP BY c1, c2
        """

        cursor.execute(query, (da, a, da, a))

        # Restituisco tuple: ID primo costruttore, ID secondo, peso
        for row in cursor:
            results.append((row["c1"], row["c2"], row["peso"]))

        cursor.close()
        conn.close()
        return results







