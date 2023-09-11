#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|


import os,shutil,time

from src.avm.indexing import Indexer
from src.avm.paths import PathHandler
from src.avm.partFinder import videoParts
from src.avm.videoMaking import videoMaker
from src.avm.toTortoise import SendToSpeech


#_    ____ _  _ ____ ____ _  _ ____ 
#|    |__| |\ | |    |___ |  | |__/ 
#|___ |  | | \| |___ |___ |__| |  \ 

# Regarde si le fichier scene.json existe, fournis des instructions si ce n'est pas le cas, et lance la génération d'audio si ca l'est.
# Par ailleurs le script fait appel à un traducteur pour chaque phrases dans le cmd si l'OS n'est pas en Francais.
class starter(PathHandler):
    def __init__(self):
        super().__init__()

        self.launchParsing()



    def launcher(self):
            
        # Vérifiez si le fichier scene.json existe dans le dossier de travail
        self.scene_file_path = os.path.join(self.working_folder_path, 'scene.json')


        if os.path.exists(self.scene_file_path):
            self.translate.print_message("Fichier scene.json trouvé", progressive_display=True)


            # Créer une instance de Indexer visant à numéroter et traduire les scenes en anglais via google translate
            n_scene_file_path = os.path.join(self.working_folder_path, 'n_scene.json')
            modifier = Indexer(self.scene_file_path, n_scene_file_path)

            self.spinner.loading_start()
            modifier.modify_scene()
            self.spinner.loading_stop()
            
            self.newJson_next_step_request()


            # Créer une instance de videoParts et commencer le processus de création de vidéo
            video_maker = videoParts(self.root_dir, self.working_folder_path)
            video_maker.start_video_creation()


            # Créer une instance de SendToSpeech pour générer les fichiers audio avec les noms des phrases numérotées
            speech_generator = SendToSpeech(self.root_dir, self.working_folder_path)
            speech_generator.generate_audio_files()


            # Créer une instance de videoMaker et lancer la méthode create_final_video
            video_maker_instance = videoMaker(self.root_dir, self.working_folder_path)
            video_maker_instance.check_parts()







        else:
            self.translate.print_message('La scène est manquante, il faut rajouter un fichier scene.json formaté selon un exemple, voulez-vous afficher l\'exemple ? (y/n)', progressive_display=True)
            print()
            self.translate.print_message('Votre réponse :', progressive_display=True)
            self.handle_example_request()





            
    def launchParsing(self):
        # Obtenez une liste de tous les dossiers dans storyboard_dir, à l'exception de '0ld'
        folder_names = [name for name in os.listdir(self.storyboard_dir) if os.path.isdir(os.path.join(self.storyboard_dir, name)) and name != '0ld']

        os.system('cls' if os.name == 'nt' else 'clear')


        # Vérifiez s'il y a plusieurs dossiers
        if len(folder_names) > 1:
            self.translate.print_message("Plusieurs dossiers trouvés. Veuillez choisir le dossier sur lequel vous souhaitez travailler :", progressive_display=True)

            # Affichez une liste numérotée des dossiers
            for i, folder_name in enumerate(folder_names):
                self.translate.print_message(f"{i+1}. {folder_name}")

            while True:
                try:
                    # Demandez à l'utilisateur de choisir un dossier
                    self.translate.print_message("Veuillez entrer le numéro du dossier que vous souhaitez choisir : ", progressive_display=True)
                    choice = int(input())

                    # Vérifiez si le choix est valide
                    if 1 <= choice <= len(folder_names):
                        # Définissez le dossier choisi comme dossier de travail
                        self.working_folder_path = os.path.join(self.storyboard_dir, folder_names[choice-1])
                        break
                    else:
                        self.translate.print_message("Choix non valide. Veuillez entrer un numéro valide.", progressive_display=True)
                except ValueError:
                    self.translate.print_message("Entrée non valide. Veuillez entrer un numéro.", progressive_display=True)

        else:
            # Si aucun dossier n'est trouvé, appelez la nouvelle méthode
            if len(folder_names) == 0:
                self.handle_no_folder_found()
            
            else:
                # S'il n'y a qu'un seul dossier, définissez-le comme dossier de travail
                self.working_folder_path = os.path.join(self.storyboard_dir, folder_names[0])
            
            
        
        self.launcher()







    def handle_no_folder_found(self):
        self.translate.print_message("Aucun dossier trouvé dans le dossier storyboard autre que '0ld'.", progressive_display=True)
        
        # Demandez à l'utilisateur s'il veut créer un dossier d'exemple
        self.translate.print_message("Voulez-vous créer un dossier d'exemple ? (y/n)", progressive_display=True)
        response = input()
        
        if response.lower() == 'y':
            # Copiez le dossier "00000_NEW_PROJECT" dans le dossier "storyboard"
            source_folder = os.path.join(self.root_dir, 'utils','examples', '00000_NEW_PROJECT')
            dest_folder = os.path.join(self.storyboard_dir, '00000_NEW_PROJECT')
            shutil.copytree(source_folder, dest_folder)
            
            # Demandez à l'utilisateur s'il veut afficher le dossier
            self.translate.print_message("Voulez-vous afficher le dossier ? (y/n)", progressive_display=True)
            response = input()
            
            if response.lower() == 'y':
                # Ouvrez le dossier "storyboard"
                os.system(f'start "" "{self.storyboard_dir}"')
                self.launchParsing()
            else:
                # Relancez le programme
                self.launchParsing()
        
        elif response.lower() == 'n':
            # Relancez le programme
            self.restart_program()
        else:
            self.translate.print_message("Réponse non valide. Veuillez réessayer.", progressive_display=True)
            self.handle_no_folder_found()
    


# Que du textes et des conditions si le fichier scene.json n'est pas présent, entre autres

    def handle_example_request(self):
        self.scene_example = os.path.join(self.root_dir, 'examples','00000_NEW_PROJECT','scene.json')
        response = input()
        if response.lower() == 'y':
            os.system('cls' if os.name == 'nt' else 'clear')
            os.system(f'start notepad {self.scene_example}')
            self.next_step()
        elif response.lower() == 'n':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.next_step()
        else:
            self.translate.print_message('Réponse non valide. Veuillez entrer y ou n.', progressive_display=True)
            self.handle_example_request()


    def next_step(self):
        self.translate.print_message('Il vous faut créer un dossier du nom que vous voulez qui contiendra votre scénario, et le mettre dans le dossier storyboard.', progressive_display=True)
        print()
        self.translate.print_message('Que voulez-vous faire ensuite ?', progressive_display=True)
        print()
        self.translate.print_message('1. Ouvrir le dossier storyboard' )
        self.translate.print_message('2. Créer un raccourci vers le dossier storyboard' )
        self.translate.print_message('3. Relancer le programme')
        print()
        self.translate.print_message('Votre réponse :', progressive_display=True)
        self.handle_next_step_request()

    def handle_next_step_request(self):
        response = input()
        if response == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.open_storyboard_dir()
        elif response == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.handle_shortcut_request()
        elif response == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.launchParsing()
        else:
            self.translate.print_message('Réponse non valide. Veuillez entrer 1, 2 ou 3.', progressive_display=True)
            self.handle_next_step_request()




    def newJson_next_step_request(self):
        self.translate.print_message('Un nouveau fichier n_json a été créé, une traduction automatique du nom des scene a été effectuée pour faciliter la recherche d\'une image correspondante, il serait préférable de vérifier le fichier avant de continuer l\'execution automatique de ce script', progressive_display=True)
        print()
        self.translate.print_message('Voulez vous vérifier ce fichier ?', progressive_display=True)
        print()
        self.translate.print_message('1. Oui')
        self.translate.print_message('2. Non')
        print()
        self.translate.print_message('Votre réponse :', progressive_display=True)
        self.newJson_next_step()


    def newJson_next_step(self):
        response = input()
        if response == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.open_json()
        elif response == '2':
            os.system('cls' if os.name == 'nt' else 'clear')

        else:
            self.translate.print_message('Réponse non valide. Veuillez entrer 1 ou 2.', progressive_display=True)
            os.system('pause')
            os.system('cls' if os.name == 'nt' else 'clear')
            self.newJson_next_step_request()

    def open_json(self):
        os.system(f'start "" "{self.storyboard_dir}"')
        os.system('pause')
        os.system('cls' if os.name == 'nt' else 'clear')




    def open_storyboard_dir(self):
        os.system(f'start "" "{self.storyboard_dir}"')
        os.system('pause')
        self.restart_program()



    def handle_shortcut_request(self):
        while True:
            self.translate.print_message("Ou voulez vous créer le raccourcis ?", progressive_display=True)
            print()
            self.translate.print_message("1- Sur le bureau")
            self.translate.print_message("2- A un chemin personnalisé")
            print()
            self.translate.print_message("Votre choix :", progressive_display=True)

            try:
                choice = int(input())
                if choice == 1:
                    self.create_desktop_shortcut()
                    break
                elif choice == 2:
                    self.create_perso_shortcut()
                    break
                else:
                    self.translate.print_message("Choix invalide. Veuillez choisir 1 pour créer un raccourci sur le bureau ou 2 pour choisir le chemin.", progressive_display=True)
            except ValueError:
                self.translate.print_message("Entrée non valide. Veuillez entrer un numéro.", progressive_display=True)



    def create_perso_shortcut(self):
        # Demandez à l'utilisateur d'entrer le chemin où il souhaite créer le raccourci
        self.translate.print_message('Veuillez entrer le chemin où vous voulez créer le raccourci (par exemple C:\\Users\\VotreNom\\Documents ) : ', progressive_display=True)
        shortcut_path = input()

        # Vérifiez si le chemin entré par l'utilisateur est valide
        if os.path.exists(shortcut_path):
            # Créez le raccourci
            os.system(f'mklink /D "{os.path.join(shortcut_path, "Storyboard Shortcut")}" "{self.storyboard_dir}"')
            self.restart_program()
        else:
            self.translate.print_message('Chemin non valide. Veuillez réessayer.', progressive_display=True)
            self.create_perso_shortcut()


    def create_desktop_shortcut(self):
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        script_directory = os.path.dirname(os.path.abspath(__file__))
        storyboard_path = self.storyboard_dir
        vbs_script_path = os.path.join(script_directory, "create_shortcut.vbs") 

        # Générer le contenu du script VBS
        vbs_script = f'''
        Set oWS = WScript.CreateObject("WScript.Shell")
        sLinkFile = "{desktop_path}\\Storyboard Shortcut.lnk"
        Set oLink = oWS.CreateShortcut(sLinkFile)
        oLink.TargetPath = "{storyboard_path}"
        oLink.WindowStyle = 1
        oLink.IconLocation = "{storyboard_path}, 0"
        oLink.Description = "Shortcut to Storyboard"
        oLink.WorkingDirectory = "{script_directory}"
        oLink.Save
        ''' 

        # Écrire le script VBS dans un fichier
        with open(vbs_script_path, 'w') as vbs_file:
            vbs_file.write(vbs_script)  

        # Exécuter le script VBS pour créer le raccourci
        os.system(f"cscript {vbs_script_path}") 

        # Supprimer le script VBS
        os.remove(vbs_script_path)  

        self.translate.print_message("Le raccourci a été créé sur le bureau.", progressive_display=True)
        time.sleep(0.5)
        self.restart_program()  


    def restart_program(self):
        self.translate.print_message('Voulez-vous relancer le programme ? (y/n)', progressive_display=True)
        response = input()
        if response.lower() == 'y':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.launchParsing()
        elif response.lower() == 'n':
            os.system('exit')
        else:
            self.translate.print_message('Réponse non valide. Veuillez entrer y ou n.', progressive_display=True)
            self.restart_program()







#____ ____ ____ _  _ ____ ___    _    ____ _  _ _  _ ____ _  _
#|__/ |  | |    |_/  |___  |     |    |__| |  | |\ | |    |__|
#|  \ |__| |___ | \_ |___  |     |___ |  | |__| | \| |___ |  |
                
#ENDING | https://www.youtube.com/watch?v=CgZVrvQZB6U&ab_channel=SECRETGUEST :3


if __name__ == "__main__":
    starting = starter()

