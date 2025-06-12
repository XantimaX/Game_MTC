import heapq
import math

def heuristic(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[0])

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
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []