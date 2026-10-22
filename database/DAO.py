from database.DB_connect import DBConnect
from model.Constructor import Constructor


class DAO():

    @staticmethod
    def getAllYears():
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
    def getConstructorForYear(da,a):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.*
FROM constructors c ,results r, races rc
where c.constructorId =r.constructorId 
and rc.raceId = r.raceId 
and rc.year between %s and %s
and r.`position` is not null
        """

        cursor.execute(query,(da,a))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results
    #output contrusctor come oggetto

    @staticmethod
    def getC1C2peso(da,a):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.constructorId as c1,c2.constructorId as c2,count(distinct r.driverId) as peso
FROM constructors c ,results r, races rc,
results r2,constructors c2 , races rc2
where c.constructorId =r.constructorId 
and rc.raceId = r.raceId 
and rc.year between %s and %s
and r.`position` is not null
and r.driverId =r2.driverId
and c2.constructorId =r2.constructorId 
and rc2.raceId =r2.raceId 
and rc2.year between %s and %s
and r2.constructorId =c2.constructorId 
and r2.`position` is not null
and c.constructorId < c2.constructorId 
group by c1,c2
        """

        cursor.execute(query,(da,a,da,a))

        for row in cursor:
            results.append((row["c1"],row["c2"],row["peso"]))

        cursor.close()
        conn.close()
        return results







