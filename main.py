import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import perceptron as pa
from tkinter import ttk

archivo = ""


def open_file():
    global archivo
    archivo = filedialog.askopenfilename()
    file_label.config(text=f"Archivo seleccionado: {archivo}")


window = tk.Tk()
window.title("Perceptrón")
#window.state("zoomed")
window.geometry("1000x700")
button_font = ("Arial", 12, "bold")
frame_bg_color = "#d9d9d9"

top_frame = tk.Frame(window)
top_frame.pack(side=tk.TOP, padx=7)

frame_parametros = tk.LabelFrame(top_frame, text="Parámetros", bg=frame_bg_color)
frame_parametros.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

rate_label = tk.Label(frame_parametros, text="Tasa de aprendizaje:", bg=frame_bg_color)
rate_label.grid(row=0, column=0, sticky="w")
rate_entry = tk.Entry(frame_parametros)
rate_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

file_button = tk.Button(frame_parametros, text="Seleccionar archivo", command=open_file)
file_button.grid(row=1, column=0, padx=10, sticky="w")

file_label = tk.Label(frame_parametros, text="", wraplength=300, justify="center", bg=frame_bg_color)
file_label.grid(row=1, column=1, pady=10, sticky="w")

error_label = tk.Label(frame_parametros, text="Error permitido:", bg=frame_bg_color)
error_label.grid(row=0, column=2, sticky="w")
error_entry = tk.Entry(frame_parametros)
error_entry.grid(row=0, column=3, padx=10, sticky="w")

i_label = tk.Label(frame_parametros, text="Iteraciones:", bg=frame_bg_color)
i_label.grid(row=0, column=4, sticky="w")
i_entry = tk.Entry(frame_parametros)
i_entry.grid(row=0, column=5, padx=10, pady=10, sticky="w")


def print_graphs(tasa_aprendizaje, error, iteraciones_n):
    pesos, errores = pa.execute(archivo, tasa_aprendizaje, error, iteraciones_n)
    pesos = np.array(pesos)
    errores = np.array(errores)
    iteraciones = np.arange(1, len(errores) + 1)

    for widget in graphics_frame.winfo_children():
        widget.destroy()

    # Grafica de error
    fig, ax = plt.subplots(figsize=(4,3))
    ax.set_title("Evolución de error")
    plt.grid(True)
    ax.set_xlabel("Iteraciones")
    ax.set_ylabel("Errores")

    ax.plot(iteraciones, errores, label="Error", color="red")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=graphics_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Grafica de pesos
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.set_title("Evolución de pesos")
    plt.grid(True)
    ax.set_xlabel("Iteraciones")
    ax.set_ylabel("Pesos")

    for i in range(len(pesos[0])):
        ax.plot(iteraciones, pesos[:, i], label=f"W{i}")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=graphics_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    # tabla de datos finales
    for widget in table_frame.winfo_children():
        widget.destroy()

    w_label = tk.Label(table_frame, text="Pesos iniciales y finales")
    w_label.pack()
    w_table = ttk.Treeview(table_frame)
    w_table.configure(height=2)
    w_table["columns"] = ("W1", "W2", "W3")

    w_table.column("#0", width=0, stretch=tk.NO)
    w_table.heading("#0", text="", anchor=tk.W)
    w_table.column("W1", anchor=tk.CENTER, width=200)
    w_table.heading("W1", text="W1", anchor=tk.CENTER)
    w_table.column("W2", anchor=tk.CENTER, width=200)
    w_table.heading("W2", text="W2", anchor=tk.CENTER)
    w_table.column("W3", anchor=tk.CENTER, width=200)
    w_table.heading("W3", text="W3", anchor=tk.CENTER)

    data = [list(pesos[0]), list(pesos[len(pesos) - 1])]
    for i in range(len(data)):
        w_table.insert(parent="", index=i, iid=i, values=data[i])

    w_table.pack(pady=10)

    text = f"Tasa de aprendizaje: {tasa_aprendizaje}\nError permitido: {error}\nIteraciones realizadas: {len(errores)}"
    datos_finales = tk.Label(table_frame, text=text)
    datos_finales.pack()


def execute_algorithm():
    tasa_aprendizaje = float(rate_entry.get())
    error = error_entry.get()
    iteraciones = int(i_entry.get())

    print_graphs(tasa_aprendizaje, error, iteraciones)


execute_button = tk.Button(frame_parametros, text="Ejecutar", command=lambda: execute_algorithm(),
                           bg="#4CAF50", fg="white", font=button_font)
execute_button.grid(row=1, column=5, padx=10, pady=10, sticky="w")

bottom_frame = tk.Frame(window)
bottom_frame.pack(padx=10)

graphics_frame = tk.Frame(bottom_frame)
graphics_frame.pack(side=tk.TOP, pady=10)

table_frame = tk.Frame(bottom_frame)
table_frame.pack(side=tk.BOTTOM, pady=10)

window.mainloop()
