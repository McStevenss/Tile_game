import numpy as np
import random


class Map_generator():
    def __init__(self):
        self.w = 0
        self.h = 0
        self.map = []
        self.rooms = {}

    #Create empty blank map
    def generate_base_map(self, w, h):
        map = []
        for height in range(h):
            map.append([0]*w)
            
        self.map = map

    #Add room at cordinates
    def add_room(self, x, y, w, h):

        start_corner = (x,y)
        end_corner = (x + (w-1), y + (h-1))

        for height in range(h):
            for width in range(w):     
                #first and last
                if width == 0 or width == w-1:
                    self.map[height + y][width + x] = 1

                #walls
                if height == 0 or height == h-1:
                    self.map[height + y][width + x] = 1

        self.rooms[len(self.rooms)] = [start_corner,end_corner]        

    #Save map to txt file
    def save_map_to_file(self, name):
        f = open(f"{name}.txt", "w")

        for row in self.map:
            for idx, tile in enumerate(row):

                if idx == len(row) -1:
                    f.write(f"{tile}")
                else:
                    f.write(f"{tile},")

            f.write(" \n")

        f.close()

    #Load saved map from file
    def read_map_from_file(self, path):
        f = open(path, "r")
        map = f.readlines()
        
        for idx, row in enumerate(map):
            map[idx] = row.replace(' \n','')
            map[idx] = map[idx].split(',')
            map[idx] = [eval(i) for i in map[idx]]
            
        return map
    
    #draw path between two cordinates
    def draw_path(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        x = x0
        y = y0
        error = dx - dy

        while x != x1 or y != y1:
            self.map[y][x] = 9

            if x == x1:
                y += sy
            elif y == y1:
                x += sx
            elif error > -dx:
                x += sx
                error -= dy
            elif error < dy:
                y += sy
                error += dx

        self.map[y][x] = 9
        
    def draw_wall(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        x = x0
        y = y0
        error = dx - dy

        while x != x1 or y != y1:
            self.map[y][x] = 1

            if x == x1:
                y += sy
            elif y == y1:
                x += sx
            elif error > -dx:
                x += sx
                error -= dy
            elif error < dy:
                y += sy
                error += dx

        self.map[y][x] = 1

    
    def generate_map_lines(self, rooms=2, outer_walls=True):
        map_width = len(self.map[0])
        map_heigth = len(self.map)

        if outer_walls:
            #Top
            self.draw_wall(0,0,map_width-1,0)
            #Left
            self.draw_wall(0,0,0,map_heigth-1)
            #Bottom
            self.draw_wall(0,map_heigth-1,map_width-1,map_heigth-1)
            #Right
            self.draw_wall(map_width-1,0,map_width-1,map_heigth-1)

        for _ in range(rooms):

            r_x0 = random.randint(1, map_width-1)
            r_x1 = random.randint(1, map_width-1)

            r_y0 = 0
            r_y1 = map_heigth-1

            self.draw_wall(r_x0,r_y0,r_x1,r_y1)

            r_x0 = 0
            r_x1 = map_width-1

            r_y0 = random.randint(1, map_heigth-1)
            r_y1 = random.randint(1, map_heigth-1)

            self.draw_wall(r_x0,r_y0,r_x1,r_y1)

    def add_room_to_map(self,room,mapX=0,mapY=0):
        map_width = len(self.map[0])
        map_heigth = len(self.map)

        room_w = len(room[0])
        room_h = len(room)
        print(f"Adding room ({room_w},{room_h}) to map with dimensions:",map_width,map_heigth)

        if mapX + room_w < map_width and mapY + room_h < map_heigth:
            
            #room fits geometrically
            for y in range(len(room)):
                for x,tile in enumerate(room[y]):
                    
                    self.map[y+mapY][x+mapX] = tile
                    



        else:
            print("ERROR: room doesnt fit")

        


#Example use
map_generator = Map_generator()

#Generate base map and add two rooms
map_generator.generate_base_map(30,30)

map_generator.generate_map_lines(rooms=0,outer_walls=True)

#Add pre defined rooms
map_generator.rooms["shop"] = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,99,1,0,0,1,0,0,0,1],
    [1,99,2,0,0,0,0,0,0,1],
    [1,99,1,0,0,1,0,0,0,1],
    [1,99,1,0,0,1,0,0,0,1],
    [1,1,1,1,2,1,1,1,1,1]
]

map_generator.rooms["apartment"] = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,0,1,0,0,99,1],
    [1,0,0,1,0,1,0,0,99,1],
    [1,1,1,1,2,1,1,1,1,1]
]

map_generator.rooms["generic_wide_room"] = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,99,0,0,0,0,0,0,1],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

map_generator.rooms["small_room"] = [
    [1, 1, 1, 1],
    [1, 0, 99,1],
    [1, 0, 1, 1]
]

map_generator.rooms["altar_room"] = [
    [1,1,1,1,0,1,1,1,1 ],
    [1,99,0,0,0,0,0,99,1],
    [1,0,0,0,0,0,0,0,1 ],
    [0,0,0,0,0,0,0,0,0 ],
    [1,0,0,0,0,0,0,0,1 ],
    [1,99,0,0,0,0,0,99,1],
    [1,1,1,1,0,1,1,1,1 ]
]

map_generator.add_room_to_map(map_generator.rooms["shop"],mapX=4,mapY=4)
map_generator.add_room_to_map(map_generator.rooms["apartment"],mapX=4,mapY=12)

map_generator.add_room_to_map(map_generator.rooms["small_room"],mapX=15,mapY=10)

map_generator.add_room_to_map(map_generator.rooms["small_room"],mapX=20,mapY=10)

map_generator.add_room_to_map(map_generator.rooms["altar_room"],mapX=15,mapY=4)




# #DEBUG PRINTOUT OF MAP
map_H = len(map_generator.map)
map_W = len(map_generator.map[0])

w_string = "   "
for n in range(map_W):
    if n > 9:
        w_string += f"{n},"
    else:
        w_string += f"{n} ,"

print(w_string)
for idx, row in enumerate(map_generator.map):
    if idx > 9:
        print(f"{idx}{row}")
    else:    
        print(idx,row)


#Save map
map_generator.save_map_to_file("test")

