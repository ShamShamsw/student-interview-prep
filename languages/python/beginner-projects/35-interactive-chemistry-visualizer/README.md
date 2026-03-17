# Beginner Project 35: Interactive Chemistry Visualizer

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** SMILES parsing, molecular property computation, Lipinski Ro5 filtering, and persistent molecule analytics

---

## Why This Project?

Understanding molecular properties is at the heart of drug discovery and cheminformatics. This project shows how to extract meaningful data from SMILES strings — the compact text notation chemists use to describe molecules — using nothing but Python's standard library.

This project teaches end-to-end molecular workflow concepts where you can:

- load or auto-generate a reusable local molecule library,
- parse SMILES strings to identify element atoms and bond patterns,
- compute molecular formulas in Hill notatioQn from atom counts,
- estimate molecular weight from atomic mass contributions,
- calculate H-bond donor and acceptor counts from functional groups,
- estimate logP as an atomic contribution sum,
- count ring systems and rotatable bonds from SMILES patterns,
- apply Lipinski's Rule of Five to assess oral bioavailability,
- persist run summaries and per-molecule property records to JSON,
- and print a readable terminal report with a molecule property table.

---

## Separate Repository

You can also access this project in a separate repository:

[Interactive Chemistry Visualizer Repository](https://github.com/ShamShamsw/interactive-chemistry-visualizer.git)

---

## What You Will Build

You will build an interactive chemistry visualizer that:

1. Loads a molecule library from `data/library.json` (or seeds a starter set).
2. Parses each SMILES string to extract element symbols.
3. Counts atoms and estimates implicit hydrogens.
4. Computes the molecular formula in Hill notation (C, H, then alphabetical).
5. Calculates molecular weight from atomic mass contributions.
6. Derives H-bond donors, H-bond acceptors, logP, and rotatable bonds.
7. Counts ring systems via SMILES ring-closure digit analysis.
8. Applies Lipinski's Rule of Five and flags pass/fail per molecule.
9. Persists per-molecule metadata and run summaries for history.
10. Prints a readable terminal report with a property table and metrics.

---

## Requirements

- Python 3.11+
- No external dependencies — the property engine uses stdlib only.

---

## Example Session

```text
======================================================================
   INTERACTIVE CHEMISTRY VISUALIZER
======================================================================

Configuration:
   Project type:         interactive_chemistry_visualizer
   Property engine:      SMILES-based (no external chem libs)
   Top properties:       6
   Include formula:      True
   Include weight:       True
   Include rings:        True
   Include H-bond:       True
   Max molecules report: 8
   Random seed:          42

Startup:
   Data directory:       data/
   Outputs directory:    data/outputs/
   Molecule library:     data/library.json (loaded 8 molecules)
   Run catalog:          data/runs.json (loaded 0 runs)
   Molecule catalog:     data/molecules.json (loaded 0 records)
   Recent molecules:     None yet

---

Run complete:
   Run ID:               20260317_090000
   Molecules processed:  8
   Properties computed:  48
   Lipinski pass:        7/8
   Elapsed time:         3.14 ms

Library metrics: mean_MW=248.31 | min_MW=46.07 | max_MW=456.46 | mean_logP=1.73 | Ro5_rate=88%

Molecule properties:
   ID      | Name              | Formula  | MW (g/mol) | Rings | logP  | Ro5
   --------+-------------------+----------+------------+-------+-------+----
   mol_003 | Ethanol           | C2H6O    |      46.07 |     0 |  0.49 | PASS
   mol_008 | Paracetamol       | C8H9NO2  |     151.16 |     1 |  1.28 | PASS
   mol_001 | Aspirin           | C9H8O4   |     180.16 |     1 |  1.43 | PASS
   mol_005 | Benzene           | C6H6     |      78.11 |     1 |  2.09 | PASS
   mol_007 | Ibuprofen         | C13H18O2 |     206.28 |     1 |  3.52 | PASS
   mol_002 | Caffeine          | C8H10N4O2|     194.19 |     2 | -0.07 | PASS
   mol_004 | Glucose           | C6H12O6  |     180.16 |     1 | -1.56 | PASS
   mol_006 | Penicillin G      | C16H18N2O4S|   334.39 |     2 |  1.72 | PASS

Artifacts saved:
   Run record:           data/outputs/run_20260317_090000.json
   Properties report:    data/outputs/properties_20260317_090000.json
   Lipinski report:      data/outputs/lipinski_20260317_090000.json
   Metadata exports:     8
```

---

## Run

```bash
python main.py
```
