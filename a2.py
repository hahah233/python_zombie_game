#!/usr/bin/env python
# coding: utf-8


"""
End of Dayz
Assignment 2
Semester 1, 2021
CSSE1001/CSSE7030

A text-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""

from typing import Tuple, Optional, Dict, List

from a2_support import *

__author__ = "zhe Sun, 46676243"
__email__ = "s4667624@student.uq.edu.au"

class Entity:
    """Class Entity is used to represent anything that can appear on 
      the game’s grid."""
    
    def step(self, position: Position, game: 'Game') -> None:
        """The method is called on every entity in the grid after each 
        move made by player, it controls every entity's action.The Entity
        class do nothing in the method.

        Parameters:
            position: A Position class represent the entity's position 
                      in the grid.
            game: A Game class represent the game which being played.
        """
        pass
    
    def display(self) -> str:
        """Return the character used to represent this entity in a text-based
        grid. An instance of Entity class don't have character to represent 
        itself. This method should only be implemented by subclasses of Entity.
        
        Raise:
            NotImplementedError: If an instance of Entity class want to 
                                 implement this method.
        """
        raise NotImplementedError
    
    def __repr__(self) -> str:
        """Return a representation of this entity.

        Return: A string of class name followed by parentheses()
        """
        return'{}()'.format(self.__class__.__name__)

class Player(Entity):
    """Player class is a subclass of the Entity class that represents the 
    player in the grid."""
    
    def display(self) -> str:
        """Return the character used to represent this player in a text-based
        grid.

        Return: The letter 'P' to represent the player.
        """
        return PLAYER

class Hospital(Entity):
    """Hospital class is a subclass of the Entity class that represents the 
    hospital in the grid.The hospital is the entity that the player has to 
    reach in order to win the game."""
    
    def display(self) -> str:
        """Return the character used to represent the hospital in a text-based
        grid.

        Return: The letter 'H' to represent the hospital.
        """
        return HOSPITAL

class Grid:
    """The Grid class is used to represent a 2D square grid. Each entity 
    appears as a letter on a (x,y) position. Each (x, y) position in the grid 
    can only contain one entity at a time."""
    
    def __init__(self, size:int):
        """
        Parameters:
            size: The length and width of the grid.
        """
        self._size = size
        self._mapping = {} # Used to store entity
    
    def get_size(self) -> int:
        """Return the size of the grid"""
        return self._size
    
    def in_bounds(self, position: Position) -> bool:
        """Return if the given position is within the bounds of the grid or not.

        Parameters:
            position: An (x, y) position that we want to check is within the 
                      bounds of the grid.
        """
        return position.get_x() in range(self._size) and \
        position.get_y() in range(self._size)
    
    def add_entity(self, position: Position, entity: Entity) -> None:
        """Add a entity at a position in the grid.If there is already an entity
        at the given position, the given entity will replace the existing 
        entity.If the given position is outside the bounds of the grid, the 
        entity should not be added.

        Parameters:
            position: The (x,y) position of the entity we want to add
            entity: An Entity class we want to add
        """
        if self.in_bounds(position) == True:
            self._mapping[position] = entity
    
    def remove_entity(self, position: Position) -> None:
        """Remove the entity, if any, at the given position.
        
        Parameters:
            position: The (x,y) position of the entity we want to remove.
        """
        self._mapping.pop(position)
    
    def get_entity(self, position: Position) -> Optional[Entity]:
        """Return the entity that is at the given position in the grid.
          If there is no entity at the given position, returns None.
        
        Parameters:
            position: The (x,y) position of the entity we want to get.
        
        Return: The entity that is at the given position in the grid,
                None if there is no entity at the given position.
        """
        return self._mapping.get(position)
    
    def get_mapping(self) -> Dict[Position, Entity]:
        """Return a dictionary with position as the keys and corresponding 
        entity in the grid as the values.
        
        Return: A dictionary with position as the keys and corresponding 
                entity in the grid as the values,
                Empty dictionary {} if the grid doesn't add anything.
        """
        # Make a copy for updating the returned list would not modify the grid.
        dic = self._mapping.copy() 
        return dic
    
    def get_entities(self) -> List[Entity] :
        """Return a list of all the entities in the grid.
        
        Return: A list of all the entities in the grid.
        """
        return list(self._mapping.values())
    
    def move_entity(self, start: Position, end: Position) -> None:
        """Move an entity from the start position to the end position.
        If the end position or start position is out of the grid bounds, 
        do not attempt to move.
        If there is an entity at the given end position,replace that entity 
        with the entity from the start position.
        
        Parameters:
            start: The starting position of the entity we want to move.
            end: The ending position of the entity we want to move.
        """
        # check if the end position or start position is out of the grid bounds
        if self.in_bounds(end) == True and self.in_bounds(start) == True:
            self._mapping[end] = self._mapping.pop(start)# replace the entity
    
    def find_player(self) -> Optional[Position]:
        """Return the position of the player within the grid.
        
        Return: the position of the player within the grid,
                None if there is no player in the grid.
        """
        for key in self._mapping:
            if isinstance(self._mapping[key], Player):
                return key
        return None
    
    def serialize(self) -> Dict[Tuple[int, int], str]:
        """Serialize the grid into a dictionary that position tuples to 
        characters.
        
        Return: Dictionary that position tuples [x,y] to characters which
                represent the entity,
                Empty dictinary {} if the grid doesn't add anything.
        """
        temp = {}
        temp1 = self._mapping.copy() # copy the dict that position to entity
        for key in temp1:
            # translate the entity values to the character
            temp1[key] = temp1[key].display() 
            # get a dictionary that position to tuple (x,y)
            temp[key] = (key.get_x(), key.get_y()) 
        # get the dictionary that tuple (x,y) to character
        serialize_map = {temp[k]: v for k, v in temp1.items()} 
        return serialize_map

class MapLoader:
    """The MapLoader class is used to read a map file and create an appropriate
    Grid instance which stores all the map file entities."""
    
    def load(self, filename:str) -> Grid:
        """Load a new Grid instance from a map file.

        Parameters:
            filename: Path where the map file should be found.
        
        Return: A new Grid instance.
        """
        # Receive serialized map and the size of the map separately
        result,size = load_map(filename) 
        grid = Grid(size) 
        # Add entities to the grid
        for key,value in result.items():
            try:
                # Translate (x,y) and characters to the position and entities
                grid.add_entity(Position(key[0], key[1]),\
                self.create_entity(value)) 
            # When the maploader do not support the entity that value represent
            except ValueError:
                continue
        return grid
    
    def create_entity(self, token:str) -> Entity:
        """Create and return a new instance of the Entity class based on the 
        provided token.
        
        Parameters:
            token: A character represent the entity
        
        Raise:
            NotImplementedError: The MapLoader class does not support any 
                                 entities, when this method is called, 
                                 raise a NotImplementedError.
        """
        raise NotImplementedError

class BasicMapLoader(MapLoader):
    """BasicMapLoader is a subclass of MapLoader which can handle loading map 
    files which include the player and hospital."""
    
    def create_entity(self, token: str) -> Entity:
        """Create and return a new instance of the Entity class based on the 
        provided token.
        
        Parameters：
            token: A character represent the entity
        
        Raise:
            ValueError: The BasicMapLoader class only supports the Player and 
                        Hospital entities.Other tokens will raise a ValueError.
        """
        if token == PLAYER:
            return Player()
        elif token == HOSPITAL:
            return Hospital()
        else:
            raise ValueError

class Game:
    """The Game class stores an instance of the Grid and controlls actions of 
    entities in the grid."""
    
    def __init__(self, grid: Grid):
        """The construction of a Game instance takes the grid upon which the 
        game is being played.
        
        Preconditions: The grid has a player.
        
        Parameters:
            grid: A Grid instance which the game play.
        """
        self._grid = grid
        self._stepnum = 0
    
    def get_grid(self) -> Grid:
        """Return the grid on which this game is being played"""
        return self._grid
    
    def get_player(self) -> Optional[Player]:
        """Return the instance of the Player class in the grid.
        
        Return: the instance of the Player class in the grid,
                None if there is no player in the grid.
        """
        for value in self._grid.get_mapping().values():
            if isinstance(value, Player):
                return value
        return None
    
    def step(self) -> None:
        """The method will call the step method of every entity in the grid 
        after every action performed by the player."""
        keys = list(self._grid.get_mapping().keys())
        values = list(self._grid.get_mapping().values())
        for i in range(len(values)):
            """Every entity call the step method pass the entity’s current 
            position and this game as parameters."""
            values[i].step(keys[i],self)
        self._stepnum += 1 # Count the step of the game
    
    def get_steps(self) -> int:
        """Return the amount of steps made in the game."""
        return self._stepnum
    
    def move_player(self, offset: Position) -> None:
        """Move the player entity in the grid by a given offset.
        
        Parameters:
            offset: A position to add to the player’s current position to 
                    produce the player’s new desired position.
        """
        position = self._grid.find_player() # Player's current position
        self._grid.move_entity(position, position.add(offset))
    
    def direction_to_offset(self, direction: str) -> Optional[Position]:
        """Convert a direction, as a string, to a offset position.
        
        Parameters:
            direction: Character representing the direction in which the player 
                       should be moved.
        
        Return: A offset position,
                None if the given direction is not valid.
        """
        if direction in DIRECTIONS: # A tuple ('W', 'A', 'S', 'D')
            if direction == UP: # 'W'
                return Position(0,-1)
            elif direction == LEFT: # 'A'
                return Position(-1,0)
            elif direction == DOWN: # 'S'
                return Position(0,1)
            else: # 'D'
                return Position(1,0)
        return None
    
    def has_won(self) -> bool:
        """Return if the player has won the game or not."""
        for value in self._grid.get_mapping().values():
            if isinstance(value,Hospital): # if there is a Hospital in the grid
                return False   
        return True
    
    def has_lost(self) -> bool:
        """Return if the player has lost the game or not.
        
        Return: False cause currently there is no way for the player to lose 
                the game."""
        return False

class TextInterface(GameInterface):
    """A text-based interface which handles all input collection from the user 
    and printing to the grid between the user and the game instance."""
    
    def __init__(self, size):
        """
        Parameters:
            size: The size of the grid in the game to be displayed and played.
        """
        self.size = size
    
    def draw(self, game: Game) -> None:
        """Print out the given game surrounded by ‘#’ characters representing
        the border of the game.

        Parameters: 
            game: An instance of the game class that is to be displayed to 
                  the user by printing the grid.
        """
        print((self.size+2)*BORDER)
        temp = [' ']*(self.size**2) # Create a list for subsequent print
        _ = game.get_grid().serialize()
        for key, value in _.items():
            # Determine the index of characters in the list 
            index = key[0] + key[1]*self.size 
            temp[index] = value
        for i in range(self.size):
            # Output border and 'size' elements per line
            print(BORDER,''.join(temp[self.size*i:self.size*(i+1)]),\
            BORDER, sep='')
        print((self.size+2)*BORDER)
    
    def play(self, game: Game) -> None:
        """The play method constantly prompting the user for their action, performing the
        action and printing the game until the game is over.
        
        Parameters:
            game: A game instance to start playing.
        """
        while True:
            self.draw(game)
            action = input(ACTION_PROMPT)
            self.handle_action(game, action)
            if game.has_won():
                print(WIN_MESSAGE)
                break
            elif game.has_lost():
                print(LOSE_MESSAGE)
                break
                
    def handle_action(self, game: Game, action: str) -> None:
        """The method is used to process the actions entered by the user 
        in a game.

        Parameters:
            game: The game that is currently being played.
            action: An action entered by the player.
        """
        # If the action in ('W', 'A', 'S', 'D')
        if game.direction_to_offset(action): 
            position = game.direction_to_offset(action)
            game.move_player(position)
        game.step() # Whatever the action is, call the method
        
class VulnerablePlayer(Player):
    """The VulnerablePlayer class is a subclass of the Player, this class 
    allow players to become infected."""
    
    def __init__(self):
        """The initial state of the player is not infected."""
        self._state = False
    
    def infect(self) -> None:
        """The player becomes infected."""
        self._state = True
    
    def is_infected(self) -> bool:
        """Return if the player is infected."""
        return self._state

class Zombie(Entity):
    """The Zombie entity will wander the grid at random direction."""
    
    def step(self, position: Position, game: Game) -> None:
        """The method move the zombie in a random direction.
        
        Parametrs:
            position: The position of this zombie currently.
            game: The game being played.
        """
        _ = random_directions()
        for i in _:
            # If the zombie move to other entities
            if position.add(Position(i[0],i[1])) in \
                game.get_grid().get_mapping(): 
                # If the zombie move to a player
                if position.add(Position(i[0],i[1])) == \
                    game.get_grid().find_player():
                    # Don't move and Infect the player
                    game.get_player().infect() 
                    break
                else:
                    continue
            else:
                """If the Zombie's next move position is in the grid and don't 
                have other entities."""
                if game.get_grid().in_bounds(position.add(Position(i[0],i[1]))):
                    # Move the zombie
                    game.get_grid().move_entity(position,\
                    position.add(Position(i[0],i[1])))
                    break
                else:
                    continue
    
    def display(self) -> str:
        """Return the character used to represent this zombie in a text-based
        grid.

        Return: The letter 'Z' to represent the zombie.
        """
        return ZOMBIE

class IntermediateGame(Game):
    """A subclass of Game, the intermediate game includes the ability for the 
    player to lose the game when they become infected."""
   
    def has_lost(self) -> bool:
        """Return true if the player has lost the game."""
        if self.get_player().is_infected():
            return True

class IntermediateMapLoader(BasicMapLoader):
    """The class extends BasicMapLoader to allow to add zombie. When a player 
    token is found, a VulnerablePlayer instance is created instead of a 
    Player."""
    
    def create_entity(self, token: str) -> Entity:
        """Create and return a new instance of the Entity class based on the 
        provided token.
        
        Parameters：
            token: A character represent the entity.
        
        Raise:
            ValueError: The IntermediateMapLoader class only supports the 
                        Player, Hospital and zombie entities.Other tokens will 
                        raise a ValueError.
        """
        if token == PLAYER:
            return VulnerablePlayer()
        elif token == HOSPITAL:
            return Hospital()
        elif token == ZOMBIE:
            return Zombie()
        else:
            raise ValueError

class TrackingZombie(Zombie):
    """TrackingZombie can see the player and move towards them"""
    
    def step(self, position: Position, game: Game) -> None:
        """This method move the tracking zombie in the best possible direction 
        to move closer to the player.If there are multiple directions that 
        result in being the same distance from the player, the direction should
        be picked in preference order picking ‘W’ first followed by ’S’, ’N’, 
        and finally ’E’.
        
        Parametrs:
            position: The position of this zombie currently.
            game: The game being played.
        """
        # Create a list by the preference 'W', 'S', 'N', 'E'
        _ = [(-1,0),(0,-1),(0,1),(1,0)]
        """Sort the list according the distance between the position of 
        tracking zombie will move and the position of player."""
        _.sort(key = lambda t: position.add(Position(t[0],t[1]))\
        .distance(game.get_grid().find_player())) 
        for i in _:
            # If the tracking zombie move to other entities
            if position.add(Position(i[0],i[1])) in \
                game.get_grid().get_mapping():
                # If the tracking zombie move to a player
                if position.add(Position(i[0],i[1])) == \
                    game.get_grid().find_player():
                    # Don't move and Infect the player
                    game.get_player().infect()
                    break
                else:
                    continue
            else:
                """If the Zombie's next move position is in the grid and don't 
                have other entities."""
                if game.get_grid().in_bounds(position.add(Position(i[0],i[1]))):
                    # Move the tracking zombie
                    game.get_grid().move_entity(position,\
                    position.add(Position(i[0],i[1])))
                    break
                else:
                    continue
    
    def display(self) -> str:
        """Return the character used to represent this zombie in a text-based
        grid.

        Return: The letter 'T' to represent the zombie.
        """
        return TRACKING_ZOMBIE      

class Pickup(Entity):
    """The player can pickup and hold this entity in their inventory. Suppose
    this entity's durability is 0."""
    
    durability = 0
    def __init__(self):
        """When a Pickup entity is created, it's lifetime should be equal to 
        it's durability."""
        self._lifetime = self.durability
    
    def get_durability(self) -> int:
        """Return the durability(maximum lifetime) of this entity.
        
        Raise:
            NotImplementedError: This method needs to be implemented by 
                                 subclasses.
        """
        raise NotImplementedError
    
    def get_lifetime(self) -> int:
        """Return the remaining lifetime of the entity."""
        return self._lifetime
    
    def hold(self) -> None:
        """Make the lifetime of the entity decrease by one."""
        self._lifetime -= 1
    
    def __repr__(self) -> str:
        """Return a string that contains the type of the pickup entity and the
        remaining lifetime."""
        return'{}({})'.format(self.__class__.__name__,self._lifetime)

class Garlic(Pickup):
    """Garlic is an entity which the player can pickup, While the player is 
    holding a garlic entity they cannot be infected by a zombie."""
    
    durability = 10
    def get_durability(self) -> int:
        """Return the durability(maximum lifetime) of garlic. It's 10."""
        return self.durability
    
    def display(self) -> str:
        """Return the character 'G' to represent the garlic in the grid."""
        return GARLIC  

class Crossbow(Pickup):
    """Crossbow is an entity which the player can pickup. While the player is 
    holding a crossbow entity they can use the fire action to remove the first 
    zombie in a direction."""
    
    durability = 5
    def get_durability(self) -> int:
        """Return the durability(maximum lifetime) of crossbow. It's 5."""
        return self.durability
    
    def display(self) -> str:
        """Return the character 'C' to represent the crossbow in the grid."""
        return CROSSBOW

class Inventory:
    """An inventory stores entities which the player can pickup."""
    
    def __init__(self):
        """When an inventory is constructed, it does not contain any items."""
        self._item = []
    
    def step(self) -> None:
        """When this method is called, the lifetime of every item stored 
        within the inventory decrease by one."""
        for i in self._item:
            i.hold() # Decrease lifetime by one
        """Update storage list, if the lifetime is less than or equal to zero, 
        the item will be removed."""
        self._item = self.get_items()
    
    def add_item(self, item: Pickup) -> None:
        """Add a entity to the inventory.
        
        Parameters: 
            item: : The pickup entity to add to the inventory.
        """
        self._item.append(item)
    
    def get_items(self) -> List[Pickup]:
        """Return the pickup entity instances currently stored in the inventory
        
        Return: A list of pickup entity instances currently stored in the 
                inventory,
                Empty list if inventory doesn't add any items.
        """
        for i in self._item:
            """if the lifetime is less than or equal to zero, the item will be 
            removed."""
            if i.get_lifetime() <= 0:
                self._item.remove(i)
        return self._item
    
    def contains(self, pickup_id: str) -> bool:
        """Return if the inventory contains any entities which is represented 
        by the given pickup_id or not.
        
        Parameters:
            pickup_id: A string represent a type of pickup entity.
        """
        for i in self._item:
            if i.display() == pickup_id:
                return True
        return False

class HoldingPlayer(VulnerablePlayer):
    """The HoldingPlayer can keep an inventory."""
    
    def __init__(self):
        """The initial state of the HoldingPlayer is not infected and have an 
        empty inventory."""
        self._state = False
        self._inventory = Inventory()
    
    def get_inventory(self) -> Inventory:
        """Return the player's Inventory instance."""
        return self._inventory
    
    def infect(self) -> None:
        """If a player is holding a garlic, the player is immune to becoming 
        infected."""
        if self._inventory.contains(GARLIC):
            self._state = False
        else:
            self._state = True
    
    def step(self, position: Position, game: Game) -> None:
        """Call the step method in the player's inventory instance.

        Parameters:
            position: The position of this HoldingPlayer.
            game: The current game being played.
        """
        self._inventory.step()           

class AdvancedGame(IntermediateGame):
    """Players can pick up a Pickup item when they come into contact with it"""
    
    def move_player(self, offset: Position) -> None:
        """Move the player in the grid by a given offset. If the player moves 
        onto a Pickup item, add the item to the player’s inventory and remove 
        from the grid.
        
        Parameters:
            offset: A position to add to the player’s current position to 
                    produce the player’s new desired position.
        """
        position = self.get_grid().find_player() # The position of the Player
        # If the new position have a entity
        if position.add(offset) in self.get_grid().get_mapping():
            entity = self.get_grid()._mapping[position.add(offset)]
            # If the entity is a pickup, add it to the inventory
            if isinstance(entity, Pickup): 
                self.get_player().get_inventory().add_item(entity)
        self.get_grid().move_entity(position, position.add(offset))

class AdvancedMapLoader(IntermediateMapLoader):
    """The class extends IntermediateMapLoader to allow to add Trackingzombie
    and Pickup(Garlic and Crossbow). When a player token is found, a 
    HoldingPlayer instance is created instead of a VulnerablePlayer."""
    
    def create_entity(self, token: str) -> Entity:
        """Create and return a new instance of the Entity class based on the 
        provided token.
        
        Parameters：
            token: A character represent the entity.
        
        Raise:
            ValueError: The AdvancedMapLoader class only supports the 
                        Player, Hospital, Zombie, TrackingZombie and Pickup
                        entities. Other tokens will raise a ValueError.
        """
        if token == PLAYER:
            return HoldingPlayer()
        elif token == HOSPITAL:
            return Hospital()
        elif token == ZOMBIE:
            return Zombie()
        elif token == TRACKING_ZOMBIE:
            return TrackingZombie()
        elif token == GARLIC:
            return Garlic()
        elif token == CROSSBOW:
            return Crossbow()
        else:
            raise ValueError

class AdvancedTextInterface(TextInterface):
    """This class extends the existing functionality of TextInterface to 
    include displaying the state of the player’s inventory and a firing 
    action."""

    def draw(self, game: Game) -> None:
        """Print out the given game surrounded by ‘#’ characters representing
        the border of the game.If a player is holding items in their inventory,
        this method would show this.
        
        Parameters: 
            game: An instance of the game class that is to be displayed to 
                  the user by printing the grid.
        """
        print((self.size+2)*BORDER)
        temp=[' ']*(self.size**2) # Create a list for subsequent print
        _ = game.get_grid().serialize()
        for key, value in _.items():
            # Determine the index of characters in the list
            index = key[0] + key[1]*self.size
            temp[index] = value
        for i in range(self.size):
            # Output border and 'size' elements per line
            print(BORDER,''.join(temp[self.size*i:self.size*(i+1)]),\
            BORDER,sep='')
        print((self.size+2)*BORDER)
        # If a player is holding items in their inventory
        if game.get_player().get_inventory().get_items():
            print(HOLDING_MESSAGE)
        for i in game.get_player().get_inventory().get_items():
            print(i)
    def handle_action(self, game: Game, action: str) -> None:
        """The method extend the interface to be able to handle the fire
        action for a crossbow.
        
        Parameters:
            game: The game that is currently being played.
            action: An action entered by the player.
        """
        if action == FIRE:
            # If the player have a crossbow
            if game.get_player().get_inventory().contains(CROSSBOW):
                direction = input(FIRE_PROMPT) # Fire direction
                _ = []
                position = game.get_grid().find_player() # Player's position
                mapping = game.get_grid().get_mapping() # Game's mapping
                if direction == UP:
                    for key in mapping:
                        # If there are entities in the 'W' direction
                        if key.get_x() == position.get_x() and \
                            key.get_y() < position.get_y():
                            _.append(key)
                    # Sort by the distance between entities and the player.
                    _.sort(key = lambda t: t.distance(position))
                    # If the first entity in the direction is zombie.
                    if _ and isinstance(mapping[_[0]],Zombie):
                        # Remove the first zombie in the fire direction.
                        game.get_grid().remove_entity(_[0])
                    else:
                        print(NO_ZOMBIE_MESSAGE)
                    game.step()
                elif direction == DOWN:
                    for key in mapping:
                        # If there are entities in the 'S' direction
                        if key.get_x() == position.get_x() and \
                            key.get_y() > position.get_y():
                            _.append(key)
                    # Sort by the distance between entities and the player.
                    _.sort(key = lambda t: t.distance(position))
                    # If the first entity in the direction is zombie.
                    if _ and isinstance(mapping[_[0]],Zombie):
                        # Remove the first zombie in the fire direction.
                        game.get_grid().remove_entity(_[0])
                    else:
                        print(NO_ZOMBIE_MESSAGE)
                    game.step()
                elif direction == LEFT:
                    for key in mapping:
                        # If there are entities in the 'A' direction
                        if key.get_y() == position.get_y() and \
                            key.get_x() < position.get_x():
                            _.append(key)
                    # Sort by the distance between entities and the player.
                    _.sort(key = lambda t: t.distance(position))
                    # If the first entity in the direction is zombie.
                    if _ and isinstance(mapping[_[0]],Zombie):
                        # Remove the first zombie in the fire direction.
                        game.get_grid().remove_entity(_[0])
                    else:
                        print(NO_ZOMBIE_MESSAGE)
                    game.step()
                elif direction == RIGHT:
                    for key in mapping:
                        # If there are entities in the 'D' direction
                        if key.get_y() == position.get_y() and \
                            key.get_x() > position.get_x():
                            _.append(key)
                    # Sort by the distance between entities and the player.
                    _.sort(key = lambda t: t.distance(position))
                    # If the first entity in the direction is zombie.
                    if _ and isinstance(mapping[_[0]],Zombie):
                        # Remove the first zombie in the fire direction.
                        game.get_grid().remove_entity(_[0])
                    else:
                        print(NO_ZOMBIE_MESSAGE)
                    game.step()
                else: 
                    # The fire direction is not one of ‘W’, ‘A’, ‘S’ or ‘D          
                    print(INVALID_FIRING_MESSAGE)
            else:
                # The player doesn't have a crossbow now
                print(NO_WEAPON_MESSAGE)
        else:
            # If the action in ('W', 'A', 'S', 'D')
            if game.direction_to_offset(action):
                game.move_player(game.direction_to_offset(action))
            game.step() # Whatever the action is, call the method
                
def main():
    """Load a map and play a game."""
    while True:
        filename = input('Map: ')
        maploader = AdvancedMapLoader()
        grid = maploader.load(filename)
        game = AdvancedGame(grid)
        interface = AdvancedTextInterface(grid.get_size())
        interface.play(game)
        answer = input('If you want to play again?: ')
        if answer == 'Y' or answer == 'y': # If player want to play again
            continue
        else:
            break

if __name__ == "__main__":
    main()







