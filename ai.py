import pyautogui

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)
grid_size = 20
screen_width = 600
screen_height = 600

class ai:

    def __init__(self, direction, food, snake, positions):
       self.direction = direction
       self.food = food
       self.snake = snake
       self.positions = positions

    def start(s):
        # First have to check is the player all directions are ready to move or not
        left_h = s.check_direction_get_h(left)
        right_h = s.check_direction_get_h(right)
        up_h = s.check_direction_get_h(up)
        down_h = s.check_direction_get_h(down);

        # for Left

        if(left_h != -1 and (left_h<=right_h or right_h==-1) and (left_h<=up_h or up_h==-1) and (left_h<=down_h or down_h==-1) and (left[0]*-1, left[1]*-1)!=s.direction):
            pyautogui.press("left")

        # For Right
        elif(right_h != -1 and (right_h<=left_h or left_h==-1) and (right_h<=up_h or up_h==-1) and (right_h<=down_h or down_h==-1) and (right[0]*-1, right[1]*-1)!=s.direction):
            pyautogui.press("right")

         # For up
        elif(up_h != -1 and (up_h<=left_h or left_h==-1) and (up_h<=right_h or right_h==-1) and (up_h<=down_h or down_h==-1) and (up[0]*-1, up[1]*-1)!=s.direction):
            pyautogui.press("up")
        
        else:
           pyautogui.press("down") 


    def check_direction_get_h(s, direction):
        x,y = direction
        current = s.snake
        new_pos = (((current[0]+(x*grid_size))%screen_width), (current[1]+(y*grid_size))%screen_height)
        # print("{}".format(new_pos))
        if(new_pos in s.positions): return -1
        return s.h_calculator(new_pos)
    
    def h_calculator(s, cur):
        return (abs(cur[0]-s.food[0]) + abs(cur[1]-s.food[1]))

