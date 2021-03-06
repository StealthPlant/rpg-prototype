import random
import tkinter as tk
import time
from random import randint
class UI():
    #setup makes main window
    def __init__(self, main):
        self.main = main
       ##self.output = tk.Label(main, anchor = 'nw', justify = 'left')
        self.inpt =  tk.Text(main, height = 1, fg='#22ee22', bg='#000800')
        #self.enterbut = tk.Button(main, text='Enter', background = 'light blue', height = 1, command = lambda:( self.enter(self.inpt,self.inpt.get('1.0','end')) ))
        #self.enterbut = tk.Button(main, text='Enter', background = 'black', height = 1, command = lambda:( self.enter(self.inpt,self.inpt.get('1.0','end')) ))
        self.text = ''

        self.situation = ["You stand in an empty room. There is a door ahead of you and a door behind you", ["Try north door", "Try south door", "Other"]]
    
   
        
        self.main.geometry("850x700")
        self.main.config(background ='#000800')

        #Big output text box. Disabled so cannot be typed in.
        #rel-x,y,height,width are relative placement for window
        #self.output = tk.Label(main, anchor = 'nw', justify = 'left')
        self.output = tk.Label(main, anchor = 'nw', justify = 'left',  font = ('Courier New', 9), fg='#22ee22', bg='#000800')
        self.output.place(relx =0.2, rely = 0.02, relheight=0.6, relwidth=0.8)

        #Input box
        #calls 'enter' on key press return/enter key
        
        self.inpt.bind("<Return>", lambda x: self.enter(self.inpt,self.inpt.get('1.0','end-1c')))
        self.inpt.place(relx =0.2, rely = 0.65,  relwidth=0.5)
        #enter is called with the .get() which takes from the ext box.
        # 1.0 is line.character, so line-1.position=0
        # end is end if text box, -1c is less 1 character (can be written as -1character)
        # 'end-1c' as oppose to 'end' ommits end \n from typed enter key

       # self.fightBTN = t

        #button that calls 'enter' same as above, save for not having the -1c after 'end' as no \n is typed (hope this makes sense)
        
        #self.enterbut.place(relx = 0.71, rely = 0.645, relwidth = 0.09)


    #write fucntion takes text and the textbox it's from 
    def enter(self,inpt,txt):
        if txt != None:
            txt = txt.replace('\n','')

            if txt == 't':
                ui.talkWindow(jeremy,C1)
            txt = self.cleanInput(txt)
            self.cleanOutput()
            
            txt = txt+'\n'
            for i in txt:
                #Types to the end of textbox with value i
                self.text += i
                self.output.config(text = self.text)

                self.inpt.delete('end-2c','end-1c')
                #sleep for that cool typing effect
                time.sleep(0.03)
                #tkinter is shit
                self.main.update()
            #scrolls output to bottom (without its not possible to scroll at all, its odd)   
            #makes sure input is empt but is currently buggy not sure why, seems to automatically lead with a \n or ' ' weird ass shit
            Interpret(txt,jeremy)
            self.inpt.delete('0.0','end')
            #disable output so cannot be typed in
        else:
            pass
           
    def write(self,txt):
        txt = str(txt)
        txt = self.cleanInput(txt)
        self.cleanOutput() 
        txt+='\n'
        self.inpt.config(state = 'disabled')
        for i in txt:
            self.text += i
            self.output.config(text = self.text)
            time.sleep(0.05)
            #tkinter is shit
            self.main.update()
        self.inpt.config(state = 'normal')
        

    def cleanOutput(self):
        if self.text.count('\n')>25:
            cutof = self.text.index('\n')+1
            self.text = self.text[cutof:]

    def cleanInput(self,txt):
        if txt[0] == '\n':
            txt = txt[1:]
        n = 0
        for i in range(len(txt)):
            if txt[i] != '\n':
                n+=1
            else:
                n = 0
                
            if n > 80 and txt[i] == ' ': #arbriaty number
                n = 0
                txt = txt[:i] + '\n' + txt[i+1:]
            elif n > 95:
                n = 0
                txt = txt[:i] + '-\n' + txt[i:]
        return(txt)

    def talkWindow(ui,player,npc):
        talkUi = TalkUi(main,player,npc)




class TalkUi():
    def __init__(self, main,player,npc):
        self.text =''
        self.main = tk.Toplevel(main) 
        self.main.geometry("600x500")
        self.main.config(background ='#001100')

        self.output = tk.Label(self.main, anchor = 'nw', justify = 'left')
        self.output.place(relx =0.2, rely = 0.02, relheight=0.6, relwidth=0.6)

        self.talkBTN = tk.Button(self.main, text='Talk', background = 'light blue', height = 2, command = lambda:(self.TalkEnter(self.inpt,self.inpt.get('1.0','end'),npc) ))
       # self.
        
        self.inpt =  tk.Text(self.main, height = 1)
        self.inpt.bind("<Return>", lambda x: self.TalkEnter(self.inpt,self.inpt.get('1.0','end-1c'),npc))
        self.inpt.bind("<space>", lambda x:self.inpt.delete('0.0','end+2c'))
        self.inpt.place(relx =0.36, rely = 0.65,  relwidth=0.25)
        self.conversationBegin(npc)

        self.mood = [' angry at ',' unhapy with ',' taken aback by ',' fine with ',' happy with ',' enthusiastic with ', ' ecstatic at ']
        
        self.prevWord = 'start'

    def conversationBegin(self,npc):
        self.TalkWrite('You enter conversation with a '+npc.desc)
        self.TalkWrite(npc.name+ ':    ' + npc.talk['start'][0])
        self.inConversation = True



    def reply(self,npc,word):
        if self.inConversation:
            if word in npc.talk:
                if npc.interest + npc.talk[word][1][0] < 7:
                    npc.interest += npc.talk[word][1][0]
                else:
                    npc.interest = 6
                if npc.interest + npc.talk[word][1][0] < 0:
                    self.TalkWrite('That seems to have struck a nerve with %s, they turn away. This conversation is clearly over.'%npc.name)
                    self.inConversation  = False
                else:    
                    self.TalkWrite(npc.name+ ' seems' +self.mood[npc.interest] +'your response')
                    self.TalkWrite(npc.name+ ':    ' + npc.talk[word][0])
                    self.prevWord = word
                
            if word not in npc.talk:
                if npc.talk[self.prevWord][1][1] != 0:
                    npc.interest += npc.talk[self.prevWord][1][1]
                    if npc.interest >-1:
                        self.TalkWrite(npc.name+ ' seems' +self.mood[npc.interest] +'your response')
                    else:
                        self.TalkWrite(npc.name +' has had enough of you. This conversation is clearly over')
                        self.inConversation = False
                else:
                    self.TalkWrite(npc.name + ' didn\'t understand you, but they didn\'t seem to care. They are still' + self.mood[npc.interest] +'you.')





    def TalkEnter(self,inpt,txt,npc):
        
        txt = txt.replace('\n','')
        if txt[-1] in ('?','.',' ','\n'):
            txt = txt[:-1]
        if txt[0] == ' ':
            txt = txt[1:]
        txt = self.cleanInput(txt)
        self.cleanOutput()
        txt = txt+'\n'
        for i in txt:
            self.text += i
            self.output.config(text = self.text)
            
            self.inpt.delete('end-2c','end-1c')
            time.sleep(0.01)
            #tkinter is shit
            self.main.update()
        txt = txt.replace('\n','')
        self.reply(npc,txt)
        self.inpt.delete('0.0','end')

                    
    def TalkWrite(self,txt):
        txt = self.cleanInput(txt)
        self.cleanOutput()
        txt+='\n'
        self.inpt.config(state = 'disabled')
        for i in txt:
            self.text += i
            self.output.config(text = self.text)
            time.sleep(0.03)
            #tkinter is shit
            self.main.update()
        self.inpt.config(state = 'normal')

    def cleanOutput(self):
        if self.text.count('\n')>16:
            cutof = self.text.index('\n')+1
            self.text = self.text[cutof:]

    def cleanInput(self,txt):
        if txt[0] == '\n':
            txt = txt[1:]
        n = 0
        for i in range(len(txt)):
            if txt[i] != '\n':
                n+=1
            else:
                n = 0
                
            if n > 50 and txt[i] == ' ': #arbriaty number
                n = 0
                txt = txt[:i] + '\n' + txt[i+1:]
            elif n >65:
                n = 0
                txt = txt[:i] + '-\n' + txt[i:]
        return(txt)

main = tk.Tk()
ui = UI(main)

class Place(object):
    def __init__(self, name, quality = 3, furnishings = [], objects = [], characters = [],search = ["an empty room"], investigation = ["There is nothing of note here."]):
        self.doors = []
        self.name = name
        #should be of the format [canBeEntered, Description, leadsTo]
        #and because a room can have multiple doors, it'll be a 2D array
        self.quality = quality
        self.furnishings = furnishings
        self.objects = objects
        self.characters = characters

        self.search = search

        self.investigation = investigation
        #should be of the form [canBeInvestigated, Description, leadsTo]
        #'cept obviously you still get a description if you can't

        for furnishing in self.furnishings:
            furnishing.room = self
            
    def showAll(self):
        temp = []
        tempTemp = []
        for furnishing in self.furnishings:
            tempTemp.append(furnishing.name)
        temp.append(tempTemp)
        
        tempTemp = []
        for anObject in self.objects:
            tempTemp.append(anObject.objName)
        temp.append(tempTemp)

        tempTemp = []
        for character in self.characters:
            tempTemp.append(character.desc)
        temp.append(tempTemp)

        tempTemp = []
        for door in self.doors:
            tempTemp.append(door.name)
        temp.append(tempTemp)

        return temp

    def showAllObjects(self):
        temp = []
        tempTemp = []
        for furnishing in self.furnishings:
            tempTemp.append(furnishing)
        temp.append(tempTemp)
        
        tempTemp = []
        for anObject in self.objects:
            tempTemp.append(anObject)
        temp.append(tempTemp)

        tempTemp = []
        for character in self.characters:
            tempTemp.append(character)
        temp.append(tempTemp)

        tempTemp = []
        for door in self.doors:
            tempTemp.append(door)
        temp.append(tempTemp)

        return temp

    def showAllObjectsAndNames(self):
        temp1 = self.showAll()
        temp2 = self.showAllObjects()
        temp3 = []
        for i in range(len(temp1)):
            temp3.append([temp1[i],temp2[i]])
        return temp3
        
            
    def showDoors(self):
        for door in self.doors:
            ui.write(door.viewDoors())
            
    def setDoors(self, otherRooms, direction=2):
        for otherRoom in otherRooms:
            self.doors.append(Door("D" + self.name + otherRoom.name, self, otherRoom, direction))

    def setDoorDescs(self):    
        for door in self.doors:
            door.setDescriptor()


    def describeRoom(self):
            
        roomDescription = ""
        roomDescription += "The room is " + self.search[0] + ". "
        randomSense = random.randint(0,3)
        if randomSense == 0:
            roomSight = []
            f = open("senses\\sights1.txt", "r")
            for row in f:
                roomSight.append(row)
            f.close()

            if self.quality == 1:
                roomDescription += roomSight[0]
            elif self.quality == 2:
                roomDescription += roomSight[1]
            elif self.quality == 3:
                roomDescription += roomSight[2]
            elif self.quality == 4:
                roomDescription += roomSight[3]
            elif self.quality == 5:
                roomDescription += roomSight[4]

        if randomSense == 1:
            roomSound = []
            f = open("senses\\sounds1.txt", "r")
            for row in f:
                roomSound.append(row)
            f.close()

            if self.quality == 1:
                roomDescription += roomSound[0]
            elif self.quality == 2:
                roomDescription += roomSound[1]
            elif self.quality == 3:
                roomDescription += roomSound[2]
            elif self.quality == 4:
                roomDescription += roomSound[3]
            elif self.quality == 5:
                roomDescription += roomSound[4]

        if randomSense == 2:
            roomFeel = []
            f = open("senses\\feels1.txt", "r")
            for row in f:
                roomFeel.append(row)
            f.close()

            if self.quality == 1:
                roomDescription += roomFeel[0]
            elif self.quality == 2:
                roomDescription += roomFeel[1]
            elif self.quality == 3:
                roomDescription += roomFeel[2]
            elif self.quality == 4:
                roomDescription += roomFeel[3]
            elif self.quality == 5:
                roomDescription += roomFeel[4]
            
                
        if randomSense == 3:
            roomSmell = []
            f = open("senses\\smells1.txt", "r")
            for row in f:
                roomSmell.append(row)
            f.close()
            
            if self.quality == 1:
                roomDescription += roomSmell[0]
            elif self.quality == 2:
                roomDescription += roomSmell[1]
            elif self.quality == 3:
                roomDescription += roomSmell[2]
            elif self.quality == 4:
                roomDescription += roomSmell[3]
            elif self.quality == 5:
                roomDescription += roomSmell[4]
        
        if len(self.furnishings) > 0:
            roomDescription += "The room is furnished with "
            for furnishing in self.furnishings:
                roomDescription += "a " +furnishing.basicDesc + ", "

        if len(self.objects) > 0:
            roomDescription += "In the room, there is "
            for roomObject in self.objects:
                if roomObject.hidden == False:
                    roomDescription += roomObject.basicDesc

        for door in self.doors:
            roomDescription += " There is a door to the " + door.name + "."
        return roomDescription
            
        
class Door(object):
    def __init__(self, doorID, room1, room2, direction, opened=False, locked=[False, None]):
        self.doorID = doorID
        self.room1 = room1
        self.room2 = room2
        self.name = ""
        self.opened = opened
        self.locked = locked
        #if it's locked, and if so, what's used to unlock it

        self.direction = direction
        #the direction RELATIVE TO ROOM1

##all mentioned direction relative to the centre of the room
##0 is south
##2 is north
##1 is west
##3 is east
##4 is above
##5 is below
##others might be added at some point if jake yaks at me enough
##
##and obviously for an overworld this either ain't gonna be necessary or will need to be changed, but we'll get to that


##    def setDoors(self):
##        self.room1.doors.append(self)
##        self.room2.doors.append(self)
    def viewDoors(self):
        return("This " + self.name + " connects " + self.room1.search[0] + " and " + self.room2.search[0] + ".")
    def goThrough(self, currentRoom):
        return self.room2
    def goBackThrough(self, currentRoom):
        return self.room1
    
    def setDescriptor(self):
##        if self == self.room1.doors[0]:
##            self.name = "north door"
##        elif self == self.room1.doors[1]:
##            self.name = "south door"
##        elif self == self.room1.doors[2]:
##            self.name = "west door"
##        elif self == self.room1.doors[3]:
##            self.name = "east door"
##        else:
##            self.name = "forbidden door"
        print("Door " + self.doorID)
        print("Room one's doors:")
        for door in self.room1.doors:
            print(door.doorID)
        print("Room two's doors:")
        for door in self.room2.doors:
            print(door.doorID)
            if door.room1 == self.room2 and door.room2 == self.room1:
                if door.direction == 2:
                    self.direction = 0

                    self.name = "south door"
                elif door.direction == 0:
                    self.direction = 2

                    self.name = "north door"
                elif door.direction == 1:
                    self.direction = 3

                    self.name = "east door"
                elif door.direction == 1:
                    self.direction = 1

                    self.name = "west door"
                elif door.direction == 4:
                    self.direction = 5

                    self.name = "trap door"
                elif door.direction == 5:
                    self.direction = 4

                    self.name = "hatch door"
                else:
                    self.name = "forbidden door"

        if self.direction == 2:
            self.name = "north door"

    def open(self, openTool):
        if self.opened == False:
            if self.locked[0] == False:
                self.opened = True
                ui.write("The " + self.name + " is not locked. You open it.")
                
        elif self.locked[0] == True:
            if openTool.objName == self.locked[1]:
                self.locked = False
                self.opened = True
                ui.write("The " + self.name + " is locked. You open it using the " + openTool.name + ".")
            else:
                ui.write("You can't unlock this with the " + openTool.objName)
        elif self.opened == True:
            ui.write("The door is already open.")

    def close(self):
        if self.opened == True:
            self.opened = False
            ui.write("You close the " + self.name)
        elif self.opened == False:
            ui.write("The " + self.name + " is already closed.")
            

class gameObject(object):
    def __init__(self, basicDesc, inspectDesc, hidden = False):
        self.basicDesc = basicDesc
        #a description that displays when you look at it

        self.inspectDesc = inspectDesc
        #a description that displays when you inspect it
        self.hidden = hidden
        #in case it's locked away and shouldn't be found immediately

        self.usable = []
        #gonna need to talk a lot of this over with jake when we get to integration

    def getDesc(self):
        #print(self.basicDesc)
        
        return self.basicDesc

class roomFurnishing(gameObject):
    def __init__(self, name, basicDesc, inspectDesc, interactive=[False, None], containedObjects=[], opened=False, locked=[False, None]):
        super(roomFurnishing, self).__init__(basicDesc, inspectDesc)
        self.name = name

        self.investigation = []
        #as with the place investigation, but on a single furnishing within a room
        self.interactive = interactive
        self.containedObjects = containedObjects
        self.room = None
        for item in self.containedObjects:
            item.hidden = True
            
        if len(self.containedObjects) > 0:
            self.interactive[0] = True
            self.interactive[1] = "open"
            
        self.opened = opened
        self.locked = locked
        
    def open(self, openTool):
        if self.opened == False:
            if self.locked[0] == False:
                self.opened = True
                ui.write("The " + self.basicDesc + " is not locked. You open it.")
                
        elif self.locked[0] == True:
            if openTool.objName == self.locked[1]:
                self.locked = False
                self.opened = True
                ui.write("The " + self.name + " is locked. You open it using the " + openTool.name + ".")
            else:
                ui.write("You can't unlock this with the " + openTool.objName)
        elif self.opened == True:
            ui.write("The door is already open.")
            
        if self.opened == True:
            print(self.containedObjects)
            if len(self.containedObjects) == 0:
                ui.write("There was nothing inside.")
            else:
                ui.write("The " + self.basicDesc + " contains:")
                for item in self.containedObjects:
                    item.hidden = False
                    self.room.objects.append(item)
                    ui.write(item.basicDesc)
                    
    def close(self):
        if self.opened == True:
            for item in self.containedObjects:
                item.hidden = True
                self.room.objects.remove(item)
            self.opened = False
            ui.write("You close the "+ self.basicDesc)
        else:
            ui.write("This " + self.basicDesc + " is already closed.")

class inventoryObject(gameObject):
    def __init__(self, objName, basicDesc, inspectDesc, taken=["No-one","You pick up the object."], expendable = [False], droppable=True, equippable = [False]):
        super(inventoryObject,self).__init__(basicDesc, inspectDesc)

        self.objName = objName

        self.taken = taken
        #include things about ownership, a description when you pick it up, etc...

        self.droppable = droppable
        #removing itself from the bag, and so on...

        self.expendable = expendable
        #if it's expendable, and if so, how many uses it has

        self.equippable = equippable
        #currently using a simple numerical value for quality



class Character(object):
    def __init__(self, name, startingRoom, inventory):
        self.name = name
        self.inventory = inventory
        self.currentRoom = startingRoom
        #an array of inventory objects
        
        basicShirt = inventoryObject(objName ="basic shirt", basicDesc="a basic synth-cloth shirt", inspectDesc="There's a small rip in the armpit...", equippable=[True,"clothesTorso"])
        basicLegs = inventoryObject(objName= "basic legwear", basicDesc="basic synth-cloth legwear", inspectDesc="This could probably do with being washed.", equippable=[True, "clothesLegs"])
        basicShoes = inventoryObject(objName="basic shoes", basicDesc="basic synthetic fabric and rubber shoes", inspectDesc="You can feel a hole in your sock. Ugh.", equippable=[True, "footwear"])
        
        self.inventory.append(basicShirt)
        self.inventory.append(basicLegs)
        self.inventory.append(basicShoes)

        #in case we decide to add stats later

        self.equipped = {
            "clothesTorso" : basicShirt,
            "clothesLegs" : basicLegs,
            "armwear" : None,
            "headgear" : None,
            "footwear" : basicShoes,
            "armourTorso" : None,
            "armourLegs" : None,
            "accessories" : [],
            "weaponLeft" : None,
            "weaponRight" : None,
            "weaponBoth" : None
            }
        #this is more for a fantasy setting and it hasn't been tested cuz I wrote it at 00:37

    def getName(self):
        return self.name

    def whatsMine(self):
        for item in self.equipped:
            if self.equipped[item] == None or self.equipped[item] == []:
                pass
            else:
                ui.write(self.equipped[item].basicDesc)
    


class nonPlayerCharacter(Character):
    def __init__(self, ID, name, desc, talk, interest, startingRoom, inventory = []):
        super(nonPlayerCharacter,self).__init__(name,startingRoom, inventory)
        self.ID = ID
        self.desc = desc
        self.talk = talk
        self.interest = interest

class playerCharacter(Character):
    def __init__(self, name, startingRoom, inventory = []):
        super(playerCharacter,self).__init__(name, startingRoom, inventory)
        #this should really be in the Character class but I want to make sure it's working first

    def useItem(self, item):
        #the actual use
        if item.expendable[0] == True:
            if item.expendable[1] == 1:
                self.inventory.remove(item)
            else:
                item.expendable[1] = item.expendable[1] -1
            #if the item's expendable
            #a confirmation message should probably be put in here at some point

    def inspect(self,item):
        if isinstance(item, inventoryObject):
            if item in self.inventory:
                #can never be too careful
                ui.write("This " + item.objName + " belongs to " + item.taken[0] + ".")
                ui.write(item.inspectDesc)
                
        elif isinstance(item, roomFurnishing):
            ui.write(item.inspectDesc)
            if item.interactive[0] == True:
                ui.write("It looks like this object can be " + item.interactive[1] + "ed.")

    def takeItem(self, item):
        if item.taken[0] == "No-one" or item.taken[0] == "you":
            item.taken[0] = "you"
            self.inventory.append(item)
            #will need to remove it from the room, too
            ui.write(item.taken[1])
        else:
            ui.write("That's not yours.")

    def equipItem(self,item):
        if self.equipped[item.equippable[1]] == None:
            self.equipped[item.equippable[1]] = item
        elif self.equipped[item.equippable[1]] == [] or isinstance(self.equipped[item.equippable[1]], list):
            #NOTE: THIS MIGHT NOT WORK
            self.equipped[item.equippable[1]].append(item)
        else:
            self.equipped[item.equippable[1]] = item
            #I'll put a swap confirmation message here when I'm bothered enough by it

    def dropItem(self, item):
        if item.droppable == False:
            ui.write("You need this object for something.")
        else:
            self.inventory.remove(item)
            currentRoom.objects.append(item)
                
    def displayInventory(self):
        ui.write("You have in your possession: ")
        for item in self.inventory:
            ui.write(item.basicDesc)

    def moveRooms(self, door):
        #self.currentRoom.doors[door]
        for aDoor in self.currentRoom.doors:
            if aDoor.doorID == door:
                self.currentRoom = aDoor.room2
                
    def showLocation(self):
        ui.write("You are in " + self.currentRoom.search[0])

    def searchRoom(self):
        ui.write(self.currentRoom.describeRoom())

    def talk(self, other):
        ui.talkWindow(self,other)
        
aSmallRock = inventoryObject("small rock", "a small rock", "hard stone")
chestOfDrawers = roomFurnishing(name="chest of drawers",basicDesc="chest of drawers", inspectDesc="a weathered wooden chest of 4 drawers.", containedObjects=[aSmallRock])
     
R1 = Place("R1", 3, [chestOfDrawers], [],[], ["a simple yet comfortable bedroom"])
R2 = Place("R2",4, [],[], [],["a lavishly decorated mezzanine"], ["a painting of yourself"])
R3 = Place("R3",5, [], [aSmallRock],[])

R1.setDoors([R2])
R2.setDoors([R1, R3], 3)
R3.setDoors([R2], 1)

R1.setDoorDescs()
R2.setDoorDescs()
R3.setDoorDescs()

##R1.showDoors()
##R2.showDoors()
##R3.showDoors()

jeremy = playerCharacter("jeremy", R1)

TalkC1 = {  'start':['Well hello there. Can I interest you in some lemons?',[0,-1]],
            'lemons':['Oh yes, fresh yellow lemons from my home. My wife picks them. Care to buy any?',[0,0]],
            'yes':['Very good sir. Goodbye',[+1,-2]],
            'no':['Well i\'m sorry to hear that. Have a good day',[-3,-6]],
            'wife':['Oh yes, i love my wife so very much',[+4,0]],
            'home':['it\'s a small house. I dont much care for it',[-1,-1]]}

C1 = nonPlayerCharacter('C1','John','a small man', TalkC1,3, R1)
#jeremy.searchRoom(None)


jeremy.showLocation()
#jeremy.moveRooms("DR1R2")
#jeremy.showLocation()
a = R1.showAllObjectsAndNames()
b = R2.showAllObjectsAndNames()
c = R3.showAllObjectsAndNames()
##print('R1')
##for i in a:
##    print(i)
##print('R2')
##for i in b:
##    print(i)
##print('R3')
##for i in c:
##    print(i)

def Execute(text, player):
    action = {}

    #text in form {'verb':Object,'using/do': object}
    
    error = False

    if 'error' in text:
        error = True
        ui.write(text['error'])
    else:    
        for item in text:
            action[item] = MatchInput({item:text[item]},player)
        ui.write(action)
        
        if error in action:
            error = True
        for key in action:
            if isinstance(action[key],dict):
                error = True
            
    if not error:
        if 'using' not in action:
            action['using'] = None

        #This doesn't yet work, haden probably should implimnet
        for key in action:
            disallowed = {'search':False, 'move':False, 'attack':False, 'talk':False, 'open':False, 'close':False, 'inspect':False, 'using':False, 'act':False}
            if isinstance(action[key],Place):
                disallowed['inspect'] = True
                disallowed['search'] = True
            elif isinstance(action[key], Door):
                disallowed['open'] = True
                disallowed['close'] = True
                disallowed['move'] = True
            elif isinstance(action[key], roomFurnishing):
                disallowed['open'] = True
                disallowed['close'] = True
                disallowed['inspect'] = True
            elif isinstance(action[key], inventoryObject):
                disallowed['inspect'] = True
                disallowed['using'] = True
            elif isinstance(action[key], nonPlayerCharacter):
                disallowed['attack'] = True
                disallowed['talk'] = True
            #we can change these as we see fit, but in terms of solutions this should be fine, right?
                
            if key == 'search' and disallowed[key] == True:
                
                #Every object could have a method for every verb, some of which jsut say u cant do that
                #Alternativley we can call the objects here and not call the ones that it wont work for but i think that will be harder
                
                #ui.write(action[key].describeRoom(action['using'])) # This method will not work
                #action[key].Search(action['using']) # it probably should just look like this
                #action[key].describeRoom()
                player.searchRoom()
            elif key == 'move' and disallowed[key] == True:
                #action[key].Move(action['using'])
                player.moveRooms(action[key].doorID)
            elif key == 'attack' and disallowed[key] == True:
                action[key].Attack(action['using'])
            elif key == 'talk' and disallowed[key] == True:
                action[key].Talk(action['using'])
            elif key == 'take' and disallowed[key] == True:
                action[key].Take(action['using'])
            elif key == 'open' and disallowed[key] == True:
                action[key].open(action['using'])
            elif key == 'close' and disallowed[key] == True:
                action[key].close()
            elif key == 'inspect' and disallowed[key] == True:
                action[key].inspect(action['using'])
            elif key == 'using' and 'act' in action and disallowed[key] == True:
                action['on'].GeneralUse(action['using']) # This one maybe should be the other way round?
            elif key == 'using' and disallowed[key] == True:
                pass
            elif key == 'act' and disallowed[key] == True:
                pass
            else:
                print('Execute error')
    else:
        ui.write('You cannot do this.')

def MatchInput(text,player):

    
    #need to add room and player to things
    #look: around, about, room
    #should default to player
    
    room = player.currentRoom
   
    things = room.showAllObjectsAndNames()
    
    
    
    things.append([['around','room','about'],[room,room,room]])
    things.append([['self','myself','me','i'],[player,player,player,player]])
    
    

    

    action = {}                  

    done = False
    
    #print(things)
        
    for key in text:
        action[key] = ''
        for thingList in things:
            for i in range(len(thingList[0])):
                if text[key] == thingList[0][i]:
                    action[key] = thingList[1][i]
    

    for key in action:
        if action[key] == '':
            break
        else:
            done = True
            ui.write(action)
            return(action[key])
            
      
    if not done:
        for key in action:
            thingType = [] 
            if action[key] == '':
                for thingList in things:
                    for i in range(len(thingList[0])):
                        thingList[0][i] = thingList[0][i].split()
                        if thingList[0][i][-1] in text[key]:
                            thingType.append([key,thingList[1][i],thingList[0][i]])
                            
            if len(thingType)!= 0:
                
                desc = []
                for i in range(len(thingType)):
                    desc.append('')
                    for x in thingType[i][2]:
                        desc[i] += x+' '
                
                if len(thingType) == 1:
                    ui.write('There is only one %s in sight, %sing the %s.'%(thingType[0][2][-1],thingType[0][0].replace('ing',''),desc[0]))
                    action[thingType[0][0]] = thingType[0][1]
                    return(action[key])
                else:
                    ui.write('There is more than one of these in sight:')
                    for item in desc:
                        ui.write('There is a %s'%item)
                    return({'error':'Ambiguous object'})
            else:
                ui.write('there is no %s in sight!'%text[key].split()[-1])
                return({'error':'Object not recognised'})
        





def Interpret(text,player):

    text = Simplify(text)

    verbs = ['search','move','attack','talk','take','open','close','inspect']
    using = 'using'
    currentVerb = ''
    verbNumber=0
    usingNumber=0
    words = text.split()
    do = {}


    for word in words:
        for verb in verbs: # Finds verb in sentence
            if word == verb:
                verbNumber+=1
                do[verb] = ''
                currentVerb = verb
                continue
                
        if word == using: # Finds 'using' in sentence
            usingNumber+=1
            do[using] = ''
            currentVerb = using
            
        if word not in verbs and word != using and currentVerb != '': # The nouns
            if do[currentVerb] == '': #nouns set as values of key being previous verb
                do[currentVerb]+=word
            else:
                do[currentVerb] += ' '+word # add space if not first word

    
    ###---Dirty fix for Use X on Y---###
    if usingNumber == 1 and verbNumber == 0 and words[0] == using:
        do['act'] = ''
        temp = do[using].split()
        do[using] = ''
        beforeOn = True
        for word in temp:

            if word == 'on':
                
                beforeOn = False
                
            if word != 'on' and beforeOn:
                if do[using] == '':
                    do[using] +=word
                else:
                    do[using] +=' '+word
            elif word != 'on' and not beforeOn:
                if do['act'] == '':
                    do['act'] +=word
                else:
                    do['act'] += ' '+word
    
        verbNumber+=1
    ###---End---###
    
    for key in do:
        do[key] = do[key].replace('on ','') # remove garbage word 'on', used in dirty fix
        if do[key] == '':
            if key == 'act':
                do[key] = 'self'
            else:
                Execute({'error':'What are you trying to %s?'%key},player)
        
    if verbNumber >1 or usingNumber>1:
        Execute({'error':'All that at once?'},player)
    elif verbNumber == 0:
        Execute({'error':'What are you trying to do?'},player)
    else:
        Execute(do,player) #sucess!

                
        
def Simplify(text):
    
    toRemove = []
    fillerWords = ['to','in','the','attempt','teh','from','a','try','trying','at','near','for','behind','under','while','and','by','my']
    punctuation = [',','.','?','!','\'',';',':']
             
    using = ['use','using','with','activate','activating','fire','firing','turn','turning']
    
    search = ['search','look','find','explore']
    
    move = ['move','go','travel','walk','climb','enter']
    
    attack = ['attack', 'assault', 'hit', 'smash','fight','kill']
    talk = ['talk','speak','talk to']
    
    take = ['take','grab','remove','carry','obtain','pick up','pick','steal']
    close = ['close','shut','block']
    inspect = ['inspect','look at','observe','see']
    
    open_ = ['open', 'unlock','unblock'] #open is keyword, uses open_ instead

    verbs = ['using','search','move','attack','talk','take','open','close','inspect']
    words = {'using':using,'search':search,'move':move,'attack':attack,'talk':talk,'take':take,'open':open_,'close':close,'inspect':inspect}
                
    
        
    text = text.lower()
    text = text.split()
    sentence = ''
    
    for i in range(len(text)):
        if text[i] in fillerWords:
            toRemove.append(text[i]) # get rid of garbage words
            
        if text[i][-1] in punctuation:
            text[i] = text[i][:-1] # get rid of punctuation
            
        for verb in verbs:
            if text[i] in words[verb]: # ***The good bit***
                text[i] = verb  #replaces synonms of verbs with general case of verb from verbs array
                
    for word in toRemove:
        text.remove(word) #remove garbage words
        
    for word in text:
        sentence+=word+' ' #make array of words into sentence
        
    sentence = sentence[:-1] #remove trailing ' '
     
    return(sentence)


 

#TO MOVE ROOMS YOU NEED THE DOOR CODE

main.mainloop()
    
#TODO: Change dialogue for objects so it doesn't sound so weird and ham-fisted by making a location in the room for them to exist in.
#Maybe work on making random descriptors for rooms. 5 senses!
#making sure the program's fully modular to save on work when we make it work with the interpreter
#scavenge from the existing file reader so I can get file reading working here too. I'll probably need multiple files.
#basic gameplay loop will obviously need to be fixed but that's partially Jake's problem, lol

        
