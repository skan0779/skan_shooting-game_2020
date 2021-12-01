import pygame
import sys
import random
from time import sleep

# black=(0,0,0)                                # RGB=0 (black screen)
game_pad_width=480
game_pad_height=640
obstacle_image=['rock01.png','rock02.png','rock03.png','rock04.png','rock05.png','rock06.png',\
                'rock07.png','rock08.png','rock09.png','rock10.png','rock11.png','rock12.png',\
                'rock13.png','rock14.png','rock15.png','rock16.png','rock17.png','rock18.png',\
                'rock19.png','rock20.png','rock21.png','rock22.png','rock23.png','rock24.png',\
                'rock25.png','rock26.png','rock27.png','rock28.png','rock29.png','rock30.png',]

def init_game():                               # game initalization function
    global game_pad,clock,background,skan,shot,explosion,font
    pygame.init()                              # library initalization
    game_pad=pygame.display.set_mode((game_pad_width,game_pad_height))     
    pygame.display.set_caption('skan_game_1')                # game name setting
    background=pygame.image.load('background.png')           # game background setting
    skan=pygame.image.load('skan.png')
    shot=pygame.image.load('shot.png')
    explosion=pygame.image.load('explosion.png')
    font=pygame.font.Font('NanumGothic.ttf',20)
    clock=pygame.time.Clock()

def run_game():                     
    global game_pad,clock,background,skan,shot,explosion

    skan_size=skan.get_rect().size             # 이미지의 사이즈를 가져옴 (x,y)
    skan_width=skan_size[0]                    # 게임속 사이즈로 매칭
    skan_height=skan_size[1]
    x=game_pad_width*0.45                      # skan 시작(x,y) 위치
    y=game_pad_height*0.9
    skanX=0
    shotXY=[]                                  # 여러개 shot, shot의 xy좌표 list값으로 보관
    obstacle=pygame.image.load(random.choice(obstacle_image))
    obstacle_size=obstacle.get_rect().size
    obstacle_width=obstacle_size[0]
    obstacle_height=obstacle_size[1]
    obstacleX=random.randrange(0,game_pad_width-obstacle_width) # x축 위치 랜덤(0~끝)
    obstacleY=0
    obstacle_speed=2
    obstacle_shot=False
    shot_count=0
    shot_missed=0

    on_game=False
    while not on_game:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:    # 창을 닫거나 다른 상황이 나올경우: 게임종료, 시스템 종료
                pygame.quit()
                sys.exit()
            if event.type in [pygame.KEYDOWN]:
                if event.key==pygame.K_LEFT:
                    skanX-=5
                elif event.key==pygame.K_RIGHT:
                    skanX+=5
                elif event.key==pygame.K_SPACE:
                    shotX=x+skan_width/2        # skan의 위치 중간에서 shot
                    shotY=y-skan_height         # skan의 위치 윗부분에서 shot
                    shotXY.append([shotX,shotY])
            if event.type in [pygame.KEYUP]:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    skanX=0

        # game_pad.fill(black)
        draw_object(background,0,0)            
        
        x+=skanX
        if x<0:                                # when the skan is over game_pad_size
            x=0
        elif x>game_pad_width-skan_width:
            x=game_pad_width-skan_width
        if y < obstacleY+obstacle_height:
            if x<obstacleX<x+skan_width or x<obstacleX+obstacle_width<x+skan_width:
                game_over()
        draw_object(skan,x,y)

        if len(shotXY)!=0:                     # shot enumerate
            for i,bxy in enumerate(shotXY):
                bxy[1]-=10
                shotXY[i][1]=bxy[1]
                if bxy[1]<obstacleY:
                    if obstacleX<bxy[0]<obstacleX+obstacle_width:
                        shotXY.remove(bxy)
                        obstacle_shot=True
                        shot_count+=1
                if bxy[1]<=0:                  # shot is over the game_pad->remove
                    try:
                        shotXY.remove(bxy)
                    except:
                        pass
        if len(shotXY)!=0:                     # shot list drawing
            for bx,by in shotXY:
                draw_object(shot,bx,by) 

        score1(shot_count)

        obstacleY+=obstacle_speed
        if obstacleY>game_pad_height:
            obstacle=pygame.image.load(random.choice(obstacle_image))
            obstacle_size=obstacle.get_rect().size
            obstacle_width=obstacle_size[0]
            obstacle_height=obstacle_size[1]
            obstacleX=random.randrange(0,game_pad_width-obstacle_width)
            obstacleY=0  
            shot_missed+=1
        if shot_missed==3:
            game_over()
        score2(shot_missed)

        if obstacle_shot:
            draw_object(explosion,obstacleX,obstacleY)
            obstacle=pygame.image.load(random.choice(obstacle_image))
            obstacle_size=obstacle.get_rect().size
            obstacle_width=obstacle_size[0]
            obstacle_height=obstacle_size[1]
            obstacleX=random.randrange(0,game_pad_width-obstacle_width)
            obstacleY=0        
            obstacle_shot=False
            obstacle_speed+=0.2
            if obstacle_speed>=10:
                obstacle_speed=10
        draw_object(obstacle,obstacleX,obstacleY)

        pygame.display.update()                # update the display
        
        clock.tick(60)                         # game speed: n per sec (= n frame per sec)
     
    pygame.quit()

def score1(count):
    global game_pad,font
    text=font.render('점수: {}'.format(str(count)),True,(0,0,0))
    game_pad.blit(text,(390,10))

def score2(count):
    global game_pad,font
    text=font.render('놓침: {}'.format(str(count)),True,(200,0,0))
    game_pad.blit(text,(390,40))

def message(text):
    global game_pad
    font=pygame.font.Font('NanumGothic.ttf',60)
    text=font.render(text,True,(0,0,0))
    game_pad.blit(text,(game_pad_width*0.27,game_pad_height*0.4))
    pygame.display.update()
    sleep(3)                            # sleep for 3 sec, and restart
    run_game()

def game_over():
    global game_pad
    message('게임 오버')

def draw_object(obj,x,y):           
    global game_pad
    game_pad.blit(obj,(x,y))        # blit: 비티 현상, object를 (x,y)좌표 위치에 그려짐

init_game()
run_game()



