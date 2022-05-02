from random import randrange
import threading

SIGHT_RANGE = 1
WIDTH = 50
HEIGHT = 50
CORPSES = 1500
AGENTS = 1 # currently only works with one agent
STEPS = 1000000

lock_move = threading.Lock()

class ant(threading.Thread):

    def __init__(self, x, y, range, map_class):
        threading.Thread.__init__(self)
        self.pos_x = x
        self.pos_y = y
        self.sight = range
        self.map_info: map = map_class
        self.steps = STEPS
        self.holding = False
    
    def run(self):
        self.brain()

    def brain(self):
        # main step loop
        for i in range(self.steps):
            # decides if it should pickup or drop
            if self.holding:
                if self.should_drop():
                    self.map_info.field[self.pos_x][self.pos_y] = 1
                    self.holding = False
            else:
                if self.should_pickup():
                    self.map_info.field[self.pos_x][self.pos_y] = 0
                    self.holding = True
            self.move()

    def should_drop(self):
        if self.map_info.field[self.pos_x][self.pos_y] == 0:
            area = ((self.sight*2) + 1)*((self.sight*2) + 1)
            chance = randrange(0,area)
            if chance <= self.amount_dead(): return True
            else: return False

    def should_pickup(self):
        if self.map_info.field[self.pos_x][self.pos_y] == 1:
            area = ((self.sight*2) + 1)*((self.sight*2) + 1)
            chance = randrange(1,area+1)
            if chance > self.amount_dead(): return True
            else: return False


    def amount_dead(self):
        amount_dead = 0
        for i in range(self.sight*2 + 1):
            temp_i = 0
            if i < self.sight+1: temp_i = self.pos_x - i
            elif i > self.sight+1: temp_i = self.pos_x + i - self.sight + 1
            else: temp_i = self.pos_x
            for j in range(self.sight*2 + 1):
                temp_j = 0
                if j < self.sight+1: temp_j = self.pos_y - j
                elif j > self.sight+1: temp_j = self.pos_y + j - self.sight + 1
                else: temp_j = self.pos_y
                # sums the designated position
                amount_dead = amount_dead + self.map_info.field[temp_i][temp_j]
        return amount_dead

    def move(self):
        moved = False
        while not moved:
            x = randrange(0,4) # 0 = west, 1 = south, 2 = east, 3 = north
            lock_move.acquire()
            if x == 0:
                temp_x = self.pos_x
                if (self.pos_x + 1) == self.map_info.width: temp_x = 0
                else: temp_x += 1
                if self.map_info.ant_location[temp_x][self.pos_y]:
                    continue
                else:
                    self.map_info.ant_location[temp_x][self.pos_y] = True
                    self.map_info.ant_location[self.pos_x][self.pos_y] = False
                    self.pos_x = temp_x
                    moved = True
            elif x == 1:
                temp_y = self.pos_y
                if (self.pos_y + 1) == self.map_info.height: temp_y = 0
                else: temp_y += 1
                if self.map_info.ant_location[self.pos_x][temp_y]:
                    continue
                else:
                    self.map_info.ant_location[self.pos_x][temp_y] = True
                    self.map_info.ant_location[self.pos_x][self.pos_y] = False
                    self.pos_y = temp_y
                    moved = True
            elif x == 2:
                temp_x = self.pos_x
                if (self.pos_x - 1) < 0: temp_x = self.map_info.width - 1
                else: temp_x = temp_x - 1
                if self.map_info.ant_location[temp_x][self.pos_y]:
                    continue
                else:
                    self.map_info.ant_location[temp_x][self.pos_y] = True
                    self.map_info.ant_location[self.pos_x][self.pos_y] = False
                    self.pos_x = temp_x
                    moved = True
            elif x == 3:
                temp_y = self.pos_y
                if (self.pos_y - 1) < 0: temp_y = self.map_info.height - 1
                else: temp_y = temp_y - 1
                if self.map_info.ant_location[self.pos_x][temp_y]:
                    continue
                else:
                    self.map_info.ant_location[self.pos_x][temp_y] = True
                    self.map_info.ant_location[self.pos_x][self.pos_y] = False
                    self.pos_y = temp_y
                    moved = True
            lock_move.release()
            # print(f"destination: {x} new x: {self.pos_x} new y:{self.pos_y}")

class map():

    def __init__(self, width, height, corpses):
        self.width = width
        self.height = height
        self.field = []
        self.ant_location = []
        self.create_field(corpses)
        pass

    # generates dead ants and places them randomly
    def create_field(self, corpses):
        i = 0
        for i in range(self.width):
            line = []
            ants = []
            for j in range(self.height):
                line.append(0)
                ants.append(False)
            self.field.append(line)
            self.ant_location.append(ants)
        for i in range(corpses):
            x = randrange(0, self.width)
            y = randrange(0, self.height)
            while self.field[x][y] == 1:
                x = randrange(0, self.width)
                y = randrange(0, self.height)
            self.field[x][y] = 1

    # prints the current field state
    def print_field(self):
        for i in range(self.width):
            printable = ""
            for j in range(self.height):
                printable += str(self.field[i][j])
            print(printable)

def read_file():
    file = open("input.txt", "r")
    for line in file:
        continue
    pass

# starts map and ant threads
mapper = map(WIDTH, HEIGHT, CORPSES)
ant_list = []
for i in range(AGENTS):
    placed = False
    x = 0
    y = 0
    while not placed:
        x = randrange(0, WIDTH)
        y = randrange(0, HEIGHT)
        if not mapper.ant_location[x][y]:
            mapper.ant_location[x][y] = True
            placed = True
    thread = ant(x, y, SIGHT_RANGE, mapper)
    ant_list.append(thread)
    thread.start()

# waits all ants to finish moving
for thread in ant_list:
    print("ants")
    thread.join()

# prints final result
mapper.print_field()
