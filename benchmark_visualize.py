import subprocess
import re
import os
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
TEST_FILES = ["testCSP.py", "testCSPTable.py", "testCSP-6.1.py"]
ALGOS = ["Backtracking", "Forward Checking", "Propagation AC3", "Propagation AC1"]

def run_test_file(filename):
    print(f"-> Analyse de {filename}...")
    try:
        process = subprocess.run(['python', filename], capture_output=True, text=True, timeout=30)
        output = process.stdout
        
        nodes = re.findall(r"Nombre de noeuds créés\s*:\s*(\d+)", output)
        fails = re.findall(r"Nombre d'échecs\s*:\s*(\d+)", output)
        times = re.findall(r"temps de résolution\s*:\s*([\d\.]+)", output)
        
        return [int(n) for n in nodes], [int(f) for f in fails], [float(t) for t in times]
    except Exception as e:
        print(f"   [!] Erreur : {e}")
        return [], [], []

def generate_graphs(results):
    labels = [f.replace('.py', '') for f in TEST_FILES]
    
    # Graphique Noeuds
    plt.figure(figsize=(10, 5))
    for i, algo in enumerate(ALGOS[:3]):
        data = [results[f]['nodes'][i] for f in TEST_FILES if f in results]
        plt.plot(labels[:len(data)], data, marker='o', label=algo)
    plt.yscale('log')
    plt.title("Complexité (Nombre de Nœuds)")
    plt.ylabel("Nœuds (Log)")
    plt.legend(); plt.grid(True, alpha=0.3)
    plt.savefig("graph_nodes.png")

    # Graphique Temps
    plt.figure(figsize=(10, 5))
    for i, algo in enumerate(ALGOS[:3]):
        data = [results[f]['times'][i] for f in TEST_FILES if f in results]
        plt.plot(labels[:len(data)], data, marker='s', linestyle='--', label=algo)
    plt.yscale('log')
    plt.title("Performance (Temps en ms)")
    plt.ylabel("Temps (ms)")
    plt.legend(); plt.grid(True, alpha=0.3)
    plt.savefig("graph_time.png")
    print("\n[V] Graphiques générés : graph_nodes.png et graph_time.png")

# --- INITIALISATION ---
all_results = {} 

print("\n" + "="*60)
print("RUNNING BENCHMARK...")
print("="*60)

for test_file in TEST_FILES:
    if os.path.exists(test_file):
        n_found, f_found, t_found = run_test_file(test_file)
        
        if len(n_found) >= 4 and len(t_found) >= 4:
            all_results[test_file] = {'nodes': n_found, 'fails': f_found, 'times': t_found}
            
        
            latex_filename = test_file.replace('_', r'\_')
            
            print(f"\n% --- Table pour {test_file} ---")
            print(r"\begin{table}[h!]\centering")
            print(r"\begin{tabular}{lcccc}\toprule")
            print(r"\textbf{Algorithme} & \textbf{Nœuds} & \textbf{Échecs} & \textbf{Temps (ms)} & \textbf{Réduction} \\ \midrule")
            
            base_nodes = n_found[0]
            for i in range(4):
                reduction = f"{((base_nodes - n_found[i]) / base_nodes * 100):.1f}\%" if i > 0 and base_nodes > 0 else "-"
                print(f"{ALGOS[i]:<20} & {n_found[i]:<10} & {f_found[i]:<10} & {t_found[i]:<12.2f} & {reduction:<10} \\\\")
            
            print(r"\bottomrule\end{tabular}")
            # Utilisation de la variable préparée
            print(f"\\caption{{Résultats : {latex_filename}}}\\end{{table}}")
            print("-" * 60)

if all_results:
    generate_graphs(all_results)