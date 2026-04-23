🏥 Healthcare Accessibility & Demographic Risk Knowledge Graph

A hybrid Knowledge Graph framework for modeling healthcare accessibility and demographic risk across Austrian regions using symbolic reasoning and graph representation learning.

------------------------------------------------------------
📌 Overview

This project integrates heterogeneous spatial, healthcare infrastructure, and demographic data into a unified RDF-based Knowledge Graph. It enables both symbolic reasoning and machine learning–based inference for analyzing healthcare accessibility and identifying underserved regions.

The system combines:
- SPARQL-based logical inference for rule-driven accessibility reasoning
- TransE knowledge graph embeddings for link prediction and structural inference
- GraphSAGE neural networks for node-level demographic risk estimation

------------------------------------------------------------
⚙️ Key Features

- Unified RDF Knowledge Graph for Austrian healthcare and demographic data
- Rule-based reasoning using SPARQL for accessibility constraints
- TransE-based knowledge graph embeddings for link prediction
- GraphSAGE-based Graph Neural Network for risk scoring
- Hybrid symbolic + neural inference pipeline
- Explainable risk outputs for public health decision support

------------------------------------------------------------
🧠 Methodology

1. Knowledge Graph Construction
   Integration of healthcare facilities, public transit, and demographic statistics into RDF format.

2. Symbolic Reasoning Layer
   SPARQL rules infer accessibility relationships (e.g., reachable within 15/30/60 minutes).

3. Embedding Layer (TransE)
   Learns latent representations of entities and relations for link prediction and inference.

4. Graph Neural Network Layer (GraphSAGE)
   Predicts continuous risk scores based on graph structure and node features.

5. Hybrid Inference Engine
   Combines symbolic reasoning and learned representations for interpretable predictions.

------------------------------------------------------------
📊 Results

- Strong consistency between rule-based and learned representations
- Improved identification of underserved regions
- Interpretable risk scoring aligned with domain knowledge

------------------------------------------------------------
🎯 Applications

- Public health planning and resource allocation
- Healthcare infrastructure optimization
- Insurance risk modeling
- Socio-spatial inequality analysis

------------------------------------------------------------
🇦🇹 Scope

Focused on Austria, with emphasis on Vienna, Upper Austria, and Tyrol.

Data sources:
- Healthcare facilities (GÖG, data.gv.at)
- Demographic statistics (Statistics Austria)
- Public transit GTFS data (Wiener Linien, ÖBB)

------------------------------------------------------------
