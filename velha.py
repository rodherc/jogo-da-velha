#!/usr/bin/python3
#encode: utf-8

import os

class Velha:


    def __init__(self) :
        #Construtor da classe Velha.
        #Inicializa um tabuleiro vazio e seta a flag de empate para False.

        self.__board  = self.emptyBoard()
        self.__isDraw = False 
    
    ## Setter e Getter do Tabuleiro
    def setBoard(self, board) : self.__board = board
    def getBoard(self) : return self.__board

    ## Preenche o tabuleiro com um determinado valor ('X' ou 'O') nas posições x e y
    def setCoord(self, x, y, value) : self.__board[x][y] = value

    ## Retorna a flag indicativa de empate
    def isDraw(self) : return self.__isDraw
    
    ## Reseta o tabuleiro
    def resetBoard(self) : self.__board = self.emptyBoard() 

    ## Cria um tabuleiro vazio
    def emptyBoard(self): 
        return [ ['-','-','-'] , ['-','-','-'] , ['-','-','-'] ]

    ## Imprime o tabuleiro com suas coordenadas
    def printBoard(self) :
        os.system("clear") # Limpa a tela
        
        # Imprime instruções
        print("  _________________________________________________________________")
        print("\t::::::::::::::::: :JOGO DA VELHA: :::::::::::::::::")
        print("  -----------------------------------------------------------------\n\n")
        print("   Quando solicitado, digite uma coordenada válida da forma NxM, onde")
        print("   N é a linha")
        print("   M é a coluna\n")
        print("   Exemplo de coordenada: 1x3 (linha 1, coluna 3)\n\n")
        print("   ::Para sair, ao ser solicitada a coordenada, digite: EXIT\n\n")

        # Imprime o tabuleiro
        #print("\t1\t2\t3\n\t_________________")
        print("\t1\t2\t3\n\t-----------------")
        print("1|\t{}\t{}\t{}".format( self.__board[0][0], self.__board[0][1], self.__board[0][2]) )
        print("2|\t{}\t{}\t{}".format( self.__board[1][0], self.__board[1][1], self.__board[1][2]) )
        print("3|\t{}\t{}\t{}".format( self.__board[2][0], self.__board[2][1], self.__board[2][2]) )
            



    ## Verifica se alguém venceu.
    def isGameOver(self):
        #Este método verifica se houve algum vencedor. Durente o processo é verificado se houve empate, sendo assim
        #modificada a flag indicativa, mas o método não acusa o empate diretamente, apenas se alguém venceu.
        #return: flag indicativa de vitória.
        #rtype: boolean


        # Verifica se houve vencedor nas linhas e colunas.
        # Retorna verdadeiro em caso positivo.
        for i in range(3) :            
            if (( (self.__board[i][0] == self.__board[i][1] == self.__board[i][2]) and self.__board[i][0] != '-') or
                ( (self.__board[0][i] == self.__board[1][i] == self.__board[2][i]) and self.__board[0][i] != '-')
                ) : return True


        # Se não houve retorno nas verificações acima, então não houve vencedor pelas linhas e colunas, então é preciso
        # testar as diagonais.
        #
        # O Teste é feito por meio de um operador ternário, onde:
        #   resultado recebe falso se o valor na posição central do tabuleiro (utilizada por ambas as diagonais) for va-
        #   zio, senão, recebe o valor da disjunção entre a comparação de igualdade dos valores da diagonal principal e
        #   a comparação de igualdade dos valores da diagonal secundária.
        #
        # Perceba que este valor só pode ser 'True' ou 'False'
        # 'True' quando se constata vencedor pelas diagonais e 'Falso' em caso contrário.
        result = False if self.__board[1][1] == '-' else (
            (self.__board[0][0] == self.__board[1][1] == self.__board[2][2]) or
            (self.__board[0][2] == self.__board[1][1] == self.__board[2][0])
        )


        # A flag indicativa de empate recebe o valor atribuído a variável de resultado, pois talvez seja necessário veri-
        # ficar empate em caso do resultado ser falso.
        self.__isDraw = result

        # Se win for falso então pode ter ocorrido empate
        # Percorre o tabuleiro verificando se existem ocorrências de área(s) vazia(s).
        #
        # A disjunção entre a flag de empate e a verificação de posição vazia nas linhas irá resultar em 'True' caso haja
        # pelo menos uma posição vazia ou em 'False' caso não haja posição vazia no tabuleiro (o que caracteriza o empate).
        if not self.__isDraw :
            for i in range(3): 
                self.__isDraw = self.__isDraw or self.__board[i].__contains__('-') 
        

        # Nega a flag, pois:
        # Caso seja verdadeira: significa que foram encontrados espaços vazios, logo não houve empate.
        # Caso seja falsa: significa que não existem posições vazias no tabuleiro, logo houve empate.
        self.__isDraw = not self.__isDraw

        
        # Retorna o resultado da verificação das diagonais, pois este método verifica o empate apenas
        # indiretamente, o objetivo principal da função é verificar se houve vencedor para assim poder
        # melhor gerenciar quem venceu e quem perdeu.
        return result




    ## Verifica se uma mensagem é válida	
    def isValid(self, coord) :
    #   Verifica se uma jogada é válida.
    #    Uma jogada é válida se e somente se ela for EXIT ou NxM, onde N e M possuem domínio no
    #    intervalo [1,3], 'x', como caractere separador das variáveis, deve ser minúsculo e deve
    #    a posição referente à coordenada não pode estar preenchida, ou seja, deve estar repre-
    #    sentada pelo caractere '-'.
    #   Args:
    #     coord (str): jogada do usuário, deve ser uma coordenada do tipo NxM ou EXIT. 
    #   Returns:
    #        bool: True se for válida, False caso contrário.
        
    
        
        # Comando de saída, é válido!
        if coord == "EXIT" : 
            return True
        
        # coord deve ter tamanho 3 (NxM), se não o tem então é inválido!
        if len(coord) != 3 :
            print("\tFormato errado, o formato correto é NxM!") 
            return False
        
        # o caractere do meio tem que ser 'x' minúsculo, se não o é então é inválido!
        if coord[1] != "x":
            print("\tFormato errado, o formato correto é NxM!") 
            return False
        
        # os números devem estar no intervalo [1,3], se não estão é inválido!
        if coord[0] not in ["1", "2", "3"] or coord[2] not in ["1", "2", "3"] : 
            print("\tErro! As coordenadas devem estar no intervalo 1x1 a 3x3!")
            return False
        
        # Nesta verificação já foi constatado que a coordenada é válida.
        # Então verifica se a posição a qual a coordenada se refere está vazia.
        # Se estiver, então retorna True.
        if self.__board[int(coord[0])-1][int(coord[2])-1] == '-': return True
        
        # Se chegou até aqui então a coordenada é até válida, mas a posição já foi
        # utilizada previamente, não podendo ser sobrescrita de acordo com as regras
        # do jogo da velha, então retorna False.
        print("\tCoordenada já preenchida!")
        return False
