#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|



import os, json
from src.avm.paths import PathHandler

from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip,clips_array
from pydub import AudioSegment





#_  _ _ ___  ____ ____    _  _ ____ _  _ _ _  _ ____ 
#|  | | |  \ |___ |  |    |\/| |__| |_/  | |\ | | __ 
# \/  | |__/ |___ |__|    |  | |  | | \_ | | \| |__] 
                                                    


class videoMaker(PathHandler):
    def __init__(self, root_dir, working_folder_path):
        super().__init__(root_dir, working_folder_path)


        self.translate.print_message("Initialisation du module videoMaker...", progressive_display=True)



    def check_parts(self):
        missing_audio_folders = []
        missing_image_folders = []

        for part_folder in os.listdir(self.parts_dir):
            part_path = os.path.join(self.parts_dir, part_folder)
            if os.path.isdir(part_path):
                files_in_part = os.listdir(part_path)
                audio_files = [file for file in files_in_part if file.endswith(('.wav', '.mp3'))]
                image_files = [file for file in files_in_part if file.endswith(('.png', '.jpg', '.jpeg', '.mp4', '.avi','.mov', '.gif'))]

                if not audio_files:
                    missing_audio_folders.append(part_folder)
                if not image_files:
                    missing_image_folders.append(part_folder)


        if missing_audio_folders or missing_image_folders:
            self.translate.print_message("Le programme ne peut pas s'exécuter car il manque des fichiers dans les dossiers suivants :", progressive_display=True)
            print()
            print()

            if missing_audio_folders:
                self.translate.print_message("Dossiers manquants de fichiers audio :", progressive_display=True)
                print(", ".join(missing_audio_folders))
                print()
                print()

            if missing_image_folders:
                self.translate.print_message("Dossiers manquants de fichiers image :", progressive_display=True)
                print(", ".join(missing_image_folders))
                print()
                print()

            self.prompt_user_action(missing_audio_folders, missing_image_folders)
        else:
            self.translate.print_message("Tous les dossiers sont complets. Prêt pour l'assemblage de la vidéo.", progressive_display=True)
            # Ici, vous pouvez appeler une méthode pour commencer l'assemblage de la vidéo





    def prompt_user_action(self, missing_audio_folders, missing_image_folders):
        self.translate.print_message('Voulez-vous ouvrir les dossiers concernés ? (y/n)', progressive_display=True)
        print()
        self.translate.print_message('Votre réponse :', progressive_display=True)
        response = input()
        if response.lower() == 'y':
            self.open_missing_folders(missing_audio_folders, missing_image_folders)
        elif response.lower() == 'n':
            self.translate.print_message('Relancez le programme après avoir ajouté les fichiers manquants.', progressive_display=True)
        else:
            self.translate.print_message('Réponse non valide. Veuillez entrer y ou n.', progressive_display=True)
            self.prompt_user_action(missing_audio_folders, missing_image_folders)

    def open_missing_folders(self, missing_audio_folders, missing_image_folders):
        missing_folders = set(missing_audio_folders + missing_image_folders)
        for folder in missing_folders:
            os.system(f'start {os.path.join(self.parts_dir, folder)}')
        self.translate.print_message('Les dossiers ont été ouverts. Veuillez ajouter les fichiers manquants et relancer le programme.', progressive_display=True)



    def create_individual_video(self, part_folder):
        # Charger les données de n_scene.json
        with open(self.n_scene_file_path, 'r') as file:
            n_scene_data = json.load(file)
        
        # Trouver les données correspondantes pour cette part
        part_number = int(part_folder.replace('part', ''))
        part_data = next(item for item in n_scene_data if item['some_key'] == part_folder)

        
        # Trouver le chemin du fichier d'expression
        expression_file_path = os.path.join(self.expressions, part_data["CharacterExpression"])
        
        # Trouver le chemin du fichier audio
        audio_file_path = next(os.path.join(self.parts_dir, part_folder, file) for file in os.listdir(os.path.join(self.parts_dir, part_folder)) if file.endswith(('.wav', '.mp3')))
        
        # Calculer la durée du fichier audio
        audio = AudioSegment.from_file(audio_file_path)
        audio_duration = len(audio) // 1000





    def create_individual_video(self, part_folder):

        # Ouvrir le fichier n_scene.json et trouver les données pour cette partie
        with open(self.n_scene_file_path, 'r') as file:
            n_scene_data = json.load(file)
            part_data = n_scene_data[part_folder]  # Ajustez cette ligne selon la structure de votre fichier JSON   

        # Ouvrir l'image/vidéo/gif de fond et la redimensionner/centrer sur le canvas
        background_path = os.path.join(self.parts_dir, part_folder, part_data['Scene'])
        background_clip = VideoFileClip(background_path)  # Ajustez pour prendre en charge les images et les gifs   

        # Ouvrir le fichier d'expression du personnage et le placer en bas à gauche du canvas
        expression_path = os.path.join(self.expressions, part_data['CharacterExpression'])
        expression_clip = VideoFileClip(expression_path)  # Ajustez pour prendre en charge les images et les gifs   

        # Positionner le clip d'expression en bas à gauche, légèrement en dehors du canvas
        expression_clip = expression_clip.set_position(("left", "bottom")).margin(left=5, bottom=5) 

        # Créer une vidéo composite avec le fond et l'expression
        final_video = CompositeVideoClip([background_clip, expression_clip])    

        # Ajouter l'audio à la vidéo
        audio_path = os.path.join(self.parts_dir, part_folder, "audiofile.wav")  # Remplacez par le chemin d'accès réel au fichier audio
        audio_clip = AudioFileClip(audio_path)
        final_video = final_video.set_audio(audio_clip) 

        # Enregistrer la vidéo dans le dossier de la partie
        output_video_path = os.path.join(self.parts_dir, part_folder, "output_video.mp4")
        final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")  

        return



    def assemble_videos(self):
        # Assembler toutes les vidéos individuelles en une seule vidéo
        video_clips = []
        for part_folder in sorted(os.listdir(self.parts_dir), key=lambda x: int(x.replace('part', ''))):
            part_video_path = os.path.join(self.parts_dir, part_folder, 'noSound.mp4')
            video_clips.append(VideoFileClip(part_video_path))

        final_video = clips_array([[clip] for clip in video_clips])
        final_video_path = os.path.join(self.parts_dir, 'noSound.mp4')
        final_video.write_videofile(final_video_path, codec='libx264')

        return


    def extract_and_save_audio(self):

        # Ouvrir le fichier "noSound.mp4"
        assembled_video_path = os.path.join(self.parts_dir, 'noSound.mp4')
        video_clip = VideoFileClip(assembled_video_path)

        # Utiliser moviepy pour extraire l'audio
        audio_clip = video_clip.audio

        # Enregistrer l'audio dans un fichier nommé "noMaster.wav"
        audio_output_path = os.path.join(self.parts_dir, 'noMaster.wav')
        audio_clip.write_audiofile(audio_output_path, codec='pcm_s16le')

        return


    def create_final_video(self):   

        self.check_parts()

        # Parcourez chaque dossier dans parts et appelez create_individual_video pour chaque dossier
        for part_folder in sorted(os.listdir(self.parts_dir), key=lambda x: int(x.replace('part', ''))):
            self.create_individual_video(part_folder)

        self.assemble_videos()
        self.extract_and_save_audio()   

        return  
