import random
import uvicorn
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi import Request

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
    0: 'segunda',
    1: 'terca',
    2: 'quarta',
    3: 'quinta',
    4: 'sexta',
    5: 'sabado',
    6: 'domingo'
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

'''
formato de dados para receber

dados = {
    "separar_genero" : True,
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
    "escale_sonoplaste" : {
        "dia_do_mes" : ["pessoa1", "pessoa2"],
        "2" : ["pessoa1"],
        "8" : ["pessoa1", "pessoa2"],
        "15" : ["pessoa1"],
    }
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

app = FastAPI()
# Configura o caminho para os templates (diretório 'templates')
env = Environment(loader=FileSystemLoader('templates'))

# Rota para listar todas as tarefas
@app.get("/")
def home():
    template = env.get_template('index_get.html')
    html_renderizado = template.render()
    return HTMLResponse(content=html_renderizado, status_code=200)

# Rota para gerar uma nova escala
@app.post("/gerar_escala")
async def gerar_escala(request: Request):
    dados = await request.json()
    schedule = []
    final_msg = ''
    #dias em que terá o evento e quantas pessoas são necessárias pro dia
    days_event = dados["days_event"]
    year_event = dados["year_event"]
    month_event = dados["month_event"]
    #lista de dicionarios sendo cada dicionario a ficha de uma pessoa
    list_dict_person = dados["list_dict_person"]
    
    async def create_message():
        '''cria o arquivo txt no formato de mensagem'''
    
        nonlocal schedule, final_msg
        '''    
        Odd/mm - sabado
        nome, nome, nome,
        instrumentista: nome 
        '''
        
        #cria a string da mensagem
        hoje = datetime.now()
        mes = hoje.month if month_event == '' else int(month_event)
        for sched in schedule:
            final_msg += f'🔵 {sched["month_day"]}/{mes} - {str(sched["weekday"]).upper()}\n'
            for person in sched["people"]:
                final_msg += f'{person} , ' if person != sched["people"][-1] else person
            final_msg += '\n\n'
    
    async def create_table():
        nonlocal schedule, final_msg
        '''
        Monta a escala de acordo com as regras:
        Alternância de Gêneros: Coloca homens e mulheres alternadamente na escala.
        Preferências: Prioriza as pessoas que têm preferências para o dia.
        Restrições: Verifica se a pessoa está disponível para o dia (não tem restrição).
        Escala Completa: Preenche o número necessário de pessoas por dia, respeitando as regras de gênero, preferências e restrições.
        Gera o arquivo JSON (final_date.json) com a tabela final de escalas.
        '''
        try:
            used_people = set()  # Para rastrear pessoas já escaladas

            if dados["separar_genero"]:
                # Separando homens e mulheres
                men = [p for p in list_dict_person if p['gender'] == 'm']
                women = [p for p in list_dict_person if p['gender'] == 'f']
                
                #iterea sobre os dias uteis
                for day in days_event:
                    day_people = []
                    people_need = day['people_need']
                    month_day = day['month_day']
                    weekday = day['weekday']
                    
                    # Filtra as pessoas que podem ser escaladas para esse dia
                    available_men = [p for p in men if p['name'] not in used_people]
                    available_women = [p for p in women if p['name'] not in used_people]
                    
                    # Alternar entre homem e mulher
                    while len(day_people) < people_need:
                        if len(day_people) % 2 == 0:  # Se a posição for par, colocar homem
                            if available_men:
                                person = available_men.pop(random.randint(0,len(available_men) - 1))
                                day_people.append(person['name'])
                                used_people.add(person['name'])
                            else:
                                person = random.choice(men)
                                if weekday in person['except_day'] : continue
                                day_people.append(person['name'])
                                used_people.add(person['name'])
                        else:  # Se a posição for ímpar, colocar mulher
                            if available_women:
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
                        "year" : year_event,
                        'month' : month_event,
                        "month_day" : month_day,
                        "weekday" : int_day[weekday],
                        "people_need" : people_need,
                        "people" : day_people
                    })
                
            else:
                #iterea sobre os dias uteis
                for day in days_event:
                    day_people = []
                    people_need = day['people_need']
                    month_day = day['month_day']
                    weekday = day['weekday']
                    
                    # Filtra as pessoas que podem ser escaladas para esse dia
                    available_person = [p for p in list_dict_person if p['name'] not in used_people]
                    
                    # Alternar entre homem e mulher
                    while len(day_people) < people_need:
                        if available_person:
                            person = available_person.pop(random.randint(0,len(available_person) - 1))
                            day_people.append(person['name'])
                            used_people.add(person['name'])
                        else:
                            person = random.choice(list_dict_person)
                            day_people.append(person['name'])
                            used_people.add(person['name'])
                                
                    # Atribuindo as pessoas ao dia
                    schedule.append({
                        "year" : year_event,
                        'month' : month_event,
                        "month_day" : month_day,
                        "weekday" : int_day[weekday],
                        "people_need" : people_need,
                        "people" : day_people
                    })
            
            if not schedule:
                print('Lista de dicionarios dos dias da escala ficaram vazios!')
                return False
            else:
                return True
        
        except Exception as er:
            #log('debug','create_table()',f'Erro: {er}')
            print(f'Erro: {er}')
            return False
     
    async def create_html():
        '''cria o html com jinja2'''

        # Carrega o template 'index_default.html' que estará na pasta templates
        nonlocal dados, schedule, final_msg
        template = env.get_template('index_default.html')
            
        # Dados que você deseja passar para o template
        dados = {
            'titulo': 'Exemplo Escala',
            'nome': 'João',
            'mes': months[month_event],
            'ano': year_event,
            'idade': 25,
            'dias_uteis': schedule,
            'msg': final_msg.replace('\n','</br>')
        }

        # Renderiza o template com os dados passados e exibe o HTML
        html_renderizado = template.render(dados)

        return html_renderizado
    
    print(f'criando tabela padrão')
    await create_table()
    if schedule:
        await create_message()
        print(f'criada tabela')
        document_html = await create_html()
        print('Tabela com escala criada com sucesso!')
        return {"success": True, "html_content": document_html}
    
    return {"success": False, "html_content": ""}

# Rota para gerar uma nova escala
@app.post("/gerar_escala_musica")
async def gerar_escala_musica(request: Request):
    dados = await request.json()
    schedule = []
    final_msg = ''
    #dias em que terá o evento e quantas pessoas são necessárias pro dia
    days_event = dados["days_event"]
    year_event = dados["year_event"]
    month_event = dados["month_event"]
    #lista de dicionarios sendo cada dicionario a ficha de uma pessoa
    list_dict_person = dados["list_dict_person"]
    #lista de funcoes instrumentista ou vocalista
    funcoes = dados["funcoes"]
    
    # Cria tabela para lista de pessoas em especifico no campo de musica
    async def create_table_music():
        nonlocal schedule, final_msg
        '''
        Monta a escala de acordo com as regras:
        Alternância de Gêneros: Coloca homens e mulheres alternadamente na escala.
        Preferências: Prioriza as pessoas que têm preferências para o dia.
        Restrições: Verifica se a pessoa está disponível para o dia (não tem restrição).
        Escala Completa: Preenche o número necessário de pessoas por dia, respeitando as regras de gênero, preferências e restrições.
        Gera o arquivo JSON (final_date.json) com a tabela final de escalas.
        '''

        def create_message():
            '''cria o arquivo txt no formato de mensagem'''
        
            nonlocal schedule, final_msg
            '''    
            Odd/mm - sabado
            nome, nome, nome,
            instrumentista: nome 
            '''
            
            #cria a string da mensagem
            hoje = datetime.now()
            mes = hoje.month if month_event == '' else int(month_event)
            for sched in schedule:
                final_msg += f'🔵 {sched["month_day"]}/{mes} - {str(sched["weekday"]).upper()}\n'
                for person in sched["people"]:
                    final_msg += f'{person} , ' if person != sched["people"][-1] else person
                final_msg += '\nInstrumentista(s): Sonoplastia'
                final_msg += f'\nSonoplasta(s): {" e ".join(sched["sonoplaste"])}'
                final_msg += '\n\n'
                if sched["weekday"] == 'sabado':
                    final_msg += '\n\n'
        
        try:
            used_people = set()  # Para rastrear pessoas já escaladas
            
            if dados["separar_genero"]:
                # Separando homens e mulheres
                men = [p for p in list_dict_person if p['gender'] == 'm' and p['vocalist']]
                women = [p for p in list_dict_person if p['gender'] == 'f' and p['vocalist']]
                
                #iterea sobre os dias uteis
                for day in days_event:
                    day_people = []
                    people_need = day['people_need']
                    month_day = day['month_day']
                    weekday = day['weekday']
                    
                    # Priorizar pessoas com preferências para o dia
                    preferred_men = [p for p in men if weekday in p['preference_day'] and p['name'] not in used_people]
                    preferred_women = [p for p in women if weekday in p['preference_day'] and p['name'] not in used_people]
                    
                    # Filtra as pessoas que podem ser escaladas para esse dia
                    available_men = [p for p in men if weekday not in p['except_day'] and p['name'] not in used_people and p not in preferred_men]
                    available_women = [p for p in women if weekday not in p['except_day'] and p['name'] not in used_people and p not in preferred_women]
                    
                    # Alternar entre homem e mulher
                    while len(day_people) < people_need:
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
                        "year" : year_event,
                        'month' : month_event,
                        "month_day" : month_day,
                        "weekday" : int_day[weekday],
                        "people_need" : people_need,
                        "people" : day_people,
                        "sonoplaste" : dados["escale_sonoplaste"].get(month_day, ["Equipe de sonoplastia"]),
                    })
                
            else:
                #iterea sobre os dias uteis
                for day in days_event:
                    day_people = []
                    people_need = day['people_need']
                    month_day = day['month_day']
                    weekday = day['weekday']
                    
                    # Filtra as pessoas que podem ser escaladas para esse dia
                    available_person = [p for p in list_dict_person if p['name'] not in used_people]
                    
                    # Alternar entre homem e mulher
                    while len(day_people) < people_need:
                        if available_person:
                            person = available_person.pop(random.randint(0,len(available_person) - 1))
                            day_people.append(person['name'])
                            used_people.add(person['name'])
                        else:
                            person = random.choice(list_dict_person)
                            day_people.append(person['name'])
                            used_people.add(person['name'])
                                
                    # Atribuindo as pessoas ao dia
                    schedule.append({
                        "year" : year_event,
                        'month' : month_event,
                        "month_day" : month_day,
                        "weekday" : int_day[weekday],
                        "people_need" : people_need,
                        "people" : day_people,
                        "sonoplaste" : dados["escale_sonoplaste"][month_day],
                    })
            
            if not schedule:
                print('Lista de dicionarios dos dias da escala ficaram vazios!')
                return False
            else:
                create_message()
                return True
        
        except Exception as er:
            #log('debug','create_table()',f'Erro: {er}')
            print(f'Erro: {er}')
            return False
    
    async def create_html():
        '''cria o html com jinja2'''

        # Carrega o template 'index.html' que estará na pasta templates
        nonlocal dados, schedule, funcoes, final_msg
        template = env.get_template('index_music.html')
            
        # Dados que você deseja passar para o template
        dados = {
            'titulo': 'Exemplo Escala',
            'nome': 'João',
            'mes': months[month_event],
            'ano': year_event,
            'idade': 25,
            'dias_uteis': schedule,
            'funcoes' : funcoes,
            'msg': final_msg.replace('\n','</br>')
        }

        # Renderiza o template com os dados passados e exibe o HTML
        html_renderizado = template.render(dados)

        return html_renderizado
    
    print(f'criando tabela de musica')
    await create_table_music()
    if schedule:
        print(f'criada tabela')
        document_html = await create_html()
        print('Tabela com escala criada com sucesso!')
        return {"success": True, "html_content": document_html}
    
        
    return {"success": False, "html_content": ""}

# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=4000)