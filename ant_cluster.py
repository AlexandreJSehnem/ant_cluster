from random import randrange
import threading

SIGHT_RANGE = 1
WIDTH = 50
HEIGHT = 50
CORPSES = 1000
AGENTS = 10

class ant(threading.Thread):

    def __init__(self, x, y, range, map_class):
        threading.Thread.__init__(self)
        self.pos_x = x
        self.pos_y = y
        self.sight = range
        self.field: map = map_class
        self.holding = False
    
    def run(self):
        self.brain()

    def brain(self):
        pass

class map():

    def __init__(self, width, height, corpses):
        self.width = width
        self.height = height
        self.field = []
        self.ant_location = []
        self.create_field(corpses)
        pass

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
        count = 0
        for i in range(corpses):
            x = randrange(0, self.width)
            y = randrange(0, self.height)
            while self.field[x][y] == 1:
                x = randrange(0, self.width)
                y = randrange(0, self.height)
            self.field[x][y] = 1
            count+=1
        self.print_field()
        print(count)

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

print("bruh")
