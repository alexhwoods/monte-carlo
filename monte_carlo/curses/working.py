import curses
import os
import time
import random
import math



sz = os.get_terminal_size()
# these are accurate
cols = sz.columns
lines = sz.lines

cardWidth = 9
cardLength = 7

symbols = {"spades": "♠", "hearts": "♥", "diamonds": "♦", "clubs": "♣"}
colorDict = {}

always_display = {":": (lines-1, 0)}
temp_display = {"Your cards are...": (3,4)}

'''
    todo - make it so people with sucky terminals can play too

    todo - How is the pot going to be represented?

    note - How am I going to pass a card into the drawing algorithm?

    note - need to set default background

'''



def setup():
    stdscr = curses.initscr()
    
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 3, -1)    # gold
    curses.init_pair(2, 5, -1)    # pink
    curses.init_pair(3, 229, -1)  # light
    curses.init_pair(4, 21, -1)   # blue
    curses.init_pair(5, 42, -1)   # cyan
    curses.init_pair(6, 208, -1)  # orange
    curses.init_pair(7, 8, 229)   # light-dark
    curses.init_pair(8, 1, -1)    # red
    curses.init_pair(9, 64, -1)   # green

    colorDict["gold"] =  curses.color_pair(1)
    colorDict["pink"] = curses.color_pair(2)
    colorDict["light"] = curses.color_pair(3)
    colorDict["white"] = curses.color_pair(3)
    colorDict["blue"] = curses.color_pair(4)
    colorDict["cyan"] = curses.color_pair(5)
    colorDict["orange"] = curses.color_pair(6)
    colorDict["red"] = curses.color_pair(8)
    colorDict["green"] = curses.color_pair(9)



    clear_display(stdscr)

    return stdscr



# don't call in program, only call wrapper methods
def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    text = stdscr.getstr(r, c + len(prompt_string), 20)
    text = text.lower()
    text = str(text).split('\'')[1]
    return str(text)  #       ^^^^  reading input at next line

# test
def string_input(stdscr):
    prompt_string = ":"
    text = my_raw_input(stdscr, lines-1, 0, prompt_string)
    return text

# test
def int_input(stdscr, y=None, x=None):
    prompt_string = ":"
    num = ""
    while True:
        num = my_raw_input(stdscr, lines-1, 0, prompt_string)
        try:
            num = int(num)
            break
        except:
            if x is None and y is None:
                y, x = get_middle_of_screen(stdscr, "Make sure your input is an integer here.")
            else:
                pass
            
            display_message(stdscr, y, x, "Make sure your input is an integer here.")
            reset_cursor(stdscr)
    return num

def flash_message(stdscr, y, x, message, seconds=3):
    stdscr.addstr(y,x, message)
    reset_cursor(stdscr)
    time.sleep(seconds)
    stdscr.move(y, x)

    for i in range(0, len(message)):
        # the characters move to the left when their left neighbor is deleted
        stdscr.delch(y,x)
        stdscr.addstr(y, x+len(message)+1, " ")

    reset_cursor(stdscr)

def display_message(stdscr, y, x, message):
    stdscr.addstr(y,x, message)
    reset_cursor(stdscr)

def get_upper_right(stdscr, message=None):
    # returns (y,x) 10 characters from the right
    if message is None:
        num_chrs = 10
    else:
        num_chrs = len(message)
    return (0, cols - num_chrs)


def get_middle_of_screen(stdscr, message=None, length=None):

    if message is None:
        num_chrs = 15
    else:
        num_chrs = len(message)

    if length is not None:
        num_chrs = length

    y = int(lines/3)
    x = int(cols/2) - int(num_chrs/2)

    return (y, x)


def clear_display(stdscr):
    stdscr.clear()
    for message in always_display.keys():
        y = always_display[message][0]
        x = always_display[message][1]
        stdscr.addstr(y, x, message)

    # stdscr.refresh()
    # move the cursor back to the prompt
    stdscr.move(lines-1, 1)



def reset_cursor(stdscr):
    stdscr.move(lines-1, 1)
    stdscr.deleteln()

    prompt_string = ":"
    y = always_display[prompt_string][0]
    x = always_display[prompt_string][1]
    stdscr.addstr(y,x, prompt_string)
    stdscr.refresh()


def draw_card(stdscr, y, x, rank="2", suit="hearts"):
    # Card will be jack of spades, for now
    nlines = cardLength

    # this value is important!
    ncols = cardWidth
    card = curses.newwin(nlines, ncols, y, x)
    

    # when adding strings to card, (0,0) is upper right corner
    # put symbol in upper right corner
    card.addstr(1, 1, symbols[suit], curses.color_pair(2))

    # put symbol in lower left corner
    card.addstr(nlines-2, ncols-2, symbols[suit], curses.color_pair(2))

    # adding the rank of the card
    card.addstr(int(nlines/2), int(ncols/2), rank, curses.color_pair(3))

    card.box()

    stdscr.refresh()
    card.refresh()
    reset_cursor(stdscr)

def drawAnonymousCard(stdscr, y, x):
    char = "◑"
    nlines = 7
    ncols = cardWidth
    card = curses.newwin(nlines, ncols, y, x)
    card.box()
    
    # I only want to use pink, light and blue for the matrix
    colors = [curses.color_pair(2), curses.color_pair(6), curses.color_pair(3), curses.color_pair(4)]

    # when adding strings to card, (0,0) is upper right corner
    # put symbol in upper right corner
    for i in range(1, nlines-1):
        mValueJ = 0   # represents the matrix value with respect to rows, since I have to skip cols
        for j in range(1, ncols-1):
            
            if j % 2 == 1 and i != nlines-2:
                mValueJ += 1
                if (mValueJ > i):
                    color = random.choice(colors[:2])
                elif (i == mValueJ):
                    color = colors[2]
                else:
                    color = colors[3]

                card.addstr(i, j, char, color)

        mValueJ = 0


    stdscr.refresh()
    card.refresh()
    reset_cursor(stdscr)


    # this will draw a facedown card, in place of the "unflipped" cards


def show_player_left(stdscr, name="Anakin Skywalker", chips=1000, cards=[]):
    x = 2      # this represents the spacing in between the border and the name
    y = 1
    stdscr.addstr(y, x, name + ": " + str(chips))

    # let the cards be [Queen of Hearts, 7 of spades]
    # todo - anonymous card
    drawAnonymousCard(stdscr, y+1, x)
    drawAnonymousCard(stdscr, y+1, x + cardWidth+1)



def show_player_right(stdscr, name="Luke Skywalker", chips=1000, cards=[]):
    y = 1
    space = 2
    x = cols - (len(name + ": " + str(chips)) + space)

    stdscr.addstr(y, x, name + ": " + str(chips))

    x = cols - (2*cardWidth + 1 + space)
    draw_card(stdscr, y+1, x, rank="2", suit="diamonds")
    draw_card(stdscr, y+1, x + cardWidth+1, rank="A", suit="clubs")



def show_community_cards(stdscr, cards=[]):
    # I want these in the middle / bottom middle of the screen
    # todo - make so if there is a card in cards, it draws it. 
    lengthCards = cardWidth*5 + 5
    y, x = get_middle_of_screen(stdscr, length=lengthCards)
    y = int(lines / 2)

    tempY, tempX = get_middle_of_screen(stdscr, "Community Cards: ")
    stdscr.addstr(y-1, tempX-1, "Community Cards: ")
    for i in range(5):
        if i < len(cards):
            if cards[i] is not None:
                # draw cards[i]
                pass
        drawAnonymousCard(stdscr, y, x)
        x += cardWidth + 1


def show_pot(stdscr, amount):
    coin = "●"

    colors = {100: "gold", 
           25: "green",
           10: "blue",
            5: "red", 
            1: "white"}

    counts = splitAmount(amount)
    num_chips = 0
    for key, value in counts.items():
        num_chips += value

    ncols = 2*num_chips + 1
    nlines = 1

    y, x = get_middle_of_screen(stdscr, length = ncols)
    y = int(7*lines/10)
    move = 3
    pot = curses.newwin(nlines, ncols, y+move, x)

    dummyY, xPot = get_middle_of_screen(stdscr, "Pot: num")
    stdscr.addstr(y+move-1, xPot, "Pot: " + str(amount))

    
    keyPadding = 3
    key = makeKey(stdscr, y, x+ncols+keyPadding, coin, colors)


    while True:
        for j in range(0, ncols-1):
            if j % 2 == 1:
                if counts[100] > 0:
                    pot.addstr(0, j, coin, colorDict[colors[100]])
                    counts[100] -= 1

                elif counts[25] > 0:
                    pot.addstr(0, j, coin, colorDict[colors[25]])
                    counts[25] -= 1

                elif counts[10] > 0:
                    pot.addstr(0, j, coin, colorDict[colors[10]])
                    counts[10] -= 1

                elif counts[5] > 0:
                    pot.addstr(0, j, coin, colorDict[colors[5]])
                    counts[5] -= 1

                elif counts[1] > 0:
                    pot.addstr(0, j, coin, colorDict[colors[1]])
                    counts[1] -= 1

                else:
                    break

        # since this will be the last one to be displayed
        if counts[1] == 0:
            break


    pot.refresh()
    key.refresh()
    reset_cursor(stdscr)

def makeKey(stdscr, y, x, coin, colors):
    key = curses.newwin(7, 11, y, x)
    key.box()

    start = 1

    key.addstr(start,2, coin, colorDict[colors[100]])
    key.addstr(start,3, " = 100")
    start += 1

    key.addstr(start,2, coin, colorDict[colors[25]])
    key.addstr(start,3, " = 25")
    start += 1

    key.addstr(start,2, coin, colorDict[colors[10]])
    key.addstr(start,3, " = 10")
    start += 1

    key.addstr(start,2, coin, colorDict[colors[5]])
    key.addstr(start,3, " = 5")
    start += 1

    key.addstr(start,2, coin, colorDict[colors[1]])
    key.addstr(start,3, " = 1")

    return key

def splitAmount(amount):


    counts = {100: 0, 
              25: 0, 
              10: 0, 
               5: 0, 
               1: 0}

    if amount >= 100:
        counts[100] += int(amount / 100)
        amount = amount % 100

    if amount >= 25:
        counts[25] += int(amount / 25)
        amount = amount % 25

    if amount >= 10:
        counts[10] += int(amount / 10)
        amount = amount % 10

    if amount >= 5:
        counts[5] += int(amount / 5)
        amount = amount % 5

    if amount >= 1:
        counts[1] += int(amount / 1)
        amount = amount % 1

    if amount != 0:
        print("something broke, fix it")

    return counts

def terminate(stdscr):
    stdscr.getch()
    curses.endwin()
    os.system('reset')
    


if __name__ == "__main__":
    stdscr = setup()
    
    curses.init_pair(1, 3, -1)

    show_player_left(stdscr)
    show_player_right(stdscr)
    show_community_cards(stdscr)

    show_pot(stdscr, 999)

    # y,x = get_middle_of_screen(stdscr, "Put messages here.")
    # flash_message(stdscr, y, x, "Put messages here.")

    # choice = string_input(stdscr)

    # clear_display(stdscr)
    # x = cols - 9
    # y = 0
    # if choice == "check":
    #     flash_message(stdscr, y, x, "Checking!")
    # elif choice == "bet":
    #     # flash_message(stdscr, y, x, " Betting!")
    #     y, x = get_upper_right(stdscr, "Betting!")
    #     display_message(stdscr, y, x, "Betting!")

    #     y, x = get_middle_of_screen(stdscr, "How much would you like to bet?")
    #     display_message(stdscr, y-1, x, "How much would you like to bet?")
    #     amount = int_input(stdscr, y, x)

    #     # flash_message will clear the display in itself
    #     # y, x = get_middle_of_screen(stdscr, "You are going to bet " + str(amount) + ".")
    #     flash_message(stdscr, y+1, x, "You are going to bet " + str(amount) + ".")

    # else:
        
    #     stdscr.addstr(y, x," Invalid input") 


    terminate(stdscr)





