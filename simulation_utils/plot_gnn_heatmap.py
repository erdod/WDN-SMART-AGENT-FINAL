import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def plot_gnn_heatmap():
    # Percorso del CSV generato da main.py
    csv_path = Path("Log_review/gnn_node_embeddings.csv")
    if not csv_path.exists():
        print(f"[Errore] File non trovato: {csv_path}. Avvia prima una simulazione.")
        return

    # Estrazione manuale per massima compatibilità (no pandas)
    times, nodes, pressures = [], [], []
    with open(csv_path, 'r') as f:
        header = f.readline()
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 4:
                times.append(float(parts[1]))
                nodes.append(parts[2])
                pressures.append(float(parts[3]))

    if not times:
        print("[Errore] CSV vuoto.")
        return

    # Creazione vettori unici e ordinati
    unique_times = sorted(list(set(times)))
    unique_nodes = sorted(list(set(nodes)))
    
    # Inizializzazione della matrice Z (Nodi x Tempi)
    z_matrix = np.zeros((len(unique_nodes), len(unique_times)))
    
    # Mapping veloce per le coordinate della matrice
    time_to_idx = {t: i for i, t in enumerate(unique_times)}
    node_to_idx = {n: i for i, n in enumerate(unique_nodes)}
    
    # Popolamento
    for t, n, p in zip(times, nodes, pressures):
        z_matrix[node_to_idx[n], time_to_idx[t]] = p

    # --- Setup del Grafico ---
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Mappa di calore (da rosso/emergenza a blu/sicuro)
    cax = ax.imshow(z_matrix, aspect='auto', cmap='coolwarm', origin='lower')
    
    # Asse Y: Nomi dei nodi
    ax.set_yticks(np.arange(len(unique_nodes)))
    ax.set_yticklabels(unique_nodes, fontsize=9)
    
    # Asse X: Tempi (mostriamo un sample di max 10 etichette per non sovrapporle)
    x_ticks = np.linspace(0, len(unique_times)-1, min(10, len(unique_times)), dtype=int)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([f"{unique_times[i]:.1f}" for i in x_ticks])

    # Formattazione
    ax.set_xlabel("Tempo (Ore)", fontweight='bold', labelpad=10)
    ax.set_ylabel("Nodi Prioritari", fontweight='bold', labelpad=10)
    ax.set_title("GNN Belief State: Evoluzione Pressione Stimata", fontweight='bold', pad=15)
    
    # Barra dei colori
    cbar = fig.colorbar(cax, ax=ax)
    cbar.set_label('Pressione Stimata (m)', fontweight='bold', rotation=270, labelpad=15)
    
    # Salvataggio
    out_path = Path("Log_review/04_gnn_attention_heatmap.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    print(f"✓ Heatmap GNN generata con successo in: {out_path}")

if __name__ == "__main__":
    plot_gnn_heatmap()