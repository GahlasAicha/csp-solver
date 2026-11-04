# 🧩 Solveur de contraintes (CSP) — Programmation Par Contraintes

Solveur de **problèmes de satisfaction de contraintes** (CSP) implémenté **from scratch** en **Python**, avec plusieurs algorithmes de résolution et une étude comparative de leurs performances.

> Projet réalisé dans le cadre du module *Programmation Par Contraintes* — Master Informatique, Université d'Orléans.

---

## 🎯 Principe

Un **CSP** est défini par un ensemble de **variables**, chacune avec son **domaine** de valeurs possibles, et un ensemble de **contraintes** à satisfaire. Le solveur explore l'espace de recherche pour trouver une (ou toutes les) affectation(s) valide(s).

---

## ⚙️ Algorithmes implémentés

| Algorithme | Description |
|-----------|-------------|
| **Backtracking** | Recherche en profondeur avec retour arrière |
| **Forward Checking** | Backtracking + élagage des domaines des variables non assignées |
| **Propagation AC-1 / AC-3** | Backtracking + maintien de la **cohérence d'arc** (arc consistency) |

**Heuristiques de choix de variable** : ordre séquentiel ou **MRV** (`minDom` — variable au plus petit domaine).

Le solveur compte les **nœuds explorés**, les **échecs**, les **solutions trouvées** et mesure le **temps de résolution**.

---

## 📂 Structure

| Fichier | Rôle |
|---------|------|
| `csp.py` | Définition d'un CSP (variables, domaines, contraintes) |
| `constraint.py` | Contraintes (`Table`, `Different`, …) |
| `solver.py` | Solveur : backtracking, forward checking, propagation AC-1/AC-3, heuristiques |
| `N_queens.py` | Application au problème des **N-Reines** |
| `testCSP*.py` | Jeux de tests |
| `benchmark_visualize.py` | Génération des **courbes de performance** |
| `plots/` | Graphes (temps, nœuds, performance) |
| `Rapport.pdf` | Rapport d'analyse |

---

## 🚀 Utilisation

```bash
# Résoudre les N-Reines
python N_queens.py

# Lancer les tests
python testCSP.py

# Générer les benchmarks / courbes
python benchmark_visualize.py
```

> Dépendances : Python 3 + `matplotlib` (pour les graphes). Installation : `pip install matplotlib`.

---

## 📊 Résultats

Le projet compare les algorithmes (backtracking vs forward checking vs propagation) sur le nombre de **nœuds explorés** et le **temps de calcul**, montrant l'intérêt de la propagation de contraintes pour réduire l'espace de recherche (voir `plots/` et `Rapport.pdf`).

---

## 👤 Auteur

**Gahlas Aicha** 
[github.com/GahlasAicha](https://github.com/GahlasAicha)