
from Halo.classes import S_Grunt, I_Grunt, S_Jackel, H_Jackel, Elite
from Halo.classes import Spartan
from os import system
from Halo.batalha import Batalha
from time import sleep

class Jogo:
    
    AMARELO = '\033[33m'
    VERMELHO ='\033[1;31m'
    RESET ='\033[m'
    def __init__(self):
        self.player = Spartan()
        self.batalha = Batalha(self.player)

    def msg(self, msg:str, modo = 'digitado', tempo = 0.007):
        system('cls')
        if modo == 'digitado':
            c = '' 
            for i in msg:
                c = c + i# concatena parte da msg a cada iteração
                # sleep combinado com system('cls') para dar a impressão de digitar
                sleep(tempo)
                system('cls')
                print(f'{c}{Jogo.RESET}')# este RESET evita que após c concatenar 
                # a cor AMARELA a próxima iteração deixe em amarelo o que não deve

        if modo == 'de uma vez':
            print(msg)
                
    def intro(self):
        PAZ ='🖔'
        system('cls')
        msg = f'{Jogo.AMARELO}Este projeto foi baseado na franquia de sucesso Halo.\n\
Apesar da baixa qualidade esperamos que seja uma\n\
experiência interessante e que ela mereça ao menos\n\
um 7.0 na nota! {PAZ} {Jogo.VERMELHO}\n\
Para uma melhor experiência ABRA a janela do TERMINAL ao MÁXIMO!{Jogo.RESET}'
        self.msg(msg)
        print()
        input('Pressione qualquer tecla para prosseguir.')
    

    def menu(self):
        msg = f'Escolha o que deseja fazer a seguir.\n{Jogo.AMARELO}\
    (1) Iniciar batalha.\n\
    (2) Gerar estatisticas de ataque.\n\
    (3) Apresentar equipe de desenvolvimento.\n\
    (4) Sair do jogo.{Jogo.RESET}'
        self.msg(msg, tempo = 0.002)
        resposta = input('~> ')

        while True:
            if resposta not in ('1','2','3','4'):
                self.msg(msg, modo = 'de uma vez')
                resposta = input(f'Tente uma resposta valida\n~> ')
            else:
                break
        return resposta
    
    def estatisticas(self):
        REPETICAO = 500
        VIDA = 800 * REPETICAO
        
        personagens = (Spartan(),
                      S_Grunt(),
                      I_Grunt(),
                      S_Jackel(), 
                      H_Jackel(),
                      Elite())        
        so_grunt =(S_Grunt(), I_Grunt())
        saco_d_pancada = Spartan(VIDA) # essa VIDA permite que saco_d_pancadas
        # aguente ataque critico de todos por todas as repetições.

        #  O laço a seguir simula ataques de todos os tipos com os grunts sem vantagem
        for _ in range(REPETICAO):
            for e in personagens:
                if e.tipo =='Master Chief':
                    e.ataque(saco_d_pancada, simular = True)
                else:
                    e.ativar_escudo()
                    e.action(saco_d_pancada)
        system('cls')

        # O laço a seguir simula ataques dos tipos grunts com vantagem
        for _ in range(REPETICAO):
            so_grunt[0].action(saco_d_pancada, simular = True)
            so_grunt[1].action(saco_d_pancada, simular = True)
        system('cls')

        # Os 2 laços a seguir geram todas as estatisticas.
        print(f'{Jogo.AMARELO}Ataques de todos os personagens com os GRUNT SEM VANTAGEM:{Jogo.RESET}')
        for e in personagens:
            e.statistic()

        print()
        print(f'{Jogo.AMARELO}Ataques de todos os personagens com os GRUNT COM VANTAGEM:{Jogo.RESET}')
        for e in so_grunt:
            e.statistic()

    def equipe(self):
        inicio ='Desenvolvedores:'
        braw ='Brawner Alves Albuquerque'
        # Completar nome do pessoal e APAGAR ESSE COMENTÁRIO
        gisele = 'Gisele'
        natan = 'Natã'
        cat = 'Catarina'
        msg =f'{inicio:^60}\n\n{Jogo.AMARELO}{braw:^60}\n{gisele:^60}\n{natan:^60}\n{cat:^60}{Jogo.RESET}'
        self.msg(msg)

    def run(self):
        self.intro()
        
        while True:
            resposta = self.menu()
            if resposta == '1':
                self.batalha.batalha()
                print()
                input('Pressione qualquer tecla para prosseguir.')
                
            if resposta == '2':
                self.estatisticas()
                print()
                input('Pressione qualquer tecla para prosseguir.')
                
            if resposta == '3':
                self.equipe()
                print()
                input('Pressione qualquer tecla para prosseguir.')
                
            if resposta == '4':
                msg = f'{Jogo.VERMELHO}Jogo encerrado!!!{Jogo.RESET}'
                self.msg(msg)
                break
        pass
