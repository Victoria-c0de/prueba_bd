from conexionbase import *
from tkinter import ttk
from tkinter import *
import time

db = BaseDatos()
ventana = Tk()
ventana.geometry("600x500")
ventana.title("Operaciones CRUD - Python - MySQL")
ventana.config(bg="#E5C06F")

#variables string
patente = StringVar()

#marco principal
marco = LabelFrame(ventana)
marco.place(
    x=50,
    y=50,
    width=500,
    height=400,
)
marco.config(bg="lightblue")


#label de patente
textpatente = Label(marco, text="Patente ")
textpatente.config(bg="lightblue")
textpatente.grid(row=1,column=1)
entrypatente = Entry(marco, textvariable=patente)
entrypatente.grid(row=1,column=2)
#relleno
relleno = Label(marco)
relleno.config(bg="lightblue")
relleno.grid(row=0,column=0)

#mensajes
#mensaje de opcion
LblMensaje= Label(marco, text="bienvenido al registro de patentes",fg="green",bg="lightblue")
LblMensaje.grid(row=2,column=0,columnspan=4)

#tabla de patentes
tvestacion = ttk.Treeview(marco)
tvestacion.grid(row=3, column=0, columnspan=4)
#columnas logicas de la tabla estudiantes
tvestacion["columns"]=("id","patente","entrada","salida","costo")
#fijar ancho de columnas
tvestacion.column("#0",width=0,stretch=NO)
tvestacion.column("id",width=40,anchor=CENTER)
tvestacion.column("patente",width=80,anchor=CENTER)
tvestacion.column("entrada",width=100,anchor=CENTER)
tvestacion.column("salida",width=100,anchor=CENTER)
tvestacion.column("costo",width=150,anchor=CENTER)
#titulos de las columnas
tvestacion.heading("#0",text="")
tvestacion.heading("id",text="ID")
tvestacion.heading("patente",text="PATENTE")
tvestacion.heading("entrada",text="ENTRADA")
tvestacion.heading("salida",text="SALIDA")
tvestacion.heading("costo",text="COSTO")

def vaciarGrilla():
    filas = tvestacion.get_children() #obtener cantidad de filas
    for fila in filas:
        tvestacion.delete(fila)
        
def cargarDatos():
    vaciarGrilla()
    sql = """SELECT * FROM parking"""
    db.cursor.execute(sql)
    filas = db.cursor.fetchall()
    for fila in filas:
        id = fila[0]
        tvestacion.insert("",END, id,text=id,values=fila)
# Función para el botón de ingreso
def ingresar_patente():
    patente = entrypatente.get()
    
    if patente:
        # Obtener la hora de ingreso
        hora_ingreso = int(time.time())

        # Insertar registro en la tabla
        #insertar en columanas id	patente	entrada	salida	costo	
        sql = "INSERT INTO parking (id, patente, entrada, salida, costo) VALUES (NULL, %s, %s, NULL, NULL)"
        db.cursor.execute(sql, (patente, hora_ingreso))
        db.conn.commit()
        
        print("Ingreso", f"Vehículo con patente {patente} ingresado correctamente.")
    else:
        print("Error", "Por favor, ingresa una patente válida.")        

    #cargar datos
    cargarDatos()
    #limpiar campos
    entrypatente.delete(0, END)
#botones
ingreso_button = Button(marco, text="Ingreso", command=ingresar_patente)
ingreso_button.grid(row = 1, column = 3)


































#boton de egreso
egreso_button = Button(marco, text="Ingreso", command=egreso_button)
egreso_button.grid(row = 1, column = 3)

#funcion del costo
def calcularCosto(hora_ingreso, hora_egreso):
    # Calcular el tiempo de permanencia
    tiempo_permanencia = hora_egreso - hora_ingreso

    # Calcular el costo
    costo = 0
    if tiempo_permanencia < 240:
        costo = 100
    else:
        costo = tiempo_permanencia * 10

    return costo
# Función para el botón de egreso
def egreso_patente():
    patente = entrypatente.get()
    
    if patente:
        # Obtener la hora de egreso
        hora_egreso = int(time.time())

        # Insertar registro en la tabla
        #insertar en columanas id	patente	entrada	salida	costo	
        sql = "UPDATE parking SET salida = %s WHERE patente = %s"
        db.cursor.execute(sql, (hora_egreso, patente))
        db.conn.commit()
        
        print("Egreso", f"Vehículo con patente {patente} egresado correctamente.")
    else:
        print("Error", "Por favor, ingresa una patente válida.")        

    #cargar datos
    cargarDatos()
    #limpiar campos
    entrypatente.delete(0, END)





































cargarDatos()
ventana.mainloop()