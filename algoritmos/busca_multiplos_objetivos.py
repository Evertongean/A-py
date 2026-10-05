from algoritmos.a_estrela import AEstrela
from algoritmos.busca_gulosa import BuscaGulosa
from algoritmos.heuristicas import calcular_heuristica
from modelos.no import No
from modelos.resultado_busca import ResultadoBusca
from modelos.resultado_multiplos_objetivos import ResultadoMultiplosObjetivos
from modelos.tipos import TipoAlgoritmo, TipoHeuristica, TipoMovimento


class BuscaMultiplosObjetivos:
    """Coordena buscas sucessivas até visitar todos os objetivos possíveis."""

    def __init__(self):
        self.a_estrela = AEstrela()
        self.busca_gulosa = BuscaGulosa()

    def buscar(
        self,
        paredes: list[list[bool]],
        inicio: tuple[int, int],
        objetivos: list[tuple[int, int]],
        tipo_algoritmo: TipoAlgoritmo,
        tipo_heuristica: TipoHeuristica,
        tipo_movimento: TipoMovimento,
    ) -> ResultadoMultiplosObjetivos:
        if not objetivos:
            raise ValueError("Informe pelo menos um objetivo para a busca.")

        posicao_atual = inicio
        objetivos_restantes = objetivos[:]
        resultados_parciais = []
        caminho_completo = []
        ordem_objetivos = []
        custo_total = 0
        nos_explorados_total = 0
        tempo_execucao_total = 0

        while objetivos_restantes:
            objetivos_ordenados = self._ordenar_objetivos(
                posicao_atual,
                objetivos_restantes,
                tipo_heuristica,
            )
            resultado_encontrado = None
            objetivo_escolhido = None

            for objetivo in objetivos_ordenados:
                resultado = self._executar_busca(
                    paredes,
                    posicao_atual,
                    objetivo,
                    tipo_algoritmo,
                    tipo_heuristica,
                    tipo_movimento,
                )
                resultados_parciais.append(resultado)
                # Tentativas sem caminho também representam trabalho real.
                nos_explorados_total += len(resultado.nos_visitados)
                tempo_execucao_total += resultado.tempo_execucao

                if resultado.encontrou:
                    resultado_encontrado = resultado
                    objetivo_escolhido = objetivo
                    break

            if resultado_encontrado is None:
                return ResultadoMultiplosObjetivos(
                    encontrou_todos=False,
                    caminho_completo=caminho_completo,
                    resultados_parciais=resultados_parciais,
                    custo_total=custo_total,
                    nos_explorados_total=nos_explorados_total,
                    tempo_execucao_total=tempo_execucao_total,
                    ordem_objetivos=ordem_objetivos,
                )

            custo_total += resultado_encontrado.custo_total
            self._adicionar_caminho_sem_repetir_origem(
                caminho_completo,
                resultado_encontrado.caminho,
            )
            ordem_objetivos.append(objetivo_escolhido)
            posicao_atual = objetivo_escolhido
            objetivos_restantes.remove(objetivo_escolhido)

        return ResultadoMultiplosObjetivos(
            encontrou_todos=True,
            caminho_completo=caminho_completo,
            resultados_parciais=resultados_parciais,
            custo_total=custo_total,
            nos_explorados_total=nos_explorados_total,
            tempo_execucao_total=tempo_execucao_total,
            ordem_objetivos=ordem_objetivos,
        )

    def _ordenar_objetivos(
        self,
        posicao_atual: tuple[int, int],
        objetivos_restantes: list[tuple[int, int]],
        tipo_heuristica: TipoHeuristica,
    ) -> list[tuple[int, int]]:
        linha_atual, coluna_atual = posicao_atual

        def obter_estimativa(objetivo):
            linha_objetivo, coluna_objetivo = objetivo
            return calcular_heuristica(
                tipo_heuristica,
                linha_atual,
                coluna_atual,
                linha_objetivo,
                coluna_objetivo,
            )

        return sorted(objetivos_restantes, key=obter_estimativa)

    def _executar_busca(
        self,
        paredes: list[list[bool]],
        inicio: tuple[int, int],
        objetivo: tuple[int, int],
        tipo_algoritmo: TipoAlgoritmo,
        tipo_heuristica: TipoHeuristica,
        tipo_movimento: TipoMovimento,
    ) -> ResultadoBusca:
        if tipo_algoritmo == TipoAlgoritmo.BUSCA_GULOSA:
            algoritmo = self.busca_gulosa
        else:
            algoritmo = self.a_estrela

        return algoritmo.buscar(
            paredes,
            inicio,
            objetivo,
            tipo_heuristica,
            tipo_movimento,
        )

    def _adicionar_caminho_sem_repetir_origem(
        self,
        caminho_completo: list[No],
        novo_caminho: list[No],
    ):
        if not caminho_completo:
            caminho_completo.extend(novo_caminho)
            return

        caminho_completo.extend(novo_caminho[1:])
