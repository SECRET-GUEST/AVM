#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|



import os
from ..trans.translater import translate
from src.animations.loadingSpinner import Spinner   

#____ ____ ____ ___ _ ____ _  _ _  _ ____ _ ____ ____    ___  ____ ____    ____ _  _ ____ _  _ _ _  _ ____ 
#| __ |___ [__   |  | |  | |\ | |\ | |__| | |__/ |___    |  \ |___ [__     |    |__| |___ |\/| | |\ | [__  
#|__] |___ ___]  |  | |__| | \| | \| |  | | |  \ |___    |__/ |___ ___]    |___ |  | |___ |  | | | \| ___] 
                                                                                                          

# Evite la récursivité 
class PathHandler:
    def __init__(self, root_dir=None, working_folder_path=None):
        self.root_dir = root_dir if root_dir else os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        self.working_folder_path = working_folder_path if working_folder_path else ""
        self.storyboard_dir = os.path.join(self.root_dir, 'storyboard')
        self.old_dir = os.path.join(self.storyboard_dir, '0ld')
        
        self.n_scene_file_path = os.path.join(self.working_folder_path, 'n_scene.json')
        self.image_database_csv = os.path.join(self.root_dir, 'assets', 'img', 'img.csv')

        self.tortoise_dir = os.path.join(self.root_dir, 'tortoise-tts')
        self.rvc_path = os.path.join(self.root_dir, 'RVC')

        self.parts_dir = os.path.join(self.working_folder_path, 'parts')
        self.expressions = os.path.join(self.root_dir, 'assets', 'Character','expression')
        self.basics_dir = os.path.join(self.root_dir, 'assets', 'basics')

        self.spinner = Spinner()
        self.translate = translate()



