# Importa o módulo random para gerar números aleatórios.
import random

#Cria uma classe para representar um jogador
class Player:
    #Inicializa um jogador com um comportamento, um saldo inicial de 300 e uma lista vazia de propriedades.
    def __init__(self, behavior):
        self.behavior = behavior
        self.balance = 300
        self.properties = []
    #Retorna a posição atual do jogador no tabuleiro. Se não tiver nenhuma propriedade, retorna 0.
    def get_player_position(self, board):
        for i in range(len(board)):
            if board[i].owner == self:
                return i
        return 0  
    #O jogador joga o dado e move-se para a posição correspondente. Em seguida, o jogador verifica a propriedade na nova posição do tabuleiro.
    def play(self, board):
        steps = random.randint(1, 6)
        current_position = self.get_player_position(board)
        position = (current_position + steps) % len(board)
        property = board[position]
        #Se a propriedade não tiver proprietário, o jogador decide se quer comprá-la,
        #dependendo do seu comportamento. Se o jogador for impulsivo, ele sempre comprará.
        #Se o jogador for exigente, comprará apenas se o aluguel for superior a 50. 
        #Se o jogador for cauteloso, comprará apenas se tiver saldo suficiente 
        #(saldo - custo da propriedade >= 80). Se o jogador for aleatório, 
        # comprará apenas se a escolha aleatória for verdadeira.
        if property.owner is None:
            if self.behavior == "impulsive":
                self.buy_property(property)
            elif self.behavior == "demanding" and property.rent > 50:
                self.buy_property(property)
            elif self.behavior == "cautious" and self.balance - property.cost >= 80:
                self.buy_property(property)
            elif self.behavior == "random" and random.choice([True, False]):
                self.buy_property(property)
        #Se a propriedade tiver proprietário e não for o próprio jogador, o jogador pagará o aluguel ao proprietário.                
        elif property.owner != self:
            self.pay_rent(property.rent, property.owner)

    #Se o jogador decidir comprar a propriedade, ele deve ter saldo suficiente para pagar por ela.
    #Se ele tiver saldo suficiente, o jogador paga pelo valor da propriedade,
    #adiciona-a à sua lista de propriedades e define-se como proprietário da propriedade.
    def buy_property(self, property):
        if self.balance >= property.cost:
            self.balance -= property.cost
            self.properties.append(property)
            property.owner = self

    #Se o jogador não tiver saldo suficiente para pagar o aluguel, ele terá que vender
    #todas as suas propriedades para pagar a dívida. Se ele não tiver propriedades suficientes, 
    # ele será removido do jogo.
    def pay_rent(self, rent, owner):
        if self.balance >= rent:
            self.balance -= rent
            owner.balance += rent
        else:
            self.properties = [p for p in self.properties if p.owner != self]
            owner.properties += self.properties
            self.properties = []
            players.remove(self)

    def __str__(self):
        return f"{self.behavior} (balance: {self.balance})"

class Property:
    def __init__(self, cost, rent):
        self.cost = cost
        self.rent = rent
        self.owner = None

    def __str__(self):
        return f"Property (cost: {self.cost}, rent: {self.rent}, owner: {self.owner})"

board = [Property(50, 10), Property(100, 20), Property(150, 30),
         Property(200, 40), Property(250, 50), Property(300, 60),
         Property(350, 70), Property(400, 80), Property(450, 90),
         Property(500, 100), Property(550, 110), Property(600, 120),
         Property(700, 130), Property(750, 140), Property(800, 150),
         Property(850, 160), Property(900, 170), Property(950, 180),
         Property(1000, 190), Property(1050, 200)]

behaviors = ["impulsive", "demanding", "cautious", "random"]

wins = {behavior: 0 for behavior in behaviors}
turns = []
timeouts = 0

for i in range(300): # Executa 300 jogos para cada combinação de comportamentos
    random.shuffle(behaviors) # Embaralha a lista de comportamentos dos jogadores para cada jogo
    players = [Player(behavior) for behavior in behaviors] # Cria uma lista de jogadores com base nos comportamentos embaralhados
    board[0].owner = players[0] # Define o proprietário da primeira propriedade como o primeiro jogador da lista de jogadores
    for j in range(1000): # Executa até 1000 rodadas para cada jogo
        for player in players: #Loop através dos jogadores
            player.play(board) # Cada jogador joga uma rodada
            if len(players) == 1: # Se houver apenas um jogador restante, esse jogador venceu o jogo
                wins[player.behavior] += 1 # Adiciona uma vitória ao jogador vencedor
                break # Sai do loop dos jogadores
        else:
            continue # Continua a próxima rodada, caso não haja um jogador vencedor
        break # Sai do loop do jogo, pois há um jogador vencedor
    else:
        timeouts += 1  # Se não houver um vencedor em 1000 rodadas, conta como um timeout
    turns.append(j + 1) # Adiciona o número total de rodadas para o jogo atual na lista de rodadas

total_turns = sum(turns)  # Soma o total de rodadas para todos os jogos
avg_turns = total_turns / len(turns) # Calcula a média de rodadas por jogo

for behavior in behaviors: # Loop através dos comportamentos dos jogadores
    win_percentage = wins[behavior] / 300 * 100 # Calcula a porcentagem de vitórias para cada comportamento
    print(f"{behavior}: {win_percentage:.2f}%") # Imprime a porcentagem de vitórias para cada comportamento com duas casas decimais

most_wins = max(wins, key=wins.get) # Identifica o comportamento com mais vitórias
print(f"\n{most_wins} wins the most ({wins[most_wins]} times)")  # Imprime o comportamento com mais vitórias e o número de vezes que venceu

print(f"\n{timeouts} games ended in time out") # Imprime o número de jogos que acabaram em timeout

print(f"\nAverage number of turns per game: {avg_turns:.2f}") # Imprime a média de rodadas por jogo com duas casas decimais.