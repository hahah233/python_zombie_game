import tkinter as tk
from constants import *
from a2_solution import *
import tkinter.messagebox

class AbstractGrid(tk.Canvas):
    """AbstractGrid is an abstract view class which inherits from tk.Canvas
    An AbstractGrid can be thought of as a grid with a set number of rows and 
    columns."""
    
    def __init__(self, master, rows, cols, width, height, **kwargs):
        """
        Parameters:
            master: The belonged frame
            rows: The number of rows of the grid
            cols: The number of columns of the grid
            width: The width of the grid(in pixels)
            height: The height of the grid(in pixels)
            **kwargs: any additional named arguments supported by tk.Canvas
        """
        super().__init__(master,width=width,height=height,**kwargs)
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height
    
    def get_bbox(self, position):
        """Returns the bounding box for the (row, column) position"""
        col_width = self._width/self._cols
        row_height = self._height/self._rows
        x=position[0]
        y=position[1]
        x_min = y*col_width
        x_max = x_min + col_width
        y_min = x*row_height
        y_max = y_min + row_height
        return(x_min, y_min, x_max, y_max)
    
    def pixel_to_position(self, pixel):
        """Converts the (x, y) pixel position to a (row, column) position"""
        column = pixel[0]//(self._width/self._cols)
        row = pixel[1]//(self._height/self._rows)
        return(row, column)
    
    def get_position_center(self, position):
        """Gets the (x, y) pixel position for the center of the cell at the 
        given (row, column) position."""
        x = (position[1]+0.5)*(self._width/self._cols)
        y = (position[0]+0.5)*(self._height/self._rows)
        return(x, y)
    
    def annotate_position(self, position, text):
        """Annotates the center of the cell at the given (row, column) position
         with the provided text."""
        self.create_text(self.get_position_center(position), text=text)
    
    def annotate_position1(self, position, text):
        """Annotates the center of the cell at the given (row, column) position
         with the provided text in white."""
        self.create_text(self.get_position_center(position), text=text,
                         fill="white")
        
class BasicMap(AbstractGrid):
    """BasicMap is a view class which inherits from AbstractGrid. Entities are 
    drawn on the map using coloured rectangles."""
    
    def __init__(self, master, size, **kwargs):
        """Create the Square map.The width and the height is equal to 50 times 
        the number of rows."""
        super().__init__(master, rows=size,cols=size,**kwargs)
        self._height = self._width = size*50
    
    def draw_entity(self, position, title_type):
        """Draws the entity with tile type at the given position using a 
        coloured rectangle with superimposed text."""
        if isinstance(title_type, Zombie):
            zombie=self.create_rectangle(self.get_bbox(position),
                                         fill=LIGHT_GREEN)
            zombie_text=self.annotate_position(position, ZOMBIE)
        if isinstance(title_type, TrackingZombie):
            zombie=self.create_rectangle(self.get_bbox(position),
                                         fill=LIGHT_GREEN)
            zombie_text=self.annotate_position(position, TRACKING_ZOMBIE)
        if isinstance(title_type, Garlic):
            garlic=self.create_rectangle(self.get_bbox(position),
                                         fill=LIGHT_PURPLE)
            garlic_text=self.annotate_position(position, GARLIC)
        if isinstance(title_type, Crossbow):
            crossbow=self.create_rectangle(self.get_bbox(position),
                                           fill=LIGHT_PURPLE)
            crossbow_text=self.annotate_position(position, CROSSBOW)
        if isinstance(title_type, Player):
            player=self.create_rectangle(self.get_bbox(position),
                                         fill=DARKEST_PURPLE)
            player_text=self.annotate_position1(position, PLAYER)
        if isinstance(title_type, Hospital):
            hospital=self.create_rectangle(self.get_bbox(position),
                                           fill=DARKEST_PURPLE)
            hospital_text=self.annotate_position1(position, HOSPITAL)

class InventoryView(AbstractGrid):
    """InventoryView is a view class which inherits from AbstractGrid and 
    displays the items the player has in their inventory."""
    
    def __init__(self, master, rows,**kwargs):
        """The Inventory view has two columns.The number of row is same with 
        the map"""
        super().__init__(master,cols=2,rows=rows,**kwargs)
    
    def draw(self, inventory):
        """Draws the inventory label and current items with their remaining 
        lifetimes."""
        self.annotate_position((0,0.5),"Inventory")
        row = 1 # Draw items from the second row
        # Different colors are used to distinguish whether it is active or not
        for item in inventory.get_items():
            if item.is_active():
                self.create_rectangle(self.get_bbox((row,0)),width=0,
                                      fill=DARKEST_PURPLE)
                self.create_rectangle(self.get_bbox((row,1)),width=0,
                                      fill=DARKEST_PURPLE)
                self.annotate_position1((row,0), item.__class__.__name__)
                self.annotate_position1((row,1), item.get_lifetime())
                row += 1
            else:
                self.create_rectangle(self.get_bbox((row,0)),width=0,
                                      fill=LIGHT_PURPLE)
                self.create_rectangle(self.get_bbox((row,1)),width=0,
                                      fill=LIGHT_PURPLE)
                self.annotate_position((row,0), item.__class__.__name__)
                self.annotate_position((row,1), item.get_lifetime())
                row += 1
    
    def toggle_item_activation(self, pixel, inventory):
        """Activates or deactivates the item (if one exists) in the row 
        containing the pixel"""
        position=self.pixel_to_position(pixel)
        row = int(position[0])
        if row in range(1,len(inventory.get_items())+1):
            if not inventory.any_active():
                inventory.get_items()[row-1].toggle_active()
            elif inventory.get_items()[row-1].is_active():
                inventory.get_items()[row-1].toggle_active()
        self.delete(tk.ALL)
        self.draw(inventory)
        
class BasicGraphicalInterface:
    """The class manage the overall view and event handling."""
    
    def __init__(self, root, size):
        self._root = root # The main window
        self._size = size # The number of rows in the map
        self._frame1 = tk.Frame(width=700,height=45)
        self._frame1.grid(row=0, column=0)
        self._frame2 = tk.Frame(width=700,height=500)
        self._frame2.grid(row=1, column=0)
        self._title_label = AbstractGrid(self._frame1,1,1,700,45,
                                         bg=DARKEST_PURPLE)
        self._title_label.annotate_position1((0,0),TITLE)
        self._title_label.pack()
        self._game_map = BasicMap(self._frame2,self._size,bg= LIGHT_BROWN,
                                  width=50*size,height=50*size)
        self._game_map.pack(side=tk.LEFT)
        self._inventory_view = InventoryView(self._frame2,self._size,width=200,
                                             height=500,bg=LIGHT_PURPLE)
        self._inventory_view.pack(side=tk.LEFT)
    
    def _inventory_click(self, event, inventory):
        """This method is called when the user left clicks on inventory view.
        It handle activating or deactivating the clicked item(if one exists)"""
        pixel=(event.x,event.y)
        self._inventory_view.toggle_item_activation(pixel, inventory)

    def draw(self, game):
        """ Clears and redraws the view based on the current game state"""
        self._game_map.delete(tk.ALL)
        for Position, entity in game.get_grid().get_mapping().items():
            position=(Position.get_y(),Position.get_x())
            self._game_map.draw_entity(position, entity)
        inventory=game.get_player().get_inventory()
        self._inventory_view.delete(tk.ALL)
        self._inventory_view.draw(inventory)   
    
    def move(self,event,game):
        """Convert incoming keyboard parameters"""
        self._move(game,event.keysym)
    
    def _move(self, game, direction):
        """Handles moving the player and redrawing the game."""
        player = game.get_player()
        if direction.upper() in DIRECTIONS:# If direction is "W","A","S","D"
            offset = game.direction_to_offset(direction.upper())
            if offset is not None:
                game.move_player(offset)
        # If the input is the "direction key"
        elif direction in ARROWS_TO_DIRECTIONS.keys():
            if player.get_inventory().has_active(CROSSBOW):
                start = game.get_grid().find_player()
                offset = game.direction_to_offset(ARROWS_TO_DIRECTIONS\
                                                  [direction])
                first = first_in_direction(game.get_grid(), start, offset)
                # If the entity is a zombie, kill it.
                if first is not None and first[1].display() in ZOMBIES:
                    position, entity = first
                    game.get_grid().remove_entity(position)
        self.draw(game) 
    
    def _step(self, game):
        """The step method is called every second.This method triggers the
        step method for the game and updates the view accordingly."""
        self.draw(game)
        game.step()
        if game.has_won() ==True or game.has_lost() == True:
            a = tk.messagebox.askyesno('Hint', 'Play Again?')
            if a:
                self._root.destroy()
                game = advanced_game(MAP_FILE)
                root = tk.Tk()
                root.title(TITLE)
                app = BasicGraphicalInterface(root, game.get_grid().get_size())
                app.play(game)
                root.mainloop()
            else:
                self._root.destroy()  
        self._root.after(1000,lambda: self._step(game))
        
    def play(self, game):
        """Binds events and initialises gameplay."""
        inventory=game.get_player().get_inventory()
        self._game_map.bind_all("<Key>",lambda event: self.move(event, game))
        self._inventory_view.bind("<Button-1>",lambda event: 
                                  self._inventory_click(event,inventory))
        self._step(game)