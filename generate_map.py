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


    def auto_generate_rooms(self, rooms_horizontal = 4, rooms_vertical = 2, paths = True):
 
        rooms_w = (len(self.map[0])) // rooms_horizontal
        rooms_h = (len(self.map)) // rooms_vertical

        print("Rooms w:",rooms_w)
        print("Rooms h:",rooms_h)

        paths_list = []

        for y in range(rooms_vertical):
            for x in range(rooms_horizontal):
                self.add_room(x*rooms_w,y*rooms_h,rooms_w,rooms_h)
                
                close = None
                far = None

                if x <rooms_horizontal-1:
                    far = (x*rooms_w + (rooms_w -1), y*rooms_h + (rooms_h // 2))

                if x > 0:
                    close = (x*rooms_w, y*rooms_h + (rooms_h // 2))
                
          

                paths_list.append((close,far))


        if paths:

            #Horizontal connection
            prev_far = None
            for close,far in paths_list:

                if prev_far == None:
                    prev_far = far
                    continue
                x1 = prev_far[0]
                y1 = prev_far[1]
                prev_far = far

                x0 = close[0]
                y0 = close[1]
                self.draw_path(x0,y0,x1,y1)

            #Vertica connection
            print("prev",prev_far)

            #pick random room
            joining_room = random.randint(0, rooms_w-1)
            print("Vertically joining at room number:",joining_room)
            #print("start:",rooms_w // 2 + (rooms_w * joining_room), rooms_h-1)
            #print("end:",rooms_w // 2 + (rooms_w * joining_room), rooms_h)
            x0,y0 = rooms_w // 2 + (rooms_w * joining_room), rooms_h-1
            x1,y1 = rooms_w // 2 + (rooms_w * joining_room), rooms_h

            self.draw_path(x0,y0,x1,y1)




#Example use
map_generator = Map_generator()

#Generate base map and add two rooms
map_generator.generate_base_map(25,25)

# map_generator.add_room(1,1,10,10)
# map_generator.add_room(1,11,5,5)
# map_generator.add_room(6,11,5,5)
# map_generator.add_room(12,0,7,15)



# #Draw path
# map_generator.draw_path(2,10,2,11)
# map_generator.draw_path(5,13,6,13)
# map_generator.draw_path(10,4,12,4)


map_generator.auto_generate_rooms()


#DEBUG PRINTOUT OF MAP
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


