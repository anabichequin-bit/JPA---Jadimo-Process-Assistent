JPA Automação – Recebimento

O código presente neste repositório corresponde à versão inicial do projeto.
A aplicação continuou evoluindo posteriormente dentro do ambiente interno da empresa, por isso a versão mais recente está disponível apenas como executável.

Este projeto foi desenvolvido para automatizar algumas tarefas administrativas do setor de recebimento logístico de uma transportadora.

No dia a dia do setor, durante a conferência de documentos, é necessário coletar e registrar diversas informações em planilhas. Com o tempo, esse processo acaba gerando uma grande quantidade de dados espalhados e organizados manualmente, o que torna o trabalho repetitivo e sujeito a erros.

Ao analisar esses dados e a forma como eram utilizados na operação, percebi que eles poderiam ser melhor aproveitados se fossem organizados automaticamente. A partir disso surgiu a ideia de criar uma ferramenta simples que ajudasse a estruturar essas informações e facilitasse o trabalho de conferência realizado pela equipe.

A aplicação foi desenvolvida em Python, com interface desktop utilizando PySide6, permitindo que qualquer pessoa do setor consiga utilizar o sistema sem precisar executar scripts ou trabalhar diretamente com código.

Funcionalidades

O sistema possui duas automações principais voltadas para tarefas realizadas no setor de recebimento.

Organização de menções (malote)

A primeira automação trata a planilha bruta utilizada pelo setor para controle de malotes contendo grandes quantidades de documentação.

As numerações de documentos como CTEs, NFs e outras referências são geralmente enviadas por e-mail e registradas manualmente em planilhas. Como essas informações chegam de forma desorganizada, o processo de registrar e organizar os dados acaba sendo demorado.

Como todas as documentações recebidas precisam ser registradas para comprovação de conferência correta, essa automação foi criada para organizar automaticamente esses dados e gerar uma planilha estruturada em formato .xlsx.

O sistema lê a planilha bruta utilizada pelo setor e reorganiza as informações no formato utilizado pelo faturamento da empresa.

Algumas colunas permanecem vazias porque são preenchidas manualmente durante a conferência realizada pela equipe de recebimento.

Controle de pendências de mapas

A segunda automação é responsável por analisar os mapas de viagem entregues pelos motoristas, documentos utilizados para controle das viagens e das documentações associadas.

Com base nesses dados, o sistema identifica automaticamente quais motoristas estão em dia com a entrega de documentação e quais possuem pendências.

No setor existe uma regra fixa para os períodos de controle de entrega:

Os períodos começam no dia 11 de um mês
e terminam no dia 10 do mês seguinte

Exemplo:

11/02 → 10/03

O sistema identifica automaticamente:

qual é o período atual (ainda aberto)

qual foi o último período fechado

A partir disso, ele analisa a última viagem entregue por cada motorista e determina o status da documentação.

EM DIA → motorista entregou o mapa do último período fechado
PENDENTE → motorista não entregou o mapa do último período fechado

O sistema também calcula automaticamente quantos períodos fechados estão em atraso.

Lógica aplicada no controle

Durante o desenvolvimento foi necessário considerar alguns comportamentos reais do processo do setor.

Em alguns casos, um motorista pode entregar um mapa mais recente e posteriormente regularizar um mapa antigo que estava pendente de documentação. Isso faz com que as datas apareçam fora de ordem na planilha.

Por esse motivo, o sistema não considera apenas a ordem dos registros. Em vez disso, ele identifica a última entrega real com base na data final do período da viagem, garantindo que o cálculo das pendências seja feito corretamente mesmo quando os registros estão fora de sequência.

Tecnologias utilizadas

O projeto foi desenvolvido utilizando:

Python

PySide6 (Qt for Python)

pandas

openpyxl

PyInstaller

A aplicação foi empacotada como um executável (.exe) utilizando PyInstaller, permitindo que o sistema seja utilizado dentro da empresa sem necessidade de instalar Python ou bibliotecas adicionais.

Objetivo do projeto

O objetivo dessa ferramenta é reduzir tarefas repetitivas do setor e melhorar o controle das informações utilizadas no recebimento logístico.

Com a automação, atividades que antes exigiam reorganização manual de planilhas passam a ser realizadas automaticamente, tornando o processo mais rápido, padronizado e confiável para a operação.
