#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|


# Traduction alternative avec gettext, mais necessite de créer des listes de messages traduits avec des id 

import gettext
import locale
import os


#_  _ ____ _  _ _  _ ____ _       ___ ____ ____ _  _ ____ _    ____ ___ ____ ____ 
#|\/| |__| |\ | |  | |__| |        |  |__/ |__| |\ | [__  |    |__|  |  |___ |__/ 
#|  | |  | | \| |__| |  | |___     |  |  \ |  | | \| ___] |___ |  |  |  |___ |  \ 
                                                                                 

class translate:
    def __init__(self, localedir='locale'):
        # Obtenez la langue du système
        self.lang = locale.getdefaultlocale()[0]

        if self.lang != 'fr_FR':
            self.translator = gettext.translation('messages', localedir=localedir, languages=[self.lang], fallback=True)
        else:
            self.translator = None

    def print_message(self, msg):
        if self.translator:
            translated_msg = self.translator.gettext(msg)
        else:
            translated_msg = msg
        os.system(f'echo {translated_msg}')

    def translate_to_english(self, msg):
        english_translator = gettext.translation('messages', localedir='locale', languages=['en_US'], fallback=True)
        return english_translator.gettext(msg)