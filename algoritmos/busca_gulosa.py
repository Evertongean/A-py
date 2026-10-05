import heapq
from time import perf_counter

from algoritmos.heuristicas import calcular_heuristica
from algoritmos.movimentos import (
    calcular_custo_movimento,
    corta_canto_de_parede,
    obter_direcoes,
)
from modelos.no import No
from modelos.passo_busca import PassoBusca
from modelos.resultado_busca import ResultadoBusca
from modelos.tipos import TipoHeuristica, TipoMovimento, TipoPassoBusca


class BuscaGulosa:
    """Busca o objetivo priorizando somente a menor heurística H."""

    def buscar(
        self,
        paredes: list[list[bool]],
        inicio: tuple[int, int],
        objetivo: tuple[int, int],
        tipo_heuristica: TipoHeuristica = TipoHeuristica.MANHATTAN,
        tipo_movimento: TipoMovimento = TipoMovimento.QUATRO_DIRECOES,
    ) -> ResultadoBusca:
        inicio_tempo = perf_counter()
        quantidade_linhas = len(paredes)
        quantidade_colunas = len(paredes[0])

        melhores_custos_g = self._criar_matriz(
            quantidade_linhas,
            quantidade_colunas,
            float("inf"),
        )
        fechados = self._criar_matriz(
            quantidade_linhas,
            quantidade_colunas,
            False,
        )

        linha_inicio, coluna_inicio = inicio
        linha_objetivo, coluna_objetivo = objetivo
        heuristica_inicial = calcular_heuristica(
            tipo_heuristica,
            linha_inicio,
            coluna_inicio,
            linha_objetivo,
            coluna_objetivo,
        )
        no_inicial = No(
            linha=linha_inicio,
            coluna=coluna_inicio,
            custo_g=0,
            heuristica_h=heuristica_inicial,
            pai=None,
        )

        melhores_custos_g[linha_inicio][coluna_inicio] = 0
        lista_aberta = []
        passos = []
        contador = 0

        # Na Busca Gulosa, H é o primeiro e único custo de prioridade.
        heapq.heappush(
            lista_aberta,
            (
                no_inicial.heuristica_h,
                contador,
                no_inicial,
            ),
        )
        passos.append(self._criar_passo(no_inicial, TipoPassoBusca.ABERTO))

        nos_visitados = []
        direcoes = obter_direcoes(tipo_movimento)

        while lista_aberta:
            _, _, no_atual = heapq.heappop(lista_aberta)
            linha_atual = no_atual.linha
            coluna_atual = no_atual.coluna

            # Uma rota melhor pode deixar uma entrada antiga dentro do heap.
            if fechados[linha_atual][coluna_atual]:
                continue

            melhor_custo = melhores_custos_g[linha_atual][coluna_atual]
            if no_atual.custo_g > melhor_custo:
                continue

            fechados[linha_atual][coluna_atual] = True
            nos_visitados.append(no_atual)
            passos.append(self._criar_passo(no_atual, TipoPassoBusca.FECHADO))

            if (linha_atual, coluna_atual) == objetivo:
                caminho = reconstruir_caminho(no_atual)
                fim_tempo = perf_counter()

                return ResultadoBusca(
                    encontrou=True,
                    caminho=caminho,
                    nos_visitados=nos_visitados,
                    custo_total=no_atual.custo_g,
                    passos=passos,
                    tempo_execucao=fim_tempo - inicio_tempo,
                )

            for deslocamento_linha, deslocamento_coluna in direcoes:
                nova_linha = linha_atual + deslocamento_linha
                nova_coluna = coluna_atual + deslocamento_coluna

                if not self._esta_dentro_da_grade(
                    nova_linha,
                    nova_coluna,
                    quantidade_linhas,
                    quantidade_colunas,
                ):
                    continue

                if paredes[nova_linha][nova_coluna]:
                    continue

                if corta_canto_de_parede(
                    paredes,
                    linha_atual,
                    coluna_atual,
                    deslocamento_linha,
                    deslocamento_coluna,
                ):
                    continue

                if fechados[nova_linha][nova_coluna]:
                    continue

                custo_movimento = calcular_custo_movimento(
                    deslocamento_linha,
                    deslocamento_coluna,
                )
                novo_custo_g = no_atual.custo_g + custo_movimento
                custo_g_conhecido = melhores_custos_g[nova_linha][nova_coluna]

                if novo_custo_g < custo_g_conhecido:
                    melhores_custos_g[nova_linha][nova_coluna] = novo_custo_g
                    heuristica_h = calcular_heuristica(
                        tipo_heuristica,
                        nova_linha,
                        nova_coluna,
                        linha_objetivo,
                        coluna_objetivo,
                    )
                    novo_no = No(
                        linha=nova_linha,
                        coluna=nova_coluna,
                        custo_g=novo_custo_g,
                        heuristica_h=heuristica_h,
                        pai=no_atual,
                    )

                    contador += 1
                    heapq.heappush(
                        lista_aberta,
                        (
                            novo_no.heuristica_h,
                            contador,
                            novo_no,
                        ),
                    )
                    passos.append(
                        self._criar_passo(novo_no, TipoPassoBusca.ABERTO)
                    )

        fim_tempo = perf_counter()
        return ResultadoBusca(
            encontrou=False,
            caminho=[],
            nos_visitados=nos_visitados,
            custo_total=float("inf"),
            passos=passos,
            tempo_execucao=fim_tempo - inicio_tempo,
        )

    def _criar_passo(self, no: No, tipo: TipoPassoBusca) -> PassoBusca:
        pai_linha = None
        pai_coluna = None

        if no.pai is not None:
            pai_linha = no.pai.linha
            pai_coluna = no.pai.coluna

        return PassoBusca(
            linha=no.linha,
            coluna=no.coluna,
            custo_g=no.custo_g,
            heuristica_h=no.heuristica_h,
            custo_f=no.custo_f,
            tipo=tipo,
            pai_linha=pai_linha,
            pai_coluna=pai_coluna,
        )

    def _criar_matriz(
        self,
        quantidade_linhas: int,
        quantidade_colunas: int,
        valor_inicial: float | bool,
    ) -> list[list[float | bool]]:
        matriz = []

        for _ in range(quantidade_linhas):
            linha = []

            for _ in range(quantidade_colunas):
                linha.append(valor_inicial)

            matriz.append(linha)

        return matriz

    def _esta_dentro_da_grade(
        self,
        linha: int,
        coluna: int,
        quantidade_linhas: int,
        quantidade_colunas: int,
    ) -> bool:
        linha_valida = 0 <= linha < quantidade_linhas
        coluna_valida = 0 <= coluna < quantidade_colunas

        return linha_valida and coluna_valida


def reconstruir_caminho(no_objetivo: No) -> list[No]:
    """Segue os pais desde Jerry e devolve o caminho iniciado em Tom."""
    caminho = []
    atual = no_objetivo

    while atual is not None:
        caminho.append(atual)
        atual = atual.pai

    caminho.reverse()
    return caminho
