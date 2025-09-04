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

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("812x516")
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
        tk.Button(self.root, text = "Generar nuevo paciente", font=("Arial", 12, "bold"),command = self.ventana_cliente).pack()   

        #Mostramos tabla donde saldrán los pacientes por atender
        tk.Label(self.root, text="Cola actual de pacientes", font=("Arial", 12, "bold")).pack(pady=10)
        self.cola_frame = tk.Frame(self.root)
        self.cola_frame.pack(pady=5, fill="both", expand=False)

        self.tree = ttk.Treeview(self.cola_frame, columns=("Nombre", "Edad", "Especialidad", "Espera"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Especialidad", text="Especialidad")
        self.tree.heading("Espera", text="Tiempo espera (min)")
        self.tree.pack(fill="both", expand=False)

        #Variables de formulario
        self.nombre_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.especialidad_var = tk.StringVar(value="Selecciona una opción")

    #Ventana generar un paciente
    def ventana_cliente(self):
        newclientwin = tk.Toplevel(self.root)
        newclientwin.geometry("600x300")
        newclientwin.title("Nuevo paciente")

        #Aqui reiniciamos los valores
        self.nombre_var.set("")
        self.edad_var.set("")
        self.especialidad_var.set("Selecciona una opción")

        label = tk.Label(newclientwin, text="Generar nuevo paciente", font=('Arial', 14, 'bold'))
        label.pack(pady=5)
        label1 = tk.Label(newclientwin, text="Llena los campos requeridos para continuar:", font=('Arial', 12))
        label1.pack(pady=5)

        #Nombre
        tk.Label(newclientwin, text="Nombre de paciente: ").pack(pady=2)
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

        edad = int(edad_txt)

        #Tiempo de espera por cada especialidad
        tiempos_especialidad = {
            "Medicina general": 10,
            "Pediatría": 15,
            "Ginecología": 20,
            "Dermatología": 25
        }
        base = tiempos_especialidad.get(especialidad, 0)

        #Acumulamos los tiempos que tenga de espera el paciente anterior + el nuevo paciente
        espera_anterior = self.cola.cola[-1].tiempo_espera if self.cola.cola else 0
        tiempoEspera = espera_anterior + base

        #Creamos paciente y lo encolamos
        paciente = Cliente(nombre, edad, especialidad, tiempoEspera)
        self.cola.encolar(paciente)

        #Feedback
        messagebox.showinfo("Paciente agregado!", f"Se agregó a la cola:\n"
            f"• Nombre: {paciente.nombre}\n"
            f"• Edad: {paciente.edad}\n"
            f"• Especialidad: {paciente.especialidad}\n"
            f"• Tiempo espera: {paciente.tiempo_espera} mins\n\n"
            f"Total en cola: {len(self.cola.cola)}"
        )

        #Actualizamos la tabla!
        self.actualizarTabla()

    #Función para actualizar la tabla
    def actualizarTabla(self):
        #Borramos todo antes de iniciar
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not self.cola.cola:
            #Cola vacía
            self.tree.insert("", "end", values=("No hay pacientes por atender", "", "", ""))
        else:
            #Mostramos todos los pacientes:
            for paciente in self.cola.cola:
                self.tree.insert(
                    "", "end",
                    values=(paciente.nombre, paciente.edad, paciente.especialidad, paciente.tiempo_espera)
                )

if __name__ == "__main__":
    mainwin = tk.Tk()
    app = App(mainwin)
    mainwin.mainloop()