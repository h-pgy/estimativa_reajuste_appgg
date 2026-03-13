from .vencimento_atual import Vencimento
from .ferias_decimo_terceiro import DecimoTerceiro, TercoAdicionalFerias
from .vale_alimentacao import ValeAlimentacao
from .previdencia import ContribuicaoIprem, ContribuicaoINSS, PrevidenciaComplementar

obter_vencimento = Vencimento()
calc_decimo_terceiro = DecimoTerceiro()
calc_terco_adicional = TercoAdicionalFerias()
calc_vale_alimentacao = ValeAlimentacao()
calc_contrib_iprem = ContribuicaoIprem()
calc_contrib_inss = ContribuicaoINSS()
calc_prev_complementar = PrevidenciaComplementar()