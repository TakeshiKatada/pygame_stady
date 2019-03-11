'''
ブロック崩し
'''
import pygame
import math

def sgn(a):
    return 1 if a > 0 else -1

WIDTH  = 640
HEIGHT = 480
WHITE  = (255,255,255)
RED    = (255,  0,  0)
YELLOW = (255,255,  0)
GREEN  = (  0,255,  0)
BLUE   = (  0,  0,255)
colortable = [RED, YELLOW, GREEN]

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
myfont = pygame.font.Font(None, 64)
myclock = pygame.time.Clock()
br = 10
paddlew = 640
paddleh = 16
blockw = 48
blockh = 24

def main():
    pygame.init()
    endflag = 0

    while endflag == 0:
        ballx = WIDTH / 2
        bally = HEIGHT - 170
        bx1 = 10
        by1 = -10
        x = WIDTH / 2
        y = HEIGHT - 64
        paddle = pygame.Rect(x - (paddlew / 2),y - (paddleh / 2), paddlew,paddleh)
        #ブロックを作る
        blocks = []
        b = [0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,1,0,0,0]
        for i in range(50):
            if b[i] == 1:
                x = (i % 10) * (blockw + 4) + 64
                y = int(i / 10) * (blockh + 4) + 64
                blocks.append(pygame.Rect(x, y, blockw, blockh))
        
        gameover = 0
        while endflag == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: endflag = 1
            #キー入力の取得
            press = pygame.key.get_pressed()
            x = paddle.centerx
            x, y = pygame.mouse.get_pos()#この1行でマウス操作になる
            if(press[pygame.K_LEFT ]): x -= 8
            if(press[pygame.K_RIGHT ]): x += 8
            if x >= (paddlew / 2) and x <= (WIDTH - (paddlew / 2)):
                paddle.centerx = x
            x = ballx + bx1
            y = bally + by1
            """画面枠に対してのボールの反射"""
            if x < br or x > (WIDTH - br): bx1 = -bx1
            if y < br: by1 = -by1
            if y > HEIGHT: gameover += 1
            """パドルに対してのボールの反射"""
            dx = paddle.centerx - x
            dy = paddle.centery - y
            if dy == 0: dy = 1
            if abs(dx) < (paddlew / 2 + br) and abs(dy) < (paddleh / 2 + br):
                if abs(dx /dy) > (paddlew / paddleh):
                    bx1 = -bx1
                    ballx = paddle.centerx - sgn(dx) * (paddlew/2 + br)
                else:
                    bx1 = -dx / 10
                    by1 = -by1
                    bally = paddle.centery - sgn(dy) * (paddleh/2 + br)
            """ブロックに対してのボールの反射"""
            for block in blocks:
                dx = block.centerx - x
                dy = block.centery - y
                if dy == 0: dy = 1
                if abs(dx) < (blockw / 2 + br) and abs(dy) < (blockh / 2 +br):
                    if abs(dx / dy) > (blockw / blockh):
                        bx1 = -bx1
                        ballx = block.centerx - sgn(dx) * (blockw / 2 + br)
                    else:
                        by1 = -by1
                        bally = block.centery - sgn(dy) * (blockh / 2 + br)
                    blocks.remove(block)
                    break
            ballx += bx1
            bally += by1
            screen.fill(BLUE)
            """ブロックの描写"""
            for block in blocks:
                color = colortable[int(block.y / 28) % 3]
                pygame.draw.rect(screen,color,block)
            """パドルの描写"""
            pygame.draw.rect(screen,WHITE,paddle)
            """ボールの描画"""
            pygame.draw.circle(screen,WHITE,(int(ballx), int(bally)), br)
            """ゲームオーバー時の処理"""
            if gameover > 0:
                imagetext = myfont.render("GAME OVER", True, WHITE)
                screen.blit(imagetext, (180, 300))
                if gameover > 200: break
            
            
            if len(blocks) == 0:
                imagetext = myfont.render("CLEAR", True, WHITE)
                screen.blit(imagetext, (180, 200))
                imagetext2 = myfont.render("PLEASE [R] TO RESTART", True, WHITE)
                screen.blit(imagetext2, (50, 300))
                bx1 = 0
                by1 = 0

                if(press[pygame.K_r ]):
                    main()

            myclock.tick(60)
            pygame.display.flip()
            

main()
pygame.quit()

