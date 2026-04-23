import os
import subprocess
import sys


def run(cmd):
    print(f"\n▶ Running: {cmd}\n")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"❌ Failed: {cmd}")


def main():

    # ------------------------
    # 1. DATA GENERATION
    # ------------------------
    run("python generator.py")

    # ------------------------
    # 2. INGESTION + FEATURES
    # ------------------------
    run("python ingestion/compute_accessibility.py")

    # ------------------------
    # 3. KG BUILDING
    # ------------------------
    run("python kg/build_graph.py")

    # ------------------------
    # 4. TRIPLES
    # ------------------------
    run("python ml/build_triples.py")

    # ------------------------
    # 5. GRAPH DATA FOR GNN
    # ------------------------
    run("python ml/build_graphsage_data.py")

    # ------------------------
    # 6. TRAIN GRAPH SAGE
    # ------------------------
    run("python ml/graphsage.py")

    # ------------------------
    # 7. TRAIN TRANSE
    # ------------------------
    run("python ml/transE.py")

    print("\n✔ PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()