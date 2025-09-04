#Importamos solo tkinter
import tkinter as tk
#Importamos ttk para el combobox
from tkinter import ttk
#Importamos messageboxes
from tkinter import messagebox

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
class Cliente:
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
class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x300")
        self.root.title("Clínica general")

        #Cola de pacientes
        self.cola = cola()

        tk.Label(self.root, text="Clínica general", font=('Arial', 14, 'bold')).pack(pady=5)
        tk.Label(self.root, text="Revisa el tiempo de atención en la siguiente tabla para la especialidad a la que vienes:", font=('Arial', 12)).pack(pady=5)

        #Tabla
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10)
        Table(table_frame)

        #Creamos boton para generar un nuevo paciente
        tk.Button(self.root, text = "Generar nuevo paciente", command = self.ventana_cliente).pack()   

        #Variables de formulario
        self.nombre_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.especialidad_var = tk.StringVar(value="Selecciona una opción")

    #Ventana generar un cliente
    def ventana_cliente(self):
        newclientwin = tk.Toplevel(self.root)
        newclientwin.geometry("600x300")
        newclientwin.title("Nuevo paciente")

        #Aqui reiniciamos los valores
        self.nombre_var.set("")
        self.edad_var.set("")
        self.especialidad_var.set("Selecciona una opción")

        label = tk.Label(newclientwin, text="Generar nuevo cliente", font=('Arial', 14, 'bold'))
        label.pack(pady=5)
        label1 = tk.Label(newclientwin, text="Llena los campos requeridos para continuar:", font=('Arial', 12))
        label1.pack(pady=5)

        #Nombre
        tk.Label(newclientwin, text="Nombre de cliente: ").pack(pady=2)
        entry_nombre = tk.Entry(newclientwin, font=('Arial', 10), textvariable=self.nombre_var)
        entry_nombre.pack(pady=2)

        #Edad
        tk.Label(newclientwin, text="Edad: ").pack(pady=2)
        tk.Entry(newclientwin, font=('Arial', 10), textvariable=self.edad_var).pack(pady=2)

        #Valores del combobox
        tk.Label(newclientwin, text="Especialidad: ").pack(pady=2)
        opciones = ["Selecciona una opción", "Medicina general", "Pediatría", "Ginecología", "Dermatología"]
        combo = ttk.Combobox(newclientwin, values=opciones, state='readonly', textvariable=self.especialidad_var)
        combo.current(0)
        combo.pack(pady=2)

        # Botón para agregar paciente a la cola:
        tk.Button(newclientwin, text="Añadir paciente a la cola!", command=self.guardar_cliente).pack(pady=10)

        entry_nombre.focus_set()

    #Función para guardar cliente
    def guardar_cliente(self):
        nombre = self.nombre_var.get().strip()
        edad_txt = self.edad_var.get().strip()
        especialidad = self.especialidad_var.get()

        #Validamos si puso los datos necesarios
        if not nombre:
            messagebox.showwarning("Faltan datos", "El nombre es obligatorio.")
            return
        if not edad_txt.isdigit():
            messagebox.showwarning("Dato inválido", "La edad debe ser un número entero.")
            return
        if especialidad == "Selecciona una opción":
            messagebox.showwarning("Faltan datos", "Selecciona una especialidad.")
            return

        if especialidad == "Medicina general":
            tiempoEspera = 10
        elif especialidad == "Pediatría":
            tiempoEspera = 15
        elif especialidad == "Ginecología":
            tiempoEspera = 20
        elif especialidad == "Dermatología":
            tiempoEspera = 25
        
        
        edad = int(edad_txt)

        #Creamos paciente y lo encolamos
        paciente = Cliente(nombre, edad, especialidad, tiempoEspera)
        self.cola.encolar(paciente)

        #Feedback
        messagebox.showinfo("Cliente agregado", f"Se agregó a la cola:\n"
            f"• Nombre: {paciente.nombre}\n"
            f"• Edad: {paciente.edad}\n"
            f"• Especialidad: {paciente.especialidad}\n"
            f"• Tiempo espera: {paciente.tiempo_espera}\n\n"
            f"Total en cola: {len(self.cola.cola)}"
        )

if __name__ == "__main__":
    mainwin = tk.Tk()
    app = App(mainwin)
    mainwin.mainloop()