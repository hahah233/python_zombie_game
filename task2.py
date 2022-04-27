import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename,asksaveasfilename
from constants import *
from a2_solution import *
from task1 import AbstractGrid,BasicMap,InventoryView,BasicGraphicalInterface
from PIL import Image, ImageTk
import tkinter.messagebox

class TimeMachine(Pickup):
    """A pickup item can be used to return five steps"""
    
    def __init__(self):
        """its maximum lifetime is infinite."""
        self._lifetime = float('inf')
        self._using = False     # Entities are not selected to be actively 
    
    def toggle_active(self) -> None:
        """Toggle whether this entity is selected as being active or not.
        Timemachine can't be triggered actively."""
        self._using = self._using
    
    def display(self) -> str:
        """A timemachine should be represented by the 'M' character."""
        return TIME_MACHINE

class ImageMap(BasicMap):
    """A view class that extends existing BasicMap class.Add map background 
    and entity image
    master - the belonged frame
    size - the number of rows and columns of the map
    """
    
    def __init__(self, master, size, **kwargs):
        super().__init__(master, size=size,**kwargs)
        global im1,im2,im3,im4,im5,im6,im11
        img1 = Image.open(IMAGES[PLAYER]) 
        im1 = ImageTk.PhotoImage(img1)
        img2 = Image.open(IMAGES[HOSPITAL]) 
        im2 = ImageTk.PhotoImage(img2)
        img3 = Image.open(IMAGES[ZOMBIE])
        im3 = ImageTk.PhotoImage(img3)
        img4 = Image.open(IMAGES[GARLIC]) 
        im4 = ImageTk.PhotoImage(img4)
        img5 = Image.open(IMAGES[CROSSBOW])
        im5 = ImageTk.PhotoImage(img5)
        img6 = Image.open(IMAGES[BACK_GROUND]) 
        im6 = ImageTk.PhotoImage(img6)
        img11 = Image.open('images/time_machine.png') 
        im11 = ImageTk.PhotoImage(img11)
    
    def draw_background(self):
        """Draw the background of the map."""
        for row in range(self._rows):
            for col in range(self._cols):
                self.create_image(self.get_position_center((row,col)),
                                  image=im6)
    
    def draw_entity(self, position, title_type):
        """Draws the entity with tile type at the given position using a 
        image."""
        if isinstance(title_type, Zombie):
            zombie=self.create_image(self.get_position_center(position),
                                     image=im3)
        if isinstance(title_type, Garlic):
            garlic=self.create_image(self.get_position_center(position),
                                     image=im4)
        if isinstance(title_type, Crossbow):
            crossbow=self.create_image(self.get_position_center(position),
                                       image=im5)
        if isinstance(title_type, Player):
            player=self.create_image(self.get_position_center(position),
                                     image=im1)
        if isinstance(title_type, Hospital):
            hospiatl=self.create_image(self.get_position_center(position),
                                       image=im2)
        if isinstance(title_type, TimeMachine):
            time_machine=self.create_image(self.get_position_center(position),
                                           image=im11)

class StatusBar(tk.Frame):
    """A class that inherits from tk.Frame.It used to show the status bar of 
    the game"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        global im9,im10
        self._master=master
        img9 = Image.open('images/chaser.png')
        im9 = ImageTk.PhotoImage(img9)
        img10 = Image.open('images/chasee.png')
        im10 = ImageTk.PhotoImage(img10)
        self.chaser = AbstractGrid(self,1,1,140,50)
        self.chaser.pack(side=tk.LEFT)
        self.time = AbstractGrid(self,2,1,140,50)
        self.time.pack(side=tk.LEFT)
        self.move_step = AbstractGrid(self,2,1,140,50)
        self.move_step.pack(side=tk.LEFT)
        self.button = AbstractGrid(self,1,1,140,50)
        self.button.pack(side=tk.LEFT)
        button1 = tk.Button(self.button, text="Restart Game", 
                            command=self.restart)
        button1.pack()
        button2 = tk.Button(self.button,text = "Quit Game",
                            command = self.quit)
        button2.pack()                                                    
        self.chasee = AbstractGrid(self,1,1,140,50)
        self.chasee.pack(side=tk.LEFT)
        self.chasee.create_image(self.chasee.get_position_center((0,0)),
                                 image=im10)
        self.chaser.create_image(self.chaser.get_position_center((0,0)),
                                 image=im9)
    def restart(self):
        """Used to restart the game"""
        self._master.destroy()
        game = advanced_game(MAP_FILE)
        root = tk.Tk()
        root.title(TITLE)
        app = ImageGraphicalInterface(root, game.get_grid().get_size())
        app.play(game)
        root.mainloop()
    
    def quit(self):
        """Quit thw game"""
        self._master.destroy()
    
class ImageGraphicalInterface(BasicGraphicalInterface):
    """A class that inherits from BasicGraphicalInterface.It expands a lot of 
    functions such as display the first three scores, restart the game, 
    save the game, etc."""
    
    def __init__(self, root, size):
        global im8
        self.sec_num = 0 # Playtime of the game 
        self.move_step = 0 # Player steps of the game
        self._root = root
        self._size = size
        self.var = tk.StringVar(root)
        self._frame1 = tk.Frame(width=700, height=BANNER_HEIGHT)
        self._frame1.grid(row=0, column=0)
        self._frame2 = tk.Frame(width=700, height=500)
        self._frame2.grid(row=1, column=0)
        self._frame3 = StatusBar(self._root, width=700, height=50)
        self._frame3.grid(row=2, column=0)
        img8 = Image.open('images/banner.png')
        img8=img8.resize((700, BANNER_HEIGHT), Image.ANTIALIAS)
        im8 = ImageTk.PhotoImage(img8)
        
        mebubar = tk.Menu(self._root)
        mebubar.add_command(label="Restart game", command=self.restart)
        mebubar.add_command(label="Save game", command=self.save)
        mebubar.add_command(label="Load game", command=self.load)
        mebubar.add_command(label="Quit", command=self.quit)
        mebubar.add_command(label="High Scores", command=self.score)
        self._root.config(menu=mebubar)

        self._title_label = AbstractGrid(self._frame1,1,1,700,BANNER_HEIGHT)
        self._title_label.pack()
        self._title_label.create_image(
                    self._title_label.get_position_center((0,0)),image=im8)
        self._game_map = ImageMap(self._frame2, self._size, width=50*size,
                                  height=50*size)
        self._game_map.pack(side=tk.LEFT)
        self._inventory_view = InventoryView(self._frame2,self._size,width=200,
                                             height=500,bg=LIGHT_PURPLE)
        self._inventory_view.pack(side=tk.LEFT)
    
    def score(self):
        """Used to show the top3 score"""
        self._root.after_cancel(s) # Pause the game
        top_level = tk.Toplevel(self._root)
        top_level.title("Top 3")
        top_level.geometry('250x130')
        tk.Label(top_level, bg=DARK_PURPLE,fg="white",text="High Scores").pack(
                                           fill=tk.X,side=tk.TOP)
        def done():
            """close the toplevel window"""
            top_level.destroy()
            if self.game.has_won() or self.game.has_lost():
                pass
            else:
                self.play(self.game)
        try:
            # Open the score file(if it exists)
            with open(HIGH_SCORES_FILE, 'r') as f: 
                for line in f:
                    v = line.strip().split(':')
                    sec_num = int(v[1])
                    if sec_num//60 == 0:
                        tk.Label(top_level,text="{0}: {1}s".format(v[0],
                        v[1])).pack()
                    else:
                        tk.Label(top_level,text="{0}: {1}m {2}s".format(v[0],
                        sec_num//60,sec_num%60)).pack()
        except:
            pass
        tk.Button(top_level,text="Done",command=done).pack(side=tk.BOTTOM)
    
    def restart(self):
        """Restart the game"""
        self._root.destroy()
        game = advanced_game(MAP_FILE)
        root = tk.Tk()
        root.title(TITLE)
        app = ImageGraphicalInterface(root, game.get_grid().get_size())
        app.play(game)
        root.mainloop()
    
    def quit(self):
        """Quit the game"""
        self._root.after_cancel(s)# Pause the game
        a = tk.messagebox.askyesno('Hint', 
                                   'Are you sure you would like to quit?')
        if a:
            self._root.destroy()
        else:# The player don't want to quit the game
            self._step(self.game)# Resume operation
    
    def save(self):
        """Save game to text file"""
        self._root.after_cancel(s)
        files = [('Text Document', '*.txt')]
        file = asksaveasfilename(filetypes=files, defaultextension = files)
        #A dictionary about entities and their position in the map
        map_information = self.game.get_grid().serialize()
        #A list about the items in the inventory
        weapon = self.game.get_player().get_inventory().get_items()
        weapon_state={}# Store activation status about the inventory items
        weapon_lifetime={}# Store lifetime about the inventory items
        for item in weapon:
            weapon_state[item.display()] = item.is_active()
            weapon_lifetime[item.display()] = item.get_lifetime()
        try:# Write in game data
            with open(file, 'a+') as f:
                for key, value in map_information.items():
                    f.write('{0}:{1}\n'.format(key, value))
                f.write('.\n')
                for key, value in weapon_state.items():
                    f.write('{0}:{1}\n'.format(key, value))
                f.write('.\n')
                for key, value in weapon_lifetime.items():
                    f.write('{0}:{1}\n'.format(key, value))
                f.write('.\n')
                f.write(str(self.move_step)+'\n')
                f.write(str(self.sec_num)+'\n')
                f.write(str(self._size)+'\n')
        except:
            pass
        self.play(self.game)
    
    def load(self):
        """load the game file"""
        self._root.after_cancel(s)
        files = [('Text Document', '*.txt')]
        file = askopenfilename(filetypes=files, defaultextension = files) 
        try:
            with open(file,"r") as f:
                lines = f.readlines()
                size = int(lines[-1])# map size
                grid = Grid(size)
                loader = AdvancedMapLoader()
            index=[]# Used to determine which part data is loaded
            for y, line in enumerate(lines):
                for char in line.strip("\n"):
                    if char == ".":
                        index.append(y)
            for line in lines[:index[0]]:
                v = line.strip().split(':')
                str1=","
                index1=v[0].index(str1)
                x = int(v[0][1:index1])
                y = int(v[0][index1+1:-1])
                entity = v[1]
                grid.add_entity(Position(x,y),loader.create_entity(entity))
            game1 = AdvancedGame(grid)#Create new game instance
            def is_true(str):
                # Determine the activation status of items
                return str == "True"
            for line in lines[index[0]+1:index[1]]:
                v = line.strip().split(':')
                item = loader.create_entity(v[0])
                if is_true(v[1]):
                    item.toggle_active()
                game1.get_player().get_inventory().add_item(item)
            for i,line in enumerate(lines[index[1]+1:index[2]]):
                v = line.strip().split(':')
                lifetime=int(v[1])
                game1.get_player().get_inventory().get_items()[i].\
                    _lifetime=lifetime
            self.move_step = int(lines[-3])
            self.sec_num = int(lines[-2])
            self.play(game1)
        except:
            tkinter.messagebox.showinfo('Hint','No file')
            self.play(self.game)
    
    def _move(self, game, direction):
        """Handles moving the player and redrawing the game."""
        player = game.get_player()
        if direction.upper() in DIRECTIONS:# If direction is "W","A","S"，"D"
            offset = game.direction_to_offset(direction.upper())
            if offset is not None:
                game.move_player(offset)
                self.move_step+=1# Count the steps of the player
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
    
    def draw(self, game):
        """Clears and redraws the view based on the current game state"""
        mins = self.sec_num//60
        secs = self.sec_num%60
        self._frame3.time.delete(tk.ALL)
        self._frame3.time.annotate_position((0,0), "Timer")
        self._frame3.time.annotate_position((1,0), 
                                    "{0} mins {1} seconds".format(mins,secs))
       
        self._frame3.move_step.delete(tk.ALL)
        self._frame3.move_step.annotate_position((0,0), "Moves made")
        self._frame3.move_step.annotate_position((1,0), 
                                    "{0} moves".format(self.move_step))
        
        self._game_map.delete(tk.ALL)
        self._game_map.draw_background()
        for Position, entity in game.get_grid().get_mapping().items():
            position=(Position.get_y(),Position.get_x())
            self._game_map.draw_entity(position, entity)
        
        inventory=game.get_player().get_inventory()
        self._inventory_view.delete(tk.ALL)
        self._inventory_view.draw(inventory)
    
    def _step(self, game):
        """The step method is called every second.This method triggers the
        step method for the game and updates the view accordingly."""
        global high_scores,s
        high_scores={}# Used to store the data about the high score
        self.draw(game)
        self.sec_num+=1# Count the playtime
        game.step()
        def quit():
            """Quit the toplevel window"""
            global high_scores
            name = self.var.get()# The name of the player
            high_scores[name] = self.sec_num
            high_scores=dict(sorted(high_scores.items(), 
                        key=lambda item:item[1]))#Sort by time consumption
            new_scores={}#For temporary storage of data
            for i,(k,v) in enumerate(high_scores.items()):
                new_scores[k]=v
                if i == MAX_ALLOWED_HIGH_SCORES-1:#Store up to three score 
                    high_scores = new_scores
                    break
            # Save the score data and create the file if it doesn't exist
            with open(HIGH_SCORES_FILE, 'w') as f:
                for key, value in high_scores.items():
                    f.write('{0}:{1}\n'.format(key, value))
            root1.destroy()# Quit the toplevel window
        
        def restart():
            """Quit the toplevel window and restart game"""
            global high_scores
            name = self.var.get()
            high_scores[name] = self.sec_num
            high_scores=dict(sorted(high_scores.items(), 
                        key=lambda item:item[1]))
            new_scores={}
            for i,(k,v) in enumerate(high_scores.items()):
                new_scores[k]=v
                if i == MAX_ALLOWED_HIGH_SCORES-1:
                    high_scores = new_scores
                    break
            with open(HIGH_SCORES_FILE, 'w') as f:
                for key, value in high_scores.items():
                    f.write('{0}:{1}\n'.format(key, value))
            root1.destroy()
            self._root.destroy()
            game = advanced_game(MAP_FILE)
            root = tk.Tk()
            root.title(TITLE)
            app = ImageGraphicalInterface(root, game.get_grid().get_size())
            app.play(game)
            root.mainloop()
        if game.has_won() or game.has_lost():
            mins=self.sec_num//60
            secs=self.sec_num%60
            root1=tk.Toplevel(self._root)#Create a toplevel
            if game.has_won():
                root1.title('You win')
                root1.geometry('250x100')
                button=tk.Button(root1,text="Enter",command=quit).grid(row=3,
                                                                     column=1)
                button=tk.Button(root1,text="Enter and play again",
                                 command=restart).grid(row=3,column=2)
                try:# If the file exists
                    with open(HIGH_SCORES_FILE, 'r') as f:
                        for line in f:
                            v = line.strip().split(':')
                            high_scores[v[0]] = int(v[1])
                    # If there are three existing high scores
                    if MAX_ALLOWED_HIGH_SCORES == len(high_scores):
                        for i in high_scores.values():
                            #If new score can enter the top three
                            if self.sec_num < i:
                                tk.Label(root1,text="You won in {0}m and {1}s! \
Enter your name:".format(mins,secs)).grid(row=1,column=1,columnspan=2)
                                entry = tk.Entry(root1,textvariable=self.var)
                                entry.grid(row=2,column=1,columnspan=2,pady=10)
                                break
                        else:
                            tk.Label(root1,text="You won in {0}m and {1}s!"\
                        .format(mins,secs)).grid(row=1,column=1,columnspan=2)
                        root1.mainloop()
                    else:
                        tk.Label(root1,text="You won in {0}m and {1}s! \
Enter your name:".format(mins,secs)).grid(row=1,column=1,columnspan=2)
                        entry = tk.Entry(root1,textvariable=self.var)
                        entry.grid(row=2,column=1,columnspan=2,pady=10)
                        root1.mainloop()
                #No file exists.You're the first winner can store score
                except:
                    tk.Label(root1,text="You won in {0}m and {1}s! \
Enter your name:".format(mins,secs)).grid(row=1,column=1,columnspan=2)
                    entry = tk.Entry(root1,textvariable=self.var)
                    entry.grid(row=2,column=1,columnspan=2,pady=10)
                    root1.mainloop()
            else:
                root1.title('You lose')
                root1.geometry('150x50')
                tk.Label(root1,text="You lose in {0}m and {1}s!"\
                    .format(mins,secs)).grid(row=1,column=1,columnspan=2)  
                root1.mainloop()
        s = self._root.after(1000,lambda: self._step(game))
    
    def play(self, game):
        """Binds events and initialises gameplay."""
        # Take game as a class property to facilitate other method calls
        self.game = game
        inventory=game.get_player().get_inventory()
        self._game_map.bind_all("<Key>",lambda event: self.move(event, game))
        self._inventory_view.bind("<Button-1>",
        lambda event: self._inventory_click(event,inventory))
        self._step(game)