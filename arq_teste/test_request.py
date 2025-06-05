import requests
import json

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


url = "https://test-1zu4.onrender.com/gerar_escala"

dados = {
    "separar_genero": False,
    "table": "default",
    "year_event": 2025,
    "month_event": 5,
    "days_event": [
        {
            "year" : 2025,
            "month" : 5,
            "month_day": 1,
            "weekday": 6,
            "people_need": 2
        },
        {
            "year" : 2025,
            "month" : 5,
            "month_day": 23,
            "weekday": 5,
            "people_need": 2
        }
    ],
    "list_dict_person": [
        {
            "name" : "jose",
            "gender": "f"
        },
        {
            "name" : "maria",
            "gender": "f"
        }
    ],
    "funcoes": {
        "instrumentistas": [
            {
                "name": "Gabriel Vidal",
                "instrumentalist": True,
                "type_instrumental": "Violão",
                "vocalist": True,
                "type_vocal": "Tenor",
                "music_message": True,
                "except_day": []
            },
            {
                "name": "Gabriel Vidal",
                "instrumentalist": True,
                "type_instrumental": "Violão",
                "vocalist": True,
                "type_vocal": "Tenor",
                "music_message": True,
                "except_day": []
            }
        ],
        "mensagem_musical": [
            {
                "name": "Pamela Souza",
                "instrumentalist": False,
                "type_instrumental": "",
                "vocalist": True,
                "type_vocal": "Tenor",
                "music_message": True
            },
            {
                "name": "Pamela Souza",
                "instrumentalist": False,
                "type_instrumental": "",
                "vocalist": True,
                "type_vocal": "Tenor",
                "music_message": True
            }
        ]
    }
}

dados_musga = {
    "separar_genero": True,
    "table": "musica",
    "year_event": 2025,
    "month_event": 5,
    "days_event": [
        {
            "year" : 2025,
            "month" : 5,
            "month_day": 1,
            "weekday": 6,
            "people_need": 2
        },
        {
            "year" : 2025,
            "month" : 5,
            "month_day": 23,
            "weekday": 5,
            "people_need": 2
        }
    ],
    "list_dict_person": [
        {
            "name" : "jose",
            "gender": "f"
        },
        {
            "name" : "maria",
            "gender": "f"
        }
    ],
    "funcoes": {
        "instrumentistas": [
            {
                "name": "Gabriel Vidal",
                "instrumentalist": True,
                "type_instrumental": "Violão",
                "vocalist": True,
                "type_vocal": "Tenor",
                "music_message": True,
                "except_day": []
            },
            {
                "name": "Gabriel Vidal",
                "instrumentalist": True,
                "type_instrumental": "Violão",
                "vocalist": True,
                "type_vocal": "Tenor",
                "music_message": True,
                "except_day": []
            }
        ],
        "mensagem_musical": [
            {
                "name": "Pamela Souza",
                "instrumentalist": False,
                "type_instrumental": "",
                "vocalist": True,
                "type_vocal": "Tenor",
                "music_message": True
            },
            {
                "name": "Pamela Souza",
                "instrumentalist": False,
                "type_instrumental": "",
                "vocalist": True,
                "type_vocal": "Tenor",
                "music_message": True
            }
        ]
    }
}


headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(dados_musga), headers=headers)

print("Status code:", response.status_code)
print("Resposta em html: ", response.text)
