import pygame
import math

# 물리엔진 클래스 정의
class PhysicsEngine:
    def __init__(self):
        self.objects = []
        self.gravity = 0.5  # 중력 가속도
        self.friction = 0.99  # 마찰 계수

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self):
        for obj in self.objects:
            # 중력 적용
            obj.velocity[1] += self.gravity
            # 마찰 적용
            obj.velocity[0] *= self.friction
            obj.velocity[1] *= self.friction
            # 위치 갱신
            obj.position[0] += obj.velocity[0]
            obj.position[1] += obj.velocity[1]

            # 바닥에 닿았을 때 반사 (간단한 충돌 처리)
            if obj.position[1] >= 400 - obj.radius:
                obj.position[1] = 400 - obj.radius
                obj.velocity[1] = -obj.velocity[1]

            # 벽에 닿았을 때 반사 (간단한 충돌 처리)
            if obj.position[0] <= 0 + obj.radius or obj.position[0] >= 800 - obj.radius:
                obj.velocity[0] = -obj.velocity[0]

# 물체 클래스 정의
class PhysicsObject:
    def __init__(self, x, y, radius, color):
        self.position = [x, y]  # x, y 좌표
        self.velocity = [0, 0]  # 속도 (x, y)
        self.radius = radius  # 반지름
        self.color = color  # 물체 색깔

    def apply_force(self, force):
        # 힘을 가해 속도에 변화
        self.velocity[0] += force[0]
        self.velocity[1] += force[1]

    def reset(self):
        # 물체 초기화
        self.position = [400, 50]
        self.velocity = [0, 0]

# 초기화
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# 폰트 설정
font = pygame.font.SysFont("Arial", 24)

# 물리 엔진 생성
engine = PhysicsEngine()

# 물체 생성
ball = PhysicsObject(400, 50, 20, (255, 0, 0))
engine.add_object(ball)

# 시간 변수
time = 0

# 슬라이더 초기값
gravity_slider = 0.5  # 중력
friction_slider = 0.99  # 마찰
velocity_slider = 0  # 초기 속도

# 메인 루프
running = True
while running:
    screen.fill((255, 255, 255))  # 화면을 흰색으로 채우기

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 슬라이더 및 버튼 인터랙션 처리
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 중력 슬라이더
            if 50 <= mouse_x <= 250 and 320 <= mouse_y <= 340:
                gravity_slider = (mouse_x - 50) / 200
                engine.gravity = gravity_slider * 2  # 중력 최대값을 2로 설정

            # 마찰 슬라이더
            if 50 <= mouse_x <= 250 and 350 <= mouse_y <= 370:
                friction_slider = (mouse_x - 50) / 200
                engine.friction = friction_slider * 0.99 + 0.01  # 마찰은 0.01 ~ 1 사이

            # 초기화 버튼
            if 650 <= mouse_x <= 750 and 320 <= mouse_y <= 360:
                ball.reset()  # 공 리셋

    # 물리 엔진 업데이트
    engine.update()

    # 물체 그리기
    pygame.draw.circle(screen, ball.color, (int(ball.position[0]), int(ball.position[1])), ball.radius)

    # 물리 값 표시
    time += 1
    velocity_text = f"Velocity: ({ball.velocity[0]:.2f}, {ball.velocity[1]:.2f})"
    position_text = f"Position: ({ball.position[0]:.2f}, {ball.position[1]:.2f})"
    time_text = f"Time: {time // 60}s {time % 60}ms"
    gravity_text = f"Gravity: {engine.gravity:.2f}"
    friction_text = f"Friction: {engine.friction:.2f}"

    # 텍스트 출력
    screen.blit(font.render(velocity_text, True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(position_text, True, (0, 0, 0)), (10, 40))
    screen.blit(font.render(time_text, True, (0, 0, 0)), (10, 70))
    screen.blit(font.render(gravity_text, True, (0, 0, 0)), (10, 100))
    screen.blit(font.render(friction_text, True, (0, 0, 0)), (10, 130))

    # 중력 슬라이더 그리기
    pygame.draw.rect(screen, (0, 0, 0), (50, 320, 200, 20))
    pygame.draw.rect(screen, (255, 0, 0), (50 + int(gravity_slider * 200), 320, 10, 20))
    screen.blit(font.render(f"Gravity: {gravity_slider * 2:.2f}", True, (0, 0, 0)), (270, 320))

    # 마찰 슬라이더 그리기
    pygame.draw.rect(screen, (0, 0, 0), (50, 350, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (50 + int(friction_slider * 200), 350, 10, 20))
    screen.blit(font.render(f"Friction: {friction_slider * 0.99 + 0.01:.2f}", True, (0, 0, 0)), (270, 350))

    # 초기화 버튼 그리기
    pygame.draw.rect(screen, (0, 0, 255), (650, 320, 100, 40))
    screen.blit(font.render("Reset", True, (255, 255, 255)), (670, 330))

    pygame.display.flip()
    clock.tick(60)  # 초당 60 프레임

pygame.quit()
