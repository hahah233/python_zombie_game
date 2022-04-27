import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename,asksaveasfilename
from constants import *
from a2_solution import *
from task1 import AbstractGrid,BasicMap,InventoryView,BasicGraphicalInterface
from task2 import *
from PIL import Image, ImageTk
import tkinter.messagebox

class MasterMapLoader(AdvancedMapLoader):
    """A MasterMaploader can extend AdvancedMapLoader to add support for
    new entities such as TimeMachine."""
    
    def create_entity(self, token: str) -> Entity:
        if token == PLAYER:
            return HoldingPlayer()
        elif token == TRACKING_ZOMBIE:
            return TrackingZombie()
        elif token == GARLIC:
            return Garlic()
        elif token == CROSSBOW:
            return Crossbow()
        elif token == TIME_MACHINE:
            return TimeMachine()
        return super().create_entity(token)

def advanced_game(filename: str) -> AdvancedGame:
    """Return an initialised advanced game that could have TimeMachine."""
    loader = MasterMapLoader()
    grid = loader.load(filename)
    return AdvancedGame(grid)

time_dict = {}# Used to store game information in every step.

class MasterStatusBar(StatusBar):
    """A class that inherits from StatusBar.It used to show the status bar of 
    the game"""
    
    def restart(self):
        """Used to restart the game"""
        self._master.destroy()
        game = advanced_game(MAP_FILE)
        root = tk.Tk()
        root.title(TITLE)
        app = MastersGraphicalInterface(root, game.get_grid().get_size())
        app.play(game)
        root.mainloop()

class MastersGraphicalInterface(ImageGraphicalInterface):
    """A class that inherits from ImageGraphicalInterface.It expands a lot of 
    functions such as display the animation of arrow and timemachine.  Because 
    global variable s cannot be passed across files, I can only copy some 
    methods here."""
    
    def __init__(self, root, size):
        super().__init__(root, size)
        self._frame3 = MasterStatusBar(self._root, width=700, height=50)
        self._frame3.grid(row=2, column=0)
    
    def score(self):
        """Used to show the top3 score"""
        self._root.after_cancel(s)# Pause the game
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
                    sec_num=int(v[1])
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
        app = MastersGraphicalInterface(root, game.get_grid().get_size())
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
                loader = MasterMapLoader()
            index=[]# Used to determine which part data is loaded
            for y, line in enumerate(lines):
                for char in line.strip("\n"):
                    if char == ".":
                        index.append(y)
            for line in lines[:index[0]]:
                v = line.strip().split(':')
                str1=","
                index1=v[0].index(str1)
                x=int(v[0][1:index1])
                y=int(v[0][index1+1:-1])
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
            self.move_step=int(lines[-3])
            self.sec_num=int(lines[-2])
            self.play(game1)
        except:
            tkinter.messagebox.showinfo('Hint','No file')
            self.play(self.game)
    
    def _move(self, game, direction):
        """Handles moving the player and redrawing the game."""
        global time_dict
        img7 = Image.open(IMAGES[ARROW])
        im7 = ImageTk.PhotoImage(img7)
        image7=img7.convert('RGBA')
        """Adjust picture orientation"""
        img8=image7.rotate(90)
        img9=img8.rotate(90)
        img10=img9.rotate(90)
        im8 = ImageTk.PhotoImage(img8)
        im9 = ImageTk.PhotoImage(img9)
        im10 = ImageTk.PhotoImage(img10)
        img = {'Left':im9, 'Right':im7, 'Up':im8, 'Down':im10}
        player = game.get_player()
        game_data=[]# Used to store map information
        weapon_state={}# Used to store inventory state
        weapon_lifetime={}# Used to store inventory lifetime
        if direction.upper() in DIRECTIONS:# If direction is "W","A","S"，"D"
            offset = game.direction_to_offset(direction.upper())
            if offset is not None:
                game.move_player(offset)
                self.move_step+=1# Count the steps of the player
                map_information = game.get_grid().serialize()
                game_data.append(map_information)
                weapon = game.get_player().get_inventory().get_items()#list
                for item in weapon:
                    weapon_state[item.display()] = item.is_active()
                    weapon_lifetime[item.display()] = item.get_lifetime()
                game_data.append(weapon_state)
                game_data.append(weapon_lifetime)
                game_data.append(self.sec_num)
                time_dict[self.move_step] = game_data
        # If the input is the "direction key"
        elif direction in ARROWS_TO_DIRECTIONS.keys():
            #Select the arrow image in the corresponding direction
            im = img[direction]
            if player.get_inventory().has_active(CROSSBOW):
                start = game.get_grid().find_player()
                offset = game.direction_to_offset(ARROWS_TO_DIRECTIONS\
                                                 [direction])  
                first = first_in_direction(game.get_grid(), start, offset)
                # If there are zombies in this direction
                if first is not None and first[1].display() in ZOMBIES:
                    position = start.add(offset)
                    entity = game.get_grid().get_entity(position)
                    if entity is not None:
                            game.get_grid().remove_entity(position)
                    else:
                        # Switch row and column
                        position1=(position.get_y(),position.get_x())
                        # Draw an arrow
                        arrow = self._game_map.create_image(self._game_map.\
                            get_position_center(position1),image=im)
                        # Repeat the painting to form an animation effect
                        animation = self._root.after(200,
                        lambda:show_arrow(game,position))
                def show_arrow(game,position):
                    """Controls display of arrows and the removal of zombies"""
                    self.draw(game)
                    position = position.add(offset)
                    if game.get_grid().in_bounds(position):
                        entity = game.get_grid().get_entity(position)
                        if entity is not None:
                            if entity.display() in ZOMBIES:
                                # Kill the zombie
                                game.get_grid().remove_entity(position)
                                self.draw(game)
                                self._root.after_cancel(animation)
                            else:#Encounter other entities
                                self._root.after_cancel(animation)
                        else:
                            position1=(position.get_y(),position.get_x())
                            arrow=self._game_map.create_image(self._game_map.\
                                get_position_center(position1),image=im)
                            self._root.after(200,
                            lambda:show_arrow(game,position))
        self.draw(game)
    
    def back(self):
        """Execute the time return operation to return the game to the previous 
        five steps"""
        self._root.after_cancel(s)#Cancel the original after loop
        grid = Grid(self._size)
        loader = MasterMapLoader()
        if self.move_step > 5:
            # Remove the data stored in the last five steps
            for i in range(self.move_step-4,self.move_step+1):
                time_dict.pop(i)
            # Remove the time machine and add other entities
            for key,value in time_dict[self.move_step-5][0].items():
                if value != TIME_MACHINE:
                    grid.add_entity(Position(key[0],key[1]),
                    loader.create_entity(value))
            game1 = AdvancedGame(grid)# Create a new game instance
            # Remove the time machine and add the state of inventory
            for key,value in time_dict[self.move_step-5][1].items():
                item = loader.create_entity(key)
                if value == True:
                    item.toggle_active()
                if not isinstance(item,TimeMachine):
                    game1.get_player().get_inventory().add_item(item)
            # Remove the time machine
            try:
                del time_dict[self.move_step-5][2][TIME_MACHINE]
            except:
                pass
            # Add lifetime of inventory
            for i,key in enumerate(time_dict[self.move_step-5][2]):
                lifetime=time_dict[self.move_step-5][2][key]
                game1.get_player().get_inventory().get_items()[i].\
                    _lifetime=lifetime
            self.move_step = self.move_step-5
            #Return time to before five steps
            self.sec_num = time_dict[self.move_step-5][3]
            self.play(game1)
        else:
            """If there have been fewer than 5 steps in the current game, 
            the game is essentially reset."""
            self.restart()
    
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
            high_scores = dict(sorted(high_scores.items(), 
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
                if i==MAX_ALLOWED_HIGH_SCORES-1:
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
            app = MastersGraphicalInterface(root, game.get_grid().get_size())
            app.play(game)
            root.mainloop()
        if game.has_won() or game.has_lost():
            mins=self.sec_num//60
            secs=self.sec_num%60
            if game.has_won():
                root1=tk.Toplevel(self._root)#Create a toplevel
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
                            high_scores[v[0]]=int(v[1])
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
                #If the player has a time machine
                if game.get_player().get_inventory().contains(TIME_MACHINE):
                    self.back()
                    self._root.after_cancel(s)
                else:
                    root1=tk.Toplevel(self._root)
                    root1.title('You lose')
                    root1.geometry('150x50')
                    tk.Label(root1,text="You lose in {0}m and {1}s!"\
                        .format(mins,secs)).grid(row=1,column=1,columnspan=2)  
                    root1.mainloop()
        s = self._root.after(1000,lambda: self._step(self.game))