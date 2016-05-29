# This program is designed to simulate a virtual pet in the terminal. 
import sys, time, random
from Tkinter import *
# import ScrolledText as tkst

# Converts between realtime (seconds) to pet years
_TIME_CONVERSION = 10 #7*24*60*60 # One week
MONEY = 100
TOTAL_SLOTS = 3

class Pet(object):
    """Generic Pet object. Stores all data related to pet
    like its health, age, happiness, etc."""
    species = "Generic"
    health_max = 100
    happiness_max = 100
    hunger_max = 100
    cost = 0
    def __init__(self, name="SampleName"):
        self.health = self.health_max
        self.age = 0 # Pet years. One Week is a year 
        self.time_alive = 0 # RealTime
        self.happiness = self.happiness_max / 2
        self.hunger = 0
        self.name = name

        # Graphics part
        self.frame = Toplevel()
        self.frame.title(self.name + " the " + self.species)
        self.textDisplay = Text(
            master = self.frame,
            wrap   = 'word',  # wrap text at full words only
            width  = 40,      # characters
            height = 10,      # text lines
            bg='beige'        # background color of edit area
        )
        self.textDisplay.pack()

        feed = Button(self.frame, text="Feed", command=lambda:self.increase_hunger(-10))
        feed.pack()
        hug = Button(self.frame, text="Hug", command=lambda:self.increase_happiness(random.randint(0,3)))
        hug.pack()
        self.update_display()

    def increase_happiness(self, x=1):
        self.happiness += x
    def increase_time_alive(self, x):
        self.time_alive += x
        self.age = self.time_alive % _TIME_CONVERSION
    def increase_health(self, x=1):
        self.health += x
    def increase_hunger(self, x=1):
        self.hunger += x

    def display_text(self):
        s = ""
        s += self.name + " the " + self.species
        s += '\n'
        s += "Health: " + str(self.health) + " of " + str(self.health_max)
        s += '\n'
        s += "Happiness: " + str(self.happiness) + " of " + str(self.happiness_max)
        s += '\n'
        s += "Hunger: " + str(self.hunger) + " of " + str(self.hunger_max)
        s += '\n'
        return s

    def display_command_line(self):
        """ For testing """
        print self.display_text

    def update_display(self):
        """ Updates an individual pet screen """
        #Deletes old data
        self.textDisplay.config(state=NORMAL)
        self.textDisplay.delete(1.0, END)

        # Setup new text
        newPet_text = self.display_text()
        self.textDisplay.insert('insert', newPet_text)

        # Publish and prevent modification
        self.textDisplay.pack(fill='both', expand=True, padx=8, pady=8)
        self.textDisplay.config(state=DISABLED)

    def save_to_file(self):
        """TODO"""
        pass

    def check_limits(self):
        """ Returns a boolean checking if the pet is alive 
        It does NOT actually kill the pet. This difference
        is intended for testing. 
        Will also reset health and happiness to maximum if they
        exceed.

        Note that since a generic pet shouldn't exist, it will
        immediately die. """

        if self.health <= 0:
            return True     
        if self.hunger > self.hunger_max:
            return True
        # if self.happiness <= 0:
        #     return True
        
        # Prevents going over or under limits.
        self.health = min(self.health, self.health_max)
        self.happiness = min(self.happiness, self.happiness_max)
        self.hunger = max(self.hunger, 0)
        self.happiness = max(self.happiness, 0)

        # Increases money coutner based on how happy pets are.
        global MONEY
        MONEY += (1+self.happiness)

        return False

    def lives(self):
        """ Checks if pet is dead. If it violates the limits, then
        the pet dies. Returns the Pet's name and type """
        if self.check_limits():
            return False
        else:
            return True

class SlimePet(Pet):
    """Weakest Pet. Has low health, doesn't require 
    food or happiness. Does not reward much money. """
    species = "Slime"
    health_max = 10
    happiness_max = 10
    hunger_max = sys.maxint # Don't worry if we hit this. No player will ever hit that
    cost = 100
    def __init__(self, name="SampleName"):
        super(SlimePet, self).__init__(name)

class FishPet(Pet):
    """Weak Pet. Has low health, doesn't require 
    happiness. Does not reward much money. """
    species = "Fish"
    health_max = 12
    happiness_max = 10
    hunger_max = 24
    cost = 500
    def __init__(self, name="SampleName"):
        super(FishPet, self).__init__(name)

def kill_pet(pets):
    for i in pets:
        if not(i.lives()):
            i.frame.destroy()
            pets.remove(i)
def update_pet(pets, x):
    map((lambda pet:pet.increase_time_alive(x)), pets)
    map((lambda pet:pet.increase_hunger(int(x))), pets)
    map((lambda pet:pet.increase_happiness(-(random.randint(0,10)/10))), pets)
    map((lambda pet:pet.update_display()), pets)
    

pets = []

# File Commands
def open_pet():
    print "TODO: Open saved pets."

def save_pet():
    print "TODO: Save open pets to file."

# BuyPet Commands

def acquirePet(species, name, frame):
    global MONEY
    if len(pets) >= TOTAL_SLOTS:
        # Failed because too many pets
        frame.destroy()
        return
    if MONEY < species.cost:
        # Failed because not enough money
        frame.destroy()
        return
    MONEY -= species.cost
    # Deal with issues from the textbox
    name = name.encode('ascii','ignore')
    name = name.strip()

    # Actually create the pet
    newpet = species(name=name)
    pets.append(newpet)
    frame.destroy()
    updateGlobalText()

def buy_pet(species):
    """ This function lets us buy a pet from the menu.
    It sets up the relevant global variables. """

    newPetFrame = Toplevel(root, bg='brown')
    newPetFrame.title("New Pet")
    newPetBar = Text(
        master = newPetFrame,
        wrap   = 'word',  # wrap text at full words only
        width  = 25,      # characters
        height = 3,      # text lines
        bg='beige'        # background color of edit area
    )
    newPet_text = '''SampleName'''
    newPetBar.insert('insert', newPet_text)
    newPetBar.pack(fill='both', expand=True, padx=8, pady=8)

    submit = Button(newPetFrame, text="Submit", command=lambda :acquirePet(species, newPetBar.get(0.0,25.0), newPetFrame))
    submit.pack()


# Buy upgrade commands
def addSlot():
    global TOTAL_SLOTS
    TOTAL_SLOTS += 1
    updateGlobalText()

def updateGlobalText():
    global_text.config(state=NORMAL)
    global_text.delete(1.0, END)
    globalText = '''\
    You have {} pets.
    You have {} additional slots.
    You have {} money.
    '''.format(len(pets), TOTAL_SLOTS - len(pets), MONEY)
    global_text.insert('insert', globalText)
    global_text.config(state=DISABLED)
    return
# Help Commands
def popup():
    frame2 = Toplevel(root, bg='brown')
    frame2.title("Instructions")
    help_bar = Text(
        master = frame2,
        wrap   = 'word',  # wrap text at full words only
        width  = 50,      # characters
        height = 20,      # text lines
        bg='beige'        # background color of edit area
    )
    help_bar.pack(fill='both', expand=True, padx=8, pady=8)
    help_text = '''\
    TODO: Help Text here.
    '''
    help_bar.insert('insert', help_text)
    help_bar.config(state=DISABLED)

root = Tk(className=" Pyagatchi-chan Menu")

menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_pet)
filemenu.add_command(label="Save", command=save_pet)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
buypetmenu = Menu(menubar, tearoff=0)
buypetmenu.add_command(label="Slime", command=lambda:buy_pet(SlimePet))
buypetmenu.add_command(label="Fish", command=lambda:buy_pet(FishPet))
menubar.add_cascade(label="Buy Pets", menu=buypetmenu)

# TODO: Implement upgrades
buyupgrademenu = Menu(menubar, tearoff=0)
buyupgrademenu.add_command(label="Additional Slot", command=addSlot)
buyupgrademenu.add_command(label="Food Quality", command=None)
menubar.add_cascade(label="Upgrades", menu=buyupgrademenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=popup)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

frame = Frame(root, bg='brown')
frame.pack(fill='both', expand='yes')
global_text = Text(
    master = frame,
    wrap   = 'word',  # wrap text at full words only
    width  = 50,      # characters
    height = 20,      # text lines
    bg='beige'        # background color of edit area
)
# the padx/pady space will form a frame
global_text.pack(fill='both', expand=True, padx=8, pady=8)
updateGlobalText()

#Start the timer
# We don't really need it actually ...
# tm = time.time()

def loop_calls():
    update_pet(pets, 1)
    kill_pet(pets)
    updateGlobalText()
    root.after(1000, func=loop_calls)


root.after(1000, func=loop_calls)
root.mainloop()

