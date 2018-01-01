number_of_game = 1

number_of_player = 2

b = 2
c = 1

# Actions (index in gammas)

C = 0
D = 1

gamma0 = [[b - c, -c],
          [b, 0]]

gamma1 = [[b - c, 0],
          [0, 0]]

# Probability p to be in gamma1 ( 1-p in gamma 0)
p = 0.5

# Distribution cost
cost_dist_type = "uniform"
d = 20
cost_dist = [0, d]

# Intuitive play

xI = C

player1_int = xI
player2_int = xI

# Deliberation play

x0 = D  # Delib. play for gamma0
x1 = C  # Delib. play for gamma1
