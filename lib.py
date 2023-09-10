#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|


import os,sys,subprocess,time
from subprocess import Popen, DEVNULL
import zipfile,shutil

from src.animations.loadingSpinner import Spinner



# ___  ____ _ _ _ ____ ____    ___  _    ____ _  _ ___ ____ 
# |__] |  | | | | |___ |__/    |__] |    |__| |\ |  |  [__  
# |    |__| |_|_| |___ |  \    |    |___ |  | | \|  |  ___] 

class installer:
    def __init__(self):

        self.spinner = Spinner()

        # Verifies we are in a conda environment
        self.check_env()
        os.system("conda update -n base -c defaults conda")
        os.system("pip install --upgrade pip")

        # Install googletrans package
        print("Installing google translate package...")

        # Launch the installation command and display a loading message simultaneously
        self.process = Popen(["pip", "install", "googletrans==4.0.0-rc1"], stdout=DEVNULL, stderr=DEVNULL)

        while self.process.poll() is None:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.5)
        
        # Import the translater module here, after installing googletrans
        from src.trans.translater import translate
        self.translate = translate()

        self.translate.print_message("Installation complété")
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')

        self.script_dir = os.getcwd()

        self.install_dependencies()
        os.chdir(self.script_dir)
        os.system('cls' if os.name == 'nt' else 'clear')

        # Liste les libraries installées avec conda et pip pour pouvoir comparer
        #self.run_cmd("conda list > conda_packages.txt") 
        #self.run_cmd("pip list > pip_packages.txt")

        # Compare les librairies et supprime les packages, cette fonction est a revoir
        #self.check_duplicate_packages()

        self.choice_shortcut()




# Avant toute chose on vérifie si on est bien dans un environnement virtuel
# le translater n'étant pas encore importé on laisse a en anglais
    def check_env(self):
        conda_exists = shutil.which("conda")
        if not conda_exists:
            print("FATAL ERROR : Conda is not installed. Exiting...")
            sys.exit()# Force le NOUVEL environnement virtuel

        else:
            # Vérifier si le script est exécuté dans un environnement Conda
            if "CONDA_DEFAULT_ENV" not in os.environ:
                print("FATAL ERROR : Script not running in conda. Exiting...")
                sys.exit()

        if os.environ["CONDA_DEFAULT_ENV"] == "base":
            print("FATAL ERROR :Create an environment for this project and activate it. Exiting...")
            sys.exit()



    # Gestion des erreurs
    def log_error(self, cmd, return_code, stdout, stderr):
        with open("INSTALLATION_ERRORS.txt", "a") as log_file:
            log_file.write(f"Command: {cmd}\n")
            log_file.write(f"Return Code: {return_code}\n")
            if stdout:
                log_file.write(f"Output: {stdout}\n")
            if stderr:
                log_file.write(f"Error: {stderr}\n")
            log_file.write("\n")





# Fonction pour supprimer les packages en double mais provoque également des erreurs : 

#    def check_duplicate_packages(self):
#        with open("conda_packages.txt") as f:
#            conda_packages = {line.split()[0] for line in f if line.strip()}    
#
#        with open("pip_packages.txt") as f:
#            pip_packages = {line.split()[0] for line in f if line.strip()}  
#
#        duplicate_packages = conda_packages.intersection(pip_packages)  
#
#        if duplicate_packages:
#            self.translate.print_message(f"Attention : Les packages suivants sont installés à la fois par conda et pip : {', '.join(duplicate_packages)}", progressive_display=True)
#            self.remove_duplicate_packages(duplicate_packages)
#        else:
#            self.translate.print_message("Aucun package en double trouvé.", progressive_display=True)
#
#        # Nettoyer les fichiers
#        os.remove("conda_packages.txt")
#        os.remove("pip_packages.txt")
#
#    def remove_duplicate_packages(self, duplicate_packages):
#        for package in duplicate_packages:
#            self.run_cmd(f"pip uninstall -y {package}")
#        self.translate.print_message("Les packages en double ont été supprimés.", progressive_display=True) 






# ____ _  _ ___     ____ _  _ _  _ _  _ ____ ____ ____ 
# |    |\/| |  \    |__/ |  | |\ | |\ | |___ |__/ [__  
# |___ |  | |__/    |  \ |__| | \| | \| |___ |  \ ___] 




# Ecriture dans le terminal avec retour des erreurs
    def run_cmd(self, cmd, env=None):
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())

            stdout, stderr = process.communicate()
            self.log_error(cmd, process.returncode, stdout, stderr)

            if stderr:
                print(stderr.strip(), file=sys.stderr)

        except Exception as e:
            print(f"Error : {e}")
            self.log_error(cmd, -1, None, str(e))   

        return process  




# Meme fonction que précédente mais permet de lancer un spinner de chargement pendant l'installation
# Remplacant tout le texte de l'installation

#    def runLoader(self, cmd):
#        self.spinner.loading_start()    
#
#        try:
#            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#            stdout, stderr = process.communicate()
#            self.log_error(cmd, process.returncode, stdout, stderr)
#
#        except Exception as e:
#            self.spinner.loading_stop()
#            print(f"Error : {e}")
#            self.log_error(cmd, -1, None, str(e))   
#
#        self.spinner.loading_stop()







# ____ ____ ____ _  _ _ ____ ____ _  _ ____ _  _ ___ ____ 
# |__/ |___ |  | |  | | |__/ |___ |\/| |___ |\ |  |  [__  
# |  \ |___ |_\| |__| | |  \ |___ |  | |___ | \|  |  ___] 
                                                        



# Installation GPU ou CPU
    def install_dependencies(self):
        while True:
            self.translate.print_message("Choisissez le type d'installation :", progressive_display=True)
            print()
            print("1- NVIDIA")
            print("2- CPU")
            print()
            self.translate.print_message("Utiliser le CPU peut s'avérer très lent, mais fonctionne lorsque la VRAM du GPU est inférieure à 4 Go.", progressive_display=True)
            print()
            self.translate.print_message("Par ailleurs, vous aurez besoin d'environ 50 Go d'espace libre pour installer l'application, quelle que soit l'option choisie. Assurez-vous de disposer de suffisamment d'espace pour éviter les erreurs.", progressive_display=True)
            print()
            self.translate.print_message("Votre choix :", progressive_display=True)
            try:
                choice = int(input())

                if choice in [1, 2]:
                    if choice == 1:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        self.translate.print_message("Installation des dépendances pour NVIDIA...", progressive_display=True)
                        self.run_cmd("conda install -y -k pytorch[version=2,build=py3.10_cuda11.7*] torchvision torchaudio pytorch-cuda=11.7 cuda-toolkit ninja git -c pytorch -c nvidia/label/cuda-11.7.0 -c nvidia")
                    
                    elif choice == 2:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        self.translate.print_message("Installation des dépendances pour CPU...", progressive_display=True)
                        self.run_cmd("conda install -y -k pytorch torchvision torchaudio cpuonly git -c pytorch")

                    requirementsTxt = os.path.join(self.script_dir, "requirements.txt")
                    self.translate.print_message("Installation d'autre dépendances...", progressive_display=True)


                    # Lire les lignes du fichier
                    with open(requirementsTxt, 'r') as file:
                        requirements_data = file.readlines()

                    # Installer chaque dépendance une par une
                    for requirement in requirements_data:
                        self.run_cmd(f"pip install {requirement.strip()}")


                    self.clone_repo()
                    break
                else:
                    self.translate.print_message("Choix invalide. Veuillez choisir 1 pour NVIDIA ou 2 pour CPU.")

            except ValueError:
                self.translate.print_message("Entrée invalide. Veuillez entrer un numéro valide.", progressive_display=True)















# _  _ ____ ____ ____    ___  _  _ _  _ ____ _  _ _ _  _    _  _ ____     _ _  _ ___ ____ _  _  
# |_/  |__| | __ |___    |__] |  | |\ | [__  |__| | |\ |    |\ | |  |     | |  |  |  [__  |  |  
# | \_ |  | |__] |___    |__] |__| | \| ___] |  | | | \|    | \| |__|    _| |__|  |  ___] |__|  


# Clonage de Tortoise, RVC et base de donnée de 9 milliard d'images google

    def clone_repo(self):
        self.cloneTortoise()
        self.cloneGoogleDB()
        self.cloneRvc()




    def cloneTortoise(self):
    # Définition des dossiers
        tortoise_folder = os.path.join(self.script_dir, "tortoise-tts")  

    # Téléchargement de tortoise
        self.translate.print_message("Téléchargement de tortoise...", progressive_display=True)
        self.spinner.loading_start()
        
        if not os.path.exists(tortoise_folder):
            os.makedirs(tortoise_folder)
            self.run_cmd(f"git clone --branch tortoise-env https://github.com/SECRET-GUEST/tortoise-tts {tortoise_folder}")
            
            # Installation du package principal à partir de tortoise-tts (inutile vu qu'on fait tout via le requierements.txt)
            #os.chdir(tortoise_folder)
            #os.system("python setup.py install")
            
            # Installation du sous-package à partir de tortoise-tts/tortoise
            # os.chdir(os.path.join(tortoise_folder, "tortoise"))
            # os.system("pip install -e .")

        else:
            self.spinner.loading_stop()
            self.translate.print_message("Le dossier tortoise-tts existe déjà, téléchargement non nécessaire.", progressive_display=True)
        




        

    # Téléchargement et extraction du fichier img.csv
    def cloneGoogleDB(self):
        # On import requests ici vu qu'il est dans requierments.txt,
        # Ca permet de savoir si les dépendances ont bien été installées
        import requests 

        self.spinner.loading_stop()
        self.translate.print_message("Téléchargement de la base de donnée d'images GOOGLE (img.csv)...", progressive_display=True)
        self.spinner.loading_start()


        img_folder = os.path.join(self.script_dir, "assets", "img")
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)




        
        img_file_path = os.path.join(img_folder, 'img.csv')

        if not os.path.exists(img_file_path):

            img_url = "https://storage.googleapis.com/openimages/2018_04/image_ids_and_rotation.csv"
            img_response = requests.get(img_url)

            with open(img_file_path, 'wb') as img_file:
                img_file.write(img_response.content)

            self.spinner.loading_stop()
            self.translate.print_message("la base de donnée d'images GOOGLE (img.csv) a été téléchargé avec succès.", progressive_display=True)
        else:
            self.spinner.loading_stop()
            self.translate.print_message("la base de donnée d'images GOOGLE (img.csv) existe déjà, téléchargement non nécessaire.", progressive_display=True)
        






    # Téléchargement de RVC
    def cloneRvc(self):
        import requests 

        self.rvc_archive_path = 'RVC.zip'
        self.rvc_directory_path = 'RVC'

        if not os.path.exists(self.rvc_directory_path):
            if not os.path.exists(self.rvc_archive_path):
                self.spinner.loading_stop()
                self.translate.print_message("Téléchargement de RVC...", progressive_display=True)
                self.spinner.loading_start()

                try:
                    url = "https://huggingface.co/secretguest/NVIDIA_RVC/resolve/main/ARCHIVES_FULL/RVC.zip"
                    response = requests.get(url)

                    if response.status_code == 200:
                        with open(self.rvc_archive_path, 'wb') as file:
                            file.write(response.content)
                    else:
                        self.spinner.loading_stop()
                        raise Exception(f"Échec du téléchargement de RVC : {response.status_code}")

                except Exception as e:
                    self.spinner.loading_stop()
                    self.error_message = f"Erreur : {e} Une erreur est survenue durant le téléchargement"
                    self.translate.print_message(self.error_message, progressive_display=True)
                    self.log_error("Download RVC issue", -1, None, self.error_message)
                    return None
            else:
                self.spinner.loading_stop()
                self.translate.print_message("Détection d'un fichier RVC.zip, début de l'extraction...", progressive_display=True)
        else:
            self.spinner.loading_stop()
            self.translate.print_message("Le dossier RVC existe déjà, téléchargement non nécessaire.", progressive_display=True)

        # Extraction de RVC
        self.spinner.loading_stop()
        self.translate.print_message("Extraction de l'archive RVC...", progressive_display=True)
        self.spinner.loading_start()        

        try:
            # Créer le dossier RVC s'il n'existe pas
            if not os.path.exists(self.rvc_directory_path):
                os.makedirs(self.rvc_directory_path)
            
            with zipfile.ZipFile(self.rvc_archive_path, 'r') as zip_ref:
                zip_ref.extractall(self.rvc_directory_path)
        
                # Vérification de l'extraction réussie
                extracted_files = os.listdir(self.rvc_directory_path)
                zip_files = zip_ref.namelist()
                
                if all(file in extracted_files for file in zip_files):
                    self.spinner.loading_stop()
                    self.translate.print_message("L'archive RVC a bien été extraite.", progressive_display=True)
                    
                    # Suppression du fichier zip après une extraction réussie
                    os.remove(self.rvc_archive_path)
                else:
                    raise Exception("L'extraction des fichiers a échoué.")
        
        except Exception as e:
            self.spinner.loading_stop()
            self.error_message = f"Erreur : {e} L'extraction du fichier a été interrompue"
            self.translate.print_message(self.error_message, progressive_display=True)
            self.log_error("Extraction Command", -1, None, self.error_message)
            return None
        





# _    ____ _  _ _  _ ____ _  _ ____ ____ 
# |    |__| |  | |\ | |    |__| |___ |__/ 
# |___ |  | |__| | \| |___ |  | |___ |  \ 


# Génerer le raccourcis sur le bureau 
    def choice_shortcut(self):
        while True:
            self.translate.print_message("Voulez-vous créer un raccourci vers le programme sur le bureau ?", progressive_display=True)
            print()
            self.translate.print_message("1- Oui")
            self.translate.print_message("2- Non, lance directement le programme")
            print()
            self.translate.print_message("Votre choix :", progressive_display=True)

            try:
                choice = int(input())
                if choice == 1:
                    self.create_shortcut()
                    break
                elif choice == 2:
                    self.launch_avm()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    self.translate.print_message("Choix invalide. Veuillez choisir 1 pour créer un raccourci ou 2 pour lancer directement le programme.", progressive_display=True)
            except ValueError:
                self.translate.print_message("Entrée invalide. Veuillez entrer un numéro valide.", progressive_display=True)


    def create_shortcut(self):
        print()
        self.translate.print_message(f"Création du raccourcis")
        print()
        

        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        script_directory = os.path.dirname(os.path.abspath(__file__))
        batch_file_path = os.path.join(script_directory, "shortcut.bat")
        icon_file_path = os.path.join(script_directory, "assets", "logo", "avm.ico")
        vbs_script_path = os.path.join(script_directory, "create_shortcut.vbs")

        # Générez le contenu du script VBS
        vbs_script = f'''
        Set oWS = WScript.CreateObject("WScript.Shell")
        sLinkFile = "{desktop_path}\\AVM.lnk"
        Set oLink = oWS.CreateShortcut(sLinkFile)
        oLink.TargetPath = "{batch_file_path}"
        oLink.WindowStyle = 1
        oLink.IconLocation = "{icon_file_path}"
        oLink.Description = "Shortcut to shortcut.bat"
        oLink.WorkingDirectory = "{script_directory}"
        oLink.Save
        '''

        # Écrivez le script VBS dans un fichier
        with open(vbs_script_path, 'w') as vbs_file:
            vbs_file.write(vbs_script)

        # Exécutez le script VBS pour créer le raccourci
        os.system(f"cscript {vbs_script_path}")

        # Supprimez le script VBS
        os.remove(vbs_script_path)

        self.translate.print_message(f"Le raccourci a été créé sur le bureau", progressive_display=True)
        print()
        self.translate.print_message(f"Initialisation...", progressive_display=True)
        self.launch_avm()





# Script de lancement
    def launch_avm(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        batch_file_path = os.path.join(script_directory, "shortcut.bat")

        # Vérifiez que le chemin est valide avant de l'utiliser
        if not os.path.exists(batch_file_path):
            print(f"Le chemin d'accès {batch_file_path} n'existe pas.")
            return  

        # Exécutez le fichier batch
        try:
            os.system(f'"{batch_file_path}"')

        except Exception as e:
            self.spinner.loading_stop()
            self.error_message = f"Erreur : {e} L'execution du script a été interrompue"
            self.translate.print_message(self.error_message, progressive_display=True)
            self.log_error("Execution de AVM", -1, None, self.error_message)
            return None



# ____ ____ ____ _  _ ____ ___    _    ____ _  _ _  _ ____ _  _
# |__/ |  | |    |_/  |___  |     |    |__| |  | |\ | |    |__|
# |  \ |__| |___ | \_ |___  |     |___ |  | |__| | \| |___ |  |


if __name__ == "__main__":
    installer_instance = installer()
