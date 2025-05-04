#!/usr/bin/env python3
"""
Script de test pour générer un diagramme UML avec l'UML-MCP-Server
"""

import os
import requests
import zlib
import base64
import json

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
    # Assurer que le code a les balises @startuml/@enduml
    if "@startuml" not in uml_code:
        uml_code = f"@startuml\n{uml_code}\n@enduml"
    
    # Encoder le code
    encoded = plantuml_encode(uml_code)
    
    # Construire l'URL
    url = f"http://www.plantuml.com/plantuml/png/{encoded}"
    
    # Récupérer l'image
    response = requests.get(url)
    
    if response.status_code == 200:
        # Créer le répertoire de sortie si nécessaire
        os.makedirs(output_dir, exist_ok=True)
        
        # Créer un nom de fichier
        file_path = os.path.join(output_dir, "test_diagram.png")
        
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

# Code UML pour un diagramme simple
uml_code = """
@startuml
title Architecture MCP pour WS - Serveur UML

package "Client MCP (Cascade/Ava)" {
  [Assistant IA] as IA
}

package "Serveur UML-MCP" {
  [UML-MCP-Server] as UMCP
  [Processeur PlantUML] as PP
  [Gestionnaire de requêtes] as GR
  [Générateur d'images] as GI
}

cloud "Service PlantUML" {
  [plantuml.com] as PUML
}

folder "Système de fichiers" {
  [Images générées] as IG
}

IA -down-> UMCP : Envoie requête MCP
UMCP -down-> PP : Traite code UML
PP -down-> GR : Prépare requête
GR -right-> PUML : Demande rendu
PUML -left-> GR : Renvoie image
GR -down-> GI : Traite image
GI -down-> IG : Sauvegarde localement
UMCP -up-> IA : Renvoie résultat (URL + chemin local)

note right of IA
  Interprète les besoins
  de l'utilisateur et 
  formule le code UML
end note

note right of UMCP
  Point d'entrée MCP
  conforme au protocole
end note

note right of PUML
  Service externe de 
  rendu PlantUML
end note
@enduml
"""

if __name__ == "__main__":
    # Générer le diagramme
    result = generate_uml_image(uml_code)
    
    # Afficher le résultat complet en JSON formaté
    if result:
        print("\nRésultat complet:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
