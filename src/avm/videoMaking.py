#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|



import os, random,subprocess,shutil
from src.avm.paths import PathHandler

from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips



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
            for part_folder in sorted(os.listdir(self.parts_dir), key=lambda x: int(x.replace('part', ''))):
                self.execute_process(part_folder)   





    def execute_process(self, part_folder):
        self.translate.print_message("Démarrage du processus global...", progressive_display=True)  

        self.translate.print_message(f"\nTraitement du dossier : {part_folder}", progressive_display=True)  

        self.translate.print_message("\nÉtape 1 : Création des vidéos individuelles", progressive_display=True)
        self.create_individual_video()  

        self.translate.print_message("\nÉtape 2 : Assemblage des vidéos", progressive_display=True)
        self.assemble_videos()  

        self.translate.print_message("\nÉtape 3 : Assemblage final", progressive_display=True)
        self.assemble_final()   







    def prompt_user_action(self, missing_audio_folders, missing_image_folders):
        total_missing_folders = list(set(missing_audio_folders + missing_image_folders))

        if len(total_missing_folders) > 3:
            self.translate.print_message(f"Il y a {len(total_missing_folders)} dossiers manquants, ce qui pourrait indiquer un problème avec l'exécution du script.", progressive_display=True)
            self.translate.print_message("Il est peut-être préférable de redémarrer avec un nouveau dossier pour éviter des problèmes potentiels.", progressive_display=True)

            # Ouvrir le dossier source des parties (parts_dir)
            os.system(f'start {self.parts_dir}')

            # Demander à l'utilisateur s'il veut relancer le script
            while True:
                self.translate.print_message('Voulez-vous relancer le script? (y/n)', progressive_display=True)
                print()
                self.translate.print_message('Votre réponse :', progressive_display=True)
                response = input()
                if response.lower() in ['y', 'n']:
                    break
                else:
                    self.translate.print_message('Réponse non valide. Veuillez entrer y ou n.', progressive_display=True)

            # Si l'utilisateur choisit de relancer, rappeler la méthode check_parts
            if response.lower() == 'y':
                self.check_parts()
            # Si l'utilisateur choisit de ne pas relancer, fermer le CMD
            elif response.lower() == 'n':
                self.translate.print_message('Fermeture du programme.', progressive_display=True)
                exit()  # Fermer le script/terminal

        else:
            while True:
                self.translate.print_message('Voulez-vous ouvrir les dossiers concernés ? (y/n)', progressive_display=True)
                print()
                self.translate.print_message('Votre réponse :', progressive_display=True)
                response = input()
                if response.lower() in ['y', 'n']:
                    break
                else:
                    self.translate.print_message('Réponse non valide. Veuillez entrer y ou n.', progressive_display=True)

            if response.lower() == 'y':
                self.open_missing_folders(missing_audio_folders, missing_image_folders)
            elif response.lower() == 'n':
                self.translate.print_message('Relancez le programme après avoir ajouté les fichiers manquants.', progressive_display=True)


    def open_missing_folders(self, missing_audio_folders, missing_image_folders):
        missing_folders = set(missing_audio_folders + missing_image_folders)
        for folder in missing_folders:
            os.system(f'start {os.path.join(self.parts_dir, folder)}')
        self.translate.print_message('Les dossiers ont été ouverts. Veuillez ajouter les fichiers manquants et relancer le programme.', progressive_display=True)






    def resizer(self, clip, max_height=1080, max_width=1920):

#        Cette fonction redimensionne un clip (vidéo, image, ou GIF) sans étirement,
#        en s'assurant que la hauteur n'excède pas 1080px et la largeur n'excède pas 1920px.

        clip_aspect_ratio = clip.w / clip.h
        new_width = min(clip.w, max_width)
        new_height = min(clip.h, max_height)

        # Si le redimensionnement pour atteindre la largeur maximale fait dépasser la hauteur maximale,
        # alors nous ajustons la largeur pour maintenir l'aspect ratio.
        if new_width / clip_aspect_ratio > max_height:
            new_width = max_height * clip_aspect_ratio

        # De même, si le redimensionnement pour atteindre la hauteur maximale fait dépasser la largeur maximale,
        # alors nous ajustons la hauteur pour maintenir l'aspect ratio.
        if new_height * clip_aspect_ratio > max_width:
            new_height = max_width / clip_aspect_ratio

        return clip.resize(newsize=(int(new_width), int(new_height)))   







    def create_individual_video(self):
        self.translate.print_message("Création des vidéos individuelles en cours...", progressive_display=True)
        self.spinner.loading_start()

        # Obtenez un fichier image aléatoire du dossier basics comme calque de fond (layer 0)
        background_image = random.choice([os.path.join(self.basics_dir, f) for f in os.listdir(self.basics_dir) if os.path.isfile(os.path.join(self.basics_dir, f))])
        background_clip = ImageClip(background_image).set_duration(0)   

        # Parcourez chaque dossier dans self.parts_dir
        for part_folder in sorted(os.listdir(self.parts_dir), key=lambda x: int(x.replace('part', ''))):
            self.spinner.loading_stop()
            self.translate.print_message(f"Traitement de : {part_folder}", progressive_display=False)
            self.spinner.loading_start()    

            part_folder_path = os.path.join(self.parts_dir, part_folder)    

            audio_path = os.path.join(part_folder_path, 'phrase.wav')
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration  

            background_clip = background_clip.set_duration(duration)
            clips = [background_clip]   

            layer_files = sorted([f for f in os.listdir(part_folder_path) if os.path.isfile(os.path.join(part_folder_path, f)) and f.split('.')[0].isdigit()], key=lambda x: int(x.split('.')[0]))  

            for layer_file in layer_files:
                self.spinner.loading_stop()
                self.translate.print_message(f"Traitement de la couche : {layer_file}", progressive_display=False)
                self.spinner.loading_start()

                layer_file_path = os.path.join(part_folder_path, layer_file)
                layer_clip = VideoFileClip(layer_file_path) if layer_file_path.lower().endswith(('mp4', 'avi')) else ImageClip(layer_file_path) 

                layer_clip = self.resizer(layer_clip, height=1080)
                layer_clip = layer_clip.set_duration(duration)
                clips.append(layer_clip)    

            self.spinner.loading_stop()
            self.translate.print_message("Assemblage des clips et écriture de la vidéo finale...", progressive_display=True)
            self.spinner.loading_start()    

            final_video = CompositeVideoClip(clips)
            final_video = final_video.set_audio(audio_clip) 

            output_video_path = os.path.join(part_folder_path, f'{part_folder}.mp4')
            final_video.write_videofile(output_video_path, codec="libx264", audio_codec="pcm_s16le", bitrate="5000k", audio_bitrate="1536k", threads=4) 

        self.spinner.loading_stop()
        self.translate.print_message("Création des vidéos individuelles terminée.", progressive_display=True)   






    def assemble_videos(self):
        self.translate.print_message("Début de l'assemblage des vidéos...", progressive_display=True)
        self.spinner.loading_start()    

        # Parcours tous les dossiers partX et récupérer les chemins des fichiers outputX.mp4
        video_paths = []
        for part_folder in sorted(os.listdir(self.parts_dir), key=lambda x: int(x.replace('part', ''))):
            part_folder_path = os.path.join(self.parts_dir, part_folder)
            video_path = os.path.join(part_folder_path, f'{part_folder}.mp4')
            if os.path.exists(video_path):
                video_paths.append(video_path)

                self.spinner.loading_stop()
                self.translate.print_message(f"Traitement de : {part_folder}", progressive_display=False)
                self.spinner.loading_start()    

        self.spinner.loading_stop()
        self.translate.print_message("Fusion des vidéos en une seule...", progressive_display=True)
        self.spinner.loading_start()    

        # Fusionne tous les outputX.mp4 en une grande vidéo
        video_clips = [VideoFileClip(vp) for vp in video_paths]
        final_video_clip = concatenate_videoclips(video_clips, method="compose")    

        self.spinner.loading_stop()
        self.translate.print_message("Écriture de la vidéo dans un fichier nosound.mp4...", progressive_display=True)
        self.spinner.loading_start()    

        # Écrit la vidéo dans un fichier nosound.mp4
        nosound_path = os.path.join(self.parts_dir, 'nosound.mp4')
        final_video_clip.write_videofile(nosound_path, codec="libx264", audio_codec="pcm_s16le", bitrate="5000k", audio_bitrate="1536k", threads=4) 

        self.spinner.loading_stop()
        self.translate.print_message("Extraction de l'audio de nosound.mp4 et écriture dans un fichier sound.wav...", progressive_display=True)
        self.spinner.loading_start()    

        # Extrait l'audio de nosound.mp4 et l'écrire dans un fichier sound.wav (et non sound.mp4)
        audio_clip = final_video_clip.audio
        sound_path = os.path.join(self.parts_dir, 'sound.wav')
        audio_clip.write_audiofile(sound_path, codec="pcm_s16le")   

        self.spinner.loading_stop()
        self.translate.print_message("Assemblage des vidéos terminé.", progressive_display=True)    




    def toRVC(self):
        commande = [
            "python", 
            os.path.join(self.rvc_path, "commander.py"), 
            "0", 
            os.path.join(self.parts_dir, "sound_path.wav"), 
            "",  # chemin_index, que nous laissons vide pour le moment
            "harvest", 
            os.path.join(self.parts_dir, "soundHD.wav"), 
            os.path.join(self.rvc_path, "assets", "pretrained_v2", "G48K.pth"), 
            "0.6", 
            "cuda:0", 
            "True", 
            "5", 
            "44100", 
            "0.5", 
            "0.33"
        ]

        try:       
            self.translate.print_message("Envois du son vers RVC...", progressive_display=True)

            processus = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, stderr = processus.communicate()

            if processus.returncode != 0:
                raise Exception(stderr)
            else:
                self.translate.print_message("La commande a été exécutée avec succès", progressive_display=True)

        
        except Exception as e:
            self.spinner.loading_stop()
            self.translate.print_message(f"RVC n'a pas fonctionné. Voici l'erreur rencontrée : {e}", progressive_display=True)
            self.translate.print_message("Il est conseillé d'essayer de faire fonctionner le processus manuellement en utilisant la commande suivante dans votre terminal. Si vous avez des difficultés à comprendre comment cela fonctionne, un tutoriel est disponible. Voulez-vous voir le tutoriel? (y/n)", progressive_display=True)

            response = input()
            if response.lower() == 'y':
                tutorial_text = [
                    'python commander.py 0 "C:\\Chemin\\vers\\le\\fichier\\vocal.wav" "C:\\Chemin\\vers\\le\\fichier\\logs\\MODEL_v2.index" harvest "C:\\Chemin\\vers\\le\\fichier\\sortie.wav" "C:\\Chemin\\vers\\le\\modèle\\model.pth" 0.6 cuda:0 True 5 44100 0.5 0.33',
                    "voici l'explication :",
                    '1. `python commander.py`: Cette commande sert à exécuter votre script Python.',
                    '2. `f0up_key` : Une clé pour spécifier la mise à jour de la fréquence fondamentale (F0). (ex : 0)',
                    '3. `input_path` : Le chemin du fichier audio d\'entrée que vous voulez traiter. (ex : "C:\\Chemin\\vers\\le\\fichier\\vocal.wav")',
                    '4. `index_path` : Le chemin du fichier index qui stocke ou récupère des informations supplémentaires pour le traitement. (ex : "C:\\Chemin\\vers\\le\\fichier\\index.log")',
                    '5. `f0method` : La méthode utilisée pour extraire le pitch (F0) du fichier audio. Les options possibles sont "harvest" ou "pm". (ex : "harvest")',
                    '6. `opt_path` : Le chemin où le fichier audio traité sera sauvegardé. (ex : "C:\\Chemin\\vers\\le\\fichier\\sortie.wav")',
                    '7. `model_path` : Le chemin vers le fichier modèle qui sera utilisé pour le traitement. (ex : "C:\\Chemin\\vers\\le\\modèle\\model.pth")',
                    '8. `index_rate` : Le taux d\'index utilisé pendant le traitement. Ce doit être une valeur de type float. (ex : 0.6)',
                    '9. `device` : Le périphérique sur lequel le traitement sera effectué. Les options possibles sont les identifiants des GPU (comme "cuda:0") ou "cpu". (ex : "cuda:0")',
                    '10. `is_half` : Un booléen indiquant si le modèle doit utiliser une précision mixte pendant le traitement. Les options possibles sont True ou False. (ex : True)',
                    '11. `filter_radius` : La taille du rayon du filtre, une valeur de type int. (ex : 5)',
                    '12. `resample_sr` : Le taux d\'échantillonnage pour le rééchantillonnage, une valeur de type int. (ex : 44100)',
                    '13. `rms_mix_rate` : Un taux utilisé pour ajuster le mixage RMS pendant le traitement, une valeur de type float. (ex : 0.5)',
                    '14. `protect` : Une valeur utilisée pour ajuster un paramètre de protection pendant le traitement, une valeur de type float. (ex : 0.33)',
                    "En cas d'incompréhension, veuillez contacter le support ici : https://github.com/SECRET-GUEST/AVM/issues (Faites Ctrl + clic sur le lien pour l'ouvrir, puisque l'affichage est dans le CMD)"
                ]
                self.spinner.loading_stop()
                for line in tutorial_text:
                    self.translate.print_message(line, progressive_display=True)





    def assemble_final(self):
        self.translate.print_message("Rendu final en cours de traitement...", progressive_display=True)
        self.spinner.loading_start()

        # Fusionne "nosound.mp4" et "soundHD.wav"
        nosound_path = os.path.join(self.parts_dir, 'nosound.mp4')
        soundHD_path = os.path.join(self.parts_dir, 'soundHD.wav')
        
        if not os.path.exists(soundHD_path):
            soundHD_path = os.path.join(self.parts_dir, 'sound.wav') # Si soundHD.wav n'existe pas, utilisez sound.wav
        
        video_clip = VideoFileClip(nosound_path)
        audio_clip = AudioFileClip(soundHD_path)
        
        final_video_clip = video_clip.set_audio(audio_clip)

        # Enregistre la vidéo finale avec un nom basé sur le nom du dossier parts_dir
        final_video_name = os.path.basename(os.path.normpath(self.parts_dir)) + '.mp4'
        final_video_path = os.path.join(self.parts_dir, final_video_name)
        final_video_clip.write_videofile(final_video_path, codec="libx264", audio_codec="aac", bitrate="5000k", audio_bitrate="384k", threads=4)
        
        # Déplace tout le dossier parts_dir vers le dossier 0ld
        old_parts_path = os.path.join(self.old_dir, os.path.basename(os.path.normpath(self.parts_dir)))
        shutil.move(self.parts_dir, old_parts_path)
        
        # Recherche la vidéo dans le dossier 0ld et la jouer avec le lecteur vidéo par défaut
        final_old_video_path = os.path.join(old_parts_path, final_video_name)

        self.spinner.loading_stop()
        self.translate.print_message("Lecture du rendu final et fermeture du programme", progressive_display=True)

        os.startfile(final_old_video_path)