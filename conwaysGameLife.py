import pygame
import random

pygame.init()


## --DECLARACION DE CONSTANTES--

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 255)

WIDTH, HEIGHT = 700, 700
TITLE_SIZE = 20
GRID_WIDTH = WIDTH // TITLE_SIZE
GRID_HEIGHT= HEIGHT // TITLE_SIZE
FPS = 60

##  --CREACION DE LA INTERFAZ
screen = pygame.display.set_mode((WIDTH, HEIGHT))

##  --Controlar la velocidad de fotogramas
clock = pygame.time.Clock()

def gen(num):
  return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

##  --DRAWING THE GRID--    Se CREA la cuadricual donse estaran apareciendo las celulas
def draw_grid(positions):
  for position in positions:
    col, row = position
    
    ##  --CELULA--
    top_left = (col * TITLE_SIZE, row * TITLE_SIZE)
    pygame.draw.rect(screen, YELLOW, (*top_left, TITLE_SIZE, TITLE_SIZE))
  
  ##  --FILAS--
  for row in range(GRID_HEIGHT):
    pygame.draw.line(screen, BLACK, (0, row * TITLE_SIZE), (WIDTH, row * TITLE_SIZE))
  
  ## --COLUMNAS--
  for col in range(GRID_HEIGHT):
    pygame.draw.line(screen, BLACK, (col * TITLE_SIZE, 0), (col * TITLE_SIZE, HEIGHT))
    
##  --UPDATING THE GRID--     -LOT OF LOGICAL!-
def adjust_grid(positions):
  all_neighbors = set()
  new_positions = set()
  
  for position in positions:
    neighbors = get_neighbors(position)
    all_neighbors.update(neighbors)
    
    neighbors = list(filter(lambda x: x in positions, neighbors))
    
    if len(neighbors) in [2, 3]:
      new_positions.add(position)
      
  for position in all_neighbors:
    neighbors = get_neighbors(position)
    neighbors = list(filter(lambda x: x in positions, neighbors))
    
    if len(neighbors) == 3:
      new_positions.add(position)
      
  return new_positions    

def get_neighbors(pos):
  x, y = pos
  neighbors = []
  for dx in [-1, 0, 1]:
    if x + dx < 0 or x + dx > GRID_WIDTH:
        continue
    for dy in [-1, 0, 1]:
      if y + dy < 0 or y + dy > GRID_HEIGHT:
        continue
      if dx == 0 and dy == 0:
        continue
      
      neighbors.append((x + dx, y + dy))
      
  return neighbors 
  
## WRITING THE MAIN LOOP
def main():
  running = True
  playing = False
  count = 0
  update_freq = 120
  
  positions = set()
  while running:
    clock.tick(FPS)
    if playing:
      count += 1
      
    if count >= update_freq:
      count = 0
      positions = adjust_grid(positions)
      
    pygame.display.set_caption("Playing" if playing else "Paused")

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        
      if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        col = x // TITLE_SIZE
        row = y // TITLE_SIZE
        pos = (col, row)
        
        if pos in positions:
          positions.remove(pos)
        else:
          positions.add(pos)
          
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          playing = not playing
          
        if event.key == pygame.K_c:
          positions = set()
          playing = False
          count = 0
          
        if event.key == pygame.K_g:
          positions = gen(random.randrange(4, 10) * GRID_WIDTH)
          

    screen.fill(GREY)
    draw_grid(positions)
    pygame.display.update()
    
    
  pygame.quit()

if __name__ == "__main__":
  main()
