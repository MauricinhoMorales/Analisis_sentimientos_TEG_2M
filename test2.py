from googletrans import Translator
from deep_translator import GoogleTranslator
translator = Translator()
text = 'hola mundo'
# print(translator.translate(text).text)
translated = GoogleTranslator(source='auto', target='english').translate('hola mundo')
print(translated)