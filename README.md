# crystals
Neste repositório encontra-se o projeto desenvolvido como iniciação científica durante o curso de Engenharia Química, na UFPE. O Projeto trata da simulação de um processo contínuo de cristalização, utilizando um modelo matemático desenvolvido por Silva *et al* (2006).

O código do projeto foi desenvolvido em linguagem Python, e inicialmente a proposta era apenas o código para a simulação. Porém, visando facilitar futuras pesquisas sobre o tema, utilizando o mesmo modelo, foi desenvolvida também uma interface gráfica de usuário utilizando o framework Tkinter, culminando num software final, executável e stand-alone.

#### Sobre o Código
O projeto foi desenvolvido totalmente em linguagem Python, utilizando as seguintes bibliotecas:
* **Numpy** para manipulação matemática
* **Pandas** para manipulação de dados
* **Matplotlib** para visualização de dados
* **Tkinter** para desenvolvimento da interface gráfica de usuário
* **pyinstaller** para criar executável

O aplicativo permite realizar as simulações usando diferentes datasets de variáveis do modelo matemático, alterando algumas propriedades dos gráficos que serão gerados e permite salvá-los na pasta desejada.


#### Um pouco sobre Cristalização

A cristalização é um processo de separação e purificação de componentes muito utilizado em indústrias químicas. O tamanho e formato dos cristais é de grande importância para suas características físico-químicas, dessa forma é necessário que haja uma previsão e controle do comportamento do processo.

Matematicamente, o processo de cristalização é complexo e desafiador, pois é classificado como um problema de fronteira móvel (ou [Problema de Stefan](https://en.wikipedia.org/wiki/Stefan_problem)), onde a barreira física em que ocorre a transferência de massa entre as fases varia sua posição com o crescimento do cristal. Para esse problema, foi proposta uma solução para a velocidade de crescimento dos cristais, por Silva *et al* (2006)*, solução esta que foi utilizada neste projeto para fazer a simulação do processo de cristalização.

A partir do modelo, é possível prever o comportamento do tamanho dos cristais em diferentes tempos de residência dentro do cristalizador, além de estudar o tamanho dominante (faixa de tamanho que apresenta maior população de cristais) e a densidade de população de cristais. Uma discussão mais aprofundada sobre cristalização, os modelos utilizados e os resultados obtidos pode ser encontrada no [Relatório Final]() deste projeto de Iniciação Científica.

**Silva, J. M. F.; Lopes, C. E. ; Meirelles, A. J. A. ; Maciel, M. R. W. . Stefan´s Problem Applied To Solution Crystalization. Journal of Chemical Engineering of Japan, 39 (1), 940- 947, 2006.*
