import pygame
import quadtree as qt  # For quadtree
from settings import * # Global variables
import numpy as np     # For the array of points
# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((WINW,WINH))
Clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)
running = True

# Variables

# Bounds for points
low:float = 10.5 # minium
high:float = WINW - 10.5 # maximum

# points
pointsX = np.random.uniform(low,high, MAX_POINTS) # random floats
pointsY = np.random.uniform(low, high, MAX_POINTS) # random floats
point:pygame.Vector2 = pygame.Vector2()

# Redefine bounds
low = -1.0
high = 1.0

# velocities, make sure its not zero
velosX = (np.random.uniform(low, high, MAX_POINTS)+0.5) * POINT_SPEED
velosY = (np.random.uniform(low, high, MAX_POINTS)+0.5) * POINT_SPEED


# Quadtree, define a vector2 quadtree with the screen boundary rectangle
quadtree = qt.QuadtreeVector2(SCREEN_BOUNDARY)

# Query Areas
rectangle_query = True # query the rectangle?
circle_query = False # query the circle?

# query values
query_rectangle:pygame.Rect = pygame.Rect(0,0,160,100) # rectangle

# circle
query_circle:pygame.Vector2 = pygame.Vector2()
query_circle_radius:float = 100

# list of found points
Query_Found = [pygame.Vector2()]

# FUNCTIONS
def GetMousePositionVec2() -> pygame.Vector2:
    # get the tuple version
    mouse_tuple = pygame.mouse.get_pos() 

    # turn the tuple version into a vector version
    # There might be an easiser way to do this but I don't know how
    mouse_vector2:pygame.Vector2 = pygame.Vector2(mouse_tuple[0], mouse_tuple[1])

    return mouse_vector2

while running:
    # Getting the query before the quadtree clears
    if circle_query:
        # Query the quadtree with CIRCLE for the points
        Query_Found=quadtree.QueryCircle(query_circle, query_circle_radius)
    elif rectangle_query:
        # Query the quadtree with RECTANGLE for points
        Query_Found=quadtree.QueryRectangle(query_rectangle)

    # Clear the quadtree every frame
    quadtree.Clear()

    # Loop through events for input
    for event in pygame.event.get():
        # X button on the screen
        if event.type == pygame.QUIT: 
            running = False
        # Escape button
        elif event.type == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # switch the values of the query circle and rect
            circle_query = not circle_query
            rectangle_query = not rectangle_query 

    # Clear the screen every frame
    screen.fill(WHITE)

    # Rendering the game

    # loop through each position in the list and draw it as a circle
    for i in range(MAX_POINTS):

        # moving the point
        pointsX[i] += velosX[i]
        pointsY[i] += velosY[i]

        # checking if its out of bounds
        if not(pygame.Rect.collidepoint(SCREEN_BOUNDARY, pointsX[i], pointsY[i])):
            # Turn the velocity into the normal of itself
            temp_velo_X = velosX[i]
            velosX[i] = -velosY[i]
            velosY[i] = temp_velo_X
        
        # Setting the point
        point = pygame.Vector2(pointsX[i], pointsY[i])
        
        # inserting the point into the quadtree
        quadtree.InsertVector2(point)

        # Drawing the circle
        pygame.draw.circle(screen, RED, point, 10)

    # Going through the query areas
    if circle_query == True:
        # Setting the query circle position
        query_circle = GetMousePositionVec2()
        
        # Drawing the query circle
        pygame.draw.circle(screen, BLACK, query_circle, query_circle_radius, width=5)
    elif rectangle_query == True:
        # Setting the query rectangle position
        query_rectangle.x = pygame.mouse.get_pos()[0] - 80
        query_rectangle.y = pygame.mouse.get_pos()[1] - 50
        
        # Drawing the query rectangle
        pygame.draw.rect(screen, BLACK, query_rectangle, width=5)
    

    # Loop through the points of the query and draw a green circle over them
    for query_point in Query_Found:
        pygame.draw.circle(screen, GREEN, query_point, 15)

    # Updating the screen
    pygame.display.flip()

    # limit the FPS
    Clock.tick(60)

    
pygame.quit()