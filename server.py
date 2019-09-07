#!/usr/bin/python3
#encode: utf-8


import socket
from velha import Velha 

# Instancia o objeto Velha.
v = Velha()

## Informações do servidor: Host e porta para conexao.
Host = '127.0.0.1'
Port = 4242

## Criação do socket TCP e início de escuta.
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.bind((Host, Port))
socket_tcp.listen(5)

# Flag que indica se o servidor deve finalizar suas atividades.
isExit = False

# Mensagem de boas vindas ao jogo.
print ('Bem vindo ao Jogo da Velha 0.1!!')

# Laço para receber conexões
while not isExit:

	# Aguarda conexão.
	print ("\n\n\tAguardando novo participante...")
	conn, client_host = socket_tcp.accept()
	
	# Reseta o tabuleiro e o imprime na tela.
	v.resetBoard()
	v.printBoard()

	# Mostra na tela do servidor qual cliente se conectou.
	print ('\n\n\tParticipante ', client_host, ' conectou-se.')

	# Laço onde acontece o jogo
	while True:

		# Recebendo e decodificando a jogada do adversário.
		print("\n\tEsperando jogada do adversário.... Aguarde.")	
		data = conn.recv(1024) 
		result = data.decode()
		
		# Se os dados recebidos foram corrompidos ou se foi recebido um "EXIT",
		# então imprime uma mensagem dizendo que o cliente se desconectou,
		# reseta o tabuleiro e encerra o laço de conexão.
		if not data or result == "EXIT":
			print ('Participante ', client_host, ' desconectou.')
			v.resetBoard() # Reseta o tabuleiro
			break
		
		
		# Escreve 'X' (jogada do cliente) na posição recebida.
		v.setCoord(int(result[0]) - 1 , int(result[2]) - 1 , "X")
		v.printBoard()

		# Verifica se houve game over com a jogada do cliente. Em caso positivo
		# significa que o cliente ganhou, imprime mensagem dizendo que o servi-
		# dor foi derrotado e que o cliente está sendo desconectado. Encerra o
		# laço de conexão.
		if (v.isGameOver()) :
			print("\n\t:::::Você foi Derrotado! Boa sorte na próxima!")
			print ("\n\t::Fim de Jogo")
			print ('\tParticipante ', client_host, ' desconectado.\n')
			break
		
		# Se não houve game over (ninguém venceu), então verifica se houve algu-
		# ma mudança na flag indicativa de empate. Em caso positivo imprime men-
		# sagem de que houve empata e que o cliente está sendo desconectado. En-
		# cerra o laço de conexão.
		if (v.isDraw()):
			print("\n\t:::::Jogo Empatado!")
			print ("\n\t::Fim de Jogo")
			print ('\tParticipante ', client_host, ' desconectado.\n')
			break
		
		# Lê a jogada do servidor
		coord = input("\n\tCoord:  ")

		# Enquanto a jogada não for válida, isto é, não estiver no formato váli-
		# do ou indicar uma posição já preenchida do tabuleiro, então solicita
		# nova coordenada.
		while not v.isValid(coord) : 
			coord = input("\tDigite uma coordenada válida: ")

		# Envia a resposta validada e codificada para o cliente
		conn.send(coord.encode())
		
		# Se a jogada lida tiver sido "EXIT", então encerra a aplicação de forma
		# geral, isto é, encerra o servidor - o que desconecta o cliente automa-
		# ticamente.
		if coord == "EXIT":
			print ('\tAplicação encerrada.')
			print ('\tParticipante ', client_host, ' desconectado.\n')			
			v.resetBoard() 	# Reseta o tabuleiro
			isExit = True	# Flag que indica que o servidor encerrou-se
			break
		
		# Se a jogada lida não tiver sido um "EXIT", então preenche a coord e im-
		# prime o tabuleiro
		v.setCoord( int( coord[0] ) - 1 , int( coord[2] ) - 1 , "O" )
		v.printBoard()

		# Se, com a jogada do servidor, houve game over, então o servidor venceu.
		if v.isGameOver() : 
			print("\n\t:::::Você Ganhou! Parabéns!")
			print ("\n\t::Fim de Jogo")
			print ('\tParticipante ', client_host, ' desconectado.\n')
			break
		
		# Se não houve game over, então verifica se houve empate.
		if (v.isDraw()):
			print("\n\t:::::Jogo Empatado!")
			print ("\n\t::Fim de Jogo")
			print ('\tParticipante ', client_host, ' desconectado.\n')
			break

# Encerra a conexão do cliente
conn.close()