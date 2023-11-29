from conexionbase import *
from tkinter import ttk
from tkinter import *
import time
# integrantes = victoria molina, maximiliano campos
db = BaseDatos()
ventana = Tk()
ventana.geometry("600x500")
ventana.title("Operaciones CRUD - Python - MySQL")
ventana.config(bg="#E5C06F")

#variables string
patente = StringVar()
entrada = StringVar()

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

def vaciarGrilla(): #limpiar tabla
    filas = tvestacion.get_children() #obtener cantidad de filas
    for fila in filas:
        tvestacion.delete(fila)
        
def cargarDatos(): #recarga de datos
    vaciarGrilla()
    sql = """SELECT * FROM parking"""
    db.cursor.execute(sql)
    filas = db.cursor.fetchall()
    for fila in filas:
        id = fila[0]
        tvestacion.insert("",END, id,text=id,values=fila)

def egreso_patente():# revisar egresos
    if validar():
        hora_egreso = int(time.time())
        costo = calcularcosto()
        val = (hora_egreso, costo,int(tvestacion.selection()[0]))
        sql = """UPDATE parking SET salida=%s, costo=%s WHERE id=%s"""
        db.cursor.execute(sql,val)
        cargarDatos()
        entrypatente.delete(0, END)
        LblMensaje.config(text="Patente egresada correctamente",fg="green")
        db.conn.commit()
    else:

        try:
            selected_item = tvestacion.focus()
            item_details = tvestacion.item(selected_item)
            tupled_items = item_details.get("values")
            entrypatente.delete(0, END)
            entrypatente.insert(0, tupled_items[1])

        except IndexError:
            LblMensaje.config(text="Ingreso de patente no valida",fg="red")
            
        #cargar datos

def validar(): #validacion interna
    r = len(patente.get())
    return r

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
        
        LblMensaje.config(text=f"Vehículo con patente {patente} ingresado correctamente.",fg="green")
    else:
        LblMensaje.config(text="Por favor, ingresa una patente válida.",fg="red")        

    #cargar datos
    cargarDatos()
    #limpiar campos
    entrypatente.delete(0, END)

def calcularcosto(): #calculo de costo por tiempo en minutos
    val = int(tvestacion.selection()[0])
    sql = f"""select entrada from parking where id={val}"""
    db.cursor.execute(sql)
    horas = db.cursor.fetchone()[0]
    hora_ingreso = horas
    hora_egreso = int(time.time())
    tiempo = (hora_egreso-hora_ingreso)/60
    if tiempo < 4:
        costo = 100*tiempo
    else:
        costo = tiempo*30
    return costo
#boton ingreso
ingreso_button = Button(marco, text="Ingreso", command=ingresar_patente)
ingreso_button.grid(row = 1, column = 3)

#boton de egreso
egreso_button = Button(marco, text="Egreso", command=egreso_patente)
egreso_button.grid(row = 4, column = 1, columnspan = 3)

cargarDatos()
ventana.mainloop()