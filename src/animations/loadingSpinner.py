#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|


import sys
import time
import threading


# ____ _ _  _ ___  _    ____    ____ ___  _ _  _ _  _ ____ ____ 
# [__  | |\/| |__] |    |___    [__  |__] | |\ | |\ | |___ |__/ 
# ___] | |  | |    |___ |___    ___] |    | | \| | \| |___ |  \ 
                                                              

class Spinner:
    def __init__(self):
        self.loading = False
        self.loading_thread = None

    def loading_spinner(self):
        symbols = ['/', '-', '\\', '|']
        i = 0
        while self.loading:
            sys.stdout.write('\r' + symbols[i % len(symbols)])
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write('\r')
        sys.stdout.write('\r')
        sys.stdout.flush()

    def loading_start(self):
        self.loading = True 
        self.loading_thread = threading.Thread(target=self.loading_spinner) 
        self.loading_thread.start()

    def loading_stop(self):
        self.loading = False
        self.loading_thread.join()
