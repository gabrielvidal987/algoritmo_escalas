from datetime import datetime
import calendar
import json


def ordinary_position_day_on_month(weekday: int, arg_date: datetime) -> int:
    """
    Retorna a posição ordinal de um dia da semana no mês.
    Exemplo: 2 significa 'segunda {data}' do mês ou 'segunda quarta-feira' do mês caso a data passada seja uma quarta feira.
    """
    contador = 0

    for dia in range(1, arg_date.day + 1):
        if datetime(arg_date.year, arg_date.month, dia).weekday() == weekday:
            contador += 1

    return contador


year = datetime.now().year
month = datetime.now().month

# Obter os dias do mês atual (retorna uma tupla (dia da semana que o mes começa , numero de dias no mês))
first_weekday_month, month_days = calendar.monthrange(year, month)

dias = {}
for day in range(1,month_days + 1):
    weekday = datetime(year, month, day).weekday()  # 0=segunda, 1=terça, ..., 6=domingo
    # No dicionario dias fica o numero do dia como chave e seu valor é uma tupla (weekday, posição ordinal de um dia da semana no mês) -> exemplo: [5] = (5, 1) dia 5 é o primeiro sabado
    dias[day] = (weekday, )