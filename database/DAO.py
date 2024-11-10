from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` desc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShapeYear(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """select distinct s.shape from sighting s where year(s.`datetime`) = %s and s.shape != "" order by s.shape asc """
            cursor.execute(query, (anno,))
            for row in cursor:
                result.append(row[0])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(anno, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary = True)
            query = """select s.* from sighting s where year(s.`datetime`) = %s and s.shape = %s"""
            cursor.execute(query, (anno, shape,))
            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getArchi(anno, shape, map):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary = True)
            query = """select s.id as sig1, s2.id as sig2, (s2.longitude-s.longitude) as peso from sighting s, sighting s2 
                        where s.id != s2.id and s.state = s2.state and s.shape = %s and s.shape = s2.shape 
                        and year(s.datetime) = %s and year(s.datetime) = year(s2.datetime) and s.longitude < s2.longitude"""
            cursor.execute(query, (shape, anno,))
            for row in cursor:
                sigh1 = map[row['sig1']]
                sigh2 = map[row['sig2']]
                peso = row['peso']
                result.append((sigh1, sigh2, peso))
            cursor.close()
            cnx.close()
        return result