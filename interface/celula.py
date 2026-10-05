import tkinter as tk

from modelos.tipos import TipoCelula


class Celula(tk.Label):
    """Representa visualmente uma posição da grade."""

    CORES = {
        TipoCelula.VAZIA: "#f4f1ea",
        TipoCelula.PAREDE: "#374151",
        TipoCelula.INICIO: "#3b82f6",
        TipoCelula.OBJETIVO: "#ef4444",
        TipoCelula.OBJETIVO_ALCANCADO: "#15803d",
        TipoCelula.ABERTA: "#facc15",
        TipoCelula.FECHADA: "#93c5fd",
        TipoCelula.CAMINHO: "#4ade80",
    }

    TEXTOS = {
        TipoCelula.INICIO: "T",
        TipoCelula.OBJETIVO: "J",
        TipoCelula.OBJETIVO_ALCANCADO: "✓",
    }

    def __init__(
        self,
        mestre,
        linha,
        coluna,
        imagem_tom=None,
        imagem_jerry=None,
    ):
        super().__init__(
            mestre,
            width=2,
            height=1,
            relief="solid",
            borderwidth=1,
            font=("Arial", 12, "bold"),
            cursor="hand2",
        )

        self.linha = linha
        self.coluna = coluna
        self.imagem_tom = imagem_tom
        self.imagem_jerry = imagem_jerry
        self.tipo = TipoCelula.VAZIA
        self.definir_tipo(TipoCelula.VAZIA)

    def definir_tipo(self, novo_tipo):
        """Altera o estado e a aparência da célula."""
        self.tipo = novo_tipo

        cor = self.CORES[novo_tipo]
        imagem = ""
        texto = self.TEXTOS.get(novo_tipo, "")

        if novo_tipo == TipoCelula.INICIO and self.imagem_tom is not None:
            imagem = self.imagem_tom
            texto = ""
        elif (
            novo_tipo == TipoCelula.OBJETIVO
            and self.imagem_jerry is not None
        ):
            imagem = self.imagem_jerry
            texto = ""

        cor_texto = "white" if novo_tipo != TipoCelula.VAZIA else "#111827"

        # Com imagem, largura e altura são medidas em pixels no Tkinter.
        # Sem imagem, voltam a ser medidas em caracteres e linhas.
        largura = 20 if imagem else 2
        altura = 16 if imagem else 1

        self.configure(
            background=cor,
            foreground=cor_texto,
            text=texto,
            image=imagem,
            compound="center",
            anchor="center",
            width=largura,
            height=altura,
        )
