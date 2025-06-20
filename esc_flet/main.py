import flet as ft
import random
import calendar
import os, subprocess, sys, re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from log import log
import json

'''VARIAVEIS GLOBAIS'''
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

list_dict_person = []
lista_jsons_person = []
days_event = []
schedule = []
funcoes = {
    "instrumentistas" : [],
    "mensagem_musical" : []
}
final_msg = ''
separar_genero = False
DADOS = None


def main(page: ft.Page):
    global device, separar_genero
    page.title = "test"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = '#dee2e5'
    page_width = page.window_width
    page_heigth = page.height

    
    def on_resize(e = None):
        page_width = page.window_width
        page_heigth = page.height
        
        global device
        if page_width <= 480:
            device = 'mobile'
            container_inserir.height = 300
            container_inserir.content.controls[2] = ft.Column(
                controls=[
                    btn_add_pendencias,
                    btn_add_carrinho,
                ],
                spacing=10,
            )
            btn_add_pendencias.width = 900
            btn_add_carrinho.width = 900
            column_main.height = page_heigth - 100
        
        else:
            device = 'desktop'
            container_inserir.height = 200
            btn_add_pendencias.width = 150
            column_main.height = page_heigth - 100
            
        print(f'Tamanho da tela {page_width}')
        print(f'DEVICE: {device}')
        page.update()
    
    
    def load_list_people(e = None):
        for arq in os.listdir():
            if 'person.json' in arq:
                dropdown_listas.options.append(ft.dropdown.Option(arq))
                lista_jsons_person.append(arq)
                
        page.update()
    
    
    def gerar_escala(e = None):
        # Obter os dias do mês atual (retorna uma tupla (dia da semana que o mes começa , numero de dias))
        ano_ref = inp_ano_escala.value if inp_ano_escala.value else datetime.now().year
        mes_ref = inp_mes_escala.value if inp_mes_escala.value else datetime.now().month
        month_days = calendar.monthrange(ano_ref, mes_ref)[1]
        list_days_require = []
        
        for day in month_days:
            pass
    
    
    '''BTNS'''
    btn_add_pendencias = ft.ElevatedButton(text="Produto Pendente", data="pendencia", icon="ADD_SHARP", height=50, style=ft.ButtonStyle(color="#f0fbf3", bgcolor="#0ea5e9", shape=ft.RoundedRectangleBorder(radius=10)))
    btn_add_carrinho = ft.ElevatedButton(text="Produto Comprado", data="comprado", icon="ADD_SHOPPING_CART", height=50, style=ft.ButtonStyle(color="#f0fbf3", bgcolor="#10b981", shape=ft.RoundedRectangleBorder(radius=10)))
    
    '''FORM_ADD'''
    list_number = [ft.dropdown.Option(i, text_style=ft.TextStyle(size=12)) for i in range(0, 11)]
    inp_ano_escala = ft.Dropdown(
        label="Número do ano em que será escalado",
        color="#000000",
        bgcolor="#ffffff",
        height=40,
        label_style=ft.TextStyle(color="#717171"),
        options=[ft.dropdown.Option(i, text_style=ft.TextStyle(size=12)) for i in range(2020, 2051)],
        value=datetime.now().year
    )
    inp_mes_escala = ft.Dropdown(
        label="Número do mês em que será escalado",
        color="#000000",
        bgcolor="#ffffff",
        height=40,
        label_style=ft.TextStyle(color="#717171"),
        options=[ft.dropdown.Option(i, text_style=ft.TextStyle(size=12)) for i in range(1, 13)],
        value=datetime.now().month
    )
    
    inp_qtd_domingo = ft.Dropdown(
        label="Quantidade de pessoas para o domingo",
        color="#000000",
        bgcolor="#ffffff",
        height=40,
        label_style=ft.TextStyle(color="#717171"),
        options=list_number,
        value=0,
    )
    inp_qtd_segunda = ft.Dropdown(
        label="Quantidade de pessoas para a segunda-feira",
        color="#000000",
        bgcolor="#ffffff",
        height=40,
        label_style=ft.TextStyle(color="#717171"),
        options=list_number,
        value=0,
    )

    inp_qtd_terca = ft.Dropdown(
        label="Quantidade de pessoas para a terça-feira",
        color="#000000",
        bgcolor="#ffffff",
        height=40,
        label_style=ft.TextStyle(color="#717171"),
        options=list_number,
        value=0,
    )

    inp_qtd_quarta = ft.Dropdown(
        label="Quantidade de pessoas para a quarta-feira",
        color="#000000",
        bgcolor="#ffffff",
        height=40,
        label_style=ft.TextStyle(color="#717171"),
        options=list_number,
        value=0,
    )

    inp_qtd_quinta = ft.Dropdown(
        label="Quantidade de pessoas para a quinta-feira",
        color="#000000",
        bgcolor="#ffffff",
        height=40,
        label_style=ft.TextStyle(color="#717171"),
        options=list_number,
        value=0,
    )

    inp_qtd_sexta = ft.Dropdown(
        label="Quantidade de pessoas para a sexta-feira",
        color="#000000",
        bgcolor="#ffffff",
        height=40,
        label_style=ft.TextStyle(color="#717171"),
        options=list_number,
        value=0,
    )

    inp_qtd_sabado = ft.Dropdown(
        label="Quantidade de pessoas para o sábado",
        color="#000000",
        bgcolor="#ffffff",
        height=40,
        label_style=ft.TextStyle(color="#717171"),
        options=list_number,
        value=0,
    )
    
    
    switch_separar_genero = ft.Switch(label="Alternar gêneros", value=False)
    btn_gerar_esc = ft.ElevatedButton(text="GERAR\nESCALA", icon="CREATE", height=50, style=ft.ButtonStyle(color="#556071", bgcolor="#ffffff", shape=ft.RoundedRectangleBorder(radius=10)), on_click=gerar_escala)
    
    
    dropdown_listas = ft.Dropdown(label="Selecione a lista de pessoas", options=[])
    load_list_people()
    inp_nome_person = ft.TextField(label="Nome", hint_text="João Maria José", height=50)
    switch_instrumentist = ft.Switch(label="Instrumentista", value=False)
    inp_type_instrument = ft.TextField(label="Instrumento", hint_text="Violão / Piano / Guitarra...", height=50)
    switch_vocalist = ft.Switch(label="Vocalista", value=False)
    inp_type_vocal = ft.TextField(label="Tipo de voz", hint_text="Tenor / Barítono / Soprano...", height=50)
    switch_msg_musical = ft.Switch(label="Faz mensagem musical", value=False)
    switch_ativo = ft.Switch(label="Ativo", value=True)
    switch_person_gender = ft.Switch(label="", value=False)
    btn_add_person = ft.ElevatedButton(text="ADICIONAR", icon="PLAYLIST_ADD_SHARP", height=50, style=ft.ButtonStyle(color="#556071", bgcolor="#ffffff", shape=ft.RoundedRectangleBorder(radius=10)))
    form_add_people = ft.Column(
        controls=[
            inp_nome_person, 
            switch_instrumentist, 
            inp_type_instrument, 
            switch_vocalist, 
            inp_type_vocal, 
            switch_msg_musical, 
            ft.Row(
                controls=[
                    ft.Text("Masculino"),
                    switch_person_gender,
                    ft.Text("Feminino"),
                ]
            ), 
            switch_ativo,
            btn_add_person
        ],
        spacing=20
    )
    
    box_data = ft.Column()

    container_form = ft.Container(
        bgcolor="#1e293b",
        border_radius=0,
        padding=20,
        height=100,
        width=700,
        shadow=ft.BoxShadow(blur_radius=5, color="#CCCCCC", offset=ft.Offset(0,15)),
        content=ft.Column(
            controls=[
                dropdown_listas,
                ft.Text("Formulário de adição",color="#1F1F1F"),
                ft.Text("Será adicionado na lista selecionada acima",color="#727272"),
                form_add_people,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    
    container_data_gerar = ft.Container(
        bgcolor="#ffffff",
        border_radius=10,
        padding=20,
        width=700,
        shadow=ft.BoxShadow(blur_radius=5, color="#CCCCCC", offset=ft.Offset(0,15)),
        content=ft.Column(
            controls=[
                inp_ano_escala,
                inp_mes_escala,
                inp_qtd_domingo,
                inp_qtd_segunda,
                inp_qtd_terca,
                inp_qtd_quarta,
                inp_qtd_quinta,
                inp_qtd_sexta,
                inp_qtd_sabado,
                switch_separar_genero,
                btn_gerar_esc,
            ],
            spacing=10,
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    
    container_exibir = ft.Container(
        bgcolor="#ffffff",
        border_radius=10,
        padding=20,
        height=250,
        width=700,
        shadow=ft.BoxShadow(blur_radius=5, color="#CCCCCC", offset=ft.Offset(0,15)),
        content=box_data
    )
    
    column_main = ft.Column(
        controls=[
            container_form,
            container_data_gerar,
            container_exibir
        ],
        spacing=20,
        scroll=ft.ScrollMode.ALWAYS
    )
    
    page.add(column_main)
    if page_width <= 480:
        global device ; device = 'mobile'
        on_resize()
    page.on_resize = on_resize


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


# async def gerar_escala():
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
#                 final_msg += '\nSonoplasta(s): Gabriel e Pâmela'
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
#                         "month_day" : month_day,
#                         "weekday" : int_day[weekday],
#                         "people_need" : people_need,
#                         "people" : day_people
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
#                         "year" : day["year"],
#                         'month' : day["month"],
#                         "month_day" : month_day,
#                         "weekday" : int_day[weekday],
#                         "people_need" : people_need,
#                         "people" : day_people
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
    
#     async def create_table():
#         nonlocal schedule, final_msg
#         '''
#         Monta a escala de acordo com as regras:
#         Alternância de Gêneros: Coloca homens e mulheres alternadamente na escala.
#         Preferências: Prioriza as pessoas que têm preferências para o dia.
#         Restrições: Verifica se a pessoa está disponível para o dia (não tem restrição).
#         Escala Completa: Preenche o número necessário de pessoas por dia, respeitando as regras de gênero, preferências e restrições.
#         Gera o arquivo JSON (final_date.json) com a tabela final de escalas.
#         '''
#         try:
#             used_people = set()  # Para rastrear pessoas já escaladas

#             if dados["separar_genero"]:
#                 # Separando homens e mulheres
#                 men = [p for p in list_dict_person if p['gender'] == 'm']
#                 women = [p for p in list_dict_person if p['gender'] == 'f']
                
#                 #iterea sobre os dias uteis
#                 for day in days_event:
#                     day_people = []
#                     people_need = day['people_need']
#                     month_day = day['month_day']
#                     weekday = day['weekday']
                    
#                     # Filtra as pessoas que podem ser escaladas para esse dia
#                     available_men = [p for p in men if p['name'] not in used_people]
#                     available_women = [p for p in women if p['name'] not in used_people]
                    
#                     # Alternar entre homem e mulher
#                     while len(day_people) < people_need:
#                         if len(day_people) % 2 == 0:  # Se a posição for par, colocar homem
#                             if available_men:
#                                 person = available_men.pop(random.randint(0,len(available_men) - 1))
#                                 day_people.append(person['name'])
#                                 used_people.add(person['name'])
#                             else:
#                                 person = random.choice(men)
#                                 if weekday in person['except_day'] : continue
#                                 day_people.append(person['name'])
#                                 used_people.add(person['name'])
#                         else:  # Se a posição for ímpar, colocar mulher
#                             if available_women:
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
#                         "year" : day["year"],
#                         'month' : day["month"],
#                         "month_day" : month_day,
#                         "weekday" : int_day[weekday],
#                         "people_need" : people_need,
#                         "people" : day_people
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
#                         "year" : day["year"],
#                         'month' : day["month"],
#                         "month_day" : month_day,
#                         "weekday" : int_day[weekday],
#                         "people_need" : people_need,
#                         "people" : day_people
#                     })
            
#             if not schedule:
#                 print('Lista de dicionarios dos dias da escala ficaram vazios!')
#                 return False
#             else:
#                 return True
        
#         except Exception as er:
#             #log('debug','create_table()',f'Erro: {er}')
#             print(f'Erro: {er}')
#             return False
     
#     async def create_html():
#         '''cria o html com jinja2'''

#         # Carrega o template 'index.html' que estará na pasta templates
#         nonlocal dados, schedule, funcoes, final_msg
#         if dados["table"] == "default":
#             template = env.get_template('index.html')
#         else:
#             template = env.get_template('index_music.html')
            
#         hoje = datetime.now()
#         ano = hoje.year if year_event == '' else int(year_event)
#         mes = hoje.month if month_event == '' else int(month_event)

#         # Dados que você deseja passar para o template
#         dados = {
#             'titulo': 'Exemplo Escala',
#             'nome': 'João',
#             'mes': months[mes],
#             'ano': ano,
#             'idade': 25,
#             'dias_uteis': schedule,
#             'funcoes' : funcoes,
#             'msg': final_msg.replace('\n','</br>')
#         }

#         # Renderiza o template com os dados passados e exibe o HTML
#         html_renderizado = template.render(dados)

#         return html_renderizado
    
#     if dados["table"] == "default":
#         print(f'criando tabela')
#         await create_table()
#         if schedule:
#             print(f'criada tabela')
#             document_html = await create_html()
#             print('Tabela com escala criada com sucesso!')
#             return HTMLResponse(content=document_html, status_code=200)
    
#     else:
#         print(f'criando tabela de musica')
#         await create_table_music()
#         if schedule:
#             print(f'criada tabela de musica')
#             document_html = await create_html()
#             print('Tabela com escala criada com sucesso!')
#             return HTMLResponse(content=document_html, status_code=200)
        
#     return "erro"


if __name__ == "__main__":
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    ft.app(target=main)
