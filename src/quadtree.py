import pygame as pg
from settings import *

# Quadtree Vector2 class
class QuadtreeVector2:
    def __init__(self, bounds:pg.Rect):
        # public variables
        self.Boundary:pg.Rect = bounds

        # protected variables, used for inheritance
        self._Capacity:int = 4 # number of items before it subdivides

        # private variables
        self.__Divided:bool = False # Has the Quadtree been divided yet?
        self.__Inserted = [pg.Vector2()] # points inserted

        # private variables subtrees, not defined as none
        self.__TopLeft = None
        self.__TopRight = None
        self.__BottomRight = None
        self.__BottomLeft = None 

    def InsertVector2(self, point:pg.Vector2) -> bool:
        
        # if it isn't colliding in the boundary return false and exit
        if pg.Rect.collidepoint(self.Boundary, point) == False:
            return False

        # if the list length is less than the capacity add the point to the list
        if len(self.__Inserted) < self._Capacity:
            self.__Inserted.append(point) # adding to list
            return True # returning operation is true
        
        else:

            # if it hasn't been subdivided subdivide
            if not(self.__Divided): 
                self._Subdivide(point)
            
            # Inserting points into other quadtrees if the subtrees inserted point is true and its not none
            
            # TOPLEFT
            if not(self.__TopLeft is None) and self.__TopLeft.InsertVector2(point) == True:
                return True
            
            # TOP RIGHT
            if not(self.__TopRight is None) and self.__TopRight.InsertVector2(point) == True:
                return True
            
            # BOTTOM RIGHT
            if not(self.__BottomRight is None) and self.__BottomRight.InsertVector2(point) == True:
                return True
            
            # BOTTOM LEFT
            if not(self.__BottomLeft is None) and self.__BottomLeft.InsertVector2(point) == True:
                return True

        # Return false if none of the operations above are true
        return False
    
    def _Subdivide(self, point:pg.Vector2):
        # Defining the subtrees with new boundaries and insert the point in them
        # We define the trees assuming that each tree starts from the top left corner

        # Helper variables
        PosX:float = self.Boundary.centerx
        PosY:float = self.Boundary.centery
        HWidth:float = self.Boundary.width/2 # We only use half width for operations
        HHeight:float = self.Boundary.height/2 # We only use half height for operations

        # TOP LEFT
        TopLeftBoundary:pg.Rect = pg.Rect(PosX-HWidth,PosY-HHeight,HWidth,HHeight)
        self.__TopLeft = QuadtreeVector2(TopLeftBoundary)
        self.__TopLeft.InsertVector2(point)

        # TOP RIGHT
        TopRightBoundary:pg.Rect = pg.Rect(PosX,PosY-HHeight,HWidth,HHeight)
        self.__TopRight = QuadtreeVector2(TopRightBoundary)
        self.__TopRight.InsertVector2(point)

        # BOTTOM LEFT
        BottomLeftBoundary:pg.Rect = pg.Rect(PosX-HWidth,PosY,HWidth,HHeight)
        self.__BottomLeft = QuadtreeVector2(BottomLeftBoundary)
        self.__BottomLeft.InsertVector2(point)

        # BOTTOM RIGHT
        BottomRightBoundary:pg.Rect = pg.Rect(PosX,PosY,HWidth,HHeight)
        self.__BottomRight = QuadtreeVector2(BottomRightBoundary)
        self.__BottomRight.InsertVector2(point)

        # Set the divided to true now that the main tree is divided
        self.__Divided = True

    def QueryCircle(self, center:pg.Vector2, radius:float):  
        found:list[pg.Vector2] = [] # THATS HOW YOU DEFINE A LIST

        # Is the Circle in the boundary
        if self.CollideCircleRect(center, radius, self.Boundary):
            # Loop through the inserted points
            for point in self.__Inserted:
                # if it collides with the query area add it to the found list
                if self.CollideCirclePoint(center, radius, point):
                    found.append(point)

            # if the quadtree is divided add their found points too
            if self.__Divided:
                
                # If the subtree is actually there query their tree

                # TOP LEFT
                if not(self.__TopLeft is None): 
                    found.extend(self.__TopLeft.QueryCircle(center, radius))

                # TOP RIGHT
                if not(self.__TopRight is None): 
                    found.extend(self.__TopRight.QueryCircle(center, radius))

                # BOTTOM LEFT
                if not(self.__BottomLeft is None): 
                    found.extend(self.__BottomLeft.QueryCircle(center, radius))

                # BOTTOM RIGHT
                if not(self.__BottomRight is None): 
                    found.extend(self.__BottomRight.QueryCircle(center, radius))

        
        return found
    
    def QueryRectangle(self, area:pg.Rect):
        found:list[pg.Vector2] = []

        # Is the rectangle in the boundary
        if pg.Rect.colliderect(area, self.Boundary):
            # Loop through the inserted points
            for point in self.__Inserted:
                # if it collides with the query area add it to the found list
                if pg.Rect.collidepoint(area, point):
                    found.append(point)

            # if the quadtree is divided add their found points too
            if self.__Divided == True:
                
                # If the subtree is actually there, query their tree

                # TOP LEFT
                if not(self.__TopLeft is None): 
                    found.extend(self.__TopLeft.QueryRectangle(area))

                # TOP RIGHT
                if not(self.__TopRight is None): 
                    found.extend(self.__TopRight.QueryRectangle(area))

                # BOTTOM LEFT
                if not(self.__BottomLeft is None): 
                    found.extend(self.__BottomLeft.QueryRectangle(area))

                # BOTTOM RIGHT
                if not(self.__BottomRight is None): 
                    found.extend(self.__BottomRight.QueryRectangle(area))

        return found

    def Clear(self) -> None:
        # Clear inserted points and set the divided to false
        self.__Inserted.clear()
        self.__Divided = False

        # Clear subtrees

        # TOP LEFT
        if not(self.__TopLeft is None):
            self.__TopLeft.Clear()
        
        # TOP RIGHT
        if not(self.__TopRight is None):
            self.__TopRight.Clear()

        # BOTTOM LEFT
        if not(self.__BottomLeft is None):
            self.__BottomLeft.Clear()

        # BOTTOM RIGHT
        if not(self.__BottomRight is None):
            self.__BottomRight.Clear()

    # Helper Functions
    def CollideCircleRect(self, center:pg.Vector2, radius:float, rect:pg.Rect) -> bool:
        """
        A circle and a rectangle only collide iff the closest point of the 
        rectangle to the circles center is less than or equal to the circles radius
        """ 

        # Calculating the closest point

        closestX:float = center.x
        closestY:float = center.y

        # Calculating closest X
        if center.x < rect.left:
            closestX = rect.left
        elif center.x > rect.right:
            closestX = rect.right
        
        # Calculating closest Y
        if center.y < rect.top:
            closestY = rect.top
        elif center.y > rect.bottom:
            closestY = rect.bottom

        # putting it into a vector2
        closest_point:pg.Vector2 = pg.Vector2(closestX, closestY)

        # calculating distance, distance squared for optimization
        distance = pg.Vector2.distance_squared_to(closest_point, center)

        # Checking if it is in the radius
        if distance <= radius ** 2:
            return True

        return False # No Collision if otherwise
    
    def CollideCirclePoint(self, center:pg.Vector2, radius:float, point:pg.Vector2) -> bool:
        return center.distance_squared_to(point) <= radius**2 
    
    def DebugDraw(self, screen:pg.Surface):
        pg.draw.rect(screen, BLACK, self.Boundary, width=1)
        if self.__Divided:
            if not(self.__TopLeft is None): 
                self.__TopLeft.DebugDraw(screen)

            # TOP RIGHT
            if not(self.__TopRight is None): 
                self.__TopRight.DebugDraw(screen)

            # BOTTOM LEFT
            if not(self.__BottomLeft is None): 
                self.__BottomLeft.DebugDraw(screen)

            # BOTTOM RIGHT
            if not(self.__BottomRight is None): 
                self.__BottomRight.DebugDraw(screen)
            

