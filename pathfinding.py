import heapq
import math

def world_to_grid(pos, tilewidth, tileheight):
    grid_x = int(pos[0] // tilewidth)
    grid_y = int(pos[1] // tileheight)
    return (grid_x, grid_y)


def mark_wall(grid,grid_width, grid_height, tile_object, tile_width, tile_height):
    start_x = int(tile_object.x // tile_width)
    start_y = int(tile_object.y // tile_height)
    end_x = int((tile_object.x + tile_object.width) // tile_width)
    end_y = int((tile_object.y + tile_object.height) // tile_height)

    for x in range(start_x, end_x):
        for y in range(start_y , end_y ):
            if 0 <= x < grid_width and 0 <= y < grid_height:
                grid[x][y] = 1 

def heuristic(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def astar(grid, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}

    g_score = {start : 0}
    f_score = {start : heuristic(start,end)}

    while open_set :
        _, current = heapq.heappop(open_set)

        if current == end :
            path = [] 
            while current in came_from :
                path.append(current)
                current = came_from[current]
            
            path.append(start)
            path.reverse()
            return path

        x,y = current
        neighbors = [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1) , (x+1, y-1), (x-1, y+1) , (x-1, y-1)
        ]


        for neighbor in neighbors :
            nx, ny = neighbor

            if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                continue  # Out of bounds
            if grid[nx][ny] == 1:
                continue  # Wall
            
            tentative_g = g_score[current] + 1  # Assume cost=1 for all moves
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []