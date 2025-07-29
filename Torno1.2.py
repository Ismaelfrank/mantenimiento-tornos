import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime

# Conexión a la base de datos
conn = sqlite3.connect('mantenimiento_torno.db')
cursor = conn.cursor()

# Crear tablas
cursor.execute('''CREATE TABLE IF NOT EXISTS mantenimiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    torno_id TEXT,
    fecha TEXT,
    tipo TEXT,
    descripcion TEXT,
    repuestos TEXT,
    tecnico TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS programacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    torno_id TEXT,
    fecha_proxima TEXT,
    tipo TEXT
)''')
conn.commit()

# Funciones
def registrar_mantenimiento():
    def guardar():
        datos = (
            entry_torno.get(),
            entry_fecha.get(),
            combo_tipo.get().lower(),
            entry_desc.get(),
            entry_repuestos.get(),
            entry_tecnico.get()
        )
        cursor.execute('''INSERT INTO mantenimiento 
                          (torno_id, fecha, tipo, descripcion, repuestos, tecnico) 
                          VALUES (?, ?, ?, ?, ?, ?)''', datos)
        conn.commit()
        messagebox.showinfo("Éxito", "Mantenimiento registrado.")
        ventana.destroy()

    ventana = tk.Toplevel(root)
    ventana.title("Registrar Mantenimiento")

    tk.Label(ventana, text="Torno ID").grid(row=0, column=0)
    tk.Label(ventana, text="Fecha (YYYY-MM-DD)").grid(row=1, column=0)
    tk.Label(ventana, text="Tipo").grid(row=2, column=0)
    tk.Label(ventana, text="Descripción").grid(row=3, column=0)
    tk.Label(ventana, text="Repuestos").grid(row=4, column=0)
    tk.Label(ventana, text="Técnico").grid(row=5, column=0)

    entry_torno = tk.Entry(ventana)
    entry_fecha = tk.Entry(ventana)
    combo_tipo = ttk.Combobox(ventana, values=["preventivo", "correctivo"])
    entry_desc = tk.Entry(ventana)
    entry_repuestos = tk.Entry(ventana)
    entry_tecnico = tk.Entry(ventana)

    entry_torno.grid(row=0, column=1)
    entry_fecha.grid(row=1, column=1)
    combo_tipo.grid(row=2, column=1)
    entry_desc.grid(row=3, column=1)
    entry_repuestos.grid(row=4, column=1)
    entry_tecnico.grid(row=5, column=1)

    tk.Button(ventana, text="Guardar", command=guardar).grid(row=6, column=0, columnspan=2)

def consultar_historial():
    opcion = simpledialog.askstring("Consulta", "Consultar por:\n1. ID del torno\n2. Rango de fechas (1/2):")

    if opcion == '1':
        torno_id = simpledialog.askstring("Consulta", "Ingrese ID del torno:")
        cursor.execute('SELECT * FROM mantenimiento WHERE torno_id = ?', (torno_id,))
    elif opcion == '2':
        fecha_inicio = simpledialog.askstring("Consulta", "Fecha inicio (YYYY-MM-DD):")
        fecha_fin = simpledialog.askstring("Consulta", "Fecha fin (YYYY-MM-DD):")
        cursor.execute('SELECT * FROM mantenimiento WHERE fecha BETWEEN ? AND ?', (fecha_inicio, fecha_fin))
    else:
        messagebox.showerror("Error", "Opción inválida.")
        return

    registros = cursor.fetchall()
    if registros:
        resultado = ""
        for r in registros:
            resultado += f"ID:{r[0]} Torno:{r[1]} Fecha:{r[2]} Tipo:{r[3]} Descripción:{r[4]} Repuestos:{r[5]} Técnico:{r[6]}\n"
        mostrar_resultado("Historial de Mantenimiento", resultado)
    else:
        messagebox.showinfo("Resultado", "No se encontraron registros.")

def programar_mantenimiento():
    def guardar():
        datos = (
            entry_torno.get(),
            entry_fecha.get(),
            combo_tipo.get().lower()
        )
        cursor.execute('INSERT INTO programacion (torno_id, fecha_proxima, tipo) VALUES (?, ?, ?)', datos)
        conn.commit()
        messagebox.showinfo("Éxito", "Mantenimiento programado.")
        ventana.destroy()

    ventana = tk.Toplevel(root)
    ventana.title("Programar Mantenimiento")

    tk.Label(ventana, text="Torno ID").grid(row=0, column=0)
    tk.Label(ventana, text="Fecha Próxima (YYYY-MM-DD)").grid(row=1, column=0)
    tk.Label(ventana, text="Tipo").grid(row=2, column=0)

    entry_torno = tk.Entry(ventana)
    entry_fecha = tk.Entry(ventana)
    combo_tipo = ttk.Combobox(ventana, values=["preventivo", "correctivo"])

    entry_torno.grid(row=0, column=1)
    entry_fecha.grid(row=1, column=1)
    combo_tipo.grid(row=2, column=1)

    tk.Button(ventana, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2)

def generar_alertas():
    hoy = datetime.today().date()
    alerta_dias = 30
    cursor.execute('SELECT torno_id, fecha_proxima, tipo FROM programacion')
    programaciones = cursor.fetchall()

    alertas = ""
    for torno_id, fecha_str, tipo in programaciones:
        fecha_proxima = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        dias = (fecha_proxima - hoy).days
        if 0 <= dias <= alerta_dias:
            alertas += f"ALERTA: {tipo} para torno {torno_id} el {fecha_str} (en {dias} días)\n"

    if alertas:
        mostrar_resultado("Alertas de Mantenimiento", alertas)
    else:
        messagebox.showinfo("Alertas", "No hay alertas próximas.")

def mostrar_resultado(titulo, texto):
    ventana = tk.Toplevel(root)
    ventana.title(titulo)
    tk.Text(ventana, width=80, height=20).pack()
    texto_widget = tk.Text(ventana)
    texto_widget.insert(tk.END, texto)
    texto_widget.config(state='disabled')
    texto_widget.pack()

# Interfaz principal
root = tk.Tk()
root.title("Sistema de Mantenimiento de Tornos")

tk.Label(root, text="Seleccione una opción:", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Registrar Mantenimiento", width=30, command=registrar_mantenimiento).pack(pady=5)
tk.Button(root, text="Consultar Historial", width=30, command=consultar_historial).pack(pady=5)
tk.Button(root, text="Programar Mantenimiento", width=30, command=programar_mantenimiento).pack(pady=5)
tk.Button(root, text="Generar Alertas", width=30, command=generar_alertas).pack(pady=5)
tk.Button(root, text="Salir", width=30, command=root.destroy).pack(pady=10)

root.mainloop()

# Cierre de base de datos
conn.close()
