#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def generar_diagrama_afd():
    print("[+] Generando diagrama de estados del autómata (diagrama_afd_ejercicio3_16d.png)...")
    
    # Crear digrafo
    G = nx.DiGraph()
    
    estados = ['q0', 'q1', 'q2', 'q3']
    G.add_nodes_from(estados)
    
    # Transiciones: (origen, destino, simbolo)
    transiciones = [
        ('q0', 'q1', 'a'),
        ('q0', 'q0', 'b'),
        ('q1', 'q1', 'a'),
        ('q1', 'q2', 'b'),
        ('q2', 'q1', 'a'),
        ('q2', 'q3', 'b'),
        ('q3', 'q3', 'a, b'),
    ]
    
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    fig.patch.set_facecolor('#0f172a') # Fondo oscuro elegante (slate-900)
    ax.set_facecolor('#0f172a')
    
    pos = {
        'q0': (0, 0),
        'q1': (2, 0),
        'q2': (4, 0),
        'q3': (6, 0)
    }
    
    # Dibujar nodos
    # q0: Inicial (cyan)
    # q1, q2: Intermedios (azul)
    # q3: Aceptación (verde/dorado con borde doble)
    
    colors = ['#38bdf8', '#60a5fa', '#818cf8', '#4ade80']
    node_sizes = [2200, 2200, 2200, 2600]
    
    nx.draw_networkx_nodes(G, pos, nodelist=['q0'], node_color='#0284c7', node_size=2400, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=['q1', 'q2'], node_color='#3b82f6', node_size=2400, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=['q3'], node_color='#10b981', node_size=2800, ax=ax)
    
    # Círculo interior para q3 (aceptación)
    nx.draw_networkx_nodes(G, pos, nodelist=['q3'], node_color='#0f172a', node_size=1800, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=['q3'], node_color='#10b981', node_size=1400, ax=ax)
    
    # Etiquetas de nodos
    labels = {'q0': 'q0\n(Inicio)', 'q1': 'q1\n[a]', 'q2': 'q2\n[ab]', 'q3': 'q3 ★\n[abb] (Fin)'}
    nx.draw_networkx_labels(G, pos, labels, font_size=11, font_weight='bold', font_color='white', ax=ax)
    
    # Dibujar aristas rectas y curvas
    # Curved transitions
    # q0 -> q1 (a)
    ax.annotate("", xy=pos['q1'], xytext=pos['q0'],
                arrowprops=dict(arrowstyle="-|>", color='#94a3b8', lw=2.5, mutation_scale=20,
                                patchA=None, patchB=None, shrinkA=30, shrinkB=30,
                                connectionstyle="arc3,rad=-0.2"))
    ax.text(1.0, 0.22, 'a', color='#38bdf8', fontsize=12, fontweight='bold', ha='center')

    # q1 -> q2 (b)
    ax.annotate("", xy=pos['q2'], xytext=pos['q1'],
                arrowprops=dict(arrowstyle="-|>", color='#94a3b8', lw=2.5, mutation_scale=20,
                                shrinkA=30, shrinkB=30, connectionstyle="arc3,rad=-0.2"))
    ax.text(3.0, 0.22, 'b', color='#38bdf8', fontsize=12, fontweight='bold', ha='center')

    # q2 -> q3 (b) [Llega a aceptación!]
    ax.annotate("", xy=pos['q3'], xytext=pos['q2'],
                arrowprops=dict(arrowstyle="-|>", color='#4ade80', lw=3.0, mutation_scale=22,
                                shrinkA=30, shrinkB=35, connectionstyle="arc3,rad=-0.2"))
    ax.text(5.0, 0.22, 'b (hecho)', color='#4ade80', fontsize=12, fontweight='bold', ha='center')

    # Retroceso q2 -> q1 (a)
    ax.annotate("", xy=pos['q1'], xytext=pos['q2'],
                arrowprops=dict(arrowstyle="-|>", color='#f43f5e', lw=2.0, mutation_scale=20,
                                shrinkA=30, shrinkB=30, connectionstyle="arc3,rad=-0.35"))
    ax.text(3.0, -0.32, 'a', color='#f43f5e', fontsize=12, fontweight='bold', ha='center')

    # Bucle q0 -> q0 (b)
    ax.annotate("", xy=(pos['q0'][0]-0.08, pos['q0'][1]+0.22), xytext=(pos['q0'][0]+0.08, pos['q0'][1]+0.22),
                arrowprops=dict(arrowstyle="-|>", color='#cbd5e1', lw=2.0, mutation_scale=18,
                                connectionstyle="arc,angleA=0,angleB=180,armA=30,armB=30,rad=10"))
    ax.text(0.0, 0.58, 'b', color='#cbd5e1', fontsize=12, fontweight='bold', ha='center')

    # Bucle q1 -> q1 (a)
    ax.annotate("", xy=(pos['q1'][0]-0.08, pos['q1'][1]+0.22), xytext=(pos['q1'][0]+0.10, pos['q1'][1]+0.22),
                arrowprops=dict(arrowstyle="-|>", color='#cbd5e1', lw=2.0, mutation_scale=18,
                                connectionstyle="arc,angleA=0,angleB=180,armA=30,armB=30,rad=10"))
    ax.text(2.0, 0.58, 'a', color='#cbd5e1', fontsize=12, fontweight='bold', ha='center')

    # Bucle q3 -> q3 (a, b)
    ax.annotate("", xy=(pos['q3'][0]-0.08, pos['q3'][1]+0.22), xytext=(pos['q3'][0]+0.10, pos['q3'][1]+0.22),
                arrowprops=dict(arrowstyle="-|>", color='#4ade80', lw=2.0, mutation_scale=18,
                                connectionstyle="arc,angleA=0,angleB=180,armA=30,armB=30,rad=10"))
    ax.text(6.0, 0.58, 'a, b', color='#4ade80', fontsize=12, fontweight='bold', ha='center')

    # Flecha de entrada al estado inicial
    ax.annotate("", xy=pos['q0'], xytext=(-1.0, 0),
                arrowprops=dict(arrowstyle="-|>", color='#38bdf8', lw=3.0, mutation_scale=22, shrinkB=32))
    ax.text(-0.6, 0.15, 'Inicio', color='#38bdf8', fontsize=11, fontweight='bold')

    plt.title("Autómata Finito Determinista (AFD) - Ejercicio 3.16 d)\nExpresión Regular: (a|b)*abb(a|b)*",
              color='white', fontsize=14, fontweight='bold', pad=25)
    
    plt.xlim(-1.2, 7.0)
    plt.ylim(-0.7, 0.9)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('diagrama_afd_ejercicio3_16d.png', facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print("[✓] Diagrama guardado en 'diagrama_afd_ejercicio3_16d.png'")


def generar_grafica_resultados():
    print("[+] Generando gráfica de resultados (resultados_ejercicio3_16.png)...")
    
    categorias = ['Cadenas Aceptadas', 'Cadenas Rechazadas', 'Error de Alfabeto']
    valores = [5, 5, 1]
    colores = ['#22c55e', '#ef4444', '#f59e0b']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    fig.patch.set_facecolor('#0f172a')
    ax1.set_facecolor('#1e293b')
    ax2.set_facecolor('#0f172a')

    # 1. Gráfica de Barras
    bars = ax1.bar(categorias, valores, color=colores, width=0.55, edgecolor='white', linewidth=1.2)
    ax1.set_title("Distribución de Resultados de Evaluación", color='white', fontsize=13, fontweight='bold', pad=15)
    ax1.set_ylabel("Cantidad de Cadenas", color='white', fontsize=11)
    ax1.tick_params(colors='white', labelsize=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.3, color='#94a3b8')

    # Añadir valores sobre las barras
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.15,
                 f'{int(height)}',
                 ha='center', va='bottom', color='white', fontweight='bold', fontsize=11)

    ax1.set_ylim(0, 6.5)

    # 2. Gráfica de Pastel (Pie chart)
    wedges, texts, autotexts = ax2.pie(valores, labels=categorias, autopct='%1.1f%%',
                                      startangle=140, colors=colores,
                                      textprops=dict(color="white", fontweight='bold'),
                                      wedgeprops=dict(width=0.4, edgecolor='white', linewidth=1.5))
    
    ax2.set_title("Porcentaje General de Efectividad", color='white', fontsize=13, fontweight='bold', pad=15)

    plt.suptitle("Resultados del Procesamiento del Autómata AFD (cadenas.txt)", color='#38bdf8', fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('resultados_ejercicio3_16.png', facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print("[✓] Gráfica guardada en 'resultados_ejercicio3_16.png'")


if __name__ == '__main__':
    generar_diagrama_afd()
    generar_grafica_resultados()
