#!/usr/bin/env python3
"""
Script pour générer un diagramme UML pour le projet SGAF à partir du fichier Markdown
"""

import os
import requests
import zlib
import base64
import json
import re
import datetime

def extract_mermaid_sequence_diagram(markdown_file):
    """
    Extrait le diagramme de séquence Mermaid du fichier Markdown
    """
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Recherche du bloc de diagramme de séquence
    sequence_pattern = r'```mermaid\nsequenceDiagram.*?```'
    match = re.search(sequence_pattern, content, re.DOTALL)
    
    if match:
        # Extraire juste le contenu du diagramme, sans les délimiteurs ```mermaid et ```
        diagram = match.group(0)[10:-3].strip()
        return diagram
    else:
        return None

def convert_mermaid_to_plantuml(mermaid_code):
    """
    Convertit le code Mermaid en PlantUML pour le diagramme de séquence
    """
    plantuml_code = "@startuml\ntitle Services d'authentification ministérielle - Flux d'authentification SGAF\n\n"
    
    # Traiter chaque ligne du code Mermaid
    lines = mermaid_code.strip().split('\n')
    
    for line in lines:
        # Ignorer la ligne autonumber
        if line.strip() == "autonumber":
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
        elif line.strip() and not "sequenceDiagram" in line:
            plantuml_code += line + "\n"
    
    plantuml_code += "@enduml"
    return plantuml_code

def plantuml_encode(text):
    """
    Encode le texte PlantUML pour l'URL
    """
    compressed = zlib.compress(text.encode('utf-8'))
    return base64.b64encode(compressed).decode('ascii')

def generate_uml_image(uml_code, output_dir="output"):
    """
    Génère une image UML à partir du code PlantUML
    """
    # Encoder le code
    encoded = plantuml_encode(uml_code)
    
    # Construire l'URL (avec ~1 pour corriger l'encodage HUFFMAN)
    url = f"http://www.plantuml.com/plantuml/png/~1{encoded}"
    
    # Récupérer l'image
    response = requests.get(url)
    
    if response.status_code == 200:
        # Créer le répertoire de sortie si nécessaire
        os.makedirs(output_dir, exist_ok=True)
        
        # Créer un nom de fichier avec format DateDuJour_hh_mn
        current_time = datetime.datetime.now()
        filename = current_time.strftime("%Y%m%d_%H%M") + "_sgaf_auth_sequence.png"
        file_path = os.path.join(output_dir, filename)
        
        # Sauvegarder l'image localement
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Diagramme UML généré avec succès!")
        print(f"URL du diagramme: {url}")
        print(f"Chemin local: {os.path.abspath(file_path)}")
        
        result = {
            "code": uml_code,
            "url": url,
            "local_path": os.path.abspath(file_path)
        }
        return result
    else:
        print(f"Erreur lors de la génération du diagramme: {response.status_code}")
        return None

if __name__ == "__main__":
    # Chemin du fichier Markdown
    markdown_file = r"E:\WSurfWSpaceGlobal\MTQ\SGAF\md\Services_authentification_minister_Project_SGAF.md"
    
    # Extraire le diagramme de séquence
    mermaid_diagram = extract_mermaid_sequence_diagram(markdown_file)
    
    if mermaid_diagram:
        print("Diagramme de séquence Mermaid extrait avec succès!")
        
        # Convertir en PlantUML
        plantuml_code = convert_mermaid_to_plantuml(mermaid_diagram)
        
        # Générer l'image
        result = generate_uml_image(plantuml_code)
        
        # Afficher le résultat complet en JSON formaté
        if result:
            print("\nRésultat complet:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Aucun diagramme de séquence trouvé dans le fichier Markdown.")
