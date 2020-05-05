import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation

MAX_AGE_RABBIT = 700
MAX_AGE_WOLF = 500

N = 128  # Grid size.

INITIAL_RABBITS = 15  # Number of initial rabbits.
INITIAL_WOLVES = 15  # Number of initial wolves.
INITIAL_GRASS = 300
REFRACTORY_PERIOD_RABBIT = 9
REFRACTORY_PERIOD_WOLF = 9

GRASS_RATE = 0.1

CALORIES_MAX = 100
CALORIES_MEAL = 25

COLOR_GRASS = (0, 255, 0)
COLOR_RABBIT = (0, 0, 255)  # (r, g, b)
COLOR_WOLF = (255, 0, 0)  # (r, g, b)


class Grass:
    def __init__(self, pos, rate, calories):
        self.pos = pos
        self.rate = rate
        self.calories = calories

    def grow(self):
        self.calories += self.rate
        self.calories = min(self.calories, CALORIES_MAX)


class Animal:
    def __init__(self, pos, age, sex, breed, calories):
        """Called when class is instantiated."""
        self.pos = pos
        self.age = age
        self.sex = sex
        self.breed = breed
        self.calories = calories


def random_walk(pos):
    """Randomly step in a direction and return a new position."""
    x, y = pos
    dx = np.random.choice([-1, 0, 1])
    dy = np.random.choice([-1, 0, 1])
    x_next = (x + dx) % N
    y_next = (y + dy) % N
    return x_next, y_next


def random_gender():
    """Randomly generate a male or female gender with equal probability."""
    return 'm' if np.random.random() > 0.5 else 'f'


def update_animals(animals, max_age):
    for a in animals:
        a.pos = random_walk(a.pos)
        a.age += 1
        a.calories -= 1
        a.breed = max(a.breed - 1, 0)
        if a.age >= max_age or a.calories <= 0:
            animals.remove(a)


def breed(animals, refractory_period):
    for a in animals:
        for b in animals:
            # Can't do it with yourself.
            if a is b:
                continue
            # Skip if breed timer is active.
            if a.breed > 0 or b.breed > 0:
                continue
            # Skip if same sex.
            if a.sex == b.sex:
                continue
            # Breed.
            child = Animal(pos=a.pos,
                           age=0,
                           sex=random_gender(),
                           breed=refractory_period,
                           calories=CALORIES_MEAL)

            animals.append(child)
            # Set breed timer.
            a.breed = refractory_period
            b.breed = refractory_period


def feed(predators, prey):
    for predator in predators:
        for meal in prey:
            if predator.pos == meal.pos:
                predator.calories += CALORIES_MEAL
                predator.calories = min(predator.calories, CALORIES_MAX)
                prey.remove(meal)

def grow(grass):
    for g in grass:
        g.grow()
        if g.calories == CALORIES_MAX:
            adj = random_walk(g.pos)
            if not any(grass_tile.pos == adj for grass_tile in grass):
                new_grass = Grass(pos=adj, rate=1, calories=0)
                grass.append(new_grass)


def update(frame_num, img, grid, rabbits, wolves, grass):
    # Grow grass.
    n_grass = len(grass)
    grow(grass)
    n_grass_grown = len(grass) - n_grass
    if n_grass_grown > 0:
        print(n_grass_grown, 'new patches of grass', len(grass), 'total')

    # Update position, age and calories of rabbits.
    n_rabbits = len(rabbits)
    update_animals(rabbits, MAX_AGE_RABBIT)
    n_rabbits_killed = len(rabbits) - n_rabbits
    if n_rabbits_killed > 0:
        print(n_rabbits_killed, 'elderly bunnies died of old age.', len(rabbits), 'remain')
    # Update position, age and calories of wolves.
    n_wolves = len(wolves)
    update_animals(wolves, MAX_AGE_WOLF)
    n_wolves_killed = len(wolves) - n_wolves
    if n_wolves_killed > 0:
        print(n_wolves_killed, 'elderly wolves died of old age.', len(wolves), 'remain')
    # Breed rabbits.
    n_rabbits = len(rabbits)
    breed(rabbits, REFRACTORY_PERIOD_RABBIT)
    n_rabbits_born = len(rabbits) - n_rabbits
    if n_rabbits_born > 0:
        print(n_rabbits_born, 'cute little bunnies entered the world.', len(rabbits), 'total')
    # Breed wolves.
    n_wolves = len(wolves)
    breed(wolves, REFRACTORY_PERIOD_WOLF)
    n_wolves_born = len(wolves) - n_wolves
    if n_wolves_born > 0:
        print(n_wolves_born, 'ferocious baby wolves entered the world.', len(wolves), 'total')
    # Wolf nom rabbit.
    n_rabbits = len(rabbits)
    feed(wolves, rabbits)
    n_rabbits_eaten = len(rabbits) - n_rabbits
    if n_rabbits_eaten > 0:
        print(n_rabbits_killed, 'slow rabbits were devoured', len(rabbits), 'total')
    # Wolf nom rabbit.
    n_grass = len(grass)
    feed(rabbits, grass)
    n_grass_eaten = len(grass) - n_grass
    if n_grass_eaten > 0:
        print(n_grass_killed, 'innocent patches of grass were devoured.', len(grass), 'total')
    feed(wolves, rabbits)
    feed(rabbits, grass)

    # Draw the image to display. NxN pixels, each pixel has 3 color channels (r, g, b).
    next_grid = np.zeros((N, N, 3), dtype=np.uint8)
    for n in range(len(grass)):
        x = grass[n].pos[0]
        y = grass[n].pos[1]
        next_grid[x][y] = COLOR_GRASS
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


rabbits = []
for _ in range(INITIAL_RABBITS):
    x = np.random.randint(0, N)
    y = np.random.randint(0, N)
    age = np.random.randint(0, MAX_AGE_RABBIT)
    r = Animal((x, y), age, random_gender(), 0, CALORIES_MEAL)
    rabbits.append(r)

wolves = []
for _ in range(INITIAL_WOLVES):
    x = np.random.randint(0, N)
    y = np.random.randint(0, N)
    age = np.random.randint(0, MAX_AGE_WOLF)
    r = Animal((x, y), age, random_gender(), 0, CALORIES_MEAL)
    wolves.append(r)

grass = []
for _ in range(INITIAL_GRASS):
    x = np.random.randint(0, N)
    y = np.random.randint(0, N)
    calories = np.random.randint(0, CALORIES_MAX)
    g = Grass((x, y), rate=GRASS_RATE, calories=calories)
    grass.append(g)


fig, ax = plt.subplots()
img = ax.imshow(grid)
ani = matplotlib.animation.FuncAnimation(fig, update,
                                         fargs=(img, grid, rabbits, wolves, grass),
                                         frames=10,
                                         interval=50,
                                         save_count=50)

plt.show()
