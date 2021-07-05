'''
Implementações: 
1) ajeitar as taxas de erro corretamente
2) pensar em como evitar o critico do segundo tiro dos jackels
3) como ajustar a estatistica dos jackels para expressar o dano*3
'''
# SIMBOLOS
# SKULL = '🕱'
# CORACAO = '♥'
# SHIELD = '⛨'
# BALA = '✐'
# LUGAR = '⦿'
from random import  choices

class Personagem:
    '''
    Cria um objeto da classe Personagem.

    Variaveis de classe:
    --------------------
    mod_dano: uma tupla com 3 valores usados para determinar e 
    ajustar o dano entre erro, normal e crítico.

    variaveis de cores: utilizadas para colorir menssagem printaveis
    e reset para marca final da coloração. 
    As cores disponiveis são: VERDE, VERMELHO, AZUL e RESET

    Atributos:
    ----------
    self.vida_max: int
       um valor de vida passado e q será decrementado ao receber dano.
    
    self.vida_atual: int
       um valor de vida passado e q será referencia de máx possivel.
    
    self.dano: int
       valor fixo de 10.
    
    self.status_escudo: str
       determina se o escudo está ativado e impacta na mecanicas de batalha. Default:'desativado'.
    
    self.escudo_atual: int 
       um valor de escudo passado e q será decrementado ao receber dano. Default:0.
    
    self.escudo_max: int
       um valorde escudo passado e q será referencia de máx possivel. Default: 0.
    
    Metodos:
    --------
    ataque(self, other): verifica se o oponente está protegido por escudo ou não
    e sorteia a partir de uma distribuição de probabilidade o tipo de ataque. imprime no terminal
    quem atacou e quem foi atacado.
    
    ativar_escudo(self):  verifica se o escudo está desativado e em caso afirmativo
    muda status_escudo para 'ativado'.
    
    status(self): retorna uma lista com situação de vida e escudo formatados em string
    com cor, cada status é um elemento da lista

    statistic(self): gera estatisticas de ataque
    '''
    mod_dano = (0, 1, 2) #(erro, normal, critico)
    
    VERDE ='\033[32m'
    VERMELHO ='\033[1;31m'
    AZUL='\033[34m'
    RESET='\033[m'

    def __init__(self, vida= 0, esc=0):
        '''
        Constroi todos os atributos necessarios para criar um objeto Personagem

        Parametro:
        ----------
        vida: quantidade de vida do personagem
        esc: quantidade de escudo do personagem
        '''
        self.vida_max = vida
        self.vida_atual = vida
        self.dano = 10
        self.status_escudo = 'desativado'
        self.escudo_atual = esc
        self.escudo_max = esc
        self.erros = 0
        self.normais = 0
        self.criticos = 0

    def ataque(self, other: object):
        '''
        Coordena mecanica basica de ataque e atualiza a vida restante do adversário.
        '''
        mod = choices(self.mod_dano, self.taxa_falha)[0] # Sorteio para saber se erra, acerta ou é crítico
                                                # A taxa_falha é um atributo das classes que herdarão esta.
        if mod == 0:
            self.erros += 1
        if mod == 1:
            self.normais += 1
        if mod == 2:
            self.criticos += 1

        if self.vida_atual > 0:
            if other.status_escudo == 'ativado':
                dif = other.escudo_atual - self.dano * mod
                if dif > 0:
                    other.escudo_atual = dif
                else:
                    other.escudo_atual = 0
                    other.status_escudo = 'destruido'
                # Bloco de msgs a seguir
                if self.tipo != 'Master Chief':
                    print(f'{self.nome:>40} causou {self.dano * mod} de dano ao escudo de {other.nome}')
                else:
                    print(f'{self.nome} causou {self.dano * mod} de dano ao escudo de {other.nome}')

            else:
                dif = other.vida_atual - self.dano * mod
                if dif > 0:
                    other.vida_atual = dif
                else:
                    other.vida_atual = 0
                # Bloco de msgs a seguir
                if self.tipo != 'Master Chief':
                    print(f'{self.nome:>40} causou {self.dano * mod} de dano a vida de {other.nome}')
                else:
                    print(f'{self.nome} causou {self.dano * mod} de dano a vida de {other.nome}')
    
    def ativar_escudo(self):
        '''
        Muda status_escudo para 'ativado'
        '''
        self.status_escudo = 'ativado'

    def status(self): 
        '''
        Retorna lista com status formatado por fstring. 1º elemento é vida e 2º elemento é escudo
        
        Formato:        
        com escudo ativado ~> [♥: x/x, ⛨: y/y]
        com escudo desativado ~> [♥: x/x, '']
        '''
        CORACAO = '♥'
        SHIELD = '⛨'
        VAZIO=''

        if self.status_escudo == 'ativado' or self.status_escudo == 'destruido':
            msg = [f'{Personagem.VERMELHO}{CORACAO}{Personagem.RESET}: {self.vida_atual}/{self.vida_max}',
                   f'{Personagem.AZUL}{SHIELD}{Personagem.RESET} : {self.escudo_atual}/{self.escudo_max:<43}']
                   # esse :<43 depois de self.escudo_max é um ajuste para alinhar os icones durante a exibição
                   #o valor foi conseguido experimentalmente
        else:
            msg = [f'{Personagem.VERMELHO}{CORACAO}{Personagem.RESET}: {self.vida_atual}/{self.vida_max}',f'{VAZIO:9}']
            # esse :9 depois de VAZIO é um ajuste para alinhar os icones durante a exibição
            #o valor foi conseguido experimentalmente.
        return msg

    def statistic(self):
        '''
        Gera estatisticas de ataque
        '''
        ataques_totais = self.erros + self.normais + self.criticos
        print(f'Ataques de {self.nome}:')
        print(f'    Erros: {self.erros/ataques_totais:.3f} %')
        print(f'    Ataques normais: {self.normais/ataques_totais:.3f} %')
        print(f'    Ataques críticos: {self.criticos/ataques_totais:.3f} %')

class S_Grunt(Personagem):
    '''
    Subclasse de Personagem. Cria um objeto da classe S_Grunt
    
    Atributos:
    ----------
    self.tipo: str
       'S_Grunt'
    
    self.nome: fstring
        f'{Personagem.VERMELHO}{self.tipo} {Personagem.RESET}'
    
    self.taxa_falha: tuple
        distribuição de probabilidade de acerto. Default: (0.15, 0.595, 0.255)
    
    Metodos próprios:
    -----------------
    avaliar_vantagem(self, dict, simular): recebe um dicionario com todos os inimigos e verifica quantos são variação de grunt
    e, estão vivos então ajusta a taxa_falha e o mod_dano de acordo.

    action(self, other, dict): organiza as ações desse tipo de inimigo a serem execultadas em jogo.
    '''
    def __init__(self, vida = 15):
        '''
        Constroi todos os atributos necessarios para criar um objeto S_Grunt.

        Parametro
        ---------
        vida: quantidade de vida do personagem
        esc: quantidade de escudo do personagem
        '''
        super().__init__(vida)
        self.tipo = 'S_Grunt'
        self.nome = f'{Personagem.VERMELHO}{self.tipo} {Personagem.RESET}'
        self.taxa_falha = (0.15, 0.595, 0.255)

    def avaliar_vantagem(self, dici: dict, simular = False):
        '''
        Parametros:
        -----------
        dici: dict
            dicionários com inimigos com chaves sendo string de numeros. ex: "1"
        simular: bool
            faz com que simule vantagem. utilizado para gerar estatisticas atraves do metodo estatistica()
            que deve se encontrar no script jogo.py

        Avalia se tem vantagem numerica dentre o grupo de inimigos vivos e ajusta taxa_falha e mod_dano
        Quando em desvantagem não consegue dá ataques críticos.
        '''
        count = 0
        VANTAGEM = 3
        if dici != {}: # Dicionario vazio ocorre quando os ataques estão sendo simulados 
            for e in dici:
                if (dici[e].tipo == 'S_Grunt' or dici[e].tipo == 'I_Grunt') and (dici[e].vida_atual != 0):
                    count += 1

        if count >= VANTAGEM or simular == True:
            self.mod_dano = (0, 1, 2)
            self.taxa_falha = (0.15, 0.595, 0.255)
            print(f'{self.nome:>40} está em vantagem.')
            
        else:
            self.mod_dano = (0, 1)
            self.taxa_falha = (0.6, 0.4)
            print(f'{self.nome:>40} está em desvantagem.')

    def action(self, other: object, dici = {}, simular = False):
        '''
        Organiza as ações desse tipo de inimigo a serem execultadas em jogo.
        '''
        # dici = {} e simular = False são necessarios para gerar estatisticas 
        self.avaliar_vantagem(dici, simular)
        self.ataque(other)
    
class I_Grunt(Personagem):   
    '''
    Subclasse de Personagem. Cria um objeto da classe S_Grunt
    
    Atributos:
    ----------
    self.tipo: str
       'S_Grunt'
    
    self.nome: fstring
        f'{Personagem.VERMELHO}{self.tipo} {Personagem.RESET}'
    
    self.taxa_falha: tuple
        distribuição de probabilidade de acerto. Default: (0.15, 0.595, 0.255)
    
    Metodos próprios:
    -----------------
    avaliar_vantagem(self, dict, simular): recebe um dicionario com todos os inimigos e verifica quantos são variação de grunt
    e, estão vivos então ajusta a taxa_falha e o mod_dano de acordo.

    action(self, other, dict): organiza as ações desse tipo de inimigo a serem execultadas em jogo.
    ''' 

    def __init__(self, vida=20):
        '''
        Constroi todos os atributos necessarios para criar um objeto I_Grunt.

        Parametro
        ---------
        vida: quantidade de vida do personagem
        esc: quantidade de escudo do personagem
        '''
        super().__init__(vida)
        self.tipo = 'I_Grunt'
        self.nome = f'{Personagem.VERMELHO}{self.tipo} {Personagem.RESET}'
        self.taxa_falha = (0.2, 0.62, 0.18)

    def avaliar_vantagem(self, dici:dict, simular = False):
        '''
        Parametros:
        -----------
        dici: dict
            dicionários com inimigos com chaves sendo string de numeros. ex: "1"
        simular: bool
            faz com que simule vantagem. utilizado para gerar estatisticas atraves do metodo estatistica()
            que deve se encontrar no script jogo.py

        Avalia se tem vantagem numerica dentre o grupo de inimigos vivos e ajusta taxa_falha e mod_dano.
        '''
        count = 0
        VANTAGEM = 2
        if dici != {}: # Dicionario vazio ocorre quando os ataques estão sendo simulados 
            for e in dici:
                if (dici[e].tipo == 'S_Grunt' or dici[e].tipo == 'I_Grunt') and (dici[e].vida_atual != 0):
                    count += 1

        if count >= VANTAGEM or simular == True:
            self.taxa_falha = (0.2, 0.62, 0.18) 
            print(f'{self.nome:>40} está em vantagem.')
        else:
            self.taxa_falha = (0.45, 0.495, 0.055)
            print(f'{self.nome:>40} está em desvantagem.')

    def action(self, other, dici = {}, simular = False):
        '''
        Organiza as ações desse tipo de inimigo a serem execultadas em jogo.
        '''
        # dici = {} e simular = False são necessarios para gerar estatisticas 
        self.avaliar_vantagem(dici, simular)
        self.ataque(other)
        
class S_Jackel(Personagem):
    '''
    Subclasse de Personagem. Cria um objeto da classe S_Jackel

    Atributos próprios:
    ------------------- 
    self.tipo: str
        'S_Jackel'

    self.nome: fstring
        f'{self.VERMELHO}{self.tipo} {self.RESET}'
    
    self.taxa_falha:tuple
        distribuição de probabilidade de acerto. Default: (0.3, 0.1785, 0.448, 0.0735)

    Metodos próprios:
    -----------------
    ataque(self, other, mod): esse metodo sobrescreveu o herdado para receber um valor
    de modificador de dano externo. Sorteia o tipo de ataque e ajusta a vida_atual do inimigo

    action(self, other): organiza as ações desse personagem.
    '''
    def __init__(self, vida = 30, esc = 15):
        '''
        Constroi todos os atributos necessarios para criar um objeto S_Jackel.

        Parametro
        ---------
        vida: quantidade de vida do personagem
        esc: quantidade de escudo do personagem
        '''
        super().__init__(vida, esc)
        self.tipo = 'S_Jackel'
        self.nome = f'{self.VERMELHO}{self.tipo} {self.RESET}'
        self.taxa_falha = (0.3, 0.1785, 0.448)
 
    def ataque(self, other:object, mod:int):
        '''
        Esse metodosobrescreveu o herdado para receber um valor
        de modificador de dano externo, mod. Sorteia o tipo de ataque e ajusta a vida_atual do inimigo
        '''
        if self.vida_atual > 0:
            if other.status_escudo == 'ativado':
                dif = other.escudo_atual - self.dano * mod
                if dif > 0:
                    other.escudo_atual = dif
                else:
                    other.escudo_atual = 0
                    other.status_escudo = 'destruido'
                print(f'{self.nome:>40} causou {self.dano * mod} de dano ao escudo de {other.nome}')

            else:
                dif = other.vida_atual - self.dano * mod
                if dif > 0:
                    other.vida_atual = dif
                else:
                    other.vida_atual = 0
                print(f'{self.nome:>40} causou {self.dano * mod} de dano a vida de {other.nome}')

    def action(self, other:object, inim ={}):
        '''
        Organiza as ações desse tipo de inimigo a serem execultadas em jogo. Tem a particularidade de caso acerte
        o primeiro ataque execulta em seguida um segundo ataque este herdado da Superclasse, caso contrario
        não ataca uma segunda vez.
        '''
        mod = choices(self.mod_dano, self.taxa_falha)[0]
        
        if self.status_escudo == 'desativado':
            self.ativar_escudo()
            print(f'{self.nome:>40} ativou o escudo')

        elif mod != 0: # Teste para saber se haverá dois golpes ou nenhum.
            self.ataque(other, mod) # Metodo ataque local para primeiro golpe.
            super().ataque(other) # Evocação do metodo ataque da superclasse para o segundo golpe.  
        else:
            print(f'{self.nome:>40} errou o primeiro ataque e não deferiu o segundo.')         

class H_Jackel(Personagem):
    '''
    Subclasse de Personagem. Cria um objeto da classe S_Jackel

    Atributos próprios:
    ------------------- 
    self.tipo: str
        'S_Jackel'

    self.nome: fstring
        f'{self.VERMELHO}{self.tipo} {self.RESET}'
    
    self.taxa_falha:tuple
        distribuição de probabilidade de acerto. Default: (0.3, 0.1785, 0.448)

    Metodos próprios:
    -----------------
    ataque(self, other, mod): esse metodo sobrescreveu o herdado para receber um valor
    de modificador de dano externo. Sorteia o tipo de ataque e ajusta a vida_atual do inimigo

    action(self, other): organiza as ações desse personagem. 
    '''
    def __init__(self, vida = 40, esc = 30):
        '''
        Constroi todos os atributos necessarios para criar um objeto S_Jackel.

        Parametro
        ---------
        vida: quantidade de vida do personagem
        esc: quantidade de escudo do personagem
        '''
        super().__init__(vida, esc)
        self.tipo = 'H_Jackel'
        self.nome = f'{self.VERMELHO}{self.tipo} {self.RESET}'
        self.taxa_falha = (0.09, 0.3885, 0.448)

    def action(self, other:object, inim ={}):
        '''
        Organiza as ações desse tipo de inimigo a serem execultadas em jogo.
        '''
        if self.status_escudo == 'desativado':
            self.ativar_escudo()
            print(f'{self.nome:>40} ativou o escudo')

        else:
            self.ataque(other)
            self.ataque(other)

class Elite(Personagem):
    '''
    Subclasse de Personagem. Cria um objeto da classe Elite.

    Atributos próprios:
    ------------------- 
    self.tipo: str
        'Elite'

    self.nome: fstring
        f'{self.VERMELHO}{self.tipo} {self.RESET}'
    
    self.taxa_falha:tuple
        distribuição de probabilidade de acerto. Default: (0.3, 0.595, 0.105)

    Metodos próprios:
    -----------------
    action(self, other): organiza as ações desse personagem.
    '''
    def __init__(self, vida = 70):
        '''
        Constroi todos os atributos necessarios para criar um objeto Elite.

        Parametro
        ---------
        vida: quantidade de vida do personagem
        '''
        super().__init__(vida)
        self.tipo = 'Elite'
        self.nome = f'{Personagem.VERMELHO}{self.tipo} {Personagem.RESET}'
        self.taxa_falha = (0.3, 0.595, 0.105)
    
    def action(self, other:object, inim ={}):
        '''
        Organiza as ações desse tipo de inimigo a serem execultadas em jogo.
        '''
        self.ataque(other)

class Spartan(Personagem):
    '''
    Subclasse de Personagem. Cria um objeto da classe Spartan
    
    Atributos próprios:
    -------------------
    self.tipo: str
        'Master Chief'.

    self.nome: fstring
        f'{Personagem.AZUL}{self.tipo}{Personagem.RESET}'.

    self.taxa_falha: tuple
        distribuição de probabilidade de acerto. Default: (0.3, 0.595, 0.105).

    self.municao_atual: int
        Representa a munição disponivel para uso. Default:5.

    self.municao_max:
        Representa a munição total possivel. Default:5.
    
    Metodos próprios:
    -----------------
    regenerar_escudo(self): retorna os status do escudo para como eram no momento da ativação.

    ataque(self): sobrescreve o metodo da classe Personagem adicionando uum condição que
    verifica se há munição que após o ataque é decrementada em 1. 

    recarregar_arma(self): retorna os status da munição para como eram no momento da ativação.
    
    status(self): sobrescreve o metodo de Personagem para adicionar o status de munição a lista.

    action(self: object, inim:dict): apresenta as possibilidades de ação e recolhe entrada do
    jogador para processar ações.
    '''
    def __init__(self, vida = 500, esc = 100):
        '''
        Constroi todos os atributos necessarios para criar um objeto Spartan.

        Parametro
        ---------
        vida: quantidade de vida do personagem
        esc: Quantidade de escudo max do personagem
        '''
        super().__init__(vida, esc)
        self.tipo = 'Master Chief'
        self.nome = f'{Personagem.AZUL}{self.tipo}{Personagem.RESET}'
        self.taxa_falha = (0.3, 0.595, 0.105)
        self.municao_atual = 5
        self.municao_max = 5

    
    def regenerar_escudo(self):
        '''
        Caso self.status_escudo == 'ativado' and self.escudo_atual < self.escudo_max
        a cada turno self.escudo_atual =  self.escudo_max
        '''
        if self.status_escudo == 'ativado' and self.escudo_atual < self.escudo_max:
            self.escudo_atual =  self.escudo_max
            print(f'{self.nome} regenerou escudo')

    def ataque(self, other:object, simular = False):
        '''
        Sobrescreve o metodo da classe Personagem adicionando uum condição que
        verifica se há munição que após o ataque é decrementada em 1. 
        '''
        # Simular é importante para a geração de estatisticas, pois quando for
        # True ignora a contagem de munição.
        if simular == True:
            super().ataque(other)
        else: 
            if self.municao_atual > 0:
                super().ataque(other)
            self.municao_atual-=1

    def recarregar_arma(self):
        '''
        Faz: self.municao_atual = self.municao_max
        '''
        self.municao_atual = self.municao_max

    def status(self):
        '''
        Sobrescreve o metodo da classe Personagem para adicionar o status de munição
        como terceiro elemento da lista de retorno.

        Formato:        
        com escudo ativado ~> [♥: x/x, ⛨: y/y, ✐: z/z]
        com escudo desativado ~> [♥: x/x, '', ✐: z/z]
        '''        
        BALA = '✐'
        VAZIO = ''

        r = super().status()
        r.append(f'{Personagem.VERDE}{BALA:}{Personagem.RESET} : {self.municao_atual}/{self.municao_max}{VAZIO:^10}')
        # Esse :^10 depois de self.municao_max é um ajuste para alinhar os icones durante a exibição
        return r # r é uma lista de tamanho 3.

    def action(self: object, inim:dict = {}):
        '''
        apresenta as possibilidades de ação e recolhe entrada do
        jogador para processar ações.
        '''
        # O defalt de inim é um dicionario vazio para não crashar a
        # aplicação durante a geração de estatisticas por falta deste parametro.  
        self.regenerar_escudo() # regeneração passiva do escudo

        print('Escolha uma ação:')
        # Apresentação de ações de acordo com as possibilidades
        if self.status_escudo == 'desativado':
            print('(A)tivar escudo \n(At)acar inmigo \n(R)ecarregar arma')
        else:
            print('(At)acar inmigo \n(R)ecarregar arma')
        
        escolha = input('~> ').title()
        while True: # Laço para garantir entrada correta
            if escolha not in 'AtR':
                escolha = input('Tente uma opção valida\n~> ').title()
            elif escolha =='A' and self.status_escudo != 'desativado':
                escolha = input('Tente uma opção valida\n~> ').title()
            else:
                break

        # Execução das ações de acordo com a escolha do jogador
        if escolha == 'A':
            self.ativar_escudo()
            print(f'{self.nome} ativou escudo.')

        elif escolha == 'At':
            print('Escolha o inimigo: ')

            i = input('~>').lower() 
            while i not in ('1', '2', '3', '4', '5'):# Laço para garantir entrada correta
                print('Escolha um inimigo valido')
                i = input('~>').lower()

            self.ataque(inim[i])

        elif escolha == 'R':
            self.recarregar_arma()
