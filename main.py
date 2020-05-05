import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation

EMPTY = 0
RABBIT = 1
WOLF = 4
RABBIT_MAX_AGE = 700
WOLF_MAX_AGE = 5000

N = 128  # Grid size.

INITIAL_POP = 40  # Number of initial rabbits.
INITIAL_RABBITS = 50  # Number of initial rabbits.
INITIAL_WOLVES = 15  # Number of initial wolves.
REFRACTORY_PERIOD_RABBIT = 9
REFRACTORY_PERIOD_WOLF = 9

COLOR_RABBIT = (0, 255, 0)  # (r, g, b)
COLOR_WOLF = (255, 0, 0)  # (r, g, b)

class Rabbit:
    def __init__(self, age, sex, breed, pos=(0, 0)):
        """Called when class is instantiated."""
        self.age = age
        self.sex = sex
        self.pos = pos
        self.breed = breed


class Wolf:
    def __init__(self, age, sex, breed, pos=(0, 0)):
        self.age = age
        self.sex = sex
        self.pos = pos
        self.breed = breed


def initialize(grid, n):
    """Randomly initialize n rabbits and wolves."""
    initialized = 0
    while initialized < n:
        x = np.random.randint(0, N)
        y = np.random.randint(0, N)
        p = np.random.randint(0, N)
        q = np.random.randint(0, N)
        if grid[x][y] == EMPTY:
            grid[x][y] = RABBIT
            initialized += 1
        elif grid[p][q] == EMPTY:
            grid[p][q] = WOLF
            initialized += 1
    return grid


def random_walk(pos):
    """Randomly step in a direction and return a new position."""
    x, y = pos
    dx = np.random.choice([-1, 0, 1])
    dy = np.random.choice([-1, 0, 1])
    x_next = (x + dx) % N
    y_next = (y + dy) % N
    return x_next, y_next


def update(frame_num, img, grid, rabbits, wolves):
    # Update position of all rabbits and wolves.
    # updates position of all wolves
    for w in wolves:
        w.pos = random_walk(w.pos)
        w.age += 1
        if w.age == WOLF_MAX_AGE:
            wolves.remove(w)
            print("Rip old wolfie", len(wolves), len(rabbits))
        elif w.breed != 0:
            w.breed -= 1
    # Compare each wolf to every other wolf.
    for i in range(len(wolves)):
        for j in range(len(wolves)):
            a = wolves[i]
            b = wolves[j]
            if a is not b:
                if a.pos == b.pos:
                    if a.breed == 0 and b.breed == 0:
                        a.breed = REFRACTORY_PERIOD_WOLF
                        b.breed = REFRACTORY_PERIOD_WOLF
                        print('bow chica wow wow: doggy style', a.pos, len(wolves), len(rabbits))
                        new = Wolf(0, 'f', 10, a.pos)
                        wolves.append(new)
    # Wolf hunts rabbits if on same space
    for i in range(len(wolves)):
        for j in rabbits:
            a = wolves[i]
            if a.pos == j.pos:
                rabbits.remove(j)
                print('ATE A RABBIT')
    for n in rabbits:
        n.pos = random_walk(n.pos)
        n.age += 1
        if n.age == RABBIT_MAX_AGE:
            rabbits.remove(n)
            print("Old rabbit died", len(wolves), len(rabbits))
        if n.breed != 0:
            n.breed -= 1
    # Compare each rabbit to every other rabbit.
    for i in range(len(rabbits)):
        for j in range(len(rabbits)):
            a = rabbits[i]
            b = rabbits[j]
            if a is not b:
                if a.pos == b.pos:
                    if (a.age > 25) and (b.age > 25) and a.breed == 0 and b.breed == 0:
                        a.breed = REFRACTORY_PERIOD_RABBIT
                        b.breed = REFRACTORY_PERIOD_RABBIT
                        print('bow chica wow wow', a.pos, len(rabbits))
                        new = Rabbit(0, 'm', 0, a.pos)
                        rabbits.append(new)

# Draw the image to display. NxN pixels, each pixel has 3 color channels (r, g, b).
    next_grid = np.zeros((N, N, 3), dtype=np.uint8)
    for n in range(len(rabbits)):
        x = rabbits[n].pos[0]
        y = rabbits[n].pos[1]
        next_grid[x][y] = COLOR_RABBIT
    for n in range(len(wolves)):
        x = wolves[n].pos[0]
        y = wolves[n].pos[1]
        next_grid[x][y] = COLOR_WOLF

    img.set_data(next_grid)
    grid[:] = next_grid[:]
    return img


grid = np.zeros((N, N, 3), dtype=np.uint8)
# grid = initialize(grid, INITIAL_POP)


rabbits = []
for _ in range(INITIAL_RABBITS):
    x = np.random.randint(0, N)
    y = np.random.randint(0, N)
    age = np.random.randint(100, RABBIT_MAX_AGE)
    r = Rabbit(age, 'm', 0, (x, y))
    rabbits.append(r)

wolves = []
for _ in range(INITIAL_WOLVES):
    x = np.random.randint(0, N)
    y = np.random.randint(0, N)
    age = np.random.randint(100, WOLF_MAX_AGE)
    r = Rabbit(age, 'm', 0, (x, y))
    wolves.append(r)

fig, ax = plt.subplots()
img = ax.imshow(grid, vmin=-RABBIT_MAX_AGE, vmax=0)
ani = matplotlib.animation.FuncAnimation(fig, update,
                                         fargs=(img, grid, rabbits, wolves),
                                         frames=10,
                                         interval=50,
                                         save_count=50)

plt.show()
