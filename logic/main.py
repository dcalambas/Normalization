import hunspell
from logic.st_util import Util
import datetime
import jellyfish

inicial = datetime.datetime.now()

spell_checker = hunspell.HunSpell('/usr/share/hunspell/es_ES.dic','/usr/share/hunspell/es_ES.aff')

spell_checker.add('bancolombia')

json_data = Util.json_chats_load()

rae = Util.import_csv("CREA")

listado_chats = {}
chat = {}
total_good = 0
total_bad = 0

grand_total_chats = 0
grand_total_good_RAE = 0
grand_total_good_hunspell = 0
grand_total_bad = 0

bad_rec = {}
recom = {}
cont_chats = 0

soundex_recom = {}

for jchat in json_data:
    cont_chats = cont_chats + 1
    id_chat = jchat['id_conversation']
    textos_chat = ""
    chat = {}

    errors = []

    total_good_sc = 0
    total_good_rae = 0
    total_bad = 0
    chat['id'] = id_chat
    for jtext in jchat['messages_all']:
        jtext['text'] = jtext['text'].replace(',', '')
        jtext['text'] = jtext['text'].replace('?', '')
        jtext['text'] = jtext['text'].replace('¿', '')
        jtext['text'] = jtext['text'].replace(':', '')
        jtext['text'] = jtext['text'].replace(';', '')
        jtext['text'] = jtext['text'].replace('!', '')
        jtext['text'] = jtext['text'].replace('¡', '')
        jtext['text'] = jtext['text'].replace('(', '')
        jtext['text'] = jtext['text'].replace(')', '')
        jtext['text'] = jtext['text'].replace('/', '')
        jtext['text'] = jtext['text'].replace('\\', '')
        jtext['text'] = jtext['text'].replace('.', '')
        jtext['text'] = jtext['text'].replace('\'', '')
        jtext['text'] = jtext['text'].replace('\"', '')
        jtext['text'] = jtext['text'].replace('|', '')
        for text in jtext['text'].split(' '):
            if not text.startswith('ACT') and not text.startswith('AGT') and not text.startswith('NUM') and not text.startswith('PHO'):
                # if text in rae:
                #     total_good_rae = total_good_rae + 1
                #elif spell_checker.spell(text):
                if spell_checker.spell(text):
                    total_good_sc = total_good_sc + 1
                else:
                    total_bad = total_bad + 1
                    errors.append(text)
                    bad_rec[id_chat+"_"+text]=spell_checker.suggest(text)

                    #|||||||||||||||||||||||||||||SOUNDEX
                    soundex_values = []
                    find_ss = False

                    soundex_text = jellyfish.soundex(text)
                    for s in bad_rec[id_chat+"_"+text]:
                        val_soundex = jellyfish.soundex(s)
                        if(val_soundex == soundex_text):
                            soundex_suggest = s
                            find_ss = True
                            break
                        else:
                            soundex_values.append(jellyfish.soundex(s))
                    if not find_ss:
                        min_diff = 999999
                        count = 0
                        for sv in soundex_values:
                            if jellyfish.jaro_distance(sv,soundex_text)<min_diff:
                            #if jellyfish.levenshtein_distance(sv,soundex_text)<min_diff:
                                min_diff = jellyfish.jaro_distance(sv,soundex_text)
                                soundex_suggest = bad_rec[id_chat+"_"+text][count]
                            count = count + 1
                    soundex_recom[id_chat + "_" + text] = soundex_suggest

    #chat['total_good_RAE'] = total_good_rae
    chat['total_good_hunspell'] = total_good_sc
    chat['total_bad'] = total_bad
    chat['errors'] = errors

    listado_chats[id_chat] = chat

    grand_total_chats = grand_total_chats + 1
    #grand_total_good_RAE = grand_total_good_RAE + total_good_rae
    grand_total_good_hunspell = grand_total_good_hunspell + total_good_sc
    grand_total_bad = grand_total_bad + total_bad

Util.export_cvs("SpellCheck_x_Chat",listado_chats)
#Util.export_cvs("SpellCheck_Total",{'Total de chats':grand_total_chats,'Palabras encontradas por Diccionario RAE':grand_total_good_RAE,'Palabras encontradas por hunspell':grand_total_good_hunspell,'Palabras no encontradas':grand_total_bad})
Util.export_cvs("SpellCheck_Total",{'Total de chats':grand_total_chats,'Palabras encontradas por hunspell':grand_total_good_hunspell,'Palabras no encontradas':grand_total_bad})
Util.export_cvs("SpellCheck_Recommendation",bad_rec)
Util.export_cvs("SpellCheck_Soundex_Recommendation",soundex_recom)

final = datetime.datetime.now()

print('Tiempo total'+str(final - inicial))