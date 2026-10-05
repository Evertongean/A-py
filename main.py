from interface.janela_principal import JanelaPrincipal


def main():
    aplicacao = JanelaPrincipal()

    # mainloop mantém a janela aberta e escuta eventos, como os cliques do mouse.
    aplicacao.mainloop()


if __name__ == "__main__":
    main()
