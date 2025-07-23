import re
import os
import requests
import calendar
import pandas as pd
import json
from datetime import datetime

url = 'http://localhost:4000/gerar_escala'
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
nome_arq_html = 'Escala.html'
arq_saida_html = os.path.join(diretorio_atual, nome_arq_html)

'''VARIAVEIS'''
separar_genero = None # True or False
days_event = [] # [ { 'month_day' : 1, 'weekday' : 5, 'people_need' : 2 } , { 'month_day' : 7, 'weekday' : 3, 'people_need' : 4 } ]
list_dict_person = [] #[ { 'name' : 'jose', 'gender' : 'm' } , { 'name' : 'maria', 'gender' : 'f' } ]
year_choice = None # 2025 / 25
month_choice = None # 1 - 12
qtd_domingo = None
qtd_segunda = None
qtd_terca = None
qtd_quarta = None
qtd_quinta = None
qtd_sexta = None
qtd_sabado = None

def preenche_variaveis():
    '''Realiza os input para poder preencher as variaveis'''
    
    global separar_genero, days_event, list_dict_person, year_choice, month_choice, qtd_domingo, qtd_segunda, qtd_terca, qtd_quarta, qtd_quinta, qtd_sexta, qtd_sabado

    separar_genero = input("Deseja fazer generos alternados?\n Responda com Sim ou Não\n   R: ").lower()[0]
    separar_genero = True if separar_genero == 's' else False

    print('\n--------\n')
    year_choice = int(re.sub(r'\D', '', input('Digite o número do ano desejado Formato: YYYY (caso deixe em branco será usado o ano vigente): \n   R: ')) or datetime.now().year)
    print('\n--------\n')
    month_choice = int(re.sub(r'\D', '', input('Digite o número do mês desejado (caso deixe em branco será usado o mês vigente): \n   R: ')) or datetime.now().month)
    print('\n--------\n')
    qtd_domingo = int(re.sub(r'\D', '', input('Digite o número de pessoas necessárias para Domingo (caso deixe em branco não serão escaladas pessoas para esse dia): \n   R: ')) or 0)
    print('\n--------\n')
    qtd_segunda = int(re.sub(r'\D', '', input('Digite o número de pessoas necessárias para Segunda-Feira (caso deixe em branco não serão escaladas pessoas para esse dia): \n   R: ')) or 0)
    print('\n--------\n')
    qtd_terca = int(re.sub(r'\D', '', input('Digite o número de pessoas necessárias para Terça-Feira (caso deixe em branco não serão escaladas pessoas para esse dia): \n   R: ')) or 0)
    print('\n--------\n')
    qtd_quarta = int(re.sub(r'\D', '', input('Digite o número de pessoas necessárias para Quarta-Feira (caso deixe em branco não serão escaladas pessoas para esse dia): \n   R: ')) or 0)
    print('\n--------\n')
    qtd_quinta = int(re.sub(r'\D', '', input('Digite o número de pessoas necessárias para Quinta-Feira (caso deixe em branco não serão escaladas pessoas para esse dia): \n   R: ')) or 0)
    print('\n--------\n')
    qtd_sexta = int(re.sub(r'\D', '', input('Digite o número de pessoas necessárias para Sexta-Feira (caso deixe em branco não serão escaladas pessoas para esse dia): \n   R: ')) or 0)
    print('\n--------\n')
    qtd_sabado = int(re.sub(r'\D', '', input('Digite o número de pessoas necessárias para Sábado (caso deixe em branco não serão escaladas pessoas para esse dia): \n   R: ')) or 0)


def preenche_datas():
    '''Gera a lista de dias úteis do mês atual (somente segunda, terça, sábado e domingo).
    Para cada dia da semana, define o número de pessoas necessárias (4 pessoas para sábado e 2 para os outros dias).
    Salva essa lista de dias em um arquivo JSON (days.json).'''
    
    global days_event
    
    ano = year_choice
    mes = month_choice
    # Obter os dias do mês atual (retorna uma tupla (dia da semana que o mes começa , numero de dias))
    first_weekday_month, month_days = calendar.monthrange(ano, mes)

    #dá um for nos dias (+1 pois é o stop dele)
    for day in range(1, month_days + 1):
        weekday = datetime(year=ano,month=mes,day=day).weekday()
        dict_day = {
            "month_day" : day,
            "weekday" : weekday,
        }
        match weekday:
            case 6:  # Domingo
                if qtd_domingo is None or qtd_domingo < 1: 
                    continue
                dict_day["people_need"] = qtd_domingo
            case 0:  # Segunda-feira
                if qtd_segunda is None or qtd_segunda < 1: 
                    continue
                dict_day["people_need"] = qtd_segunda
            case 1:  # Terça-feira
                if qtd_terca is None or qtd_terca < 1: 
                    continue
                dict_day["people_need"] = qtd_terca
            case 2:  # Quarta-feira
                if qtd_quarta is None or qtd_quarta < 1: 
                    continue
                dict_day["people_need"] = qtd_quarta
            case 3:  # Quinta-feira
                if qtd_quinta is None or qtd_quinta < 1: 
                    continue
                dict_day["people_need"] = qtd_quinta
            case 4:  # Sexta-feira
                if qtd_sexta is None or qtd_sexta < 1: 
                    continue
                dict_day["people_need"] = qtd_sexta
            case 5:  # Sábado
                if qtd_sabado is None or qtd_sabado < 1: 
                    continue
                dict_day["people_need"] = qtd_sabado

                
        days_event.append(dict_day)


def preenche_dict_person():
    '''Lê um arquivo Excel (pessoas.xlsx) contendo informações sobre as pessoas.
    Converte essas informações para um formato de dicionário (com nome, preferências, restrições de dias, gênero, etc.).
    Gera um arquivo JSON (people.json) com a lista de pessoas formatada.'''
    
    def validate_data(row):
        '''Função de validação para garantir que os dados estejam corretos'''
        
        errors = []

        # Validação do gênero
        if row['Genero'].lower() != 'm' and row['Genero'].lower() != 'f':
            errors.append(f"linha {row} contém genero inválido ")

        # Validação da atividade
        if type(row['Atuando']) != float:
            if row['Atuando'].lower() != 'sim' and row['Atuando'].lower().replace('ã','') != 'nao':
                errors.append(f"linha {row} contém um valor inválido para a coluna 'ativo' ")

        return errors
    
    global list_dict_person
        
    planilha_people = os.path.join(diretorio_atual, 'pessoas_default.xlsx')
    df = pd.read_excel(planilha_people)
    #itera sobre as linhas para criar uma lista alternando entre homem e mulher
    for i, row in df.iterrows():
        #verifica se a row contem dados validos
        errors = validate_data(row)
        if errors:
            raise Exception(f'debug || create_people_list() || Erro captado no validate_data() erros: {errors}')
        
        row = {
            "name" : row['Nome'], #nome da pessoa
            "gender" : row['Genero'].lower(), #genero da pessoa f = feminino e m = masculino
            "active" : True if str(row['Atuando']).lower() == 'sim' else False #se a pessoa está ativa ou não
        }
        
        list_dict_person.append(row)


def hello():
    print('-'*40)
    print('EXECUTANDO ALGORITMO DE CRIAÇÃO DE ESCALA PADRÃO')
    print('-'*40)


def msg_final():
    print('-'*40)
    print('ESCALA FINALIZADA')
    print(f'VERIFIQUE ELA NA MESMA PASTA DO PROGRAMA ABRINDO O ARQUIVO: "{nome_arq_html}" ')
    print('-'*40)
    
    
if __name__ == '__main__':
    hello()
    
    preenche_variaveis()
    preenche_datas()
    preenche_dict_person()


    if not any([separar_genero, days_event, list_dict_person]):
        print(f'Variavel separar_genero:\n {separar_genero}')
        print(f'Variavel days_event:\n {days_event}')
        print(f'Variavel list_dict_person:\n {list_dict_person}')
        
        raise Exception(f'Erro em alguma variavel')


    dados = {
        "separar_genero" : separar_genero,
        "days_event" : days_event,
        "year_event" : year_choice,
        "month_event" : month_choice,
        "list_dict_person" : list_dict_person
    }

    response = requests.post(url, json=dados, verify=False, proxies={"http": None, "https": None})

    response_json = json.loads(response.text)
    if response_json["success"]:
        doc_html = response_json["html_content"]
        with open(arq_saida_html, 'w', encoding="utf-8") as f:
            f.write(doc_html)
        
        msg_final()
    else:
        print(f'Sem resultados: {response_json}')