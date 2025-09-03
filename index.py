import tkinter as tk

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

# Crear la tabla dentro del frame
t = Table(table_frame)

mainwin.mainloop()
