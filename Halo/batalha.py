from random import choices
from Halo.classes import S_Grunt, I_Grunt, S_Jackel, H_Jackel, Elite
from os import system
from time import sleep

class Batalha:
    '''
    Cria um objeto da classe batalha que administra confronto no jogo.

    Variaveis de classe:
    --------------------
    variaveis de cores: utilizadas para colorir menssagem printaveise reset para 
    marca final da coloração. 
    As cores disponiveis são: VERDE, VERMELHO, AZUL e RESET
    QNT_INIM: um numero fixo que estabelece a quantidade de inimigos criados
    
    Atributos:
    ----------
    self.player:
        objeto da classe Spartan

    self.inimigos:
        dicionario contendo objetos sorteados de diversasa classes que compoem os inimigos 
    
    Metodos:
    --------
    verificar_vencedor(self): 
        retorna vencedor, player ou inimigos, caso exista.

    arena(self): 
        imprime a arena de batalha com os participantes e seus status alinhados.

    acoes(self, num: int): 
        administra a ordem de ataque atraves do parametro num que vale de 0 a 5.

    batalha(self): 
        administra toda a batalha até haver um vencedor
    '''
    VERDE ='\033[32m'
    VERMELHO ='\033[1;31m'
    AMARELO = '\033[33m'
    AZUL='\033[34m'
    RESET='\033[m'
    QNT_INIM = 5

    def __init__(self,player):
        '''
        Constroi todos os atributos necessários para criar um objeto Personagem.

        Parametro:
        ----------
        player:
            objeto do tipo Spartan
        '''
        system('cls')

        inimigos={}
        for i in range(Batalha.QNT_INIM):
            PROB_INIM = (0.3, 0.3, 0.15, 0.15, 0.1) # probabilidade de sorteio dos inimigos
            INIM= (S_Grunt(), I_Grunt(), S_Jackel(), H_Jackel(), Elite())
            aux = choices(INIM, PROB_INIM)[0]
            inimigos[f'{i+1}'] = aux

        self.player = player
        self.inimigos = inimigos
        
    def verificar_vencedor(self):
        '''
        Verifica a vida dos inimigos e do player e retorna o vencedor caso existe
        caso contrario retorna string vazia.
        '''
        vencedor = 'Você'
        i = self.inimigos
        if self.player.vida_atual == 0:
            vencedor = 'Inimigos'
        else:
            for k in i:
                if i[k].vida_atual != 0:
                    vencedor =''
        return vencedor

    def arena(self):
        '''
        Organiza a disposição dos inimigos e player exibindo seus status.
        '''
        p = self.player
        i = self.inimigos
        VAZIO =''
        titulo= 'ARENA'
        SKULL = '🕱'

        print(f'{Batalha.AMARELO}{titulo:^65}')
        print(f'{Batalha.AMARELO}={Batalha.RESET}'*65) # imprime o limite superior da arena de batalha
        for k in i:
            # A condicional a seguir verifica se o inimigo da vez está vivo.
            # caso esteja s recebe a chave do dicionario referente a ele
            # caso esteja morto, s recebe '🕱' para indicar inimigo morto
            if i[k].vida_atual != 0:
                s=k
            else:                
                s= SKULL

            # A condicional a seguir imprimi o inimigo em questão e seu status alinhado a direita.
            # caso o inimigo seja o terceiro a impressão é adaptada para acomodar tambem o personagem
            # do jogador na msm linha. 
            if k == '3':
                print(f'{p.nome:<58}({s}){i[k].nome}')
                print(f'{p.status()[0]:<59}{i[k].status()[0]}') # Valores de alinhamento foram conseguidos experimentalmente
                print(f'{p.status()[1]:<50}{i[k].status()[1]}')
                print(f'{p.status()[2]}')
                print()
            else:
                print(f'{VAZIO:>50}({s}){i[k].nome}')
                print(f'{VAZIO:>52}{i[k].status()[0]}')
                print(f'{VAZIO:>51}{i[k].status()[1]}')
                print()

        print(f'{Batalha.AMARELO}={Batalha.RESET}'*65) # imprime o limite inferior da arena de batalha
                              
    def acoes(self, num:int):
        '''
        Recebe inteiro de 0 a 5 que determina a ordem de atuação dos personagens. 
        O primeiro valor deve ser igual a 0, correspondendo ao jogador.
        '''
        COUNT = num
        TIME = 0.8
        if COUNT == 0:
            self.player.action(self.inimigos)
            sleep(TIME)
        if COUNT == 1:
            self.inimigos['1'].action(self.player, self.inimigos)
            sleep(TIME)
        if COUNT == 2:
            self.inimigos['2'].action(self.player, self.inimigos)
            sleep(TIME)
        if COUNT == 3:
            self.inimigos['3'].action(self.player, self.inimigos)
            sleep(TIME)
        if COUNT == 4:
            self.inimigos['4'].action(self.player, self.inimigos)
            sleep(TIME)
        if COUNT == 5:
            self.inimigos['5'].action(self.player, self.inimigos) 
            sleep(TIME)    
        
    def batalha(self):
        '''
        Utiliza os outros metodos da classe para apresentar a batalha entre jpgador e máquina.
        sempre limpando o terminal a cad interação.
        '''
        system('cls')
        NUM = 0
        winner = ''
        while True:
            winner = self.verificar_vencedor()
            system('cls')
            self.arena()
            if winner != '': break # essa condição garante q arena exibirá todos os
            # mortos atualizados e sairá antes de chamar self.acoes(num) novamente. 
            self.acoes(NUM)
            if NUM < 5:
                NUM += 1
            else:
                NUM = 0     
                
        if winner == 'Você':
            print(f'Parabêns! {winner} venceu!')
        else:
            print(f'{winner} venceram! Que pena, tente outra vez.')
