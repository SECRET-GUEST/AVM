#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|



import os, json
from src.avm.paths import PathHandler


#___ ____ _  _ ___    ___ ____    ____ ___  ____ ____ ____ _  _ 
# |  |___  \/   |      |  |  |    [__  |__] |___ |___ |    |__| 
# |  |___ _/\_  |      |  |__|    ___] |    |___ |___ |___ |  | 


# Génere les fichiers son dans un dossier sentences dans le dossier storyboard


class SendToSpeech(PathHandler):
    def __init__(self, root_dir, working_folder_path):
        super().__init__(root_dir, working_folder_path)

    def generate_audio_files(self):
        # Lisez le fichier n_scene.json
        with open(self.n_scene_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    
        # Initialisez idx à 0
        idx = 0
    
        # Parcourez chaque élément dans le fichier json
        for item in data:
            for key, value in item.items():
                if key.startswith("Phrase"):
                    # Incrémente idx chaque fois qu'une clé qui commence par "Phrase" est trouvée
                    idx += 1
    
                    # Créez le dossier 'partX' s'il n'existe pas
                    part_dir = os.path.join(self.working_folder_path, 'parts', f'part{idx}')
                    if not os.path.exists(part_dir):
                        os.makedirs(part_dir)
                    
                    # Construisez et exécutez la commande
                    command = f'python "{os.path.join(self.tortoise_dir,"scripts","tortoise_tts.py")}" "{value}" -v william -p ultra_fast --seed -1 --cvvp-amount 0.0 --num-autoregressive-samples 4 --diffusion-iterations 32 --temperature 0.8 --length-penalty 1.0 --repetition-penalty 4.0 --top-p 0.8 --max-mel-tokens 500 --cond-free True --cond-free-k 0 --diffusion-temperature 0.8 -O "{part_dir}" -fn "{key}"'
                    os.system(command)

        # Après la génération de tous les fichiers, effectuez la suppression et le renommage
        # Pourquoi apres ? => pourquoi apres...???????? pourquoi ????????
        self.handle_generated_files()

    def handle_generated_files(self):
        parts_dir = os.path.join(self.working_folder_path, 'parts')
        for root, dirs, _ in os.walk(parts_dir):
            for dir in dirs:
                part_dir = os.path.join(root, dir)
                generated_files = [f for f in os.listdir(part_dir) if os.path.isfile(os.path.join(part_dir, f))]

                # Identification du fichier à renommer
                file_to_rename = None
                for file in generated_files:
                    if file.endswith(".wav") and not file.endswith("_combined.wav"):
                        file_to_rename = file
                        break   

                # Suppression des fichiers combinés
                for file in generated_files:
                    if file.endswith("_combined.wav"):
                        os.remove(os.path.join(part_dir, file)) 

                # Renommage du fichier identifié
                if file_to_rename:
                    old_file_path = os.path.join(part_dir, file_to_rename)
                    file_extension = os.path.splitext(file_to_rename)[1]
                    new_file_path = os.path.join(part_dir, f"phrase{file_extension}")
                    os.rename(old_file_path, new_file_path) 







