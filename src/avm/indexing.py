#_ _  _ ____ ___ ____ _    _    ____ ___ _ ____ _  _
#| |\ | [__   |  |__| |    |    |__|  |  | |  | |\ |
#| | \| ___]  |  |  | |___ |___ |  |  |  | |__| | \|



import json
from src.avm.paths import PathHandler


#_  _ _  _ _  _ ____ ____ ____ ___ ____ ___ _ ____ _  _ 
#|\ | |  | |\/| |___ |__/ |  |  |  |__|  |  | |  | |\ | 
#| \| |__| |  | |___ |  \ |__|  |  |  |  |  | |__| | \| 
                                                       

# numérote les phrases et les scenes du json et les traduit en anglais
class Indexer(PathHandler):
    def __init__(self, input_file, output_file):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file

    def modify_scene(self):
        with open(self.input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        phrase_count = 1
        section_count = 1
        scene_count = 1
        expression_count = 1

        for item in data:
            if "Phrase" in item:
                phrase_value = item.pop("Phrase")
                item[f"Phrase{phrase_count}"] = self.translate.translate_to_english(phrase_value)
                phrase_count += 1

            if "SectionTitle" in item:
                section_title_value = item.pop("SectionTitle")
                item[f"SectionTitle{section_count}"] = self.translate.translate_to_english(section_title_value)
                section_count += 1

            if "Scene" in item:
                scene_value = item.pop("Scene")
                item[f"Scene{scene_count}"] = self.translate.translate_to_english(scene_value)
                scene_count += 1

            if "CharacterExpression" in item:
                expression_value = item.pop("CharacterExpression")
                item[f"CharacterExpression{expression_count}"] = self.translate.translate_to_english(expression_value)
                expression_count += 1

        with open(self.output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


