'''algoritmo para escala, ele monta a escala de forma aleatória porém com algumas regras de execucao
    parans: 
    name = str, #nome da pessoa
    music_message = bool, #booleana se ela faz mensagem musical
    except_day = [], #dias em que ela não consegue ficar
    preference_day = [], #dias em que ela prefere ficar
    active = bool #se a pessoa está ativa ou não
'''

import calendar
import json
import pandas as pd
import random
import os, subprocess, sys, re
from log import log
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

day_int = {
    'segunda': 0,
    'terca': 1,
    'quarta': 2,
    'quinta': 3,
    'sexta': 4,
    'sabado': 5,
    'domingo': 6
}
int_day = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}
months = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
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

# Estrutura: {"dia : int" : "nome do sonoplasta"}
escale_sonoplaste = {}
list_dict_person = []
util_days = []
schedule = []
final_msg = ''
pasta_arquivos = 'arquivos'
os.makedirs(pasta_arquivos, exist_ok=True)

year_choice = int(re.sub(r'\D', '', input('Digite o numero do ano desejado (caso deixe em branco será usado o ano vigente): \n')) or datetime.now().year)
month_choice = int(re.sub(r'\D', '', input('Digite o numero do mês desejado (caso deixe em branco será usado o mês vigente): \n')) or datetime.now().month)
qtd_quarta = int(re.sub(r'\D', '', input('Digite o numero de pessoas necessárias para Quarta-Feira (caso deixe em branco não serão escaladas pessoas para esse dia): \n')) or 0)
qtd_sabado = int(re.sub(r'\D', '', input('Digite o numero de pessoas necessárias para Sábado (caso deixe em branco não serão escaladas pessoas para esse dia): \n')) or 0)
qtd_domingo = int(re.sub(r'\D', '', input('Digite o numero de pessoas necessárias para Domingo (caso deixe em branco não serão escaladas pessoas para esse dia): \n')) or 0)

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

def create_people_list() -> None:
    '''Lê um arquivo Excel (pessoas.xlsx) contendo informações sobre as pessoas.
    Converte essas informações para um formato de dicionário (com nome, preferências, restrições de dias, gênero, etc.).
    Gera um arquivo JSON (people.json) com a lista de pessoas formatada.'''
    
    try:
        planilha_people = 'pessoas.xlsx'
        df = pd.read_excel(planilha_people)
        #itera sobre as linhas para criar uma lista alternando entre homem e mulher
        for i, row in df.iterrows():
            #verifica se a row contem dados validos
            errors = validate_data(row)
            if errors:
                log('debug','create_people_list()',f'Erro captado no validate_data() erros: \n {errors}')
                return False
            
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
            print('Lista de dicionarios das pessoas ficou vazio!')
            return False
        else:
            #cria o arquivo json da lista de pessoas
            with open(os.path.join(pasta_arquivos, 'pessoas da escala.json'),'w',encoding='utf-8') as  f:
                json.dump(list_dict_person, f, ensure_ascii=False, indent=4)
            return True
    
    except Exception as er:
        log('debug','create_people_list()',f'Erro: {er}')
        return False

def create_people_func_list() -> None:
    '''Lista as pessoas que possuem funções diferentes de cantar'''
    for p in list_dict_person:
        if p['active'] and p['instrumentalist'] or p['music_message']:
            if p['instrumentalist']:
                funcoes['instrumentistas'].append(p)
            if p['music_message']:
                funcoes['mensagem musical'].append(p)
    
def create_list_days() -> None:
    '''Gera a lista de dias úteis do mês atual (somente segunda, terça, sábado e domingo).
    Para cada dia da semana, define o número de pessoas necessárias (4 pessoas para sábado e 2 para os outros dias).
    Salva essa lista de dias em um arquivo JSON (days.json).'''
    
    try:
        hoje = datetime.now()
        try:
            ano = hoje.year if year_choice == '' else int(year_choice)
            mes = hoje.month if month_choice == '' else int(month_choice)
            # Obter os dias do mês atual (retorna uma tupla (dia da semana que o mes começa , numero de dias))
            month_days = calendar.monthrange(ano, mes)[1]
        except Exception as er:
            log('debug','create_list_days()',f'Erro ao pegar dias do mês: {er}')
            return False

        #dá um for nos dias (+1 pois é o stop dele)
        for day in range(1, month_days + 1):
            weekday = datetime(year=ano,month=mes,day=day).weekday()
            if weekday == 2 or weekday == 5 or weekday == 6:
                #adiciona uma tupla (numero do dia , numero weekday daquele dia)
                dict_day = {
                    "month_day" : day,
                    "weekday" : weekday,
                }
                match weekday:
                    case 2:
                        if qtd_quarta < 1: continue
                        dict_day["people_need"] = qtd_quarta
                    case 5:
                        if qtd_sabado < 1: continue
                        dict_day["people_need"] = qtd_sabado
                    case 6:
                        if qtd_domingo < 1: continue
                        dict_day["people_need"] = qtd_domingo
                    case _:
                        print(f'Dia não encontrado weekday: {weekday}')
                        
                util_days.append(dict_day)

        if not util_days:
            print('Lista de dias uteis disponiveis ficou vazio!')
            return False
        else:
            #cria o arquivo json da lista de dias
            with open(os.path.join(pasta_arquivos, 'dias requeridos.json'),'w',encoding='utf-8') as  f:
                json.dump(util_days, f, ensure_ascii=False, indent=4)
            return True
    
    except Exception as er:
        log('debug','create_list_days()',f'Erro: {er}')
        return False

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
        log('debug','create_sonoplaste_escale()',f'Erro: {er}')
        return False

def create_table():
    '''Monta a escala de acordo com as regras:
    Alternância de Gêneros: Coloca homens e mulheres alternadamente na escala.
    Preferências: Prioriza as pessoas que têm preferências para o dia.
    Restrições: Verifica se a pessoa está disponível para o dia (não tem restrição).
    Escala Completa: Preenche o número necessário de pessoas por dia, respeitando as regras de gênero, preferências e restrições.
    Gera o arquivo JSON (final_date.json) com a tabela final de escalas.'''
    
    try:
        used_people = set()  # Para rastrear pessoas já escaladas
        
        # Separando homens e mulheres
        men = [p for p in list_dict_person if p['gender'] == 'm' and p['active'] and p['vocalist']]
        women = [p for p in list_dict_person if p['gender'] == 'f' and p['active'] and p['vocalist']]
        
        #iterea sobre os dias uteis
        for day in util_days:
            day_people = []
            required_people = day['people_need']
            month_day = day['month_day']
            weekday = day['weekday']
            
            # Priorizar pessoas com preferências para o dia
            preferred_men = [p for p in men if weekday in p['preference_day'] and p['name'] not in used_people]
            preferred_women = [p for p in women if weekday in p['preference_day'] and p['name'] not in used_people]
            
            # Filtra as pessoas que podem ser escaladas para esse dia
            available_men = [p for p in men if weekday not in p['except_day'] and p['name'] not in used_people and p not in preferred_men]
            available_women = [p for p in women if weekday not in p['except_day'] and p['name'] not in used_people and p not in preferred_women]
            
            # Alternar entre homem e mulher
            while len(day_people) < required_people:
                if len(day_people) % 2 == 0:  # Se a posição for par, colocar homem
                    if preferred_men:
                        person = preferred_men.pop(random.randint(0,len(preferred_men) - 1))
                        day_people.append(person['name'])
                        used_people.add(person['name'])
                    elif available_men:
                        person = available_men.pop(random.randint(0,len(available_men) - 1))
                        day_people.append(person['name'])
                        used_people.add(person['name'])
                    else:
                        person = random.choice(men)
                        if weekday in person['except_day'] : continue
                        day_people.append(person['name'])
                        used_people.add(person['name'])
                else:  # Se a posição for ímpar, colocar mulher
                    if preferred_women:
                        person = preferred_women.pop(random.randint(0,len(preferred_women) - 1))
                        day_people.append(person['name'])
                        used_people.add(person['name'])
                    elif available_women:
                        person = available_women.pop(random.randint(0,len(available_women) - 1))
                        day_people.append(person['name'])
                        used_people.add(person['name'])
                    else:
                        person = random.choice(women)
                        if person['except_day'] == weekday: continue
                        day_people.append(person['name'])
                        used_people.add(person['name'])
                        
            # Atribuindo as pessoas ao dia
            schedule.append({
                "month_day" : month_day,
                "weekday" : int_day[weekday],
                "required_people" : required_people,
                "people" : day_people,
                "sonoplaste" : escale_sonoplaste[month_day],
            })
        
        
        if not schedule:
            print('Lista de dicionarios dos dias da escala ficaram vazios!')
            return False
        else:
            #cria o arquivo json do resultado final
            with open(os.path.join(pasta_arquivos,'resultado_escala.json'),'w',encoding='utf-8') as  f:
                json.dump(schedule, f, ensure_ascii=False, indent=4)
            return True
    
    except Exception as er:
        log('debug','create_table()',f'Erro: {er}')
        return False
   
def create_message():
    '''cria o arquivo txt no formato de mensagem'''
 
    global final_msg
    '''    
    Odd/mm - sabado
    nome, nome, nome,
    instrumentista: nome 
    '''
    
    #cria a string da mensagem
    hoje = datetime.now()
    mes = hoje.month if month_choice == '' else int(month_choice)
    for sched in schedule:
        final_msg += f'🔵 {sched["month_day"]}/{mes} - {str(sched["weekday"]).upper()}\n'
        for person in sched["people"]:
            final_msg += f'{person} , ' if person != sched["people"][-1] else person
        final_msg += '\nInstrumentista(s): Sonoplastia'
        final_msg += f'\nSonoplasta(s): {" e ".join(sched["sonoplaste"])}'
        final_msg += '\n\n'
        if sched["weekday"] == 'sabado':
            final_msg += '\n\n'
   
def create_html():
    '''cria o html com jinja2'''

    # Configura o caminho para os templates (diretório 'templates')
    env = Environment(loader=FileSystemLoader('templates'))

    # Carrega o template 'index.html' que estará na pasta templates
    template = env.get_template('index.html')

    hoje = datetime.now()
    ano = hoje.year if year_choice == '' else int(year_choice)
    mes = hoje.month if month_choice == '' else int(month_choice)

    # Dados que você deseja passar para o template
    dados = {
        'titulo': 'Exemplo De Escala',
        'nome': 'João',
        'mes': months[mes],
        'ano': ano,
        'idade': 25,
        'dias_uteis': schedule,
        'funcoes' : funcoes,
        'msg': final_msg.replace('\n','</br>')
    }

    # Renderiza o template com os dados passados e exibe o HTML
    html_renderizado = template.render(dados)

    #escreve o html em um arquivo
    with open(os.path.join(pasta_arquivos, 'escala criada.html'), 'w', encoding='utf-8') as f:
        f.write(html_renderizado)
        
    arquivo_html = os.path.join(os.path.join(pasta_arquivos,'escala criada.html'))
    os.startfile(arquivo_html)

if __name__ == '__main__':
    if create_people_list() and list_dict_person:
        create_people_func_list()
        if create_list_days() and util_days:
            if create_sonoplaste_escale() and escale_sonoplaste:
                if create_table() and schedule:
                    create_message()
                    create_html()
                    print('Tabela com escala criada com sucesso!')
                else:
                    print('Erro create_table(). Checar log')
            else:
                print('Erro no create_sonoplaste_escale(). Checar log')
        else:
            print('Erro no create_list_days(). Checar log')
    else:
        print('Erro no create_people_list(). Checar log')