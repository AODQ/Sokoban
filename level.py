class Level:
    def __init__(self, tile_map, name):
        self.name = name
        self.player_pos = []
        self.tile_map = []
        self.boxes = []
        self.goals = []

        for r, row in enumerate(tile_map.split("\n")):
            wall_index = row.index("#")
            tile_row = []
            box_row = []

            for c, col in enumerate(row):
                if col == "@":
                    tile_row.append("_")
                    box_row.append(" ")
                    self.player_pos = [c, r]

                elif col == "$":
                    tile_row.append("_")
                    box_row.append(col)

                elif col in ("+", "*"):
                    tile_row.append(".")
                    self.goals.append((c, r))

                    if col == "+":
                        box_row.append(" ")
                        self.player_pos = [c, r]
                    else:
                        box_row.append("$")

                else:
                    if col == ".":
                        self.goals.append((c, r))
                    
                    elif col == " ":
                        col = "-" if c < wall_index else "_"
                    
                    tile_row.append(col)
                    box_row.append(" ")
    
            self.tile_map.append(tile_row)
            self.boxes.append(box_row)
        
        self.width = len(max(self.tile_map, key=len))
        self.height = len(self.tile_map)

        for row in self.tile_map:   
            row.extend(["-"] * (self.width - len(row)))

def collection(file_path):
    levels = []
    
    with open(file_path, "r") as file:
        collection = file.read().replace("\n\n", "\n").split(";")

        for l, line in enumerate(collection[:-1]):
            tile_map = "\n".join(line.replace("\n\n", "\n").split("\n")
                [1 if l else 0:-1])
            name = collection[l+1].split("\n")[0].lstrip()
            levels.append(Level(tile_map, name))
    return levels