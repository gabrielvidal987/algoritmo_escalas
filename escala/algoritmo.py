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
import os, sys, subprocess
from log import log
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

day_int = {
    'quarta': 2,
    'sabado': 5,
    'domingo': 6
}
int_day = {
    2: 'quarta',
    5: 'sabado',
    6: 'domingo'
}

list_dict_person = []
util_days = []
schedule = []
final_msg = ''

year_choice = input('Digite o numero do ano desejado (caso deixe em branco será usado o ano vigente): \n')
month_choice = input('Digite o numero do mês desejado (caso deixe em branco será usado o mês vigente): \n')

# Função de validação para garantir que os dados estejam corretos
def validate_data(row):
    errors = []

    # Verifica se os dias informados são válidos
    if type(row['Dias que não pode ir']) != float and row['Dias que não pode ir'] != 'nan':
        for day in row['Dias que não pode ir'].split(','):
            if str(day).lower().replace('á','a') not in day_int:
                errors.append(f"linha {row} contém dia inválido na coluna 'dias que não pode ir' ")
                
    if type(row['Dias preferenciais']) != float and row['Dias que não pode ir'] != 'nan':
        for day in row['Dias preferenciais'].split(','):
            if str(day).lower().replace('á','a') not in day_int:
                errors.append(f"linha {row} contém dia inválido na coluna 'Dias preferenciais' ")

    # Validação do gênero
    if row['Genero'].lower() != 'm' and row['Genero'].lower() != 'f':
        errors.append(f"linha {row} contém genero inválido ")

    # Validação da atividade
    if row['Atuando'].lower() != 'sim' and row['Atuando'].lower().replace('ã','') != 'nao':
        errors.append(f"linha {row} contém um valor inválido para a coluna 'ativo' ")

    return errors

#Lê um arquivo Excel (pessoas.xlsx) contendo informações sobre as pessoas.
#Converte essas informações para um formato de dicionário (com nome, preferências, restrições de dias, gênero, etc.).
#Gera um arquivo JSON (people.json) com a lista de pessoas formatada.
def create_people_list() -> None:
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
                "music_message" : True if str(row['Mensagem Musical']).lower() == 'sim' else False, #booleana se ela faz mensagem musical
                "except_day" : [day_int[day.lower().replace('á','a')] for day in row['Dias que não pode ir'].split(',')] if type(row['Dias que não pode ir']) != float else [], #dias em que ela não consegue ficar
                "preference_day" : [day_int[day.lower().replace('á','a')] for day in row['Dias preferenciais'].split(',')] if type(row['Dias preferenciais']) != float else [], #dias em que ela prefere ficar
                "gender" : row['Genero'].lower(),
                "active" : True if row['Atuando'].lower() == 'sim' else False #se a pessoa está ativa ou não
            }
            list_dict_person.append(row)
        
        #cria o arquivo json da lista de pessoas
        with open('people.json','w',encoding='utf-8') as  f:
            json.dump(list_dict_person, f, ensure_ascii=False, indent=4)
        
        return True
    
    except Exception as er:
        log('debug','create_people_list()',f'Erro: {er}')
        return False

#Gera a lista de dias úteis do mês atual (somente segunda, terça, sábado e domingo).
#Para cada dia da semana, define o número de pessoas necessárias (4 pessoas para sábado e 2 para os outros dias).
#Salva essa lista de dias em um arquivo JSON (days.json).
def create_list_days() -> None:
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
                util_days.append({
                    "month_day" : day,
                    "weekday" : weekday,
                    "people_need" : 4 if weekday == 5 else 2 #se for sábado precisa de 4 pessoas, em outro caso só precisa de 2
                })

        #cria o arquivo json da lista de dias
        with open('days.json','w',encoding='utf-8') as  f:
            json.dump(util_days, f, ensure_ascii=False, indent=4)
        
        return True
    
    except Exception as er:
        log('debug','create_list_days()',f'Erro: {er}')
        return False

# Monta a escala de acordo com as regras:
# Alternância de Gêneros: Coloca homens e mulheres alternadamente na escala.
# Preferências: Prioriza as pessoas que têm preferências para o dia.
# Restrições: Verifica se a pessoa está disponível para o dia (não tem restrição).
# Escala Completa: Preenche o número necessário de pessoas por dia, respeitando as regras de gênero, preferências e restrições.
# Gera o arquivo JSON (final_date.json) com a tabela final de escalas.
def create_table():
    try:
        used_people = set()  # Para rastrear pessoas já escaladas
        
        # Separando homens e mulheres
        men = [p for p in list_dict_person if p['gender'] == 'm' and p['active']]
        women = [p for p in list_dict_person if p['gender'] == 'f' and p['active']]
        
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
                        person = preferred_men.pop(0)
                        day_people.append(person['name'])
                        used_people.add(person['name'])
                    elif available_men:
                        person = available_men.pop(0)
                        day_people.append(person['name'])
                        used_people.add(person['name'])
                    else:
                        person = random.choice(men)
                        if weekday in person['except_day'] : continue
                        day_people.append(person['name'])
                        used_people.add(person['name'])
                else:  # Se a posição for ímpar, colocar mulher
                    if preferred_women:
                        person = preferred_women.pop(0)
                        day_people.append(person['name'])
                        used_people.add(person['name'])
                    elif available_women:
                        person = available_women.pop(0)
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
                "people" : day_people
            })
        
        #cria o arquivo json do resultado final
        with open('final_date.json','w',encoding='utf-8') as  f:
            json.dump(schedule, f, ensure_ascii=False, indent=4)
            
        return True
    
    except Exception as er:
        log('debug','create_table()',f'Erro: {er}')
        return False
   
#cria o arquivo txt no formato de mensagem
def create_message():
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
        final_msg += f'🔵 {sched["month_day"]}/{mes} - {sched["weekday"]}\n'
        for person in sched["people"]:
            final_msg += person + ' , ' if person != sched["people"][-1] else person
        final_msg += '\nInstrumentista: Sonoplastia'
        final_msg += '\n\n'
        if sched["weekday"] == 'sabado':
            final_msg += '\n\n'
   
#cria o html com jinja2
def create_html():
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
    # Configura o caminho para os templates (diretório 'templates')
    env = Environment(loader=FileSystemLoader('templates'))

    # Carrega o template 'index.html' que estará na pasta templates
    template = env.get_template('index.html')

    hoje = datetime.now()
    ano = hoje.year if year_choice == '' else int(year_choice)
    mes = hoje.month if month_choice == '' else int(month_choice)

    # Dados que você deseja passar para o template
    dados = {
        'titulo': 'Exemplo Escala',
        'nome': 'João',
        'mes': months[mes],
        'ano': ano,
        'idade': 25,
        'dias_uteis': schedule,
        'msg': final_msg.replace('\n','</br>')
    }

    # Renderiza o template com os dados passados e exibe o HTML
    html_renderizado = template.render(dados)

    #escreve o html em um arquivo
    with open('exemplo.html', 'w', encoding='utf-8') as f:
        f.write(html_renderizado)
        
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    arquivo_html = os.path.join(diretorio_script,'exemplo.html')
    subprocess.run(["start", arquivo_html], shell=True)

if __name__ == '__main__':
    if create_people_list():
        if create_list_days():
            if create_table():
                create_message()
                create_html()
                print('Tabela com escala criada com sucesso!')
            else:
                print('Erro. Checar log')
        else:
            print('Erro. Checar log')
    else:
        print('Erro. Checar log')