# PlantUML-MCP-Server

## Introduction

PlantUML-MCP-Server est un outil de génération de diagrammes UML basé sur le protocole MCP (Model Context Protocol). Il permet de générer différents types de diagrammes UML à partir de descriptions en langage naturel ou de code PlantUML.

Ce module fait partie de la suite d'outils de diagrammes du workspace WSurfWSpaceGlobal, complémentaire à RestAPIDiagrammeFabric.

## Fonctionnalités principales

- Support de multiples types de diagrammes UML : diagrammes de classe, de séquence, d'activité, de cas d'utilisation, etc.
- Génération de diagrammes UML à partir de descriptions en langage naturel
- Utilisation directe de code PlantUML pour générer des diagrammes
- Retourne le code PlantUML et des liens URL accessibles pour faciliter le partage et la visualisation
- Sauvegarde locale des diagrammes générés avec horodatage
- Support pour les chemins de sauvegarde personnalisés
- Intégration en tant que serveur MCP avec d'autres clients compatibles

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Accès à Internet pour la génération des diagrammes via l'API PlantUML

### Configuration de l'environnement

1. Création et activation d'un environnement virtuel :

```powershell
cd "Diagramme Maker\PlantUML-MCP-Server"
python -m venv plantuml-mcp-venv
.\plantuml-mcp-venv\Scripts\activate
```

2. Installation des dépendances :

```powershell
pip install -r requirements.txt
```

## Utilisation

### Utilisation directe dans le workspace

Le module peut être utilisé directement depuis la ligne de commande :

```powershell
python uml_mcp_server.py
```

### Pour générer un diagramme à partir d'un fichier Markdown

Nous avons créé un script `generate_diagram.py` qui permet d'extraire et de convertir les diagrammes depuis des fichiers Markdown :

```powershell
python generate_diagram.py --source "chemin/vers/fichier.md" --type "sequence"
```

Les diagrammes générés seront sauvegardés dans le dossier `output` avec le format de nommage standard `YYYYMMDD_HHMM_name.png`.

### Problèmes connus et solutions

#### Erreur d'encodage HUFFMAN

Si vous rencontrez une erreur indiquant "This URL does not look like DEFLATE data. It looks like your plugin is using HUFFMAN encoding", il s'agit d'un problème avec le service en ligne PlantUML.

**Solutions possibles :**
1. Ajouter le préfixe "~1" à l'URL PlantUML
2. Utiliser directement Mermaid pour le rendu dans un navigateur (recommandé)

> ⚠️ **Note importante :** Pour les diagrammes de séquence complexes, il est généralement préférable d'utiliser directement Mermaid dans un fichier HTML comme alternative plus fiable.

### Convention de nommage et stockage

Les diagrammes générés doivent être stockés selon les conventions suivantes :

1. Dossier : `[Projet]/diagrammes/YYYY-MM-DD_HH_MM/`
2. Nom de fichier : `YYYYMMDD_HHMM_[type]_[nom].png`
3. Viewer HTML : `[nom]_viewer.html` dans le même dossier

## Intégration avec le workflow existant

PlantUML-MCP-Server est conçu pour compléter RestAPIDiagrammeFabric dans les cas où des diagrammes UML spécifiques sont nécessaires. Il est particulièrement utile pour :

1. Extraire et visualiser des diagrammes depuis la documentation existante
2. Générer rapidement des diagrammes de séquence à partir de descriptions
3. Servir d'outil d'aide pour Ava lors de l'analyse et la génération de diagrammes

## Références

- [Guide Mermaid optimisé](../md/guide-mermaid-optimise.md)
- [Documentation RestAPIDiagrammeFabric](../RestAPIDiagrammeFabric/md/README.md)
- [Exemples de diagrammes SGAF](../../MTQ/SGAF/diagrammes/)
