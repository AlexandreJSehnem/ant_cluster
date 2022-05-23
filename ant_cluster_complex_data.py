from random import shuffle, random, randrange
from math import sqrt
# import os

SIGHT_RANGE = 1
WIDTH = 50
HEIGHT = 100
CORPSES = 1000
AGENTS = 1  # currently only works with one agent
STEPS = 10000000
ALPHA = 4
K1 = 0.05
K2 = 0.01
total_picks = 0
total_drops = 0


class ant():

    def __init__(self, x, y, range, map_class):
        self.pos_x = x
        self.pos_y = y
        self.sight = range
        self.map_info: map = map_class
        self.holding = False
        self.being_hold = []

    def brain(self):
        # decides if it should pickup or drop
        if self.holding:
            if self.should_drop():
                aux = self.map_info.field[self.pos_x][self.pos_y]
                if aux[2] == 0:
                    self.map_info.field[self.pos_x][self.pos_y] = self.being_hold
                    self.holding = False
                else:
                    self.map_info.field[self.pos_x][self.pos_y] = self.being_hold
                    self.being_hold = aux
        elif self.map_info.field[self.pos_x][self.pos_y][2] != 0:
            if self.should_pickup():
                self.being_hold = self.map_info.field[self.pos_x][self.pos_y]
                self.map_info.field[self.pos_x][self.pos_y] = ["0", "0", 0]
                self.holding = True
        self.move()

    def should_drop(self):
        area = ((self.sight*2) + 1)*((self.sight*2) + 1)
        ed = (self.euclidian_distance())/(area*area)
        chance = (ed/(K2+ed))*(ed/(K2+ed))
        # print("Drops man:"+str(chance)+" "+str(ed))
        n = random()
        global total_drops
        if n < chance:
            total_drops += 1
            # print("eo")
            return True
        else:
            return False

    def should_pickup(self):
        area = ((self.sight*2) + 1)*((self.sight*2) + 1)
        pre_ed = self.euclidian_distance()
        # if pre_ed == 0: pre_ed = 1
        ed = (pre_ed)/(area*area)
        chance = (K1/(K1+ed))*(K1/(K1+ed))
        # print(str(pre_ed)+"  "+str(ed)+"  "+str(chance))
        n = random()
        global total_picks
        if n > chance:
            total_picks += 1
            return True
        else:
            return False

    def euclidian_distance(self):
        distance = 0
        to_compare = []
        count_to_divide = 0
        if self.holding:
            to_compare = self.being_hold
        else:
            to_compare = self.map_info.field[self.pos_x][self.pos_y]
        for i in range(self.sight*2 + 1):
            temp_i = 0
            if i < self.sight + 1:
                temp_i = self.pos_x - i
            elif i > self.sight + 1:
                temp_i = self.pos_x + i - self.sight + 1
            else:
                temp_i = self.pos_x
            for j in range(self.sight*2 + 1):
                temp_j = 0
                if j < self.sight + 1:
                    temp_j = self.pos_y - j
                elif j > self.sight + 1:
                    temp_j = self.pos_y + j - self.sight + 1
                else:
                    temp_j = self.pos_y
                # sums the designated position
                if temp_i >= WIDTH:
                    temp_i = temp_i - WIDTH
                if temp_j >= HEIGHT:
                    temp_j = temp_j - HEIGHT
                if self.map_info.field[temp_i][temp_j][2] != 0:
                    count_to_divide += 1
                    distance = distance + (1 - sqrt(
                        (float(to_compare[0]) - float(self.map_info.field[temp_i][temp_j][0]))*(float(to_compare[0]) - float(self.map_info.field[temp_i][temp_j][0])) +
                        (float(to_compare[1]) - float(self.map_info.field[temp_i][temp_j][1]))*(float(to_compare[1]) - float(self.map_info.field[temp_i][temp_j][1]))
                        )/ALPHA)
        if distance < 0:
            return 0
        return distance

    def move(self):
        moved = False
        while not moved:
            x = randrange(0, 4)  # 0 = west, 1 = south, 2 = east, 3 = north
            if x == 0:
                temp_x = self.pos_x
                if (self.pos_x + 1) == self.map_info.width:
                    temp_x = 0
                else:
                    temp_x += 1
                if self.map_info.ant_location[temp_x][self.pos_y]:
                    continue
                else:
                    self.map_info.ant_location[temp_x][self.pos_y] = True
                    self.map_info.ant_location[self.pos_x][self.pos_y] = False
                    self.pos_x = temp_x
                    moved = True
            elif x == 1:
                temp_y = self.pos_y
                if (self.pos_y + 1) == self.map_info.height:
                    temp_y = 0
                else:
                    temp_y += 1
                if self.map_info.ant_location[self.pos_x][temp_y]:
                    continue
                else:
                    self.map_info.ant_location[self.pos_x][temp_y] = True
                    self.map_info.ant_location[self.pos_x][self.pos_y] = False
                    self.pos_y = temp_y
                    moved = True
            elif x == 2:
                temp_x = self.pos_x
                if (self.pos_x - 1) < 0:
                    temp_x = self.map_info.width - 1
                else:
                    temp_x = temp_x - 1
                if self.map_info.ant_location[temp_x][self.pos_y]:
                    continue
                else:
                    self.map_info.ant_location[temp_x][self.pos_y] = True
                    self.map_info.ant_location[self.pos_x][self.pos_y] = False
                    self.pos_x = temp_x
                    moved = True
            elif x == 3:
                temp_y = self.pos_y
                if (self.pos_y - 1) < 0:
                    temp_y = self.map_info.height - 1
                else:
                    temp_y = temp_y - 1
                if self.map_info.ant_location[self.pos_x][temp_y]:
                    continue
                else:
                    self.map_info.ant_location[self.pos_x][temp_y] = True
                    self.map_info.ant_location[self.pos_x][self.pos_y] = False
                    self.pos_y = temp_y
                    moved = True
            # print(f"destination: {x} new x: {self.pos_x} new y:{self.pos_y}")


class map():

    def __init__(self, width, height, corpses):
        self.width = int(width)
        self.height = int(height)
        self.field = []
        self.ant_location = []
        self.create_field(corpses)
        pass

    # generates dead ants and places them randomly
    def create_field(self, corpses):
        i = 0
        list_count = []
        for i in range(self.width*self.height):
            list_count.append(i)
        shuffle(list_count)
        line_count = 0
        for i in range(self.width):
            line = []
            ants = []
            for j in range(self.height):
                line.append(corpses[list_count[line_count]])
                line_count += 1
                ants.append(False)
            self.field.append(line)
            self.ant_location.append(ants)

    # prints the current field state
    def print_field(self):
        for i in range(self.width):
            printable = ""
            for j in range(self.height):
                if self.field[i][j][2] == 0:
                    printable += " "
                else:
                    printable += str(self.field[i][j][2])
            print(printable)


def read_file():
    file = open("input.txt", "r")
    data_list = []
    for line in file:
        splitted = line.split()
        data_list.append(splitted)
    file.close()
    return data_list


data_list = read_file()
print(data_list.__len__())
size = data_list.__len__()
for i in range((WIDTH*HEIGHT)-size):
    data_list.append(["0", "0", 0])
# starts map
mapper = map(WIDTH, HEIGHT, data_list)

# starts ant list
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
    list = ant(x, y, SIGHT_RANGE, mapper)
    ant_list.append(list)

mapper.print_field()
step_count = 0
while True:
    for agent in ant_list:
        if step_count < STEPS:
            agent.brain()
            continue
        else:
            break
    if step_count > STEPS:
        break
    else:
        # if step_count % 1000 == 0:
            # os.system('cls' if os.name == 'nt' else 'clear')
            # mapper.print_field()
        step_count += 1

# prints final result
print("-----------------------------")
mapper.print_field()
print(total_picks)
print(total_drops)
