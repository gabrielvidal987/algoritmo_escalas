import os
import json
import random
import uvicorn
import calendar
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

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
pasta_script = os.getcwd()
PASTA_ESCALAS = os.path.join(pasta_script, "escalas")
os.makedirs(PASTA_ESCALAS, exist_ok=True)

# '''
# formato de dados para receber

# dados = {
#     "separar_genero" : True,
#     "days_event" : [
#         {
#             'month_day' : 1,
#             'weekday' : 6,
#             'people_need' : 2,    
#         },
#         {
#             'month_day' : 23,
#             'weekday' : 5,
#             'people_need' : 2,
#         }
#     ],
#     ## para tabela normal:
#     "list_dict_person" : [
#         {
#             'name' : 'jose',
#             'gender' : 'f',
#         },
#         {
#             'name' : 'maria',
#             'gender' : 'f',
#         },
#     ],
#     ## para musica:
#     "list_dict_person" : [
#         {
#             'name' : 'jose',
#             'vocalist' : True,
#             'type_vocal' : 'Tenor',
#             'music_message' : True,
#             'except_day' : [],
#             'preference_day' : [5],
#             'gender' : 'f',
#         },
#         {
#             'name' : 'maria',
#             'vocalist' : True,
#             'type_vocal' : 'Tenor',
#             'music_message' : True,
#             'except_day' : [],
#             'preference_day' : [5],
#             'gender' : 'f',
#         },
#     ],
#     "escale_sonoplaste" : {
#         "dia_do_mes" : ["pessoa1", "pessoa2"],
#         "2" : ["pessoa1"],
#         "8" : ["pessoa1", "pessoa2"],
#         "15" : ["pessoa1"],
#     }
#     "funcoes" : {
#         "instrumentistas" : [
#             {
#                 'name' : 'Gabriel Vidal',
#                 'instrumentalist' : True,
#                 'type_instrumental' : 'Violão',
#                 'vocalist' : True,
#                 'type_vocal' : 'Tenor',
#                 'music_message' : True,
#                 'except_day' : [],
#             },
#             {
#                 'name' : 'Gabriel Vidal',
#                 'instrumentalist' : True,
#                 'type_instrumental' : 'Violão',
#                 'vocalist' : True,
#                 'type_vocal' : 'Tenor',
#                 'music_message' : True,
#                 'except_day' : [],
#             },
#         ],
#         "mensagem_musical" : [
#             {
#                 'name' : 'Pamela Souza',
#                 'instrumentalist' : False,
#                 'type_instrumental' : '',
#                 'vocalist' : True,
#                 'type_vocal' : 'Tenor',
#                 'music_message' : True,
#             },
#             {
#                 'name' : 'Pamela Souza',
#                 'instrumentalist' : False,
#                 'type_instrumental' : '',
#                 'vocalist' : True,
#                 'type_vocal' : 'Tenor',
#                 'music_message' : True,
#             }
#         ]
#     }
# }
# '''

''' FUNCOES '''
def get_days_event(dados):
    '''
    dados = {
        Nome: "",
        Mes: 11,
        Ano: 2025,
        SepararGenero: false,
        Domingo : 0,
        Segunda : 0,
        Terca : 0,
        Quarta : 0,
        Quinta : 0,
        Sexta : 0,
        Sabado : 0,
    }
    '''
    month_days = calendar.monthrange(dados["Ano"], dados["Mes"])[1]
    #dá um for nos dias (+1 pois é o stop dele)
    data_convert = {
        6 : "Domingo",
        0 : "Segunda",
        1 : "Terca",
        2 : "Quarta",
        3 : "Quinta",
        4 : "Sexta",
        5 : "Sabado",
    }
    dias = []
    data_free = []
    if dados["Domingo"] > 0: dias.append(6)
    if dados["Segunda"] > 0: dias.append(0)
    if dados["Terca"] > 0: dias.append(1)
    if dados["Quarta"] > 0: dias.append(2)
    if dados["Quinta"] > 0: dias.append(3)
    if dados["Sexta"] > 0: dias.append(4)
    if dados["Sabado"] > 0: dias.append(5)
    
    for day in range(1, month_days + 1):
        weekday = datetime(year=dados["Ano"], month=dados["Mes"], day=day).weekday()
        
        if weekday in dias:
            #adiciona uma tupla (numero do dia , numero weekday daquele dia)
            dict_day = {
                "month_day" : day,
                "weekday" : weekday,
                "people_need" : dados[data_convert[weekday]],
                "name_day" : data_convert[weekday]
            }
                    
            data_free.append(dict_day)

    return data_free
    
def get_people_music():
    people = []
    total_people = []
    with open("pessoas_music.json", "r", encoding="utf-8") as f:
        total_people = json.load(f)
    for p in total_people:
        if p["Atuando"]: people.append(p)
    return people

def get_sonoplaste_scale(dados):
    escale_sonoplaste = {}
    escale_names = {}
    
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

        with open('pessoas_sonoplaste.json', 'r', encoding='utf-8') as f:
            escale_names = json.load(f)
        
        # Obter os dias do mês atual (retorna uma tupla (dia da semana que o mes começa , numero de dias no mês))
        first_weekday_month, month_days = calendar.monthrange(dados["Ano"], dados["Mes"])

        dias = {}
        for day in range(1,month_days + 1):
            date = datetime(dados["Ano"], dados["Mes"], day)
            weekday = date.weekday()  # 0=segunda, 1=terça, ..., 6=domingo
            if weekday != 2 and weekday != 5 and weekday != 6: continue
            # No dicionario dias fica o numero do dia como chave e seu valor é uma tupla (weekday, posição ordinal do dia da semana no mês) -> exemplo: [5] = (5, 1) dia 5 é o primeiro sabado
            dias[day] = (weekday, ordinary_position_day_on_month(weekday, date))

        for k, v in dias.items():
            for date, name in escale_names.items():
                v = str(v).replace('(','').replace(')','').replace(' ','')
                if v == date:
                    escale_sonoplaste[k] = name
                    break

    except Exception as er:
        escale_sonoplaste = {}
    
    finally:
        return escale_sonoplaste


''' CLASSES DE INTERFACE '''

''' ENDPOINTS '''
app = FastAPI()
# Configura o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 permite qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # 👈 permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # 👈 permite todos os headers
)
# Configura o caminho para os templates (diretório 'templates')
env = Environment(loader=FileSystemLoader('templates'))
app.mount("/assets", StaticFiles(directory=os.path.join(pasta_script, "assets")), name="assets")

# Rota que joga para pagina principal e a propria pagina se altera dependendo do que vem após a barra
@app.get("/")
def func():
    template = env.get_template('index_get.html')
    html_renderizado = template.render()
    return HTMLResponse(content=html_renderizado, status_code=200)

# Rota que joga para pagina principal e a propria pagina se altera dependendo do que vem após a barra
@app.get("/admin_cidAd")
def func():
    template = env.get_template('index_get.html')
    html_renderizado = template.render()
    return HTMLResponse(content=html_renderizado, status_code=200)

@app.get("/lista_escalas")
def func():
    lista_arq = os.listdir(PASTA_ESCALAS)
    return {"lista_arq" : lista_arq}

@app.get("/conteudo_escala")
def func(nome_arq):
    arquivo = os.path.join(PASTA_ESCALAS, nome_arq)
    existe = os.path.exists(arquivo)
    conteudo = ""
    if existe:
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = json.load(f)
            conteudo = conteudo["escala"]
    return {"existe" : existe, "conteudo" : conteudo}

@app.get("/deletar_escala")
def func(nome_arq):
    arquivo = os.path.join(PASTA_ESCALAS, nome_arq)
    existe = os.path.exists(arquivo)
    if existe:
        try:
            os.remove(arquivo)
        except:
            pass
    
    return {"existe" : os.path.exists(arquivo)}

@app.get("/lista_user_music")
def func():
    conteudo = []
    with open("pessoas_music.json", 'r', encoding='utf-8') as f: conteudo = json.load(f)
    return {"lista_user_music" : conteudo}

@app.post("/add_user_music")
def func(dados_user : dict):
    conteudo = []
    with open("pessoas_music.json", 'r', encoding='utf-8') as f: conteudo = json.load(f)
    conteudo.append(dados_user)
    with open("pessoas_music.json", 'w') as f: json.dump(conteudo, f, indent=4)
    return {"Tipo Vocal" : conteudo}

@app.post("/salvar_alteracao")
def func(dados : dict):
    file = os.path.join(PASTA_ESCALAS, dados["file"])
    if os.path.exists(file):
        with open(file, 'w') as f: json.dump(dados['conteudo'], f, indent=4)
    return {"sucess" : True}

# Rota para gerar uma nova escala
@app.post("/gerar_escala_normal")
async def func(request: Request):
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
async def func(dados : dict):
    '''
    dados = {
        Nome: "",
        Mes: "",
        Ano: "",
        SepararGenero: false,
        Domingo : 0,
        Segunda : 0,
        Terca : 0,
        Quarta : 0,
        Quinta : 0,
        Sexta : 0,
        Sabado : 0,
    }
    '''
    if not dados["Nome"]: dados["Nome"] = f'Escala de {months[dados["Mes"]]} de {dados["Ano"]}'
    arq_json = os.path.join(PASTA_ESCALAS, f'{dados["Nome"]}.json')
    schedule = []
    final_msg = ''
    #dias em que terá o evento e quantas pessoas são necessárias pro dia
    days_event = get_days_event(dados=dados)
    dados["escale_sonoplaste"] = get_sonoplaste_scale(dados=dados)
    #lista de dicionarios sendo cada dicionario a ficha de uma pessoa
    list_dict_person = get_people_music()
    
    year_event = dados["Ano"]
    month_event = dados["Mes"]
    
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
            final_msg += f'ESCALA DE {months[mes]} DE {hoje.year}\n'
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
            
            if dados["SepararGenero"]:
                # Separando homens e mulheres
                men = [p for p in list_dict_person if p['Genero'] == 'm' and p['Vocalista']]
                women = [p for p in list_dict_person if p['Genero'] == 'f' and p['Vocalista']]
                
                #iterea sobre os dias uteis
                for day in days_event:
                    day_people = []
                    people_need = day['people_need']
                    month_day = day['month_day']
                    weekday = day['weekday']
                    name_day = day['name_day']
                    
                    # Priorizar pessoas com preferências para o dia
                    preferred_men = [p for p in men if name_day in p['Dias preferenciais'] and p['Nome'] not in used_people]
                    preferred_women = [p for p in women if name_day in p['Dias preferenciais'] and p['Nome'] not in used_people]
                    
                    # Filtra as pessoas que podem ser escaladas para esse dia
                    available_men = [p for p in men if name_day not in p['Dias não preferenciais'] and p['Nome'] not in used_people and p not in preferred_men]
                    available_women = [p for p in women if name_day not in p['Dias não preferenciais'] and p['Nome'] not in used_people and p not in preferred_women]
                    
                    # Alternar entre homem e mulher
                    while len(day_people) < people_need:
                        if len(day_people) % 2 == 0:  # Se a posição for par, colocar homem
                            if preferred_men:
                                person = preferred_men.pop(random.randint(0,len(preferred_men) - 1))
                                day_people.append(person['Nome'])
                                used_people.add(person['Nome'])
                            elif available_men:
                                person = available_men.pop(random.randint(0,len(available_men) - 1))
                                day_people.append(person['Nome'])
                                used_people.add(person['Nome'])
                            else:
                                person = random.choice(men)
                                if weekday in person['Dias não preferenciais'] : continue
                                day_people.append(person['Nome'])
                                used_people.add(person['Nome'])
                        else:  # Se a posição for ímpar, colocar mulher
                            if preferred_women:
                                person = preferred_women.pop(random.randint(0,len(preferred_women) - 1))
                                day_people.append(person['Nome'])
                                used_people.add(person['Nome'])
                            elif available_women:
                                person = available_women.pop(random.randint(0,len(available_women) - 1))
                                day_people.append(person['Nome'])
                                used_people.add(person['Nome'])
                            else:
                                person = random.choice(women)
                                if person['Dias não preferenciais'] == weekday: continue
                                day_people.append(person['Nome'])
                                used_people.add(person['Nome'])
                                
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
                    name_day = day['name_day']
                    
                    # Filtra as pessoas que podem ser escaladas para esse dia
                    available_person = [p for p in list_dict_person if p['Nome'] not in used_people and name_day not in p['Dias não preferenciais'] ]
                    
                    # Alternar entre homem e mulher
                    while len(day_people) < people_need:
                        if available_person:
                            person = available_person.pop(random.randint(0,len(available_person) - 1))
                            day_people.append(person['Nome'])
                            used_people.add(person['Nome'])
                        else:
                            person = random.choice(list_dict_person)
                            day_people.append(person['Nome'])
                            used_people.add(person['Nome'])
                                
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
    
    await create_table_music()
        
    if schedule:
        with open(arq_json, 'w') as f: json.dump({"escala" : final_msg}, f, indent=4)
        
    return {"success": os.path.exists(arq_json), "schedule" : schedule, "final_msg" : final_msg, "html_content": ""}

# BACKUP
# Rota para gerar uma nova escala
# @app.post("/gerar_escala_musica")
# async def func(request: Request):
#     dados = await request.json()
#     schedule = []
#     final_msg = ''
#     #dias em que terá o evento e quantas pessoas são necessárias pro dia
#     days_event = dados["days_event"]
#     year_event = dados["year_event"]
#     month_event = dados["month_event"]
#     #lista de dicionarios sendo cada dicionario a ficha de uma pessoa
#     list_dict_person = dados["list_dict_person"]
#     #lista de funcoes instrumentista ou vocalista
#     funcoes = dados["funcoes"]
    
#     # Cria tabela para lista de pessoas em especifico no campo de musica
#     async def create_table_music():
#         nonlocal schedule, final_msg
#         '''
#         Monta a escala de acordo com as regras:
#         Alternância de Gêneros: Coloca homens e mulheres alternadamente na escala.
#         Preferências: Prioriza as pessoas que têm preferências para o dia.
#         Restrições: Verifica se a pessoa está disponível para o dia (não tem restrição).
#         Escala Completa: Preenche o número necessário de pessoas por dia, respeitando as regras de gênero, preferências e restrições.
#         Gera o arquivo JSON (final_date.json) com a tabela final de escalas.
#         '''

#         def create_message():
#             '''cria o arquivo txt no formato de mensagem'''
        
#             nonlocal schedule, final_msg
#             '''    
#             Odd/mm - sabado
#             nome, nome, nome,
#             instrumentista: nome 
#             '''
            
#             #cria a string da mensagem
#             hoje = datetime.now()
#             mes = hoje.month if month_event == '' else int(month_event)
#             for sched in schedule:
#                 final_msg += f'🔵 {sched["month_day"]}/{mes} - {str(sched["weekday"]).upper()}\n'
#                 for person in sched["people"]:
#                     final_msg += f'{person} , ' if person != sched["people"][-1] else person
#                 final_msg += '\nInstrumentista(s): Sonoplastia'
#                 final_msg += f'\nSonoplasta(s): {" e ".join(sched["sonoplaste"])}'
#                 final_msg += '\n\n'
#                 if sched["weekday"] == 'sabado':
#                     final_msg += '\n\n'
        
#         try:
#             used_people = set()  # Para rastrear pessoas já escaladas
            
#             if dados["separar_genero"]:
#                 # Separando homens e mulheres
#                 men = [p for p in list_dict_person if p['gender'] == 'm' and p['vocalist']]
#                 women = [p for p in list_dict_person if p['gender'] == 'f' and p['vocalist']]
                
#                 #iterea sobre os dias uteis
#                 for day in days_event:
#                     day_people = []
#                     people_need = day['people_need']
#                     month_day = day['month_day']
#                     weekday = day['weekday']
                    
#                     # Priorizar pessoas com preferências para o dia
#                     preferred_men = [p for p in men if weekday in p['preference_day'] and p['name'] not in used_people]
#                     preferred_women = [p for p in women if weekday in p['preference_day'] and p['name'] not in used_people]
                    
#                     # Filtra as pessoas que podem ser escaladas para esse dia
#                     available_men = [p for p in men if weekday not in p['except_day'] and p['name'] not in used_people and p not in preferred_men]
#                     available_women = [p for p in women if weekday not in p['except_day'] and p['name'] not in used_people and p not in preferred_women]
                    
#                     # Alternar entre homem e mulher
#                     while len(day_people) < people_need:
#                         if len(day_people) % 2 == 0:  # Se a posição for par, colocar homem
#                             if preferred_men:
#                                 person = preferred_men.pop(random.randint(0,len(preferred_men) - 1))
#                                 day_people.append(person['name'])
#                                 used_people.add(person['name'])
#                             elif available_men:
#                                 person = available_men.pop(random.randint(0,len(available_men) - 1))
#                                 day_people.append(person['name'])
#                                 used_people.add(person['name'])
#                             else:
#                                 person = random.choice(men)
#                                 if weekday in person['except_day'] : continue
#                                 day_people.append(person['name'])
#                                 used_people.add(person['name'])
#                         else:  # Se a posição for ímpar, colocar mulher
#                             if preferred_women:
#                                 person = preferred_women.pop(random.randint(0,len(preferred_women) - 1))
#                                 day_people.append(person['name'])
#                                 used_people.add(person['name'])
#                             elif available_women:
#                                 person = available_women.pop(random.randint(0,len(available_women) - 1))
#                                 day_people.append(person['name'])
#                                 used_people.add(person['name'])
#                             else:
#                                 person = random.choice(women)
#                                 if person['except_day'] == weekday: continue
#                                 day_people.append(person['name'])
#                                 used_people.add(person['name'])
                                
#                     # Atribuindo as pessoas ao dia
#                     schedule.append({
#                         "year" : year_event,
#                         'month' : month_event,
#                         "month_day" : month_day,
#                         "weekday" : int_day[weekday],
#                         "people_need" : people_need,
#                         "people" : day_people,
#                         "sonoplaste" : dados["escale_sonoplaste"].get(month_day, ["Equipe de sonoplastia"]),
#                     })
                
#             else:
#                 #iterea sobre os dias uteis
#                 for day in days_event:
#                     day_people = []
#                     people_need = day['people_need']
#                     month_day = day['month_day']
#                     weekday = day['weekday']
                    
#                     # Filtra as pessoas que podem ser escaladas para esse dia
#                     available_person = [p for p in list_dict_person if p['name'] not in used_people]
                    
#                     # Alternar entre homem e mulher
#                     while len(day_people) < people_need:
#                         if available_person:
#                             person = available_person.pop(random.randint(0,len(available_person) - 1))
#                             day_people.append(person['name'])
#                             used_people.add(person['name'])
#                         else:
#                             person = random.choice(list_dict_person)
#                             day_people.append(person['name'])
#                             used_people.add(person['name'])
                                
#                     # Atribuindo as pessoas ao dia
#                     schedule.append({
#                         "year" : year_event,
#                         'month' : month_event,
#                         "month_day" : month_day,
#                         "weekday" : int_day[weekday],
#                         "people_need" : people_need,
#                         "people" : day_people,
#                         "sonoplaste" : dados["escale_sonoplaste"][month_day],
#                     })
            
#             if not schedule:
#                 print('Lista de dicionarios dos dias da escala ficaram vazios!')
#                 return False
#             else:
#                 create_message()
#                 return True
        
#         except Exception as er:
#             #log('debug','create_table()',f'Erro: {er}')
#             print(f'Erro: {er}')
#             return False
    
#     async def create_html():
#         '''cria o html com jinja2'''

#         # Carrega o template 'index.html' que estará na pasta templates
#         nonlocal dados, schedule, funcoes, final_msg
#         template = env.get_template('index_music.html')
            
#         # Dados que você deseja passar para o template
#         dados = {
#             'titulo': 'Exemplo Escala',
#             'nome': 'João',
#             'mes': months[month_event],
#             'ano': year_event,
#             'idade': 25,
#             'dias_uteis': schedule,
#             'funcoes' : funcoes,
#             'msg': final_msg.replace('\n','</br>')
#         }

#         # Renderiza o template com os dados passados e exibe o HTML
#         html_renderizado = template.render(dados)

#         return html_renderizado
    
#     print(f'criando tabela de musica')
#     await create_table_music()
#     if schedule:
#         print(f'criada tabela')
#         document_html = await create_html()
#         print('Tabela com escala criada com sucesso!')
#         return {"success": True, "html_content": document_html}
    
        
#     return {"success": False, "html_content": ""}


if __name__ == '__main__':
    pass
    uvicorn.run(app, host="0.0.0.0", port=4000)