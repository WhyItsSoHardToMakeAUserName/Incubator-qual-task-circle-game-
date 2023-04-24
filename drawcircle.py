import pygame 
import math
pygame.init()
class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.center = (x,y)
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), 10)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
game_state = True
radius = 2
best_score = 0
dead_zone_radius = 70
last_rad_change = 0
last_mouse_motion = 0
circle_drawn = False
drawn_angle = 0

pygame.draw.circle(screen,(255,255,255),(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),10)
dot = Circle(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,30)
score_surface = pygame.Surface((500,100),pygame.SRCALPHA)
score_surface.set_colorkey((0, 0, 0))
painting_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
painting_surface.set_colorkey((0, 0, 0))
image = pygame.image.load('plainblack.jpg')
screen.blit(image,(0,0))

pixel_font = pygame.font.Font('PublicPixel.ttf',60)
pixel_font_small = pygame.font.Font('PublicPixel.ttf',50)
pixel_font_very_small = pygame.font.Font('PublicPixel.ttf',30)
font_small = pygame.font.SysFont("Arial", 40)
wrong_way = font_small.render("Wrong way", True, (255,255,255))
close_to_dot = font_small.render("Too close to dot",True,(255,255,255))
new_best_score = font_small.render("New best score",True,(255,255,255))
draw_full_circle = font_small.render("Draw full circle",True,(255,255,255))
too_slow = font_small.render("Too slow",True,(255,255,255))

def refresh_scoreboard(total_score):
    score_surface.fill((0,0,0))
    if total_score<10:
        score_surface.blit(pixel_font.render(f"{int(total_score)}",True,color_depending_on_percentage(int(total_score)/100)),(50,0))
    else:
        score_surface.blit(pixel_font.render(f"{int(total_score)}",True,color_depending_on_percentage(int(total_score)/100)),(0,0))
    score_surface.blit(pixel_font_small.render(f"{int((round(total_score,1)-int(round(total_score,1)))*10)}%",True,color_depending_on_percentage(int(total_score)/100)),(150,10))
    screen.blit(score_surface,(270,350))
def blit_what_is_drawn_and_refresh_score_board():
    global score
    global score_g
    global total_score
    dx = event.pos[0] - prev_pos[0]
    dy = event.pos[1] - prev_pos[1]
    distance = max(abs(dx), abs(dy)) 
    for i in range(distance):
        xc = prev_pos[0] + int(float(i) / distance * dx)
        yc = prev_pos[1] + int(float(i) / distance * dy)
        d = math.sqrt((xc - SCREEN_WIDTH//2)**2 + (yc - SCREEN_HEIGHT//2)**2)
        dist = abs(r-d)
        if dist>=51:
            red = 255
            green = 0
        else:
            red = 5*dist
            green = 255 - 5*dist
        score +=green+red
        score_g +=green
        pygame.draw.circle(painting_surface, (red, green, 0), (xc, yc), radius)
    screen.blit(painting_surface,(0,0))
    total_score = score_g/score*100

    refresh_scoreboard(total_score)
def blit_best_score():
    global best_score
    global circle_drawn
    if drawn_angle >=360:
        if total_score > best_score:
            best_score = total_score
            screen.blit(new_best_score,(300,430))
        else:
            screen.blit(pixel_font_very_small.render(f"{int(best_score)}.{int((round(best_score,1)-int(round(best_score,1)))*10)}%",True,(255,255,255)),(400,438))
            best_score_txt = font_small.render(f"Best:",True,(255,255,255))
            screen.blit(best_score_txt,(300,430))
        audio = pygame.mixer.Sound('sounds/success.mp3')
        audio.play()
        circle_drawn = True
def color_depending_on_percentage(percentage):
    print (percentage)
    if percentage<=0.75:
        return(255,0,0)
    if (1-percentage)*100<12.5:
        green = 255
        red = int(2060*((1-percentage)))
        print(green)
        print(red)
    else:
        red = 255
        green = int(255-816*((1-percentage)))
        print(green)
        print(red)
    return (red,green,0)
def mouse_in_circle(x, y, radius):
    mouse_pos = pygame.mouse.get_pos()
    distance = math.sqrt((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2)
    return distance <= radius
def render_blit_errortext(text):
    screen.blit(image,(0,0))
    score_surface.fill((0,0,0))
    score_surface.blit(pixel_font.render("XX",True,(255,0,0)),(0,0))
    score_surface.blit(pixel_font_small.render("x%",True,(255,0,0)),(150,10))
    screen.blit(painting_surface,(0,0))
    screen.blit(score_surface,(270,350))
    screen.blit(text,(300,430))
    global circle_drawn 
    circle_drawn = True
    audio = pygame.mixer.Sound('sounds/fail.mp3')
    audio.play()
def have_time_to_draw(time_to_draw,current_time,start_time):
    if current_time-start_time>time_to_draw:
        render_blit_errortext(too_slow)
def angle_check(direction,angle,prev_angle):
    global drawn_angle
    if abs(angle-prev_angle)>100:
        if direction == "clockwise":
            drawn_angle+=angle
        else:
            drawn_angle+=360 - angle
        angle+=360
        return False
    else:
        drawn_angle+=abs(angle-prev_angle)
    if direction == "clockwise":
        if angle<prev_angle:
            return True
    elif direction == "counter_clockwise":
        if angle>prev_angle:
            return True
    return False

while game_state:
    mouse_state = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP and circle_drawn == False:
            render_blit_errortext(draw_full_circle)

        if event.type == pygame.MOUSEBUTTONDOWN:
            screen.blit(image,(0,0))
            painting_surface.fill((0,0,0))
            dot.draw(painting_surface)
            dot.draw(screen)
            prev_pos = None
            last_mouse_motion = 0
            last_rad_change = 0
            circle_drawn = False
            start_angle = None
            direction = None
            drawn_angle = 0
            score = 0
            score_g = 0
            total_score = 0
            radius = 2
            start_time = pygame.time.get_ticks()
            if mouse_in_circle(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,dead_zone_radius):
                render_blit_errortext(close_to_dot)

        if event.type == pygame.MOUSEMOTION and mouse_state[0] == True and circle_drawn == False:
            screen.blit(image,(0,0))
            angle = math.degrees(math.atan2(event.pos[1] - SCREEN_HEIGHT//2, event.pos[0] - SCREEN_WIDTH//2))
            if angle < 0:
                angle += 360
            
            if start_angle == None:
                start_angle = angle
            elif direction == None:
                if angle>start_angle:
                    direction = "clockwise"
                else:
                    direction = "counter_clockwise"
            
            dead_zone_radius = 30
            if prev_pos is not None:
                blit_what_is_drawn_and_refresh_score_board()

                #checks if player goes wrong way
                if angle_check(direction,angle,prev_angle) :
                    render_blit_errortext(wrong_way)

                blit_best_score()
                
            #set the radius of required circle if there is not
            if prev_pos is None:
                r = math.sqrt((event.pos[0] - SCREEN_WIDTH//2)**2 + (event.pos[1] - SCREEN_HEIGHT//2)**2)
            
            prev_pos = event.pos
            prev_angle = angle
            last_mouse_motion = pygame.time.get_ticks()
            #check if mouse is too close to circle
            if mouse_in_circle(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,dead_zone_radius):
                render_blit_errortext(close_to_dot)
            #check if player takes too long to draw
            have_time_to_draw(7000,pygame.time.get_ticks(),start_time)
        
    #отвечает за увеличивание ширины круга чем рисует игрок
    if pygame.time.get_ticks() - last_rad_change > 80:
        elapsed_time = pygame.time.get_ticks() - last_mouse_motion
        if elapsed_time > 10 and radius <= 10:
            radius += 1  
        elif elapsed_time < 10 and radius >= 3:
            radius -= 1 
        last_rad_change = pygame.time.get_ticks()

    pygame.display.update()