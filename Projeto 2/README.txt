### Grupo: SO-TI-06
# Aluno 1: João Pereira (fc57573)
# Aluno 2: Mariana Valente (fc55945)
# Aluno 3: Tiago Silveira (fc56589)

### Exemplos de comandos para executar o pgrepwc:

PROCESSOS 

1) ./pgrepwc -l -c palavra ficheiro1.txt
2) ./pgrepwc -c -p 3 palavra ficheiro1.txt ficheiro2.txt
3) ./pgrepwc -c -l -p 6 -e palavra ficheiro1.txt
4) ./pgrepwc -c -p 3 teste f1.txt f2.txt f3.txt f4.txt f5.txt f6.txt
5) ./pgrepwc -c -p 3 -l -e 20 f1.txt f2.txt f3.txt f4.txt
6) ./pgrepwc -c -l -e 80 f1.txt


### Limitações da implementação:
- Se ao passar o argumento "-p" não passar-mos nenhum número o programa encontra um erro
- Se ao passar o argumento "-k" não passar-mos nenhum número o programa encontra um erro
- Caso o ficheiro tenha um tamanho razoável, demora algum tempo a ser reallizada a busca
- Podem ocorrer casos em que o alarme imprime que já diz que todos os ficheiros foram processados, mas ainda não foram imprimidos resultados

### Abordagem para a divisão dos ficheiros:

Os ficheiros dados como argumentos foram colocados numa lista e ordenados por tamanho (Do menor para maior). Esta ordenação é feita através da função ficheirosOrdenadosTamanho, que recebe como argumento a lista de ficheiros a ordenar.
realizando assim uma divisão justa por cada processo, certificando de que um ficheiro não é colocado numa lista mais do que as vezes que ele aparece na lista dos ficheiros, e certificando de que todos os ficheiros vão ficar numa lista.

### Outras informações pertinentes:

O tratamento dos argumentos não foi feito da melhor maneira possivel, dando possibilidade de caso ao utilizar o comando, não ser de acordo como está no enunciado, haja erros de execução

