import requests

url = 'https://localhost:4000/gerar_escala'

'''VARIAVEIS'''
separar_genero = None
days_event = [{}, {}, {}]
list_dict_person = 

# Seu JSON em formato de dicionário Python
dados = {
    "nome": "João",
    "idade": 30,
    "email": "joao@example.com"
}

# Enviando como JSON
response = requests.post(url, json=dados)

# Exibindo resultado
print("Status:", response.status_code)
print("Resposta:", response.text)
