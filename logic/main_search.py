from logic.st_util import Util
import urllib.request
from Utils.u_service.service import Service
import json
from urllib.parse import quote
from collections import Counter


json_data = Util.json_chats_load()

listado_chats = {}
consolidado_terminos = {}
cont_chats = 0

for jchat in json_data:
    cont_chats = cont_chats + 1
    id_chat = jchat['id_conversation']
    textos_chat = ""

    for jtext in jchat['messages_all']:

        textos_chat = textos_chat + jtext['text'] + " "

    if textos_chat == "":
        listado_chats[id_chat] = ""
    else:
        service = Service()

        text_type = 'Standard'
        text = quote(textos_chat)
        parameters = quote(json.dumps({'text_type': text_type}))
        encodedText = quote(text.encode("utf-8"))
        url = service.get_web_service_url('TextAnalysis', 'syntax_task',
                                          dict(task='term_extraction',
                                               text=text,
                                               parameters=parameters,
                                               lang='es'))
        conn = urllib.request.urlopen(url)
        content = conn.read()
        resp = json.loads(content.decode())

        for key in resp:
            terms = resp[key]
            tally_variable = Counter(terms).most_common()
            sorted_tally = sorted(tally_variable, key=lambda tup: tup[0])
            # print(sorted_tally)
            listado_chats[id_chat] = sorted_tally
            for words in sorted_tally:
                if words[0] in consolidado_terminos:#.has_key(words[0]):
                    consolidado_terminos[words[0]] = consolidado_terminos[words[0]] + words[1]
                else:
                    consolidado_terminos[words[0]] = words[1]
        conn.close()


Util.export_cvs("total_terminos",consolidado_terminos)
Util.export_cvs("terminos_x_chat",listado_chats)