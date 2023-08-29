

class BaseSolution:

    def __init__(self):
        pass

    def load_frame(self):
        # Nacteni jednoho snimku ze serveru 
        pass

    def detect_playground(self):
        # Detekce hriste z nacteneho snimku
        pass

    def detect_robot(self):
        # Detekce robota [ArUCo tag]
        pass

    def recognize_objects(self):
        # Rozpoznani objektu na hristi - cil, body, prekazky
        pass

    def analyze_playground(self):
        # Analyza dat vytezenych ze snimku
        pass

    def generate_path(self, map, start, finish, direction):
        def cpp_modulo(x, y):
            return (x % y + y) % y
        # first, make a list of tiles, then convert to Left Right Forward string

        # default distance is 100 for all tiles
        grid = [
            [100,100,100,100,100,100,100,100],
            [100,100,100,100,100,100,100,100],
            [100,100,100,100,100,100,100,100],
            [100,100,100,100,100,100,100,100],
            [100,100,100,100,100,100,100,100],
            [100,100,100,100,100,100,100,100],
            [100,100,100,100,100,100,100,100],
            [100,100,100,100,100,100,100,100],
        ]
        # calculate distance grid
        grid[start[0]][start[1]] = 0
        for _ in range(MAX_STEPS):
            grid_old = copy.deepcopy(grid)
            for x in range(0,8):
                for y in range(0,8):
                    for (a,b) in [(0,1), (1,0), (0,-1), (-1,0)]:
                        try:
                            assert x+a > -1 and x+a < 8
                            assert y+b > -1 and y+b < 8
                            if grid_old[x+a][y+b] > grid_old[x][y]+map[x+a][y+b]:
                                grid[x+a][y+b] = grid_old[x][y]+map[x+a][y+b]
                        except:
                            pass
        
        # make the path from the distance grid, starting at the finish
        lrf_path = ""
        current_pos = finish
        current_dist = grid[finish[0]][finish[1]]
        current_direction = 0 # direction at which robot leaves the current square
        for _ in range(MAX_STEPS):
            for (a,b) in [(0,1), (1,0), (0,-1), (-1,0)]:
                try:
                    assert ((current_pos[0]+a) > -1) and ((current_pos[0]+a) < 8)
                    assert ((current_pos[1]+b) > -1) and ((current_pos[1]+b) < 8)
                    if current_dist >= grid[current_pos[0]+a][current_pos[1]+b]:
                        
                        enter_direction = 0 # direction at which robot enteres current square
                        if a == 1:
                            enter_direction = 1
                            # current square was entered in x+ direction
                        if a == -1:
                            enter_direction = 3
                            # x-
                        if b == 1:
                            enter_direction = 2
                            # y+
                        if b == -1:
                            enter_direction = 0
                            # y-
                        
                        # We now have leave direction and enter direction. Now we calculate direction difference
                        turn = cpp_modulo((current_direction - enter_direction), 4)
                        if turn > 0:
                            lrf_path = turn*'R' + lrf_path
                        if turn < 0:
                            lrf_path = (-turn)*'L' + lrf_path
                        
                        current_direction = enter_direction
                        
                        # we go forward every time anyway
                        lrf_path = 'F' + lrf_path

                        current_pos = (current_pos[0]+a, current_pos[1]+b)
                        current_dist -= 1
                        break
                except:
                    pass
            if current_pos == start: 
                break
        # reverse the string before returning
        lrf_path = lrf_path.replace('RRR', 'L')
        print(lrf_path)
        return lrf_path[::-1]

    def send_solution(self):
        # Poslani reseni na server pomoci UTP spojeni.
        pass

    def solve(self):
        self.load_frame()
        self.detect_playground()
        self.detect_robot()
        self.recognize_objects()
        self.analyze_playground()
        self.generate_path()
        self.send_solution()
        pass


if __name__ == "__main__":
    solution = BaseSolution()
    solution.solve()
