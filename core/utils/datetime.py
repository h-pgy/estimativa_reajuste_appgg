from datetime import datetime
import calendar

def meses_passados(data_atual:datetime, data_anterior:datetime)->int:

    anos_passados = data_atual.year - data_anterior.year
    meses_passados = data_atual.month - data_anterior.month

    meses_ajustado = anos_passados * 12 + meses_passados

    #ajustar para o dia caso não tenha completado o mês
    if data_atual.day < data_anterior.day:
        meses_ajustado -= 1
    
    return meses_ajustado

def adicionar_meses(data_original: datetime, n_meses: int) -> datetime:
    # Calcula o total de meses acumulados a partir do mês 0 (Janeiro)
    # Subtraímos 1 do month para trabalhar no intervalo 0-11
    total_months = (data_original.year * 12 + (data_original.month - 1)) + n_meses
    
    new_year = total_months // 12
    new_month = (total_months % 12) + 1
    
    # Obtém o último dia do mês de destino para tratar meses curtos e bissextos
    _, last_day_of_new_month = calendar.monthrange(new_year, new_month)
    
    # Garante que o dia não ultrapasse o limite do novo mês
    new_day = min(data_original.day, last_day_of_new_month)
    
    return data_original.replace(year=new_year, month=new_month, day=new_day)