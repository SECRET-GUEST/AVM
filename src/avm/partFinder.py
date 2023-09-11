#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|



import os, json,shutil,glob

import requests, random
from shutil import copy
import pandas as pd
from random import choice
from src.avm.paths import PathHandler


#___  ____ ____ ___ ____    ____ _ _  _ ___  ____ ____ 
#|__] |__| |__/  |  [__     |___ | |\ | |  \ |___ |__/ 
#|    |  | |  \  |  ___]    |    | | \| |__/ |___ |  \ 
                


class videoParts(PathHandler):
    def __init__(self, root_dir, working_folder_path):
        super().__init__(root_dir, working_folder_path)
        
        self.basic_image_chosen = None

        self.translate.print_message("Initialisation...", progressive_display=True)

        if not os.path.exists(self.parts_dir):
            os.makedirs(self.parts_dir)
            self.translate.print_message(f"Dossier 'parts' créé à l'emplacement : {self.parts_dir}", progressive_display=True)

        self.scene_image_mapping = {}






# Lanceur
    def start_video_creation(self):
        self.translate.print_message("Début de la création de la vidéo...", progressive_display=True)
        n_scene_data = self.load_n_scene()
        image_data = self.load_image_database()
        self.process_scenes(n_scene_data, image_data)
        self.rename_images() # Renomme les images "2" 
        self.expression_sorting() 






# Fonctions de récupérations des informations dans le csv, ou ailleurs
    def load_n_scene(self):
        self.translate.print_message("Chargement du fichier n_scene.json...")
        with open(self.n_scene_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def load_image_database(self):
        self.translate.print_message("Chargement de la base de données d'images...")
        image_data = pd.read_csv(self.image_database_csv, low_memory=False, dtype={'ImageID': str, 'Title': str, 'OriginalURL': str})
        return image_data

    def find_image_by_title(self, keyword, image_data):
        self.translate.print_message(f"Recherche d'images avec le titre contenant : {keyword}...")
        matched_images = image_data[image_data['Title'].str.contains(keyword, case=False, na=False, regex=True)]
        return matched_images

    def download_image(self, url, part_dir):
        self.translate.print_message(f"Téléchargement de l'image depuis l'URL : {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            image_name = os.path.basename(url)
            image_path = os.path.join(part_dir, image_name)
            with open(image_path, 'wb') as file:
                file.write(response.content)
            return image_path
        else:
            return None
        

    def get_basic_image(self, part_dir, scene_keyword=None):
        self.translate.print_message("Recherche d'une image basique...")
        
        basic_images = [f for f in os.listdir(self.basics_dir) if os.path.isfile(os.path.join(self.basics_dir, f))]

        if basic_images:
            if self.basic_image_chosen is None:
                self.basic_image_chosen = random.choice(basic_images)       

            chosen_image = self.basic_image_chosen
            source_path = os.path.join(self.basics_dir, chosen_image)
            destination_path = os.path.join(part_dir, chosen_image)
            copy(source_path, destination_path)
            self.translate.print_message(f"Image basique choisie et copiée vers : {destination_path}")
            self.log_image_info(scene_keyword or "Basic Image", "basic image", part_dir)  # Log l'info ici
            return destination_path

        else:
            self.translate.print_message("Aucune images standard trouvées dans le dossier basics")
            return None


    def rename_images(self):
        for part_dir in glob.glob(os.path.join(self.parts_dir, 'part*')):
            for file_path in glob.glob(os.path.join(part_dir, '*')):
                file_extension = os.path.splitext(file_path)[1]  
                new_file_path = os.path.join(part_dir, f"2{file_extension}")  
                os.rename(file_path, new_file_path)  
                self.translate.print_message(f"Fichier renommé : {new_file_path}")



# Lance la répartition des images dans les dossiers correspodants
    def process_scenes(self, n_scene_data, image_data):
        self.translate.print_message("Traitement des scènes...")

        # Créer un ensemble pour suivre les scènes sans images
        scenes_without_images = set()

        for idx, item in enumerate(n_scene_data):
            self.translate.print_message(f"Traitement de l'élément {idx+1} : {item}")  

            # Trouver toutes les clés de scènes dans l'élément actuel
            scene_keys = [key for key in item.keys() if key.startswith("Scene")]

            for scene_key in scene_keys:
                scene_keyword = item.get(scene_key)
                part_number = int(scene_key.replace("Scene", ""))
                part_dir = os.path.join(self.parts_dir, f'part{part_number}')

                if not os.path.exists(part_dir):
                    os.makedirs(part_dir)
                    self.translate.print_message(f"Dossier créé : {part_dir}")  

                if scene_keyword:
                    self.translate.print_message(f"Mot-clé de scène trouvé : {scene_keyword}")  

                    if scene_keyword in scenes_without_images:
                        self.translate.print_message(f"Aucune images correspondante à {scene_keyword} trouvée précédemment. Utilisation d'une image basique à la place.")
                        self.get_basic_image(part_dir)
                        continue

                    if scene_keyword not in self.scene_image_mapping:
                        matched_images = self.find_image_by_title(scene_keyword, image_data)
                        if not matched_images.empty:
                            random_image = choice(matched_images.to_dict('records'))
                            image_url = random_image.get('OriginalURL')
                            image_title = random_image.get('Title')  # Obtenez le titre de l'image ici
                            if image_url:
                                downloaded_image_path = self.download_image(image_url, part_dir)
                                if downloaded_image_path:
                                    # Mise à jour du mappage des images de scène
                                    self.scene_image_mapping[scene_keyword] = downloaded_image_path
                                    self.log_image_info(image_title, image_url, part_dir)  # Log l'info ici
                                else:
                                    self.translate.print_message(f"Impossible de télécharger l'image correspondante à {scene_keyword}. Utilisation d'une image basique à la place.")
                                    self.get_basic_image(part_dir, scene_keyword)  
                                    scenes_without_images.add(scene_keyword)
                            else:
                                self.translate.print_message(f"Aucune URL pour {scene_keyword}. Utilisation d'une image basique à la place.")
                                self.get_basic_image(part_dir, scene_keyword)  
                                scenes_without_images.add(scene_keyword)
                        else:
                            self.translate.print_message(f"Aucune images correspondante à {scene_keyword}. Utilisation d'une image basique à la place.")
                            self.get_basic_image(part_dir, scene_keyword)  
                            scenes_without_images.add(scene_keyword)
                    else:
                        existing_image_path = self.scene_image_mapping[scene_keyword]
                        new_image_path = os.path.join(part_dir, os.path.basename(existing_image_path))
                        copy(existing_image_path, new_image_path)
                        self.translate.print_message(f"Image copiée avec succès vers : {new_image_path}")
                else:
                    self.translate.print_message("Aucun mots clé de scène trouvé, utilisation d'une image basique à la place.")
                    self.get_basic_image(part_dir)



    def expression_sorting(self):
        # Lisez le fichier n_scene.json
        with open(self.n_scene_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Parcourez chaque élément dans le fichier json
        for item in data:
            # Cherchez les clés qui commencent par "CharacterExpression"
            for key, value in item.items():
                if key.startswith("CharacterExpression"):

                    # Extrait le numéro de l'expression (par exemple, '1' de 'CharacterExpression1')
                    expression_number = int(key.replace("CharacterExpression", ""))

                    # Déterminez le dossier de destination (par exemple, 'part1' pour 'CharacterExpression1')
                    part_dir = os.path.join(self.parts_dir, f'part{expression_number}')
                    if not os.path.exists(part_dir):
                        os.makedirs(part_dir)

                    
                    # Construisez le chemin vers le fichier d'expression dans le dossier assets/Character/expression
                    expression_file_path = os.path.join(self.expressions, f"{value}.*")
                    
                    # Utilisez glob pour trouver le fichier avec l'extension correcte (peut être .gif, .png, .jpg, .mp4, .avi)
                    found_files = glob.glob(expression_file_path)
                    
                    # Si aucun fichier n'est trouvé, utilisez le fichier 'smile' par défaut
                    if not found_files:
                        found_files = glob.glob(os.path.join(self.expressions, "smile.*"))

                    # Copiez le fichier trouvé dans le dossier de destination et renommez-le
                    if found_files:
                        # Obtenez l'extension du fichier trouvé
                        extension = os.path.splitext(found_files[0])[1]
                        
                        # Construisez le chemin de destination avec le nom "1" et l'extension appropriée
                        destination_file_path = os.path.join(part_dir, f"1{extension}")
                        
                        # Copiez le fichier
                        shutil.copy(found_files[0], destination_file_path)





# Crée un logger pour avoir une trace de l'assemblage
    def log_image_info(self, title, url, part_dir):
        parent_dir = os.path.dirname(self.parts_dir)
        log_file_path = os.path.join(parent_dir, 'asm_logs.txt')
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Title : {title}\n")
            log_file.write(f"url : {url}\n")
            log_file.write(f"dossier : {os.path.basename(part_dir)}\n\n")


