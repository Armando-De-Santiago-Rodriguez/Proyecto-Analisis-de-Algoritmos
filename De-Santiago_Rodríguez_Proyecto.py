import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
import time

# Función para leer el archivo CSV y mostrar su contenido
def leer_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            global df
            df = pd.read_csv(file_path)
            # Dibuja el grafo basado en los datos del DataFrame
            dibujar_grafo(df)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")


# Función para dibujar el grafo basado en los datos del DataFrame
def dibujar_grafo(df):
    global G
    G = nx.Graph()
    # Añade nodos al grafo
    for index, row in df.iterrows():
        lugar = row['Lugar']
        nodo = row['Nodo']
        G.add_node(nodo, label=lugar)
    # Añade aristas al grafo con las distancias
    for index, row in df.iterrows():
        nodo = row['Nodo']
        for col in df.columns[2:]:
            destino = col.split()[-1]
            distancia = row[col]
            if distancia > 0:
                G.add_edge(nodo, destino, weight=distancia)
    # Dibuja el grafo
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Grafo de Distancias")
    plt.show()


#Función para calcular y mostrar el camino más corto
def calcular_camino_mas_corto():
    nodo_inicio = entrada_inicio.get()
    nodo_destino = entrada_destino.get()
    if nodo_inicio in G and nodo_destino in G:
        try:
            start_time = time.time()
            camino = nx.dijkstra_path(G, nodo_inicio, nodo_destino)
            distancia = nx.dijkstra_path_length(G, nodo_inicio, nodo_destino)
            end_time = time.time()
            duracion = end_time - start_time
            messagebox.showinfo("Camino más corto", f"Camino: {' -> '.join(camino)}\nDistancia total: {distancia}\nTiempo de cálculo: {duracion:.6f} segundos")
        except nx.NetworkXNoPath:
            messagebox.showerror("Error", "No existe un camino entre los nodos especificados.")
    else:
        messagebox.showerror("Error", "Uno o ambos nodos no existen en el grafo.")

# Creación de la ventana principal de la aplicación
Pantalla = tk.Tk()
Pantalla.title("Proyecto")
Pantalla.geometry("1920x1080")
Pantalla.configure(bg="gray")  # Cambiar el color de fondo de la ventana principal

# Etiqueta para mostrar el título de la práctica
Titulo = tk.Label(Pantalla, text="Proyecto", bg="cyan", fg="black", font="Arial 14")
Titulo.pack(fill=tk.X)

# Botón para ingresar un Database con extensión csv
BotonA = tk.Button(Pantalla, text="Leer Archivo", bg="light green", fg="black", font="Arial 12", command=leer_archivo)
BotonA.pack(side=tk.TOP, padx=10, pady=10)

# Etiqueta y campo de entrada para el nodo de inicio
label_inicio = tk.Label(Pantalla, text="Nodo de Inicio:", bg="black", fg="white", font="Arial 12")
label_inicio.pack(padx=10, pady=5)
entrada_inicio = tk.Entry(Pantalla, font="Arial 12", bg="gray", fg="white")
entrada_inicio.pack(padx=10, pady=5)

# Etiqueta y campo de entrada para el nodo de destino
label_destino = tk.Label(Pantalla, text="Nodo de Destino:", bg="black", fg="white", font="Arial 12")
label_destino.pack(padx=10, pady=5)
entrada_destino = tk.Entry(Pantalla, font="Arial 12", bg="gray", fg="white")
entrada_destino.pack(padx=10, pady=5)

# Botón para calcular el camino más corto
BotonB = tk.Button(Pantalla, text="Calcular Camino Más Corto", bg="light green", fg="black", font="Arial 12", command=calcular_camino_mas_corto)
BotonB.pack(side=tk.TOP, padx=10, pady=10)

# Método principal para mostrar la ventana y ejecutar la aplicación
Pantalla.mainloop()
