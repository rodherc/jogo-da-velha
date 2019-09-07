#!/usr/bin/python3
#encode: utf-8


import socket
from velha import Velha

# Instancia o objeto Velha.
v = Velha()

# Flag indicativa de conexão estabelecida com sucesso
con = True

print ('Bem vindo ao Jogo da Velha 0.1!!')

# Laço de conexões
while True:
	
	# Informação do endereço do servidor ao qual se conectar.
	Host = input ( "\nEndereço IP do servidor: ")
	Port = 4242
	
	# Criacao do socket para comunicacao
	socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Tentativa de se conectar com o endereço fornecido.
	# Em caso de sucesso, a flag 'con' é setada como True.
	# Em caso de falha, a flag 'con' é setada como False.
	try:		
		socket_tcp.connect((Host, Port))
		print( "Conexão estabelecida!" )
		v.resetBoard() # Reseta o tabuleiro
		con = True
	
	except:
		print( "\nConexão não pôde ser estabelecida! Verifique o endereço." )
		con = False
	

	## laco para enviar mensagens
	while con:

		# Imprime o Tabuleiro
		v.printBoard()
		
		# lendo mensagem
		coord = input("\n\tCoord:  ")

		# Enquanto a jogada não for válida, isto é, não estiver no formato váli-
		# do ou indicar uma posição já preenchida do tabuleiro, então solicita
		# nova coordenada.
		while not v.isValid(coord) : 
			coord = input("\tDigite uma coordenada válida: ")
		
		# Se a jogada lida tiver sido "EXIT", então encerra a o laço de conexão
		# com o servidor.
		if coord == "EXIT":
			print ('\tAplicação encerrada.\n\tDesconectou-se.\n')
			break
		
		# Se a jogada lida não tiver sido um "EXIT", então preenche a coord e im-
		# prime o tabuleiro
		v.setCoord( int( coord[0] ) - 1 , int( coord[2] ) - 1 , "X" )
		v.printBoard()

		# Envia a jogada, validada e codificada, para o servidor
		socket_tcp.send(coord.encode())

		# Se, com a jogada do cliente, houve game over, então o cliente venceu.
		if v.isGameOver() : 
			print("\n\t:::::Você Ganhou! Parabéns!")
			print ("\n\t::Fim de Jogo")
			break

		# Se não houve game over, então verifica se houve empate.
		if (v.isDraw()):
			print("\n\t:::::Jogo Empatado!")
			print ("\n\t::Fim de Jogo")
			break

		
		# Senão, espera resposta do servidor.
		print("\n\tEsperando jogada do adversário.... Aguarde.")
		resposta = socket_tcp.recv(1024)
		resposta = resposta.decode()
		# 

		# Se os dados recebidos foram corrompidos ou se foi recebido um "EXIT",
		# então imprime uma mensagem dizendo que o servidor se desconectou,
		# reseta o tabuleiro e encerra o laço de conexão.
		if not resposta or resposta == "EXIT":
			print ('\n\tHost ', Host, ' desconectou-se.\n')
			v.resetBoard() # Reseta o tabuleiro
			break

		# Escreve 'O' (jogada do servidor) na posição recebida.
		v.setCoord(int(resposta[0])-1, int(resposta[2])-1, "O")
		v.printBoard()

		# Verifica se houve game over com a jogada do servidor. Em caso positi-
		# vo significa que o cliente ganhou, imprime mensagem dizendo que o cli-
		# ente foi derrotado. Encerra o laço de conexão.
		if v.isGameOver() :
			print("\n\t:::::Você foi Derrotado! Boa sorte na próxima!")
			print ("\n\t::Fim de Jogo")
			break

		# Se não houve game over (ninguém venceu), então verifica se houve algu-
		# ma mudança na flag indicativa de empate. Em caso positivo imprime men-
		# sagem de que houve empate. Encerra o laço de conexão.
		if (v.isDraw()):
				print("\n\t:::::Jogo Empatado!")
				print ("\n\t::Fim de Jogo")
				break

	# Fecha a conexão com o servidor
	socket_tcp.close()