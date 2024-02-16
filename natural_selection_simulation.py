"""
Simple Genetics and Natural Selection Simulation Program

Natural selection rules: There are initially 100 strategies. Every round, 500 pairs of strategies are selected to compete. The total scores are ranked, and the 50 least fit strategies are eliminated. Then, 50 offspring are randomly selected from the surviving strategies. Each offspring has an 80% chance of being identical to its parent and a 20% chance of mutation.

Strategy representation: The strategy is represented by a decision tree. The first layer takes the opponent's most recent choice as input; the second layer takes the opponent's second-to-last choice as input, and so on. The third branch is activated when the game has just started and there is no choice on that layer.

Mutation rules: A subtree of the decision tree is randomly selected for mutation. It can be transformed into an always-cooperate branch, an always-betray branch, or a new subtree.

Game rule: Modified Prisoner's Dilemma

+-----------+-----------+--------+
|           | Cooperate | Betray |
+-----------+-----------+--------+
| Cooperate |    2/2    | -1/3   |
+-----------+-----------+--------+
| Betray    |    3/-1   | 1/1    |
+-----------+-----------+--------+
"""

import random, copy
from collections import Counter

mutate1 = 25
mutate2 = 25
mutate3 = 25

def mutate(asdf):
  if isinstance(asdf, int):
    return random.choice([
      0, 1,
      [random.choice([0, 1]),
       random.choice([0, 1]),
       random.choice([0, 1])]
    ])
  x = random.randint(0, 100)
  if x <= mutate1: return [mutate(asdf[0]), asdf[1], asdf[2]]
  elif x <= mutate1 + mutate2: return [asdf[0], mutate(asdf[1]), asdf[2]]
  elif x == mutate1 + mutate2 + mutate3: return [asdf[0], asdf[1], random.choice([
      0, 1])]
  else:
    return random.choice([
      0, 1,
      [random.choice([0, 1]),
       random.choice([0, 1]),
       random.choice([0, 1])]
    ])


class Bot:

  def __init__(self, strategy):
    self.strategy = strategy
    self.score = 0

  def __str__(self):
    return "(" + str(self.strategy) + ", " + str(self.score) + ")"

  def getOperation(self, history):
    x = self.strategy
    while not isinstance(x, int) and history != []:
      x = x[history[0]]
      history = history[1:]
    if history == []:
      return 0
    return x

  def mutate(self):
    return Bot(mutate(self.strategy))

  def fight(self, opponent):
    history_x, history_y = [], []
    for i in range(100):
      history_x.append(2)
      history_y.append(2)
    for i in range(100):
      x, y = self.getOperation(history_x), opponent.getOperation(history_y)
      if x == 0 and y == 0:
        self.score += 2
      elif x == 0 and y == 1:
        self.score += -1
      elif x == 1 and y == 0:
        self.score += 3
      else:
        self.score += 1
      history_x = [y] + history_x
      history_y = [x] + history_y

#initial_species = [Bot([0, 1, 0]), Bot([0, [0, 1, 0], 1])]
initial_species = [Bot(0)] # Initially the whole population
pool_size = 100 # Total numbers of strategies
tournament_length = 500 # How many matches each round of selection will run
threshold = 80 # How many strategies will survive each round
mutation_rate = 0.01 # Mutation rate

pool = []
for i in range(pool_size):
  pool.append(copy.deepcopy(random.choice(initial_species))) # Initialization

while 1:
  for i in range(len(pool)):
    pool[i].score = 0
  for i in range(tournament_length):
    pool[random.randint(0,
                        len(pool) - 1)].fight(pool[random.randint(
                          0,
                          len(pool) - 1)])
  pool.sort(key=lambda x: x.score)
  print(Counter(list(map(lambda x: str(x.strategy), pool))).most_common(3))
  pool = pool[threshold:]
  for i in range(threshold):
    if random.random() < mutation_rate:
      pool.append(copy.deepcopy(pool[random.randint(0, len(pool) - 1)].mutate()))
    else:
      pool.append(copy.deepcopy(pool[random.randint(0, len(pool) - 1)]))
