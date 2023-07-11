from datetime import date, timedelta


def get_referencia_atual():
    data_hoje = date.today()
    if data_hoje.day >= 26:
        referencia_atual = data_hoje.replace(day=26)
    else:
        ultimo_dia_mes_passado = data_hoje.replace(day=1) - timedelta(days=1)
        referencia_atual = ultimo_dia_mes_passado.replace(day=26)
    return referencia_atual

def get_referencia_passada():
    referencia_atual = get_referencia_atual()
    if referencia_atual.month == 1:
        referencia_passada = referencia_atual.replace(month=12, year=referencia_atual.year - 1)
    else:
        referencia_passada = referencia_atual.replace(month=referencia_atual.month - 1)
    return referencia_passada