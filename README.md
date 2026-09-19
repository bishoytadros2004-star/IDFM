# IDFM: in silico network pharmacology and pharmacovigilance analysis

Supplementary data and code for the manuscript

> **In Silico Network Pharmacology and Pharmacovigilance Analysis of a Four-Drug Combination in Informal Circulation (Ivermectin, Dronedarone, Fenbendazole, Methylene Blue): Target Convergence and Pharmacokinetic Interaction Hazards**
> Bishoy Tadros, Department of Medical Biotechnology, Badr University in Cairo, Egypt.

**Status:** manuscript in preparation for submission. This repository will be archived on Zenodo when the manuscript is submitted; the DOI will be added here.

## What this study is (and is not)

The study builds a bipartite drug–target network for ivermectin, dronedarone, fenbendazole and methylene blue from predicted targets (SwissTargetPrediction, STITCH, ChEMBL annotations), tests how robust the convergence nodes are to score thresholds, and cross-references them against FDA prescribing information and the published literature.

**It is a computational hypothesis-generating analysis. It does not evaluate the efficacy, synergy or safety of this combination, and nothing here is medical advice or a dosing suggestion.**

## Main results reproduced by this repository

| Quantity | Full network (all edges) | Strict network (Tier 1 only) |
|---|---|---|
| Nodes (drugs + targets) | 56 (4 + 52) | 37 (4 + 33) |
| Edges | 54 | 34 |
| Drug degree (ivermectin / dronedarone / fenbendazole / methylene blue) | 16 / 18 / 10 / 10 | 9 / 11 / 4 / 10 |
| Targets shared by two drugs | 2 of 52 (3.8%): ABCB1, CYP2D6 | 1 of 33: CYP2D6 |

ABCB1 is shared only at SwissTargetPrediction cut-offs of 0.25 or lower, because the dronedarone–ABCB1 probability is 0.282 (Tier 2). See Table S3.

## Files

| File | Contents |
|---|---|
| `Table_S1_Edges.xlsx` | All 54 drug–target edges with source scores, UniProt accessions, tier and retention note. **Input for the script.** |
| `Table_S2_Summary.xlsx` | Degree, tier counts and shared-target counts, calculated by Excel formulas (contains a copy of S1 as its input tab). |
| `Table_S3_Sensitivity.xlsx` | Edges, targets and shared targets across SwissTargetPrediction (0.05–0.30) and STITCH (0.40, 0.70) cut-offs. |
| `Table_S4_STP_Ivermectin_raw.xlsx` | Raw SwissTargetPrediction output for ivermectin (top 100 predictions). |
| `Table_S5_STP_other_raw_TEMPLATE.xlsx` | Raw SwissTargetPrediction output for dronedarone and fenbendazole (to be completed). |
| `Table_S6_Enrichment_TEMPLATE.xlsx` | KEGG terms shown in Figure 5 with fold enrichment, gene counts, FDR and genes (numeric columns to be completed from the ShinyGO export). |
| `Table_S7_PV_evidence.xlsx` | Label-, literature- and case-report-derived evidence used in the pharmacovigilance sections, with sources. |
| `README_Supplementary_Tables.xlsx` | Legend, tier definitions and provenance notes for the tables. |
| `network_analysis.py` | Recomputes every network number in the manuscript from `Table_S1_Edges.xlsx`. |
| `LICENSE` | GNU General Public License v3.0. |

## Tier definitions

- **Tier 1:** the edge meets the retention thresholds: SwissTargetPrediction probability ≥ 0.30 **or** STITCH combined score ≥ 0.70. Methylene blue targets taken from ChEMBL target annotations are retained as recorded.
- **Tier 2:** the edge was retained in the permissive network but is below these thresholds. Tier 2 edges are exploratory. The reason each Tier 2 edge is below threshold is given in the *Retention note* column of Table S1.

## Reproducing the network analysis

Requirements: Python 3.9+ with `pandas`, `networkx` and `openpyxl`.

```bash
pip install pandas networkx openpyxl
python network_analysis.py Table_S1_Edges.xlsx
```

The script prints the network summary for the full and the strict (Tier 1) networks, including drug degree, shared targets, Jaccard overlaps and connected components. It also writes `sensitivity.csv` (the threshold grid reported in Table S3).

## Data sources

| Resource | Used for | Access |
|---|---|---|
| SwissTargetPrediction (*Homo sapiens*) | Predicted targets (probability) | swisstargetprediction.ch |
| STITCH | Chemical–protein association scores | stitch.embl.de |
| ChEMBL | Methylene blue target annotations | ebi.ac.uk/chembl |
| STRING | Protein–protein associations (confidence ≥ 0.700) | string-db.org |
| ShinyGO / Enrichr | KEGG and GO enrichment (FDR < 0.05) | see manuscript Section 3.3 |
| US prescribing information | Multaq (dronedarone) and Provayblue (methylene blue) labels | DailyMed / Drugs@FDA |

Database access dates and versions: *to be added.*

## Known limitations

- The study is prediction-only, with no experimental validation.
- Scores from different resources are not directly comparable, and 20 of the 54 edges are Tier 2.
- CYP3A4, central to the clearance discussion, is **not** a predicted target. It enters through labeling and the literature.
- Label data refer to approved routes and doses; informal regimens are not characterized.

## How to cite

Tadros, B. (2026). *Supplementary data and code for: In silico network pharmacology and pharmacovigilance analysis of a four-drug combination in informal circulation* [Data set and code]. GitHub. https://github.com/bishoytadros2004-star/IDFM (Zenodo DOI to be added).

## Contact

Bishoy Tadros: bishoytadros2004@gmail.com
