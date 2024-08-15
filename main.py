import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置游戏界面大小、背景颜色和游戏标题
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('贪吃蛇')

# 加载 Arival 字体
font = pygame.font.SysFont('Arival', 36)  # 或者使用 'Helvetica' 等常见字体

# 定义一个标志来表示游戏是否开始
game_started = False

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 定义蛇的初始位置、大小和速度
snake_x = 100
snake_y = 100
snake_size = 20
snake_speed = 5

# 定义食物的初始位置和大小
food_x = random.randrange(0, screen_width - snake_size, 20)
food_y = random.randrange(0, screen_height - snake_size, 20)
food_size = 20

# 定义蛇的移动方向
snake_direction = 'right'

# 定义一个列表来保存蛇的身体坐标
snake_body = []

# 定义一个计时器来控制蛇的移动速度
clock = pygame.time.Clock()

# 定义一个标志来表示游戏是否暂停
paused = False

# 定义一个函数来绘制文本
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# 定义一个函数来绘制蛇和食物
def draw(snake_x, snake_y, snake_body, food_x, food_y):
    screen.fill(BLACK)

    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, [pos[0], pos[1], snake_size, snake_size])

    if not game_started:
        draw_text('Click to Start!', (screen_width - 200) // 2, (screen_height - 50) // 2, WHITE)

    pygame.draw.rect(screen, RED, [food_x, food_y, food_size, food_size])

    # 如果游戏暂停，显示暂停提示
    if paused:
        font = pygame.font.Font(None, 36)
        text = font.render('PAUSED', True, WHITE)
        screen.blit(text, ((screen_width - text.get_width()) / 2, (screen_height - text.get_height()) / 2))

    pygame.display.update()

# 主循环
while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 退出游戏
            pygame.quit()
            quit()

        # 处理鼠标点击事件，如果点击了开始游戏按钮，开始游戏
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (mouse_x > (screen_width - 200) // 2 and mouse_x < (screen_width - 200) // 2 + 200) and (mouse_y > (screen_height - 50) // 2 and mouse_y < (screen_height - 50) // 2 + 50):
                    game_started = True

        # 处理按键事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_direction = 'up'
            elif event.key == pygame.K_DOWN:
                snake_direction = 'down'
            elif event.key == pygame.K_LEFT:
                snake_direction = 'left'
            elif event.key == pygame.K_RIGHT:
                snake_direction = 'right'
            elif event.key == pygame.K_SPACE:  # 按下空格键切换暂停状态
                paused = not paused

    if game_started:
        # 如果游戏未暂停，执行以下逻辑
        if not paused:
            # 移动蛇的头部
            if snake_direction == 'up':
                snake_y -= snake_speed
            elif snake_direction == 'down':
                snake_y += snake_speed
            elif snake_direction == 'left':
                snake_x -= snake_speed
            elif snake_direction == 'right':
                snake_x += snake_speed

            # 判断是否吃到食物
            if (snake_x == food_x and snake_y == food_y) or (snake_x == food_x and abs(snake_y - food_y) < snake_size) or (snake_y == food_y and abs(snake_x - food_x) < snake_size):
                food_x = random.randrange(0, screen_width - snake_size, 10)
                food_y = random.randrange(0, screen_height - snake_size, 10)
                snake_body.append([snake_x, snake_y])

            # 更新蛇的身体坐标
            snake_body.insert(0, [snake_x, snake_y])
            if len(snake_body) > 1:
                snake_body.pop()

            # 判断游戏是否结束
            if snake_x < 0 or snake_x > screen_width - snake_size or snake_y < 0 or snake_y > screen_height - snake_size or [snake_x, snake_y] in snake_body[1:]:
                # 游戏结束，显示分数并等待退出
                font = pygame.font.Font(None, 36)
                text = font.render('Score: ' + str(len(snake_body)), True, WHITE)
                screen.blit(text, ((screen_width - text.get_width()) / 2, (screen_height - text.get_height()) / 2))
                pygame.display.update()
                pygame.time.wait(2000)
                pygame.quit()
                quit()

    # 绘制蛇和食物
    draw(snake_x, snake_y, snake_body, food_x, food_y)

    # 控制蛇的移动速度
    clock.tick(20)