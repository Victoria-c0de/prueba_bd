import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host= "localhost",
        user= "root",
        # password = "",
        port = "3306",
        database = "parkdb”,
    )

     print( conn.is_connected() )
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")

    
    for ele in cursor:
        print( ele )

    if conn.is_connected():
        conn.close()

except Error as ex:
   print("Error durante la conexion:", format(ex))


#El programa debe calcular el monto a cobrar por el tiempo de permanencia de un vehículo
#en el estacionamiento
#el egreso es pagado siempre.
#El monto a cobrar se calcula de la siguiente manera:
#Por permanencias inferiores a 4 minutos se cobran $100. 
