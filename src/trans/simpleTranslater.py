#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|


import locale
from googletrans import Translator


#____ _ _  _ ___  _    ____    ___ ____ ____ _  _ ____ _    ____ ___ ____ ____ 
#[__  | |\/| |__] |    |___     |  |__/ |__| |\ | [__  |    |__|  |  |___ |__/ 
#___] | |  | |    |___ |___     |  |  \ |  | | \| ___] |___ |  |  |  |___ |  \ 
                                                                              

class translate:
    def __init__(self):
        self.translator = Translator()
        self.lang = locale.getdefaultlocale()[0]


    def print_message(self, msg):
        if self.translator:
            translated_msg = self.translator.translate(msg, dest=self.lang).text
        else:
            translated_msg = msg
        print(translated_msg)

    def translate_to_english(self, msg):
        if self.translator:
            return self.translator.translate(msg, dest='en').text
        else:
            return msg
