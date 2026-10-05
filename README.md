# A-Star Tom & Jerry — Python

Projeto acadêmico de Inteligência Artificial para visualizar algoritmos de
busca em uma grade. A versão atual permite alternar entre **A\*** e
**Busca Gulosa**.

O tema usa Tom como ponto A (início) e Jerry como ponto B (objetivo).

## Etapa atual

Além do editor visual feito com Python e Tkinter, a etapa atual contém:

- A* e Busca Gulosa;
- heurísticas Manhattan, Euclidiana e Diagonal;
- movimentos em quatro ou oito direções;
- custo 10 para movimento ortogonal e 14 para movimento diagonal;
- visualização passo a passo da lista aberta, nós fechados e caminho final;
- controles para iniciar, pausar, continuar, avançar e reiniciar;
- controle de velocidade;
- valores G, H e F do evento atual;
- quantidade de nós explorados, custo total e tempo de cálculo;
- modo Manual e três labirintos prontos e editáveis;
- restauração dos labirintos para o desenho original;
- comparação visual lado a lado entre A* e Busca Gulosa;
- modo opcional com múltiplos objetivos.

Tom representa o início e Jerry representa o objetivo. Nos algoritmos:

- **G** é o custo já percorrido desde Tom;
- **H** é a estimativa da heurística selecionada até Jerry;
- **F = G + H** combina o custo percorrido com a estimativa restante.

## Algoritmos

O **A\*** usa `F = G + H` como prioridade. Ele considera tanto o caminho já
percorrido quanto a estimativa até Jerry.

A **Busca Gulosa** usa somente `H` como prioridade. Ela tenta se aproximar de
Jerry rapidamente, mas pode encontrar um caminho mais caro. Mesmo assim, ela
continua calculando G, H e F para informar o custo real, exibir os valores e
atualizar uma posição quando surgir uma rota com G menor.

Por exemplo:

- nó A: G = 100, H = 2 e F = 102;
- nó B: G = 2, H = 5 e F = 7.

O A* escolhe o nó B porque ele possui o menor F. A Busca Gulosa escolhe o nó A
porque ele possui o menor H.

## Heurísticas

Considerando `dx` e `dy` como as diferenças entre linhas e colunas:

- **Manhattan:** `H = (dx + dy) * 10`;
- **Euclidiana:** `H = floor(sqrt(dx² + dy²) * 10)`;
- **Diagonal:** `H = 14 * min(dx, dy) + 10 * (max(dx, dy) - min(dx, dy))`.

Manhattan soma as diferenças horizontal e vertical. Euclidiana estima a
distância em linha reta. Diagonal combina a quantidade de passos diagonais e
ortogonais.

Quando oito direções estão habilitadas, Manhattan pode superestimar o custo,
pois uma diagonal custa 14 enquanto dois movimentos ortogonais custam 20. A
interface informa essa observação, mas não impede a combinação.

## Movimentos e custos

No modo de quatro direções são permitidos movimentos para cima, baixo,
esquerda e direita. Cada passo custa 10.

No modo de oito direções também são permitidas diagonais, que custam 14. Uma
diagonal só é aceita quando suas duas posições laterais estão livres. Isso
impede que Tom atravesse o canto formado por uma ou duas paredes.

## Como a animação funciona

O algoritmo selecionado primeiro calcula toda a busca e registra cada
acontecimento em um `PassoBusca`. O `ResultadoBusca` guarda esses passos na
ordem em que ocorreram. Depois do cálculo, a interface usa o `after()` do
Tkinter para reproduzi-los.

A animação não executa o algoritmo lentamente: ela apenas reproduz uma gravação
que já está pronta. Por isso, o tempo exibido mede somente o cálculo do
algoritmo escolhido, sem incluir animação, pausas ou o tempo do usuário.

Durante a reprodução:

- amarelo representa uma posição na lista aberta;
- azul-claro representa uma posição fechada e explorada;
- verde representa o caminho final.

## Labirintos

O seletor de cenário oferece quatro opções:

- **Manual:** mantém o editor livre para posicionar Tom, Jerry e paredes;
- **Cozinha:** cenário fácil, com poucos móveis e pequenos desvios;
- **Sala:** cenário médio, com divisórias, corredores, rotas alternativas e
  alguns becos;
- **Porão:** cenário difícil, com corredores longos, becos e uma rota enganosa
  pensada para comparar o A* com a Busca Gulosa.

Trocar a opção no seletor não apaga o mapa. O cenário só é aplicado depois do
clique em **Carregar cenário**. Todos os mapas prontos continuam editáveis: é
possível adicionar ou remover paredes e mover Tom ou Jerry. O botão
**Restaurar cenário** descarta essas alterações e recria o desenho original.
No modo Manual, esse botão permanece desabilitado.

## Comparação A* x Busca Gulosa

O botão **Comparar A* x Gulosa** abre uma nova janela com duas grades. Os dois
algoritmos recebem uma fotografia do mesmo mapa, as mesmas posições de Tom e
Jerry, a mesma heurística e o mesmo tipo de movimento. A única diferença entre
os lados é o critério de prioridade: o A* usa `F = G + H`, enquanto a Busca
Gulosa usa somente `H`.

Os resultados são calculados separadamente antes da animação e depois
reproduzidos lado a lado. Em cada passo visual, cada algoritmo avança no máximo
um evento. Se um lado terminar primeiro, o outro continua normalmente. A
quantidade de nós explorados cresce durante a reprodução sempre que um evento
`FECHADO` é exibido.

Ao final, a janela informa separadamente:

- o algoritmo que encontrou o menor custo;
- o algoritmo que explorou menos nós;
- o algoritmo com menor tempo de cálculo.

Não existe um vencedor geral, pois cada uma dessas métricas representa um
critério diferente. O custo corresponde ao caminho efetivamente encontrado e
o tempo considera somente o cálculo do algoritmo, sem incluir a animação. O
tempo é uma métrica experimental e pode apresentar pequenas variações entre
execuções.

## Múltiplos objetivos

O modo padrão **Um objetivo** mantém o comportamento original: existe um Tom e
um Jerry, e posicionar outro Jerry substitui o anterior. No modo opcional
**Múltiplos objetivos**, cada clique em **Posicionar Jerry** acrescenta outro
objetivo ao mapa.

A execução é uma sequência de buscas. A partir da posição atual, os objetivos
restantes são ordenados pelo valor da heurística selecionada. O sistema tenta o
mais próximo pela estimativa e, se ele for inalcançável, tenta os candidatos
seguintes. Depois de encontrar um objetivo, sua posição passa a ser a origem da
próxima busca.

Cada trecho continua sendo calculado pelo A* ou pela Busca Gulosa normal. Os
custos dos trechos encontrados são acumulados. A quantidade de nós explorados
e o tempo incluem todas as buscas executadas, inclusive tentativas que não
encontraram caminho. O tempo considera somente os cálculos, sem incluir a
animação.

Ao final, a interface mostra a quantidade de objetivos alcançados, custo
acumulado, nós explorados, tempo acumulado e ordem visitada. A comparação lado
a lado permanece disponível apenas no modo de um objetivo.

**Limitação:** essa estratégia não resolve globalmente o problema da melhor
ordem para visitar todos os objetivos. Escolher o próximo objetivo pela menor
heurística é uma estratégia simples e não garante a menor rota total.

## Recursos visuais

Tom representa o ponto inicial e Jerry representa cada objetivo. As imagens
PNG esperadas pelo programa ficam em:

- `recursos/imagens/tom.png`;
- `recursos/imagens/jerry.png`.

Os caminhos são encontrados com `pathlib` a partir da pasta do próprio
projeto, portanto não dependem do nome do usuário nem do diretório em que o
projeto foi instalado. A `Grade` carrega cada arquivo uma vez com
`tk.PhotoImage` e mantém as referências enquanto a interface existir. Se um
arquivo estiver ausente ou inválido, a aplicação continua funcionando e usa
as letras **T** e **J** como fallback.

## Estrutura do projeto

```text
A*_PY/
├── algoritmos/
│   ├── a_estrela.py
│   ├── busca_gulosa.py
│   ├── busca_multiplos_objetivos.py
│   ├── heuristicas.py
│   └── movimentos.py
├── interface/
│   ├── celula.py
│   ├── controle_velocidade.py
│   ├── grade.py
│   ├── janela_comparacao.py
│   └── janela_principal.py
├── labirintos/
│   └── fabrica_labirintos.py
├── modelos/
│   ├── dados_labirinto.py
│   ├── no.py
│   ├── passo_busca.py
│   ├── resultado_busca.py
│   ├── resultado_multiplos_objetivos.py
│   └── tipos.py
├── recursos/
│   └── imagens/
│       ├── tom.png
│       └── jerry.png
├── .gitignore
├── README.md
└── main.py
```

## Requisitos

- Python 3.11 ou superior
- Tkinter (biblioteca padrão do Python)

## Como executar

No diretório do projeto, execute:

```bash
python3 main.py
```

Em ambientes nos quais o comando `python` já aponta para o Python 3.11 ou
superior, também é possível executar `python main.py`.
