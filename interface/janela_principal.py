import tkinter as tk
from tkinter import messagebox, ttk

from algoritmos.a_estrela import AEstrela
from algoritmos.busca_gulosa import BuscaGulosa
from algoritmos.busca_multiplos_objetivos import BuscaMultiplosObjetivos
from interface.controle_velocidade import converter_nivel_em_atraso
from interface.grade import Grade
from interface.janela_comparacao import JanelaComparacao
from labirintos.fabrica_labirintos import FabricaLabirintos
from modelos.passo_busca import PassoBusca
from modelos.tipos import (
    ModoEdicao,
    TipoAlgoritmo,
    TipoHeuristica,
    TipoLabirinto,
    TipoMovimento,
    TipoPassoBusca,
)


class JanelaPrincipal(tk.Tk):
    """Janela principal e painel de controles do editor."""

    COR_FUNDO = "#111827"
    COR_PAINEL = "#1f2937"
    COR_DESTAQUE = "#f59e0b"
    COR_TEXTO = "#f9fafb"
    NOME_A_ESTRELA = "A*"
    NOME_BUSCA_GULOSA = "Busca Gulosa"
    NOME_MANHATTAN = "Manhattan"
    NOME_EUCLIDIANA = "Euclidiana"
    NOME_DIAGONAL = "Diagonal"
    NOME_QUATRO_DIRECOES = "4 direções"
    NOME_OITO_DIRECOES = "8 direções"
    NOME_MANUAL = "Manual"
    NOME_COZINHA = "Cozinha"
    NOME_SALA = "Sala"
    NOME_PORAO = "Porão"
    NOME_UM_OBJETIVO = "Um objetivo"
    NOME_MULTIPLOS_OBJETIVOS = "Múltiplos objetivos"

    def __init__(self):
        super().__init__()

        self.title("Tom & Jerry - Visualizador de Busca")
        self.geometry("1366x768")
        self.minsize(1180, 700)
        self.configure(background=self.COR_FUNDO)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.a_estrela = AEstrela()
        self.busca_gulosa = BuscaGulosa()
        self.busca_multiplos_objetivos = BuscaMultiplosObjetivos()
        self.tipo_algoritmo_atual = TipoAlgoritmo.A_ESTRELA
        self.tipo_heuristica_atual = TipoHeuristica.MANHATTAN
        self.tipo_movimento_atual = TipoMovimento.QUATRO_DIRECOES
        self.labirinto_atual = TipoLabirinto.MANUAL
        self.resultado_atual = None
        self.resultado_multiplos_atual = None
        self.indice_passo_atual = 0
        self.indice_caminho_atual = 1
        self.indice_resultado_parcial = 0
        self.indice_objetivo_alcancado = 0
        self.quantidade_objetivos_total = 0
        self.custo_acumulado_visual = 0
        self.tempo_acumulado_visual = 0
        self.modo_multiplos_em_execucao = False
        self.busca_em_reproducao = False
        self.busca_pausada = False
        self.id_agendamento = None
        self.atraso_animacao = 250
        self.quantidade_fechados_visual = 0

        self.texto_modo_atual = tk.StringVar(value="Modo atual: Parede")
        self.algoritmo_selecionado = tk.StringVar(value=self.NOME_A_ESTRELA)
        self.heuristica_selecionada = tk.StringVar(value=self.NOME_MANHATTAN)
        self.movimento_selecionado = tk.StringVar(
            value=self.NOME_QUATRO_DIRECOES
        )
        self.labirinto_selecionado = tk.StringVar(value=self.NOME_MANUAL)
        self.modo_objetivo_selecionado = tk.StringVar(
            value=self.NOME_UM_OBJETIVO
        )
        self.texto_labirinto_atual = tk.StringVar(
            value="Cenário atual: Manual"
        )
        self.texto_descricao_labirinto = tk.StringVar(
            value=FabricaLabirintos.obter_descricao(TipoLabirinto.MANUAL)
        )
        self.texto_algoritmo = tk.StringVar(value="Algoritmo: A*")
        self.texto_heuristica = tk.StringVar(value="Heurística: Manhattan")
        self.texto_movimento = tk.StringVar(value="Movimento: 4 direções")
        self.texto_criterio = tk.StringVar(value="Critério: menor F")
        self.texto_explicacao_algoritmo = tk.StringVar(
            value=self._obter_explicacao_algoritmo(TipoAlgoritmo.A_ESTRELA)
        )
        self.texto_explicacao_heuristica = tk.StringVar(
            value=self._obter_explicacao_heuristica(
                TipoHeuristica.MANHATTAN
            )
        )
        self.texto_observacao = tk.StringVar(value="")
        self.texto_status = tk.StringVar(value="Status: Pronto.")
        self.texto_quantidade_objetivos = tk.StringVar(
            value="Objetivos no mapa: 0"
        )
        self.texto_objetivos_alcancados = tk.StringVar(
            value="Objetivos alcançados: -"
        )
        self.texto_nos_explorados = tk.StringVar(value="Nós explorados: 0")
        self.texto_custo_total = tk.StringVar(value="Custo total: -")
        self.texto_tempo_execucao = tk.StringVar(value="Tempo de execução: -")
        self.texto_no_atual = tk.StringVar(value=self._texto_no_vazio())
        self.texto_ordem_objetivos = tk.StringVar(value="Ordem visitada: -")
        self.valor_velocidade = tk.IntVar(value=5)
        self.botoes_edicao = []
        self.rotulos_com_quebra = []

        self._criar_cabecalho()
        self._criar_barra_cenario()
        self._criar_area_principal()

    def _criar_cabecalho(self):
        cabecalho = tk.Frame(self, background=self.COR_PAINEL, pady=6)
        cabecalho.grid(row=0, column=0, sticky="ew")
        cabecalho.grid_columnconfigure(0, weight=1)

        area_titulos = tk.Frame(cabecalho, background=self.COR_PAINEL)
        area_titulos.grid(row=0, column=0)

        titulo = tk.Label(
            area_titulos,
            text="TOM & JERRY",
            background=self.COR_PAINEL,
            foreground=self.COR_DESTAQUE,
            font=("Arial", 19, "bold"),
        )
        titulo.pack()

        nome_projeto = tk.Label(
            area_titulos,
            text="Visualizador de Algoritmos de Busca",
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            font=("Arial", 11, "bold"),
        )
        nome_projeto.pack()

        subtitulo = tk.Label(
            area_titulos,
            text="A* e Busca Gulosa",
            background=self.COR_PAINEL,
            foreground="#d1d5db",
            font=("Arial", 9),
        )
        subtitulo.pack(pady=(2, 0))

        botao_ajuda = tk.Button(
            cabecalho,
            text="Como funciona?",
            command=self.abrir_ajuda,
            background="#4b5563",
            foreground=self.COR_TEXTO,
            activebackground=self.COR_DESTAQUE,
            activeforeground="#111827",
            relief="flat",
            cursor="hand2",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=5,
        )
        botao_ajuda.grid(row=0, column=1, padx=(8, 18))

    def _criar_barra_cenario(self):
        barra = tk.Frame(
            self,
            background="#374151",
            padx=18,
            pady=6,
        )
        barra.grid(row=1, column=0, sticky="ew")
        barra.grid_columnconfigure(5, weight=1)

        titulo = tk.Label(
            barra,
            text="CENÁRIO",
            background="#374151",
            foreground=self.COR_DESTAQUE,
            font=("Arial", 10, "bold"),
        )
        titulo.grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.seletor_labirinto = ttk.Combobox(
            barra,
            textvariable=self.labirinto_selecionado,
            values=(
                self.NOME_MANUAL,
                self.NOME_COZINHA,
                self.NOME_SALA,
                self.NOME_PORAO,
            ),
            state="readonly",
            width=12,
            font=("Arial", 9),
        )
        self.seletor_labirinto.grid(
            row=0,
            column=1,
            padx=(0, 8),
            sticky="w",
        )

        self.botao_carregar_labirinto = tk.Button(
            barra,
            text="Carregar cenário",
            command=self.carregar_labirinto_selecionado,
            background="#047857",
            foreground=self.COR_TEXTO,
            activebackground=self.COR_DESTAQUE,
            activeforeground="#111827",
            relief="flat",
            cursor="hand2",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=4,
        )
        self.botao_carregar_labirinto.grid(
            row=0,
            column=2,
            padx=(0, 6),
        )

        self.botao_restaurar_labirinto = tk.Button(
            barra,
            text="Restaurar cenário",
            command=self.restaurar_labirinto,
            background="#b45309",
            foreground=self.COR_TEXTO,
            activebackground=self.COR_DESTAQUE,
            activeforeground="#111827",
            relief="flat",
            cursor="hand2",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=4,
            state="disabled",
        )
        self.botao_restaurar_labirinto.grid(
            row=0,
            column=3,
            padx=(0, 18),
        )

        atual = tk.Label(
            barra,
            textvariable=self.texto_labirinto_atual,
            background="#374151",
            foreground=self.COR_TEXTO,
            font=("Arial", 9, "bold"),
            anchor="w",
        )
        atual.grid(row=0, column=4, padx=(0, 18), sticky="w")

        self.rotulo_descricao_labirinto = tk.Label(
            barra,
            textvariable=self.texto_descricao_labirinto,
            background="#374151",
            foreground="#d1d5db",
            font=("Arial", 9),
            justify="left",
            anchor="w",
            wraplength=520,
        )
        self.rotulo_descricao_labirinto.grid(
            row=0,
            column=5,
            sticky="ew",
        )
        barra.bind("<Configure>", self._ajustar_descricao_cenario)

    def _criar_area_principal(self):
        area_principal = tk.Frame(self, background=self.COR_FUNDO)
        area_principal.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=6,
            pady=4,
        )
        area_principal.grid_rowconfigure(0, weight=1)
        # A lateral preserva sua largura mínima e a grade recebe o espaço extra.
        area_principal.grid_columnconfigure(0, weight=1)
        area_principal.grid_columnconfigure(1, weight=0, minsize=480)

        area_grade = tk.Frame(area_principal, background=self.COR_FUNDO)
        area_grade.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        area_grade.grid_rowconfigure(0, weight=1)
        area_grade.grid_columnconfigure(0, weight=1)

        self.grade = Grade(area_grade, ao_editar=self._ao_editar_grade)
        self.grade.grid(row=0, column=0)
        area_grade.bind("<Configure>", self._redimensionar_grade_principal)

        self._criar_painel_lateral(area_principal)

    def _criar_painel_lateral(self, mestre):
        painel = tk.Frame(
            mestre,
            background=self.COR_PAINEL,
        )
        painel.grid(row=0, column=1, sticky="nsew")
        painel.grid_rowconfigure(0, weight=1)
        painel.grid_columnconfigure(0, weight=1)

        self.canvas_painel = tk.Canvas(
            painel,
            background=self.COR_PAINEL,
            highlightthickness=0,
            borderwidth=0,
        )
        self.canvas_painel.grid(row=0, column=0, sticky="nsew")

        barra_rolagem = ttk.Scrollbar(
            painel,
            orient="vertical",
            command=self.canvas_painel.yview,
        )
        barra_rolagem.grid(row=0, column=1, sticky="ns")
        self.canvas_painel.configure(yscrollcommand=barra_rolagem.set)

        corpo_painel = tk.Frame(
            self.canvas_painel,
            background=self.COR_PAINEL,
            padx=10,
            pady=10,
        )
        self.janela_canvas_painel = self.canvas_painel.create_window(
            (0, 0),
            window=corpo_painel,
            anchor="nw",
        )
        corpo_painel.bind("<Configure>", self._atualizar_area_rolavel)
        self.canvas_painel.bind(
            "<Configure>",
            self._ajustar_largura_painel,
        )
        corpo_painel.grid_columnconfigure(0, weight=1, uniform="painel")
        corpo_painel.grid_columnconfigure(1, weight=1, uniform="painel")

        coluna_esquerda = tk.Frame(corpo_painel, background=self.COR_PAINEL)
        coluna_esquerda.grid(row=0, column=0, sticky="new")

        coluna_direita = tk.Frame(corpo_painel, background=self.COR_PAINEL)
        coluna_direita.grid(
            row=0,
            column=1,
            sticky="new",
            padx=(10, 0),
        )
        coluna_direita.bind("<Configure>", self._ajustar_quebra_painel)

        self._criar_secao_editor(coluna_esquerda)
        self._criar_secao_algoritmo(coluna_esquerda)
        self._criar_secao_metricas(coluna_direita)
        self._criar_painel_no_atual(coluna_direita)
        self._criar_legenda(coluna_direita)

    def _redimensionar_grade_principal(self, evento):
        self.grade.ajustar_ao_espaco(evento.width, evento.height)

    def _atualizar_area_rolavel(self, evento=None):
        self.canvas_painel.configure(
            scrollregion=self.canvas_painel.bbox("all")
        )

    def _ajustar_largura_painel(self, evento):
        self.canvas_painel.itemconfigure(
            self.janela_canvas_painel,
            width=evento.width,
        )

    def _ajustar_quebra_painel(self, evento):
        largura = max(180, evento.width - 20)

        for rotulo in self.rotulos_com_quebra:
            rotulo.configure(wraplength=largura)

    def _ajustar_descricao_cenario(self, evento):
        largura = max(220, min(650, evento.width - 690))
        self.rotulo_descricao_labirinto.configure(wraplength=largura)

    def _criar_botao(self, mestre, texto, comando, cor="#4b5563"):
        botao = tk.Button(
            mestre,
            text=texto,
            command=comando,
            background=cor,
            foreground=self.COR_TEXTO,
            activebackground=self.COR_DESTAQUE,
            activeforeground="#111827",
            relief="flat",
            cursor="hand2",
            font=("Arial", 10, "bold"),
            pady=4,
        )
        botao.pack(fill="x", pady=2)
        return botao

    def _criar_botao_controle(
        self,
        mestre,
        texto,
        comando,
        linha,
        coluna,
        cor="#4b5563",
    ):
        botao = tk.Button(
            mestre,
            text=texto,
            command=comando,
            background=cor,
            foreground=self.COR_TEXTO,
            activebackground=self.COR_DESTAQUE,
            activeforeground="#111827",
            relief="flat",
            cursor="hand2",
            font=("Arial", 8, "bold"),
            pady=4,
        )
        botao.grid(row=linha, column=coluna, sticky="ew", padx=2, pady=2)
        return botao

    def _criar_bloco(self, mestre, titulo, espacamento=(0, 8)):
        bloco = tk.LabelFrame(
            mestre,
            text=titulo,
            background=self.COR_PAINEL,
            foreground=self.COR_DESTAQUE,
            font=("Arial", 10, "bold"),
            borderwidth=1,
            relief="groove",
            padx=8,
            pady=6,
        )
        bloco.pack(fill="x", pady=espacamento)
        return bloco

    def _criar_secao_editor(self, mestre):
        bloco = self._criar_bloco(mestre, "EDITOR DO MAPA")

        indicador_modo = tk.Label(
            bloco,
            textvariable=self.texto_modo_atual,
            background="#374151",
            foreground=self.COR_TEXTO,
            font=("Arial", 9, "bold"),
            padx=8,
            pady=5,
        )
        indicador_modo.pack(fill="x", pady=(0, 5))

        self._criar_rotulo_configuracao(bloco, "MODO DE OBJETIVO")
        self.seletor_modo_objetivo = ttk.Combobox(
            bloco,
            textvariable=self.modo_objetivo_selecionado,
            values=(
                self.NOME_UM_OBJETIVO,
                self.NOME_MULTIPLOS_OBJETIVOS,
            ),
            state="readonly",
            font=("Arial", 9),
        )
        self.seletor_modo_objetivo.pack(fill="x", pady=(0, 4))
        self.seletor_modo_objetivo.bind(
            "<<ComboboxSelected>>",
            self._ao_alterar_modo_objetivo,
        )

        quantidade_objetivos = tk.Label(
            bloco,
            textvariable=self.texto_quantidade_objetivos,
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            font=("Arial", 9),
        )
        quantidade_objetivos.pack(fill="x", pady=(0, 6))

        comandos = (
            ("Posicionar Tom", self._selecionar_modo_inicio, "#4b5563"),
            ("Posicionar Jerry", self._selecionar_modo_objetivo, "#4b5563"),
            ("Criar parede", self._selecionar_modo_parede, "#4b5563"),
            ("Apagar", self._selecionar_modo_apagar, "#4b5563"),
            ("Limpar mapa", self._limpar_mapa, "#b91c1c"),
        )

        for texto, comando, cor in comandos:
            botao = self._criar_botao(bloco, texto, comando, cor)
            self.botoes_edicao.append(botao)

    def _criar_secao_algoritmo(self, mestre):
        configuracao = self._criar_bloco(
            mestre,
            "CONFIGURAÇÃO DA BUSCA",
        )

        self._criar_rotulo_configuracao(configuracao, "ALGORITMO")
        self.seletor_algoritmo = ttk.Combobox(
            configuracao,
            textvariable=self.algoritmo_selecionado,
            values=(self.NOME_A_ESTRELA, self.NOME_BUSCA_GULOSA),
            state="readonly",
            font=("Arial", 9),
        )
        self.seletor_algoritmo.pack(fill="x", pady=(0, 6))
        self.seletor_algoritmo.bind(
            "<<ComboboxSelected>>",
            self._ao_alterar_configuracao,
        )

        self._criar_rotulo_configuracao(configuracao, "HEURÍSTICA")
        self.seletor_heuristica = ttk.Combobox(
            configuracao,
            textvariable=self.heuristica_selecionada,
            values=(
                self.NOME_MANHATTAN,
                self.NOME_EUCLIDIANA,
                self.NOME_DIAGONAL,
            ),
            state="readonly",
            font=("Arial", 9),
        )
        self.seletor_heuristica.pack(fill="x", pady=(0, 4))
        self.seletor_heuristica.bind(
            "<<ComboboxSelected>>",
            self._ao_alterar_configuracao,
        )

        self._criar_rotulo_configuracao(configuracao, "MOVIMENTO")
        self.seletor_movimento = ttk.Combobox(
            configuracao,
            textvariable=self.movimento_selecionado,
            values=(
                self.NOME_QUATRO_DIRECOES,
                self.NOME_OITO_DIRECOES,
            ),
            state="readonly",
            font=("Arial", 9),
        )
        self.seletor_movimento.pack(fill="x", pady=(0, 6))
        self.seletor_movimento.bind(
            "<<ComboboxSelected>>",
            self._ao_alterar_configuracao,
        )

        controles = self._criar_bloco(mestre, "CONTROLES", espacamento=(0, 0))
        grade_botoes = tk.Frame(controles, background=self.COR_PAINEL)
        grade_botoes.pack(fill="x")
        grade_botoes.grid_columnconfigure(0, weight=1)
        grade_botoes.grid_columnconfigure(1, weight=1)

        self.botao_iniciar = self._criar_botao_controle(
            grade_botoes,
            "▶ Iniciar busca",
            self.iniciar_busca,
            0,
            0,
            cor="#047857",
        )
        self.botao_pausar = self._criar_botao_controle(
            grade_botoes,
            "⏸ Pausar",
            self.pausar_busca,
            0,
            1,
        )
        self.botao_continuar = self._criar_botao_controle(
            grade_botoes,
            "▶ Continuar",
            self.continuar_busca,
            1,
            0,
        )
        self.botao_proximo = self._criar_botao_controle(
            grade_botoes,
            "⏭ Próximo passo",
            self.executar_um_passo,
            1,
            1,
        )
        self.botao_reiniciar = self._criar_botao_controle(
            grade_botoes,
            "↻ Reiniciar busca",
            self.reiniciar_busca,
            2,
            0,
            cor="#b45309",
        )
        self.botao_comparar = self._criar_botao_controle(
            grade_botoes,
            "Comparar A* x Gulosa",
            self.abrir_comparacao,
            2,
            1,
            cor="#7c3aed",
        )

        texto_velocidade = tk.Label(
            controles,
            text="Velocidade: 1 (lenta) a 10 (rápida)",
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            font=("Arial", 9, "bold"),
        )
        texto_velocidade.pack(pady=(7, 0))

        escala = tk.Scale(
            controles,
            from_=1,
            to=10,
            orient="horizontal",
            variable=self.valor_velocidade,
            command=self._alterar_velocidade,
            showvalue=True,
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            highlightthickness=0,
            troughcolor="#4b5563",
        )
        escala.pack(fill="x")

        self._atualizar_estado_botoes_animacao()

    def _criar_rotulo_configuracao(self, mestre, texto):
        rotulo = tk.Label(
            mestre,
            text=texto,
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            font=("Arial", 8, "bold"),
        )
        rotulo.pack(anchor="w", pady=(4, 2))

    def _criar_secao_metricas(self, mestre):
        bloco = self._criar_bloco(mestre, "MÉTRICAS")

        variaveis = (
            self.texto_algoritmo,
            self.texto_nos_explorados,
            self.texto_custo_total,
            self.texto_tempo_execucao,
            self.texto_status,
            self.texto_heuristica,
            self.texto_movimento,
            self.texto_criterio,
            self.texto_objetivos_alcancados,
            self.texto_ordem_objetivos,
        )

        for variavel in variaveis:
            rotulo = tk.Label(
                bloco,
                textvariable=variavel,
                justify="left",
                anchor="w",
                wraplength=210,
                background=self.COR_PAINEL,
                foreground=self.COR_TEXTO,
                font=("Arial", 10),
            )
            rotulo.pack(fill="x", pady=2)
            self.rotulos_com_quebra.append(rotulo)

    def _criar_painel_no_atual(self, mestre):
        bloco = self._criar_bloco(mestre, "NÓ ATUAL")

        dados = tk.Label(
            bloco,
            textvariable=self.texto_no_atual,
            justify="left",
            anchor="w",
            background="#374151",
            foreground=self.COR_TEXTO,
            font=("Arial", 10),
            padx=12,
            pady=10,
        )
        dados.pack(fill="x")

        significado = tk.Label(
            bloco,
            text=(
                "G = custo percorrido\n"
                "H = estimativa até Jerry\n"
                "F = G + H"
            ),
            justify="left",
            anchor="w",
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            font=("Arial", 9, "bold"),
            wraplength=210,
        )
        significado.pack(fill="x", pady=(6, 0))
        self.rotulos_com_quebra.append(significado)

        explicacao = tk.Label(
            bloco,
            textvariable=self.texto_explicacao_algoritmo,
            justify="left",
            anchor="w",
            background=self.COR_PAINEL,
            foreground="#d1d5db",
            font=("Arial", 9),
            wraplength=210,
        )
        explicacao.pack(fill="x", pady=(5, 0))
        self.rotulos_com_quebra.append(explicacao)

        explicacao_heuristica = tk.Label(
            bloco,
            textvariable=self.texto_explicacao_heuristica,
            justify="left",
            anchor="w",
            wraplength=210,
            background=self.COR_PAINEL,
            foreground="#d1d5db",
            font=("Arial", 9),
        )
        explicacao_heuristica.pack(fill="x", pady=(5, 0))
        self.rotulos_com_quebra.append(explicacao_heuristica)

        observacao = tk.Label(
            bloco,
            textvariable=self.texto_observacao,
            justify="left",
            anchor="w",
            wraplength=210,
            background=self.COR_PAINEL,
            foreground=self.COR_DESTAQUE,
            font=("Arial", 9, "bold"),
        )
        observacao.pack(fill="x", pady=(5, 0))
        self.rotulos_com_quebra.append(observacao)

    def _criar_legenda(self, mestre):
        bloco = self._criar_bloco(mestre, "LEGENDA", espacamento=(0, 0))
        itens = (
            ("#3b82f6", "Tom = início"),
            ("#ef4444", "Jerry = objetivo"),
            ("#374151", "Cinza escuro = parede"),
            ("#facc15", "Amarelo = lista aberta"),
            ("#93c5fd", "Azul claro = nó fechado"),
            ("#4ade80", "Verde = caminho final"),
            ("#15803d", "Verde escuro = objetivo alcançado"),
        )

        for cor, texto in itens:
            self._adicionar_item_legenda(bloco, cor, texto)

    def _adicionar_item_legenda(self, mestre, cor, texto):
        linha = tk.Frame(mestre, background=self.COR_PAINEL)
        linha.pack(fill="x", pady=1)

        amostra = tk.Frame(
            linha,
            width=13,
            height=13,
            background=cor,
            borderwidth=1,
            relief="solid",
        )
        amostra.pack(side="left", padx=(0, 6))
        amostra.pack_propagate(False)

        rotulo = tk.Label(
            linha,
            text=texto,
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            font=("Arial", 9),
            anchor="w",
            justify="left",
            wraplength=210,
        )
        rotulo.pack(side="left", fill="x", expand=True)
        self.rotulos_com_quebra.append(rotulo)

    def abrir_ajuda(self):
        """Abre um resumo curto para apoiar a explicação do projeto."""
        janela = tk.Toplevel(self)
        janela.title("Como funciona?")
        janela.geometry("430x390")
        janela.resizable(False, False)
        janela.configure(background=self.COR_FUNDO)
        janela.transient(self)

        titulo = tk.Label(
            janela,
            text="COMO FUNCIONA?",
            background=self.COR_FUNDO,
            foreground=self.COR_DESTAQUE,
            font=("Arial", 15, "bold"),
        )
        titulo.pack(pady=(18, 10))

        texto = (
            "A*: usa F = G + H e escolhe o menor F.\n\n"
            "Busca Gulosa: usa H e escolhe o menor H.\n\n"
            "G = custo percorrido.\n"
            "H = estimativa até Jerry.\n"
            "F = G + H.\n\n"
            "ABERTO (amarelo): nó descoberto e candidato.\n"
            "FECHADO (azul): nó já explorado.\n"
            "CAMINHO (verde): rota reconstruída até Jerry."
        )
        explicacao = tk.Label(
            janela,
            text=texto,
            justify="left",
            anchor="w",
            wraplength=370,
            background=self.COR_PAINEL,
            foreground=self.COR_TEXTO,
            font=("Arial", 10),
            padx=16,
            pady=14,
        )
        explicacao.pack(fill="x", padx=20)

        fechar = tk.Button(
            janela,
            text="Fechar",
            command=janela.destroy,
            background="#4b5563",
            foreground=self.COR_TEXTO,
            activebackground=self.COR_DESTAQUE,
            activeforeground="#111827",
            relief="flat",
            cursor="hand2",
            font=("Arial", 9, "bold"),
            padx=18,
            pady=5,
        )
        fechar.pack(pady=14)

    def _alterar_modo(self, modo, nome):
        self.grade.definir_modo_edicao(modo)
        self.texto_modo_atual.set(f"Modo atual: {nome}")

    def _selecionar_modo_inicio(self):
        self._alterar_modo(ModoEdicao.INICIO, "Tom")

    def _selecionar_modo_objetivo(self):
        self._alterar_modo(ModoEdicao.OBJETIVO, "Jerry")

    def _selecionar_modo_parede(self):
        self._alterar_modo(ModoEdicao.PAREDE, "Parede")

    def _selecionar_modo_apagar(self):
        self._alterar_modo(ModoEdicao.APAGAR, "Apagar")

    def carregar_labirinto_selecionado(self):
        """Carrega o cenário escolhido sem confundi-lo com a seleção visual."""
        if self.busca_em_reproducao:
            return

        tipo_labirinto = self._obter_tipo_labirinto_selecionado()
        self.reiniciar_busca()

        if tipo_labirinto == TipoLabirinto.MANUAL:
            self.grade.limpar_grade()
        else:
            dados = FabricaLabirintos.criar_labirinto(
                tipo_labirinto,
                Grade.LINHAS,
                Grade.COLUNAS,
            )
            self.grade.carregar_labirinto(dados)

        self.labirinto_atual = tipo_labirinto
        self._atualizar_textos_labirinto()
        self._atualizar_quantidade_objetivos()
        self._definir_controles_labirinto_habilitados(True)

    def restaurar_labirinto(self):
        """Descarta edições e recria o cenário atualmente carregado."""
        if (
            self.busca_em_reproducao
            or self.labirinto_atual == TipoLabirinto.MANUAL
        ):
            return

        self.reiniciar_busca()
        dados = FabricaLabirintos.criar_labirinto(
            self.labirinto_atual,
            Grade.LINHAS,
            Grade.COLUNAS,
        )
        self.grade.carregar_labirinto(dados)
        self._atualizar_textos_labirinto()
        self._atualizar_quantidade_objetivos()

    def _obter_tipo_labirinto_selecionado(self) -> TipoLabirinto:
        tipos_por_nome = {
            self.NOME_COZINHA: TipoLabirinto.COZINHA,
            self.NOME_SALA: TipoLabirinto.SALA,
            self.NOME_PORAO: TipoLabirinto.PORAO,
        }
        return tipos_por_nome.get(
            self.labirinto_selecionado.get(),
            TipoLabirinto.MANUAL,
        )

    def _atualizar_textos_labirinto(self):
        nome = FabricaLabirintos.obter_nome(self.labirinto_atual)
        descricao = FabricaLabirintos.obter_descricao(self.labirinto_atual)
        self.texto_labirinto_atual.set(f"Cenário atual: {nome}")
        self.texto_descricao_labirinto.set(descricao)

    def _ao_editar_grade(self):
        """Remove uma busca antiga quando o mapa volta a ser editado."""
        if (
            self.resultado_atual is not None
            or self.resultado_multiplos_atual is not None
        ):
            self.reiniciar_busca()

        self._atualizar_quantidade_objetivos()

    def _ao_alterar_modo_objetivo(self, evento=None):
        if self.busca_em_reproducao:
            return

        quantidade_objetivos = len(self.grade.obter_posicoes_objetivo())

        if (
            not self._usa_multiplos_objetivos()
            and quantidade_objetivos > 1
        ):
            messagebox.showwarning(
                "Múltiplos objetivos no mapa",
                "Apague os objetivos extras antes de usar Um objetivo.",
                parent=self,
            )
            self.modo_objetivo_selecionado.set(
                self.NOME_MULTIPLOS_OBJETIVOS
            )
            return

        self.reiniciar_busca()
        self.grade.definir_multiplos_objetivos_habilitados(
            self._usa_multiplos_objetivos()
        )

    def _usa_multiplos_objetivos(self) -> bool:
        return (
            self.modo_objetivo_selecionado.get()
            == self.NOME_MULTIPLOS_OBJETIVOS
        )

    def _atualizar_quantidade_objetivos(self):
        quantidade = len(self.grade.obter_posicoes_objetivo())
        self.texto_quantidade_objetivos.set(
            f"Objetivos no mapa: {quantidade}"
        )

    def abrir_comparacao(self):
        """Abre uma comparação usando uma fotografia do mapa atual."""
        if self._usa_multiplos_objetivos():
            messagebox.showwarning(
                "Comparação indisponível",
                "A comparação lado a lado está disponível, nesta versão, "
                "apenas para um objetivo.",
                parent=self,
            )
            return None

        inicio = self.grade.obter_posicao_inicio()
        objetivo = self.grade.obter_posicao_objetivo()

        if inicio is None:
            messagebox.showwarning(
                "Tom ausente",
                "Posicione Tom antes de abrir a comparação.",
                parent=self,
            )
            return None

        if objetivo is None:
            messagebox.showwarning(
                "Jerry ausente",
                "Posicione Jerry antes de abrir a comparação.",
                parent=self,
            )
            return None

        paredes = self.grade.obter_paredes()
        tipo_heuristica = self._obter_tipo_heuristica_selecionada()
        tipo_movimento = self._obter_tipo_movimento_selecionado()

        return JanelaComparacao(
            self,
            paredes,
            inicio,
            objetivo,
            tipo_heuristica,
            tipo_movimento,
        )

    def iniciar_busca(self):
        if self.busca_em_reproducao:
            return

        inicio = self.grade.obter_posicao_inicio()
        objetivos = self.grade.obter_posicoes_objetivo()

        if inicio is None:
            messagebox.showwarning(
                "Tom ausente",
                "Posicione Tom antes de iniciar a busca.",
                parent=self,
            )
            return

        if not objetivos:
            messagebox.showwarning(
                "Jerry ausente",
                "Posicione pelo menos um Jerry antes de iniciar a busca.",
                parent=self,
            )
            return

        if not self._usa_multiplos_objetivos() and len(objetivos) != 1:
            messagebox.showwarning(
                "Quantidade de objetivos",
                "O modo Um objetivo exige exatamente um Jerry.",
                parent=self,
            )
            return

        tipo_algoritmo = self._obter_tipo_algoritmo_selecionado()
        tipo_heuristica = self._obter_tipo_heuristica_selecionada()
        tipo_movimento = self._obter_tipo_movimento_selecionado()
        nome_algoritmo = self._obter_nome_algoritmo(tipo_algoritmo)
        self.reiniciar_busca()
        self.tipo_algoritmo_atual = tipo_algoritmo
        self.tipo_heuristica_atual = tipo_heuristica
        self.tipo_movimento_atual = tipo_movimento
        self.texto_status.set(f"Status: Executando {nome_algoritmo}...")
        self.update_idletasks()

        paredes = self.grade.obter_paredes()

        if self._usa_multiplos_objetivos():
            self.resultado_multiplos_atual = (
                self.busca_multiplos_objetivos.buscar(
                    paredes,
                    inicio,
                    objetivos,
                    tipo_algoritmo,
                    tipo_heuristica,
                    tipo_movimento,
                )
            )
            self.modo_multiplos_em_execucao = True
            self.quantidade_objetivos_total = len(objetivos)
            self.resultado_atual = (
                self.resultado_multiplos_atual.resultados_parciais[0]
            )
            self.texto_objetivos_alcancados.set(
                f"Objetivos alcançados: 0 / {len(objetivos)}"
            )
            self.texto_custo_total.set("Custo acumulado: 0")
            self.texto_tempo_execucao.set("Tempo acumulado: 0.000 ms")
            self.texto_ordem_objetivos.set("Ordem visitada: -")
        elif tipo_algoritmo == TipoAlgoritmo.A_ESTRELA:
            objetivo = objetivos[0]
            self.resultado_atual = self.a_estrela.buscar(
                paredes,
                inicio,
                objetivo,
                tipo_heuristica,
                tipo_movimento,
            )
        else:
            objetivo = objetivos[0]
            self.resultado_atual = self.busca_gulosa.buscar(
                paredes,
                inicio,
                objetivo,
                tipo_heuristica,
                tipo_movimento,
            )

        self.indice_passo_atual = 0
        self.indice_caminho_atual = 1
        self.quantidade_fechados_visual = 0
        self.busca_em_reproducao = True
        self.busca_pausada = False
        self.grade.definir_edicao_habilitada(False)
        self._definir_botoes_edicao_habilitados(False)
        self._definir_configuracoes_habilitadas(False)
        self._definir_controles_labirinto_habilitados(False)
        self.texto_status.set(f"Status: Executando {nome_algoritmo}...")
        if self.modo_multiplos_em_execucao:
            self.texto_status.set("Status: Buscando próximo objetivo...")
        self._atualizar_estado_botoes_animacao()
        self.executar_proximo_passo()

    def executar_proximo_passo(self):
        self.id_agendamento = None

        if not self.busca_em_reproducao or self.busca_pausada:
            return

        deve_continuar = self._executar_um_evento_visual()

        if deve_continuar and not self.busca_pausada:
            self.id_agendamento = self.after(
                self.atraso_animacao,
                self.executar_proximo_passo,
            )

    def _executar_um_evento_visual(self) -> bool:
        if self.resultado_atual is None:
            return False

        if self.indice_passo_atual < len(self.resultado_atual.passos):
            passo = self.resultado_atual.passos[self.indice_passo_atual]
            self.grade.aplicar_passo_busca(passo)
            self._mostrar_dados_passo(passo)
            self.indice_passo_atual += 1

            if passo.tipo == TipoPassoBusca.FECHADO:
                self.quantidade_fechados_visual += 1
                self.texto_nos_explorados.set(
                    f"Nós explorados: {self.quantidade_fechados_visual}"
                )

            if self._ha_evento_visual_pendente():
                return True

            return self._finalizar_resultado_atual()

        caminho = self.resultado_atual.caminho
        ultimo_indice = len(caminho) - 1

        if (
            self.resultado_atual.encontrou
            and self.indice_caminho_atual < ultimo_indice
        ):
            no = caminho[self.indice_caminho_atual]
            self.grade.marcar_no_caminho(no)
            self.indice_caminho_atual += 1
            self.texto_status.set("Status: Reconstruindo caminho")

            if self._ha_evento_visual_pendente():
                return True

            return self._finalizar_resultado_atual()

        return self._finalizar_resultado_atual()

    def _ha_evento_visual_pendente(self) -> bool:
        if self.resultado_atual is None:
            return False

        if self.indice_passo_atual < len(self.resultado_atual.passos):
            return True

        ultimo_indice = len(self.resultado_atual.caminho) - 1
        return (
            self.resultado_atual.encontrou
            and self.indice_caminho_atual < ultimo_indice
        )

    def pausar_busca(self):
        if not self.busca_em_reproducao or self.busca_pausada:
            return

        self.busca_pausada = True
        self._cancelar_agendamento()
        self.texto_status.set("Status: Busca pausada.")
        self._atualizar_estado_botoes_animacao()

    def continuar_busca(self):
        if not self.busca_em_reproducao or not self.busca_pausada:
            return

        self.busca_pausada = False
        nome_algoritmo = self._obter_nome_algoritmo(
            self.tipo_algoritmo_atual
        )
        self.texto_status.set(f"Status: Executando {nome_algoritmo}...")
        if self.modo_multiplos_em_execucao:
            self.texto_status.set("Status: Buscando próximo objetivo...")
        self._atualizar_estado_botoes_animacao()
        self.executar_proximo_passo()

    def executar_um_passo(self):
        if not self.busca_em_reproducao or not self.busca_pausada:
            return

        self._executar_um_evento_visual()

    def reiniciar_busca(self):
        self._cancelar_agendamento()
        self.grade.limpar_resultado_busca()
        self.grade.definir_edicao_habilitada(True)
        self._definir_botoes_edicao_habilitados(True)
        self._definir_configuracoes_habilitadas(True)
        self._definir_controles_labirinto_habilitados(True)

        self.resultado_atual = None
        self.resultado_multiplos_atual = None
        self.indice_passo_atual = 0
        self.indice_caminho_atual = 1
        self.indice_resultado_parcial = 0
        self.indice_objetivo_alcancado = 0
        self.quantidade_objetivos_total = 0
        self.custo_acumulado_visual = 0
        self.tempo_acumulado_visual = 0
        self.modo_multiplos_em_execucao = False
        self.quantidade_fechados_visual = 0
        self.busca_em_reproducao = False
        self.busca_pausada = False

        self.texto_status.set("Status: Pronto.")
        self._atualizar_textos_configuracao()
        self.texto_objetivos_alcancados.set("Objetivos alcançados: -")
        self.texto_nos_explorados.set("Nós explorados: 0")
        self.texto_custo_total.set("Custo total: -")
        self.texto_tempo_execucao.set("Tempo de execução: -")
        self.texto_no_atual.set(self._texto_no_vazio())
        self.texto_ordem_objetivos.set("Ordem visitada: -")
        self._atualizar_estado_botoes_animacao()

    def _finalizar_resultado_atual(self) -> bool:
        if self.modo_multiplos_em_execucao:
            return self._avancar_resultado_multiplos()

        self._finalizar_reproducao()
        return False

    def _avancar_resultado_multiplos(self) -> bool:
        resultado_parcial = self.resultado_atual
        self.tempo_acumulado_visual += resultado_parcial.tempo_execucao

        if resultado_parcial.encontrou:
            objetivo = self.resultado_multiplos_atual.ordem_objetivos[
                self.indice_objetivo_alcancado
            ]
            self.grade.marcar_objetivo_alcancado(objetivo)
            self.indice_objetivo_alcancado += 1
            self.custo_acumulado_visual += resultado_parcial.custo_total

        self.texto_objetivos_alcancados.set(
            "Objetivos alcançados: "
            f"{self.indice_objetivo_alcancado} / "
            f"{self.quantidade_objetivos_total}"
        )
        self.texto_custo_total.set(
            f"Custo acumulado: {self.custo_acumulado_visual:g}"
        )
        self.texto_tempo_execucao.set(
            "Tempo acumulado: "
            f"{self.tempo_acumulado_visual * 1000:.3f} ms"
        )

        self.indice_resultado_parcial += 1
        resultados = self.resultado_multiplos_atual.resultados_parciais

        if self.indice_resultado_parcial < len(resultados):
            self.grade.limpar_exploracao_busca()
            self.resultado_atual = resultados[self.indice_resultado_parcial]
            self.indice_passo_atual = 0
            self.indice_caminho_atual = 1
            self.texto_status.set("Status: Buscando próximo objetivo...")
            return True

        self._finalizar_reproducao_multiplos()
        return False

    def _finalizar_reproducao_multiplos(self):
        self._cancelar_agendamento()
        self.busca_em_reproducao = False
        self.busca_pausada = False
        self.grade.definir_edicao_habilitada(True)
        self._definir_botoes_edicao_habilitados(True)
        self._definir_configuracoes_habilitadas(True)
        self._definir_controles_labirinto_habilitados(True)

        for no in self.resultado_multiplos_atual.caminho_completo:
            self.grade.marcar_no_caminho(no)

        if self.resultado_multiplos_atual.encontrou_todos:
            self.texto_status.set(
                "Status: Todos os objetivos foram alcançados!"
            )
        else:
            self.texto_status.set(
                "Status: Nem todos os objetivos são alcançáveis"
            )

        self.texto_nos_explorados.set(
            "Nós explorados: "
            f"{self.resultado_multiplos_atual.nos_explorados_total}"
        )
        self.texto_custo_total.set(
            f"Custo acumulado: {self.resultado_multiplos_atual.custo_total:g}"
        )
        tempo_ms = self.resultado_multiplos_atual.tempo_execucao_total * 1000
        self.texto_tempo_execucao.set(
            f"Tempo acumulado: {tempo_ms:.3f} ms"
        )
        self.texto_ordem_objetivos.set(self._formatar_ordem_objetivos())
        self._atualizar_estado_botoes_animacao()

    def _formatar_ordem_objetivos(self) -> str:
        if not self.resultado_multiplos_atual.ordem_objetivos:
            return "Ordem visitada: nenhum objetivo"

        itens = []
        for indice, posicao in enumerate(
            self.resultado_multiplos_atual.ordem_objetivos,
            start=1,
        ):
            itens.append(f"{indice}. {posicao}")

        return "Ordem visitada: " + "  ".join(itens)

    def _finalizar_reproducao(self):
        self._cancelar_agendamento()
        self.busca_em_reproducao = False
        self.busca_pausada = False
        self.grade.definir_edicao_habilitada(True)
        self._definir_botoes_edicao_habilitados(True)
        self._definir_configuracoes_habilitadas(True)
        self._definir_controles_labirinto_habilitados(True)

        if self.resultado_atual.encontrou:
            self.texto_status.set("Status: Jerry encontrado!")
            self.texto_custo_total.set(
                f"Custo total: {self.resultado_atual.custo_total:g}"
            )
            self.texto_objetivos_alcancados.set(
                "Objetivos alcançados: 1 / 1"
            )
            objetivo = self.grade.obter_posicao_objetivo()
            self.texto_ordem_objetivos.set(
                f"Ordem visitada: 1. {objetivo}"
            )
        else:
            self.texto_status.set("Status: Caminho não encontrado.")
            self.texto_custo_total.set("Custo total: -")
            self.texto_objetivos_alcancados.set(
                "Objetivos alcançados: 0 / 1"
            )
            self.texto_ordem_objetivos.set(
                "Ordem visitada: nenhum objetivo"
            )

        tempo_ms = self.resultado_atual.tempo_execucao * 1000
        self.texto_tempo_execucao.set(
            f"Tempo de execução: {tempo_ms:.3f} ms"
        )
        self._atualizar_estado_botoes_animacao()

    def _mostrar_dados_passo(self, passo: PassoBusca):
        self.texto_no_atual.set(
            f"Linha: {passo.linha}\n"
            f"Coluna: {passo.coluna}\n\n"
            f"G: {passo.custo_g:g}\n"
            f"H: {passo.heuristica_h:g}\n"
            f"F: {passo.custo_f:g}\n\n"
            f"Estado: {passo.tipo.name}"
        )

    def _cancelar_agendamento(self):
        if self.id_agendamento is not None:
            self.after_cancel(self.id_agendamento)
            self.id_agendamento = None

    def _definir_botoes_edicao_habilitados(self, habilitados: bool):
        estado = "normal" if habilitados else "disabled"

        for botao in self.botoes_edicao:
            botao.configure(state=estado)

    def _definir_configuracoes_habilitadas(self, habilitadas: bool):
        seletores = (
            self.seletor_algoritmo,
            self.seletor_heuristica,
            self.seletor_movimento,
            self.seletor_modo_objetivo,
        )
        estado = "readonly" if habilitadas else "disabled"

        for seletor in seletores:
            seletor.configure(state=estado)

    def _definir_controles_labirinto_habilitados(
        self,
        habilitados: bool,
    ):
        estado_seletor = "readonly" if habilitados else "disabled"
        estado_carregar = "normal" if habilitados else "disabled"
        pode_restaurar = (
            habilitados
            and self.labirinto_atual != TipoLabirinto.MANUAL
        )

        self.seletor_labirinto.configure(state=estado_seletor)
        self.botao_carregar_labirinto.configure(state=estado_carregar)
        self.botao_restaurar_labirinto.configure(
            state="normal" if pode_restaurar else "disabled"
        )

    def _ao_alterar_configuracao(self, evento=None):
        if self.busca_em_reproducao:
            return

        self.reiniciar_busca()

    def _atualizar_textos_configuracao(self):
        tipo_algoritmo = self._obter_tipo_algoritmo_selecionado()
        tipo_heuristica = self._obter_tipo_heuristica_selecionada()
        tipo_movimento = self._obter_tipo_movimento_selecionado()
        nome_algoritmo = self._obter_nome_algoritmo(tipo_algoritmo)
        nome_heuristica = self._obter_nome_heuristica(tipo_heuristica)
        nome_movimento = self._obter_nome_movimento(tipo_movimento)

        self.texto_algoritmo.set(f"Algoritmo: {nome_algoritmo}")
        self.texto_heuristica.set(f"Heurística: {nome_heuristica}")
        self.texto_movimento.set(f"Movimento: {nome_movimento}")

        if tipo_algoritmo == TipoAlgoritmo.A_ESTRELA:
            self.texto_criterio.set("Critério: menor F")
        else:
            self.texto_criterio.set("Critério: menor H")

        self.texto_explicacao_algoritmo.set(
            self._obter_explicacao_algoritmo(tipo_algoritmo)
        )
        self.texto_explicacao_heuristica.set(
            self._obter_explicacao_heuristica(tipo_heuristica)
        )
        self.texto_observacao.set(
            self._obter_observacao_configuracao(
                tipo_heuristica,
                tipo_movimento,
            )
        )

    def _obter_tipo_algoritmo_selecionado(self) -> TipoAlgoritmo:
        if self.algoritmo_selecionado.get() == self.NOME_BUSCA_GULOSA:
            return TipoAlgoritmo.BUSCA_GULOSA

        return TipoAlgoritmo.A_ESTRELA

    def _obter_tipo_heuristica_selecionada(self) -> TipoHeuristica:
        nome = self.heuristica_selecionada.get()

        if nome == self.NOME_EUCLIDIANA:
            return TipoHeuristica.EUCLIDIANA

        if nome == self.NOME_DIAGONAL:
            return TipoHeuristica.DIAGONAL

        return TipoHeuristica.MANHATTAN

    def _obter_tipo_movimento_selecionado(self) -> TipoMovimento:
        if self.movimento_selecionado.get() == self.NOME_OITO_DIRECOES:
            return TipoMovimento.OITO_DIRECOES

        return TipoMovimento.QUATRO_DIRECOES

    def _obter_nome_algoritmo(self, tipo_algoritmo: TipoAlgoritmo) -> str:
        if tipo_algoritmo == TipoAlgoritmo.BUSCA_GULOSA:
            return self.NOME_BUSCA_GULOSA

        return self.NOME_A_ESTRELA

    def _obter_nome_heuristica(self, tipo_heuristica: TipoHeuristica) -> str:
        if tipo_heuristica == TipoHeuristica.EUCLIDIANA:
            return self.NOME_EUCLIDIANA

        if tipo_heuristica == TipoHeuristica.DIAGONAL:
            return self.NOME_DIAGONAL

        return self.NOME_MANHATTAN

    def _obter_nome_movimento(self, tipo_movimento: TipoMovimento) -> str:
        if tipo_movimento == TipoMovimento.OITO_DIRECOES:
            return self.NOME_OITO_DIRECOES

        return self.NOME_QUATRO_DIRECOES

    def _obter_explicacao_algoritmo(
        self,
        tipo_algoritmo: TipoAlgoritmo,
    ) -> str:
        if tipo_algoritmo == TipoAlgoritmo.BUSCA_GULOSA:
            return (
                "Busca Gulosa considera a estimativa até Jerry. "
                "Critério: menor H"
            )

        return (
            "A* considera o custo percorrido e a estimativa até Jerry. "
            "Critério: menor F"
        )

    def _obter_explicacao_heuristica(
        self,
        tipo_heuristica: TipoHeuristica,
    ) -> str:
        if tipo_heuristica == TipoHeuristica.EUCLIDIANA:
            return "Euclidiana estima a distância em linha reta até Jerry."

        if tipo_heuristica == TipoHeuristica.DIAGONAL:
            return "Diagonal considera movimentos diagonais e ortogonais."

        return "Manhattan soma as diferenças horizontal e vertical."

    def _obter_observacao_configuracao(
        self,
        tipo_heuristica: TipoHeuristica,
        tipo_movimento: TipoMovimento,
    ) -> str:
        usa_manhattan = tipo_heuristica == TipoHeuristica.MANHATTAN
        usa_diagonais = tipo_movimento == TipoMovimento.OITO_DIRECOES

        if usa_manhattan and usa_diagonais:
            return (
                "Observação: Manhattan pode superestimar o custo com "
                "movimentos diagonais."
            )

        return ""

    def _atualizar_estado_botoes_animacao(self):
        if not hasattr(self, "botao_iniciar"):
            return

        esta_reproduzindo = self.busca_em_reproducao
        esta_pausada = self.busca_pausada

        self.botao_iniciar.configure(
            state="disabled" if esta_reproduzindo else "normal"
        )
        self.botao_pausar.configure(
            state=(
                "normal"
                if esta_reproduzindo and not esta_pausada
                else "disabled"
            )
        )
        self.botao_continuar.configure(
            state="normal" if esta_reproduzindo and esta_pausada else "disabled"
        )
        self.botao_proximo.configure(
            state="normal" if esta_reproduzindo and esta_pausada else "disabled"
        )
        self.botao_reiniciar.configure(
            state="normal" if self.resultado_atual is not None else "disabled"
        )
        self.botao_comparar.configure(
            state="disabled" if esta_reproduzindo else "normal"
        )

    def _alterar_velocidade(self, valor):
        nivel = int(float(valor))
        self.atraso_animacao = self._converter_velocidade(nivel)

    def _converter_velocidade(self, nivel: int) -> int:
        return converter_nivel_em_atraso(nivel)

    def _texto_no_vazio(self) -> str:
        return (
            "Linha: -\n"
            "Coluna: -\n\n"
            "G: -\n"
            "H: -\n"
            "F: -\n\n"
            "Estado: -"
        )

    def _limpar_mapa(self):
        self.reiniciar_busca()
        self.grade.limpar_grade()
        self._atualizar_quantidade_objetivos()
