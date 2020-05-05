
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation

EMPTY = 0
RABBIT = 1
WOLF = 2
MAX_AGE = 700
REFRACTORY_PERIOD = 10
N = 128  # Grid size.
INITIAL_RABBITS = 40  # Number of initial rabbits.
INITIAL_WOLVES = 40  # Number of initial wolves.

COLOR_RABBIT = (0, 255, 0)  # (r, g, b)
COLOR_WOLF = (255, 0, 0)  # (r, g, b)

class Rabbit:
    def __init__(self, age, sex, breed, pos=(0, 0)):
        """Called when class is instantiated."""
        self.age = age
        self.sex = sex
        self.pos = pos
        self.breed = breed


def initialize(grid, n):
    """Randomly initialize n rabbits."""
    initialized = 0
    while initialized < n:
        x = np.random.randint(0, N)
        y = np.random.randint(0, N)
        if grid[x][y] == EMPTY:
            grid[x][y] = RABBIT
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
    # Update position of all rabbits.
    for n in rabbits:
        n.pos = random_walk(n.pos)
        n.age += 1
        if n.age == MAX_AGE:
            rabbits.remove(n)
            print("Old fella died",  len(rabbits))
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
                        a.breed = REFRACTORY_PERIOD
                        b.breed = REFRACTORY_PERIOD
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
    age = np.random.randint(100, MAX_AGE)
    r = Rabbit(age, 'm', 0, (x, y))
    rabbits.append(r)

wolves = []
for _ in range(INITIAL_WOLVES):
    x = np.random.randint(0, N)
    y = np.random.randint(0, N)
    age = np.random.randint(100, MAX_AGE)
    r = Rabbit(age, 'm', 0, (x, y))
    wolves.append(r)

fig, ax = plt.subplots()
img = ax.imshow(grid)
ani = matplotlib.animation.FuncAnimation(fig, update,
                                         fargs=(img, grid, rabbits, wolves),
                                         frames=10,
                                         interval=50,
                                         save_count=50)

plt.show()
