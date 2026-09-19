"""
network_analysis.py  --  reproduces every network number reported in the manuscript.
Input : Table_S1_Edges.xlsx, sheet "S1_Edges" (one row per drug-target edge)
Output: printed summary + 'sensitivity.csv'
Requires: pandas, networkx, openpyxl
"""
import sys, itertools
import pandas as pd, networkx as nx

XLSX = sys.argv[1] if len(sys.argv) > 1 else "Table_S1_Edges.xlsx"
E = pd.read_excel(XLSX, sheet_name="S1_Edges")
DRUGS = ["Ivermectin", "Dronedarone", "Fenbendazole", "Methylene Blue"]

def build(df):
    G = nx.Graph()
    for d in DRUGS: G.add_node(d, bipartite=0)
    for _, r in df.iterrows():
        G.add_node(r.Gene, bipartite=1); G.add_edge(r.Drug, r.Gene)
    return G

def summarise(G, label):
    targets = [n for n, d in G.nodes(data=True) if d["bipartite"] == 1]
    shared = sorted(t for t in targets if G.degree(t) > 1)
    print(f"\n=== {label} ===")
    print(f"nodes={G.number_of_nodes()} (4 drugs + {len(targets)} targets)  edges={G.number_of_edges()}")
    print("drug degree:", {d: G.degree(d) for d in DRUGS})
    print("shared targets:", {t: sorted(G.neighbors(t)) for t in shared},
          f"-> {len(shared)}/{len(targets)} = {100*len(shared)/len(targets):.1f}%")
    for a, b in itertools.combinations(DRUGS, 2):
        A, B = set(G.neighbors(a)), set(G.neighbors(b))
        if A & B: print(f"  Jaccard({a},{b}) = {len(A&B)}/{len(A|B)} = {len(A&B)/len(A|B):.3f}")
    comps = [sorted(d for d in c if d in DRUGS) for c in nx.connected_components(G)]
    comps = [c for c in comps if c]
    print("drug-containing connected components:", comps)
    return shared

full = build(E)
summarise(full, "Full (permissive) network: all 54 edges")
strict = build(E[E.Tier == "Tier 1"])
summarise(strict, "Strict network: Tier 1 edges only (STP>=0.30, STITCH>=0.70, ChEMBL-annotated)")

# threshold sweep (STP cutoff x STITCH cutoff); ChEMBL-annotated edges always retained
rows = []
for stp_c, sti_c in itertools.product([0.05, 0.10, 0.20, 0.25, 0.30], [0.40, 0.70]):
    keep = E[(E.STP_probability.fillna(-1) >= stp_c) | (E.STITCH_score.fillna(-1) >= sti_c) | E.ChEMBL_confidence.notna()]
    G = build(keep)
    tg = [n for n, d in G.nodes(data=True) if d["bipartite"] == 1]
    sh = sorted(t for t in tg if G.degree(t) > 1)
    rows.append(dict(STP_cutoff=stp_c, STITCH_cutoff=sti_c, edges=G.number_of_edges(), targets=len(tg),
                     shared_targets=", ".join(sh) if sh else "none"))
S = pd.DataFrame(rows); S.to_csv("sensitivity.csv", index=False); print("\n", S.to_string(index=False))
