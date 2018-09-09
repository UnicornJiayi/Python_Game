import pygame
import sys
import traceback #更好退出
import myplane
import enemy
import bullet
from pygame.locals import * #导入常用的函数和常量
from random import *

pygame.init() #初始化pygame
pygame.mixer.init() #混音器初始化

bg_size = width,height = 480,600
screen = pygame.display.set_mode(bg_size) #创建一个游戏窗口
pygame.display.set_caption("飞机大战--Lee Demo") #设置窗口标题

background = pygame.image.load("images/background.png").convert() #加载并转换图片

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

#载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)
def add_big_enemies(group1,group2,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

        
def main():
    pygame.mixer.music.play(-1) #播放背景音乐

    me = myplane.MyPlane(bg_size) #生成我方飞机

    enemies = pygame.sprite.Group()

    small_enemies = pygame.sprite.Group()#生成敌方小飞机
    add_small_enemies(small_enemies,enemies,15)

    mid_enemies = pygame.sprite.Group()#生成敌方中型飞机
    add_mid_enemies(mid_enemies,enemies,4)

    big_enemies = pygame.sprite.Group()#生成敌方大飞机
    add_big_enemies(big_enemies,enemies,2)

    #生成普通子弹
    bullet1 = [] #索引
    bullet1_index = 0 
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop)) #midtop即顶部中央
    

    clock = pygame.time.Clock()

    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    #统计得分
    score

    switch_image = True #切换图片

    delay = 100 #用于延迟，以显示我方飞机图像交替

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT: #接收到退出事件后退出程序
                pygame.quit() #优化退出
                sys.exit()
                
        #检测用户的键盘操作
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveRight()      

        screen.blit(background,(0,0)) #将背景图画上去

        #发射子弹
        #每一次while循环delay减一，从100开始，每一次while循环是一帧是一帧
        if not(delay % 10): #每十帧调用一次，即只有被十整除才会调用以下内容
            bullet1[bullet1_index].reset(me.rect.midtop)
            bullet1_index = (bullet1_index + 1) % BULLET1_NUM #bullet1指向下一个索引但不能等于4

        #检测子弹是否击中敌机
        for b in bullet1:
            if b.active:
                b.move()
                screen.blit(b.image,b.rect)
                enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        if e in mid_enemies or e in big_enemies:
                            e.hit = True
                            e.energy -= 1
                            if e.energy == 0:
                                e.active = False
                        else:
                            e.active = False
                        
        #绘制大型敌机
        for each in big_enemies:
            if each.active:
                each.move()
                if switch_image:
                    screen.blit(each.image1,each.rect)
                else:
                    screen.blit(each.image2,each.rect)

                #绘制血槽
                pygame.draw.line(screen,BLACK,\
                                 (each.rect.left,each.rect.top - 5),\
                                 (each.rect.right,each.rect.top - 5),\
                                 2) #2个像素的宽度
                #当生命大于20%显示绿色，否则显示红色
                energy_remain = each.energy / enemy.BigEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen,energy_color, \
                                 (each.rect.left,each.rect.top - 5), \
                                 (each.rect.left + each.rect.width * energy_remain , \
                                 each.rect.top - 5), 2)
                
                #即将出现在画面中，播放音效
                if each.rect.bottom == -50:
                    enemy3_fly_sound.play(-1) #-1循环播放音效
            else:
                #毁灭
                if not(delay % 3):
                    if e3_destroy_index == 0: #敌机初始化，然后播放音乐
                        enemy3_down_sound.play()
                    screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                    e3_destroy_index = (e3_destroy_index + 1) % 6
                    if e3_destroy_index == 0:
                        enemy3_fly_sound.stop()
                        each.reset()
                    
                
        #绘制中型敌机
        for each in mid_enemies:
            if each.active:
                each.move()
                screen.blit(each.image,each.rect)


                #绘制血槽
                pygame.draw.line(screen,BLACK,\
                                 (each.rect.left,each.rect.top - 5),\
                                 (each.rect.right,each.rect.top - 5),\
                                 2) #2个像素的宽度
                #当生命大于20%显示绿色，否则显示红色
                energy_remain = each.energy / enemy.MidEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen,energy_color,\
                                 (each.rect.left,each.rect.top - 5),\
                                 (each.rect.left + each.rect.width * energy_remain,\
                                 each.rect.top - 5),2)
                
            else:
                #毁灭
                if not(delay % 3):
                    if e2_destroy_index == 0:
                        enemy2_down_sound.play()
                    screen.blit(each.destroy_images[e2_destroy_index],each.rect)
                    e2_destroy_index = (e2_destroy_index + 1) % 4
                    if e2_destroy_index == 0:
                        each.reset()

                        
        #绘制小型敌机
        for each in small_enemies:
            if each.active:
                each.move()
                screen.blit(each.image,each.rect)
            else:
                #毁灭
                if not(delay % 3):
                    if e1_destroy_index == 0:
                        enemy1_down_sound.play()
                    screen.blit(each.destroy_images[e1_destroy_index],each.rect)
                    e1_destroy_index = (e1_destroy_index + 1) % 4
                    if e1_destroy_index == 0:
                        each.reset()
    
        #检测我方飞机是否被撞
        enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask) #spritecollide函数默认以矩形区域为检测范围
        if enemies_down:
            me.active = False #若把这句屏蔽掉则我方飞机永生！
            for e in enemies_down:
                e.active = False


        #绘制我方飞机,两个图像交替出现
        if me.active:
            if switch_image:
                screen.blit(me.image1,me.rect)
            else:
                screen.blit(me.image2,me.rect)
        else:
            #毁灭
            if not(delay % 3):
                if me_destroy_index == 0:
                    me_down_sound.play()
                screen.blit(me.destroy_images[me_destroy_index],me.rect)
                me_destroy_index = (me_destroy_index + 1) % 4
                if me_destroy_index == 0:
                    print("Game Over!")
                    running = False

        #切换图片
        if not(delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip() #刷新交替显示

        clock.tick(60) #一秒钟图像更新60帧
    
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
        


#convert函数是将图像数据都转化为Surface对象，
#每次加载完图像以后就应该做这件事情（事实上因为它太常用了如果不写Python也会帮你做）；
#convert_Algha相比convert保留了Alpha通道信息（可以简单理解为透明的部分），
#这样我们的光标才可以是不规则的形状。


#blit是个重要参数，第一个参数是一个Surface对象，第二个为左上角位置，
#画完以后用update更新一下以防画面漆黑，这里用clock函数设定了更新。





        


