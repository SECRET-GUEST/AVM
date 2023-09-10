#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|


# Installer google translate via cette methode, les versions plus récentes ne sont pas stables :
# pip install googletrans==4.0.0-rc1

import locale, re,time
from googletrans import Translator
from typing import Dict, List

# ___ ____ ____ _  _ ____ _    ____ ___ ____ ____ 
#  |  |__/ |__| |\ | [__  |    |__|  |  |___ |__/ 
#  |  |  \ |  | | \| ___] |___ |  |  |  |___ |  \ 

class translate:
    def __init__(self):
        self.translator = Translator()
        self.lang = locale.getdefaultlocale()[0]


    def colorize_words(self, message, word_color_dict):
        words = message.split()
        new_words = []
        default_color = "\033[92m"  # Couleur verte par défaut

        for word in words:
            clean_word = re.sub(r'\W+', '', word)  # Enlever la ponctuation et convertir en minuscules
            if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', word):
                new_words.append(f"\033[93m{word}{default_color}")  # Coloriser les URLs en jaune puis revenir à la couleur verte
            elif re.match(r'[a-zA-Z]:\\[^\0*:?<>|]+', word):
                new_words.append(f"\033[93m{word}{default_color}")  
            elif clean_word.lower() in word_color_dict:
                new_words.append(word.replace(clean_word, f"\033[{word_color_dict[clean_word]}m{clean_word}{default_color}"))  
            else:
                new_words.append(word)
        return ' '.join(new_words)


# Traduit UNIQUEMENT les mots de groupes de mots
    def translate_words(self, word_groups: Dict[str, List[str]]) -> Dict[str, str]:
        translated_words = {}
        for color, words in word_groups.items():
            for word in words:
                translated_word = self.translate_word(word)
                translated_words[translated_word.lower()] = color
        return translated_words 

# Traduit pour coloriser les mots dans l'invite de commande
    def translate_word(self, word: str) -> str:
        try:
            if self.translator:
                return self.translator.translate(word, dest=self.lang).text
            else:
                return word
        except Exception as e:
            print(f"Error : {e}")
            return word 




    def print_message(self, msg, progressive_display=False):
        if self.lang == 'fr_FR':
            self.translator = None

        if self.translator:
            translated_msg = self.translator.translate(msg, dest=self.lang).text
        else:
            translated_msg = msg

        # Coloration du message entier en vert par défaut
        translated_msg = f"\033[92m{translated_msg}\033[0m"

        word_groups = {
            "red_words": ["non valide","aucun", "aucune","interrompue","error","erreur","erreurs","je n'arrive pas", "Impossible","relancer","Échec"],
            "green_words": [""],
            "yellow_words": ["attention","telechargement", "avertissement","téléchargement","recherche","chargement","créé","généré","générer","installation complété"],
            "white_words": ["information", "note", "initialisation","succès", "réussi"]
        }


        color_dict = {
            "red_words": "91",
            "green_words": "92",
            "yellow_words": "93",
            "white_words": "97"
        }

        word_color_dict = {}

        for group, words in word_groups.items():
            translated_words = self.translate_words({group: words})
            for word in translated_words:
                word_color_dict[word] = color_dict[group]

        colored_msg = self.colorize_words(translated_msg, word_color_dict)

        if progressive_display:
            for char in colored_msg:
                print(char, end='', flush=True)
                time.sleep(0.0001)
            print()
        else:
            print(colored_msg)



    def translate_to_english(self, msg):
        if self.translator:
            return self.translator.translate(msg, dest='en').text
        else:
            return msg


