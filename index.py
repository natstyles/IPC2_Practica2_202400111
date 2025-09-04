#Importamos solo tkinter
import tkinter as tk
#Importamos ttk para el combobox
from tkinter import ttk

# Ventana principal
mainwin = tk.Tk()
mainwin.geometry("700x300")

# Labels con pack (en el contenedor principal)
label = tk.Label(mainwin, text="Clínica general", font=('Arial', 14, 'bold'))
label.pack(pady=5)

label1 = tk.Label(mainwin, text="Revisa el tiempo de atención en la siguiente tabla para la especialidad a la que vienes:", font=('Arial', 12))
label1.pack(pady=5)

# Frame para la tabla (aquí sí usamos grid)
table_frame = tk.Frame(mainwin)
table_frame.pack(pady=10)

# Datos
lst = [("Especialidad", "Tiempo estimado"),
       ("Medicina general", "10 minutos"),
       ("Pediatría", "15 minutos"),
       ("Ginecología", "20 minutos"),
       ("Dermatología", "25 minutos")]

total_rows = len(lst)
total_columns = len(lst[0])

class Table:
    def __init__(self, parent):
        for i in range(total_rows):
            for j in range(total_columns):
                e = tk.Entry(parent, width=25, font=('Arial', 12, 'bold'))
                e.grid(row=i, column=j, padx=4, pady=2, sticky="w")
                e.insert(tk.END, lst[i][j])
                #Quiero que no toquen los valores ded los entrys que hacen la tabla:
                e.config(state="readonly")


#Generación de los pacientes
#clase nuevo paciente:
class paciente:
    def __init__(self, nombre, edad, especialidad, tiempo_espera):
        self.nombre = nombre
        self.edad = edad
        self.especialidad = especialidad
        self.tiempo_espera = tiempo_espera

#Como vamos a usar FIFO, tenemos que usar colas
class cola:
    def __init__(self):
        self.cola = []

    def encolar(self, paciente):
        self.cola.append(paciente)

    def desencolar(self):
        self.cola.pop(0)    #El indice 0 en el pop es lo que diferencia una pila de una cola literal xd

#Creación de ventana para guardar clientes
def ventana_cliente():
    newclientwin = tk.Toplevel()
    newclientwin.geometry("600x300")

    label = tk.Label(newclientwin, text="Generar nuevo cliente", font=('Arial', 14, 'bold'))
    label.pack(pady=5) #Usamo pady paa los margenes
    label1 = tk.Label(newclientwin, text="Llena los campos requeridos para continuar:", font=('Arial', 12))
    label1.pack(pady=5)

    label2 = tk.Label(newclientwin, text="Nombre de cliente: ")
    label2.pack(pady=2)
    txtBoxNombreCliente = tk.Entry(newclientwin, font=('Arial', 10))
    txtBoxNombreCliente.pack(pady=2)
    label2 = tk.Label(newclientwin, text="Edad: ")
    label2.pack(pady=2)
    txtBoxEdadCliente = tk.Entry(newclientwin, font=('Arial', 10))
    txtBoxEdadCliente.pack(pady=2)
    label2 = tk.Label(newclientwin, text="Nombre de cliente: ")
    label2.pack(pady=2)

    #Valores del combobox
    opciones = ["Selecciona una opción", "Medicina general", "Pediatría", "Ginecología", "Dermatología"]
    comboBoxEspecialidad = ttk.Combobox(newclientwin, values = opciones, state='readonly')
    comboBoxEspecialidad.current(0)
    comboBoxEspecialidad.pack(pady=2)

    #Boton para agregar paciente a la cola:
    boton1 = tk.Button(newclientwin, text="Añadir paciente a la cola!")
    boton1.pack(pady=2)

#Creamos boton para generar un nuevo paciente
boton1 = tk.Button(mainwin, text = "Generar nuevo paciente", command = ventana_cliente)
boton1.pack()



# Crear la tabla dentro del frame
t = Table(table_frame)

mainwin.mainloop()
