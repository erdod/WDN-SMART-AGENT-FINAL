import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def plot_risk_decomposition():
    csv_path = Path("Log_review/ai_risk_decomposition.csv")
    if not csv_path.exists():
        print(f"[Errore] File non trovato: {csv_path}")
        return

    times, total_risk, deficit, uncertainty = [], [], [], []
    
    # Lettura sicura del CSV
    with open(csv_path, 'r') as f:
        header = f.readline()
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 5:
                times.append(float(parts[1]))
                total_risk.append(float(parts[2]))
                deficit.append(float(parts[3]))
                uncertainty.append(float(parts[4]))

    if not times:
        print("[Errore] CSV vuoto.")
        return

    # In priority_agent.py, il rischio è calcolato come:
    # Risk = (0.7 * Deficit) + (0.3 * Uncertainty)
    # Calcoliamo le componenti pesate per fare in modo che la loro somma
    # corrisponda esattamente alla curva del Rischio Totale.
    weighted_deficit = np.array(deficit) * 0.7
    weighted_uncertainty = np.array(uncertainty) * 0.3

    # --- Setup del Grafico ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # Grafico ad aree sovrapposte (Stacked Area)
    ax.stackplot(times, weighted_deficit, weighted_uncertainty,
                 labels=['Deficit Idraulico (Rischio Reale)', 'Packet Loss (Rischio Cyber)'],
                 colors=['#3498db', '#e74c3c'], alpha=0.8)

    # Linea tratteggiata per evidenziare il profilo totale del rischio
    ax.plot(times, total_risk, color='black', linewidth=1.5, linestyle='--', label='Rischio Totale (Percepito)')

    # Formattazione
    ax.set_xlabel("Tempo di Simulazione (Ore)", fontweight='bold')
    ax.set_ylabel("Livello di Rischio Normalizzato [0 - 1]", fontweight='bold')
    ax.set_title("Explainable AI: Scomposizione del Rischio (Idraulica vs Telecomunicazioni)", fontweight='bold', pad=15)
    
    # Limiti e Griglia
    ax.set_xlim(min(times), max(times))
    ax.set_ylim(0, 1.05)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Legenda in alto fuori dal grafico
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)

    # Salvataggio
    out_path = Path("Log_review/05_ai_risk_decomposition.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✓ Grafico Scomposizione Rischio generato: {out_path}")

if __name__ == "__main__":
    plot_risk_decomposition()