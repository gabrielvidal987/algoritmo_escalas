
'''
formato de dados

dados = {
    "separar_genero" : True,
    "table" : "default",
    "days_event" : [
        {
            'month_day' : 1,
            'weekday' : 6,
            'people_need' : 2,    
        },
        {
            'month_day' : 23,
            'weekday' : 5,
            'people_need' : 2,
        }
    ],
    ### para musica:
    "list_dict_person" : [
        {
            'name' : 'jose',
            'vocalist' : True,
            'type_vocal' : 'Tenor',
            'music_message' : True,
            'except_day' : [],
            'preference_day' : [5],
            'gender' : 'f',
        },
        {
            'name' : 'maria',
            'vocalist' : True,
            'type_vocal' : 'Tenor',
            'music_message' : True,
            'except_day' : [],
            'preference_day' : [5],
            'gender' : 'f',
        },
    ],
    ### para tabela normal:
    "list_dict_person" : [
        {
            'name' : 'jose',
            'gender' : 'f',
        },
        {
            'name' : 'maria',
            'gender' : 'f',
        },
    ],
    "funcoes" : {
        "instrumentistas" : [
            {
                'name' : 'Gabriel Vidal',
                'instrumentalist' : True,
                'type_instrumental' : 'Violão',
                'vocalist' : True,
                'type_vocal' : 'Tenor',
                'music_message' : True,
                'except_day' : [],
            },
            {
                'name' : 'Gabriel Vidal',
                'instrumentalist' : True,
                'type_instrumental' : 'Violão',
                'vocalist' : True,
                'type_vocal' : 'Tenor',
                'music_message' : True,
                'except_day' : [],
            },
        ],
        "mensagem_musical" : [
            {
                'name' : 'Pamela Souza',
                'instrumentalist' : False,
                'type_instrumental' : '',
                'vocalist' : True,
                'type_vocal' : 'Tenor',
                'music_message' : True,
            },
            {
                'name' : 'Pamela Souza',
                'instrumentalist' : False,
                'type_instrumental' : '',
                'vocalist' : True,
                'type_vocal' : 'Tenor',
                'music_message' : True,
            }
        ]
    }
}
'''

import requests
import json

url = "http://127.0.0.1:8000/gerar_escala"

dados = {}

headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(dados), headers=headers)

print("Status code:", response.status_code)
print("Resposta:", response.text)
