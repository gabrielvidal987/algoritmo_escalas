import calendar
import json
import pandas as pd
import random
import requests
import os, re
from datetime import datetime

url = 'https://algoritmo-escalas.onrender.com/gerar_escala_musica'
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
nome_arq_html = 'Escala Musica.html'
arq_saida_html = os.path.join(diretorio_atual, nome_arq_html)

'''VARIAVEIS'''
day_int = {
    'segunda': 0,
    'terca': 1,
    'quarta': 2,
    'quinta': 3,
    'sexta': 4,
    'sabado': 5,
    'domingo': 6
}
escale_names = {
    (6, 1) : ["Marcos"], 
    (6, 3) : ["Marcos"], 
    (6, 2) : ["Alan"], 
    (6, 4) : ["Alan"], 
    (5, 1) : ["Davi"], 
    (5, 3) : ["Davi"], 
    (5, 2) : ["Gabriel", "Thiago"], 
    (5, 4) : ["Gabriel", "Thiago"], 
    (2, 1) : ["Pamela", "Iohana"], 
    (2, 3) : ["Pam", "Iohana"], 
    (2, 2) : ["Pedro"], 
    (2, 4) : ["Pedro"], 
    (2, 5) : ["Gabriel"], 
    (5, 5) : ["Gabriel"], 
    (6, 5) : ["Gabriel"], 
}
funcoes = {
    "instrumentistas" : [],
    "mensagem musical" : []
}

escale_sonoplaste = {}
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
    global list_dict_person
    
    def validate_data(row):
        '''Função de validação para garantir que os dados estejam corretos'''
        
        errors = []

        # Validação se os dias informados são validos para o "dias que não pode ir" 
        if type(row['Dias que não pode ir']) != float and row['Dias que não pode ir'] != 'nan':
            for day in row['Dias que não pode ir'].replace(' ','').split(','):
                if str(day).lower().replace('á','a').replace('ç','c') not in day_int:
                    errors.append(f"linha {row} contém dia inválido na coluna 'dias que não pode ir' ")
                
        # Validação se os dias informados são validos para o "dias preferenciais" 
        if type(row['Dias preferenciais']) != float and row['Dias preferenciais'] != 'nan':
            for day in row['Dias preferenciais'].replace(' ','').split(','):
                if str(day).lower().replace('á','a').replace('ç','c') not in day_int:
                    errors.append(f"linha {row} contém dia inválido na coluna 'Dias preferenciais' ")

        # Validação do campo instrumentista
        if type(row['Instrumentista']) != float:
            if row['Instrumentista'].lower() != 'sim' and row['Instrumentista'].lower().replace('ã','') != 'nao':
                errors.append(f"linha {row} contém um valor inválido para a coluna 'Instrumentista' ")
                
        # Validação do campo vocalista
        if type(row['Vocalista']) != float:
            if row['Vocalista'].lower() != 'sim' and row['Vocalista'].lower().replace('ã','') != 'nao':
                errors.append(f"linha {row} contém um valor inválido para a coluna 'Vocalista' ")

        # Validação do gênero
        if row['Genero'].lower() != 'm' and row['Genero'].lower() != 'f':
            errors.append(f"linha {row} contém genero inválido ")

        # Validação da atividade
        if type(row['Atuando']) != float:
            if row['Atuando'].lower() != 'sim' and row['Atuando'].lower().replace('ã','') != 'nao':
                errors.append(f"linha {row} contém um valor inválido para a coluna 'ativo' ")

        return errors

    planilha_people = os.path.join(diretorio_atual, 'pessoas_music.xlsx')
    df = pd.read_excel(planilha_people)
    #itera sobre as linhas para criar uma lista alternando entre homem e mulher
    for i, row in df.iterrows():
        #verifica se a row contem dados validos
        errors = validate_data(row)
        if errors:
            raise Exception(f'debug || create_people_list() || Erro captado no validate_data() erros: {errors}')
        
        row = {
            "name" : row['Nome'], #nome da pessoa
            "instrumentalist" : True if str(row['Instrumentista']).lower() == 'sim' else False, #Booleana que diz se a pessoa é instrumentista
            "type_instrumental" : str(row['Instrumento']) if type(row['Instrumento']) != float else '', #tipo de instrumento tocado
            "vocalist" : True if str(row['Vocalista']).lower() == 'sim' else False, #Booleana que diz se a pessoa é vocalista
            "type_vocal" : str(row['Tipo Vocal']) if type(row['Tipo Vocal']) != float else '', #tipo de voz
            "music_message" : True if str(row['Faz mensagem musical']).lower() == 'sim' else False, #booleana se ela faz mensagem musical
            "except_day" : [day_int[day.lower().replace('á','a')] for day in row['Dias que não pode ir'].replace(' ','').split(',')] if type(row['Dias que não pode ir']) != float else [], #dias em que ela não consegue ficar
            "preference_day" : [day_int[day.lower().replace('á','a')] for day in row['Dias preferenciais'].replace(' ','').split(',')] if type(row['Dias preferenciais']) != float else [], #dias em que ela prefere ficar
            "gender" : row['Genero'].lower(), #genero da pessoa f = feminino e m = masculino
            "active" : True if str(row['Atuando']).lower() == 'sim' else False #se a pessoa está ativa ou não
        }
        
        list_dict_person.append(row)
        
    if not list_dict_person:
        raise Exception(f'debug || create_people_list() || Lista de dicionarios das pessoas ficou vazio')
    else:
        #cria o arquivo json da lista de pessoas
        # with open(os.path.join(pasta_arquivos, 'pessoas da escala.json'),'w',encoding='utf-8') as  f:
            # json.dump(list_dict_person, f, ensure_ascii=False, indent=4)
        return True


def create_people_func_list():
    '''Lista as pessoas que possuem funções diferentes de cantar'''
    for p in list_dict_person:
        if p['active'] and p['instrumentalist'] or p['music_message']:
            if p['instrumentalist']:
                funcoes['instrumentistas'].append(p)
            if p['music_message']:
                funcoes['mensagem musical'].append(p)
  

def create_sonoplaste_escale():
    global escale_sonoplaste
    
    try:    
        def ordinary_position_day_on_month(weekday: int, arg_date: datetime) -> int:
            """
            Retorna a posição ordinal de um dia da semana no mês.
            Exemplo: "2" significa 'segunda {data}' do mês ou 'segunda quarta-feira' do mês caso a data passada seja uma quarta feira.
            """
            contador = 0

            for dia in range(1, arg_date.day + 1):
                if datetime(arg_date.year, arg_date.month, dia).weekday() == weekday:
                    contador += 1

            return contador


        # Obter os dias do mês atual (retorna uma tupla (dia da semana que o mes começa , numero de dias no mês))
        first_weekday_month, month_days = calendar.monthrange(year_choice, month_choice)

        dias = {}
        for day in range(1,month_days + 1):
            date = datetime(year_choice, month_choice, day)
            weekday = date.weekday()  # 0=segunda, 1=terça, ..., 6=domingo
            if weekday != 2 and weekday != 5 and weekday != 6: continue
            # No dicionario dias fica o numero do dia como chave e seu valor é uma tupla (weekday, posição ordinal do dia da semana no mês) -> exemplo: [5] = (5, 1) dia 5 é o primeiro sabado
            dias[day] = (weekday, ordinary_position_day_on_month(weekday, date))

        for k, v in dias.items():
            for date, name in escale_names.items():
                if v == date:
                    escale_sonoplaste[k] = name
                    break

        return True
    
    except Exception as er:
        raise Exception(f'debug || create_sonoplaste_escale() || Erro: {er}')


def hello():
    print('-'*40)
    print('EXECUTANDO ALGORITMO DE CRIAÇÃO DE ESCALA PARA MÚSICA')
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
    create_people_func_list()
    create_sonoplaste_escale()

    if not all([days_event, list_dict_person, escale_sonoplaste, funcoes]):
        print(f'Variavel separar_genero:\n {separar_genero}')
        print(f'Variavel days_event:\n {days_event}')
        print(f'Variavel list_dict_person:\n {list_dict_person}')
        print(f'Variavel escale_sonoplaste:\n {escale_sonoplaste}')
        print(f'Variavel funcoes:\n {funcoes}')
        
        raise Exception(f'Erro em alguma variavel')


    dados = {
        "separar_genero" : separar_genero,
        "days_event" : days_event,
        "year_event" : year_choice,
        "month_event" : month_choice,
        "list_dict_person" : list_dict_person,
        "escale_sonoplaste" : escale_sonoplaste,
        "funcoes" : funcoes,
    }

    response = requests.post(url, json=dados, verify=False)

    response_json = json.loads(response.text)
    if response_json["success"]:
        doc_html = response_json["html_content"]
        with open(arq_saida_html, 'w', encoding="utf-8") as f:
            f.write(doc_html)
            
        msg_final()
    else:
        print(f'Sem resultados: {response_json}')