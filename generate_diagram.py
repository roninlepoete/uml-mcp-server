#!/usr/bin/env python3
"""
Script pour générer un diagramme UML à partir d'un fichier Markdown
Auteur: Ava
Date: 2025-05-05
"""

import os
import re
import sys
import zlib
import base64
import requests
import argparse
import datetime
from pathlib import Path

def extract_diagram(markdown_file, diagram_type="sequence"):
    """
    Extrait un diagramme de type spécifié depuis un fichier Markdown
    """
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Définir le pattern en fonction du type de diagramme
    if diagram_type == "sequence":
        pattern = r'```mermaid\nsequenceDiagram.*?```'
    elif diagram_type == "flowchart":
        pattern = r'```mermaid\nflowchart.*?```'
    elif diagram_type == "class":
        pattern = r'```mermaid\nclassDiagram.*?```'
    else:
        pattern = r'```mermaid\n.*?```'
    
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # Extraire juste le contenu du diagramme, sans les délimiteurs ```mermaid et ```
        diagram = match.group(0)[10:-3].strip()
        return diagram
    else:
        return None

def convert_mermaid_to_plantuml(mermaid_code, diagram_type="sequence"):
    """
    Convertit le code Mermaid en PlantUML selon le type de diagramme
    """
    if diagram_type == "sequence":
        return convert_sequence_diagram(mermaid_code)
    elif diagram_type == "flowchart":
        return convert_flowchart_diagram(mermaid_code)
    elif diagram_type == "class":
        return convert_class_diagram(mermaid_code)
    else:
        # Pour les autres types, conversion basique
        return "@startuml\n" + mermaid_code + "\n@enduml"

def convert_sequence_diagram(mermaid_code):
    """
    Convertit un diagramme de séquence Mermaid en PlantUML
    """
    plantuml_code = "@startuml\ntitle Diagramme de séquence\n\n"
    
    lines = mermaid_code.strip().split('\n')
    
    for line in lines:
        # Ignorer la ligne sequenceDiagram
        if line.strip() == "sequenceDiagram":
            continue
        # Conserver autonumber
        elif line.strip() == "autonumber":
            plantuml_code += "autonumber\n"
        # Traiter les définitions de participants
        elif "participant" in line:
            plantuml_code += line + "\n"
        # Traiter les flèches de séquence
        elif "->" in line or "->>" in line:
            plantuml_code += line.replace("->>", "->") + "\n"
        # Traiter les notes
        elif "Note over" in line:
            plantuml_code += line + "\n"
        # Ajouter les autres lignes qui ne nécessitent pas de conversion
        elif line.strip():
            plantuml_code += line + "\n"
    
    plantuml_code += "@enduml"
    return plantuml_code

def convert_flowchart_diagram(mermaid_code):
    """
    Convertit un diagramme flowchart Mermaid en PlantUML
    """
    plantuml_code = "@startuml\n"
    
    # Transformation basique - à améliorer pour une meilleure conversion
    plantuml_code += "title Diagramme de flux\n\n"
    plantuml_code += "' Converti depuis Mermaid flowchart\n"
    plantuml_code += "' Note: La conversion directe peut nécessiter des ajustements manuels\n\n"
    
    lines = mermaid_code.strip().split('\n')
    for line in lines:
        if "flowchart" in line or "graph" in line:
            if "TB" in line:
                plantuml_code += "top to bottom direction\n"
            elif "LR" in line:
                plantuml_code += "left to right direction\n"
        elif "-->" in line:
            plantuml_code += line.replace("-->", "->") + "\n"
        elif "subgraph" in line:
            package_name = line.split("subgraph")[1].strip()
            plantuml_code += f"package {package_name} {{\n"
        elif "end" == line.strip():
            plantuml_code += "}\n"
        elif line.strip():
            plantuml_code += line + "\n"
    
    plantuml_code += "@enduml"
    return plantuml_code

def convert_class_diagram(mermaid_code):
    """
    Convertit un diagramme de classe Mermaid en PlantUML
    """
    plantuml_code = "@startuml\ntitle Diagramme de classe\n\n"
    
    lines = mermaid_code.strip().split('\n')
    for line in lines:
        if "classDiagram" in line:
            continue
        elif "class" in line and "{" in line:
            plantuml_code += line.replace("{", " {") + "\n"
        elif "-->" in line:
            plantuml_code += line.replace("-->", "-->") + "\n"
        elif line.strip():
            plantuml_code += line + "\n"
    
    plantuml_code += "@enduml"
    return plantuml_code

def plantuml_encode(text):
    """
    Encode le texte PlantUML pour l'URL avec correction pour éviter le problème HUFFMAN
    """
    compressed = zlib.compress(text.encode('utf-8'))
    return base64.b64encode(compressed).decode('ascii')

def generate_uml_image(uml_code, output_dir="output", base_name="diagram"):
    """
    Génère une image UML à partir du code PlantUML
    """
    # Encoder le code
    encoded = plantuml_encode(uml_code)
    
    # Construire l'URL (avec ~1 pour corriger l'encodage HUFFMAN)
    url = f"http://www.plantuml.com/plantuml/png/~1{encoded}"
    
    # Créer le répertoire de sortie si nécessaire
    os.makedirs(output_dir, exist_ok=True)
    
    # Créer un nom de fichier avec format DateDuJour_hh_mm
    current_time = datetime.datetime.now()
    filename = current_time.strftime("%Y%m%d_%H%M") + f"_{base_name}.png"
    file_path = os.path.join(output_dir, filename)
    
    try:
        # Récupérer l'image
        response = requests.get(url)
        
        if response.status_code == 200:
            # Sauvegarder l'image localement
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Diagramme UML généré avec succès!")
            print(f"URL du diagramme: {url}")
            print(f"Chemin local: {os.path.abspath(file_path)}")
            
            return {
                "code": uml_code,
                "url": url,
                "local_path": os.path.abspath(file_path)
            }
        else:
            print(f"Erreur lors de la génération du diagramme: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erreur lors de la génération du diagramme: {str(e)}")
        # En cas d'erreur avec PlantUML, suggérer l'utilisation de Mermaid
        print("Suggestion: Utilisez la bibliothèque Mermaid pour une meilleure compatibilité.")
        return None

def create_html_viewer(diagram_path, mermaid_code, base_name="diagram"):
    """
    Crée un fichier HTML pour visualiser le diagramme
    """
    output_dir = os.path.dirname(diagram_path)
    html_path = os.path.join(output_dir, f"{base_name}_viewer.html")
    
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualiseur de diagramme</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@9.3.0/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #333;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }}
        .mermaid-container {{
            text-align: center;
            margin: 20px 0;
            background-color: white;
        }}
        .controls {{
            margin: 20px 0;
            text-align: center;
        }}
        button {{
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 0 5px;
        }}
        button:hover {{
            background-color: #45a049;
        }}
        .image-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .image-container img {{
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .image-controls {{
            margin: 20px 0;
            text-align: center;
        }}
        .metadata {{
            margin-top: 30px;
            padding: 10px;
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Visualiseur de diagramme</h1>
        
        <div class="controls">
            <button onclick="showMermaid()">Afficher en Mermaid</button>
            <button onclick="showImage()">Afficher l'image</button>
        </div>
        
        <div id="mermaid-container" class="mermaid-container">
            <div class="mermaid" style="display: none;">
{mermaid_code}
            </div>
        </div>
        
        <div id="image-container" class="image-container">
            <img src="{os.path.basename(diagram_path)}" alt="Diagramme">
        </div>
        
        <div class="image-controls">
            <button onclick="saveAsSVG()">Exporter en SVG</button>
            <button onclick="saveAsPNG()">Exporter en PNG</button>
        </div>
        
        <div class="metadata">
            <p><strong>Date de génération:</strong> {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <p><strong>Généré par:</strong> Ava via PlantUML-MCP-Server</p>
        </div>
    </div>

    <script>
        // Initialiser Mermaid
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            logLevel: 'fatal',
            securityLevel: 'strict',
            sequence: {{
                diagramMarginX: 50,
                diagramMarginY: 10,
                actorMargin: 80,
                width: 150,
                height: 65,
                boxTextMargin: 10,
                noteMargin: 10,
                messageMargin: 35,
                mirrorActors: true
            }},
            flowchart: {{
                useMaxWidth: false
            }}
        }});
        
        // Fonction pour basculer l'affichage
        function showMermaid() {{
            document.querySelector('.mermaid').style.display = 'block';
            document.getElementById('image-container').style.display = 'none';
        }}
        
        function showImage() {{
            document.querySelector('.mermaid').style.display = 'none';
            document.getElementById('image-container').style.display = 'block';
        }}
        
        // Fonction pour exporter en SVG
        function saveAsSVG() {{
            const svgElement = document.querySelector('.mermaid svg');
            if (svgElement) {{
                const svgData = new XMLSerializer().serializeToString(svgElement);
                const svgBlob = new Blob([svgData], {{type: 'image/svg+xml;charset=utf-8'}});
                const svgUrl = URL.createObjectURL(svgBlob);
                const downloadLink = document.createElement('a');
                
                downloadLink.href = svgUrl;
                downloadLink.download = '{os.path.splitext(os.path.basename(diagram_path))[0]}.svg';
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
            }} else {{
                // Si le SVG Mermaid n'est pas généré, télécharger depuis l'image
                const img = document.querySelector('#image-container img');
                fetch(img.src)
                .then(res => res.blob())
                .then(blob => {{
                    const a = document.createElement('a');
                    a.href = URL.createObjectURL(blob);
                    a.download = '{os.path.splitext(os.path.basename(diagram_path))[0]}.png';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                }});
            }}
        }}
        
        // Fonction pour exporter en PNG
        function saveAsPNG() {{
            const img = document.querySelector('#image-container img');
            fetch(img.src)
            .then(res => res.blob())
            .then(blob => {{
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = '{os.path.splitext(os.path.basename(diagram_path))[0]}.png';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }});
        }}
    </script>
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Visualiseur HTML créé: {os.path.abspath(html_path)}")
    return html_path

def main():
    """
    Fonction principale
    """
    parser = argparse.ArgumentParser(description='Générateur de diagrammes UML depuis des fichiers Markdown')
    parser.add_argument('--source', '-s', required=True, help='Chemin du fichier Markdown source')
    parser.add_argument('--type', '-t', default='sequence', choices=['sequence', 'flowchart', 'class'], help='Type de diagramme à extraire')
    parser.add_argument('--output', '-o', default='output', help='Dossier de sortie')
    parser.add_argument('--name', '-n', default='diagram', help='Nom de base du fichier de sortie')
    
    args = parser.parse_args()
    
    # Vérifier si le fichier source existe
    if not os.path.exists(args.source):
        print(f"Erreur: Le fichier {args.source} n'existe pas.")
        return 1
    
    # Extraire le diagramme
    mermaid_diagram = extract_diagram(args.source, args.type)
    
    if not mermaid_diagram:
        print(f"Aucun diagramme de type {args.type} trouvé dans {args.source}")
        return 1
    
    print(f"Diagramme {args.type} extrait avec succès!")
    
    # Convertir en PlantUML
    plantuml_code = convert_mermaid_to_plantuml(mermaid_diagram, args.type)
    
    # Générer l'image
    result = generate_uml_image(plantuml_code, args.output, args.name)
    
    if result:
        # Créer le visualiseur HTML
        create_html_viewer(result["local_path"], mermaid_diagram, args.name)
        print("\nTraitement terminé avec succès!\n")
        return 0
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
