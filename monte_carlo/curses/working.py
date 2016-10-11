import curses
import os
import time

'''
TODO - test string_input() and int_input()
       What other methods will you need?
       How should you package this? As a class?

'''





sz = os.get_terminal_size()
# these are accurate
cols = sz.columns
lines = sz.lines

always_display = {"Type 'check' to call or check, 'bet' to bet" + 
        ", or 'q' to quit": (0,0),
                  ":": (lines-1, 0)}
temp_display = {"Your cards are...": (3,4)}

def setup():
    stdscr = curses.initscr()
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
    text = my_raw_input(stdscr, lines-1, 0, prompt_string)
    return text

# test
def int_input(stdscr):
    num = my_raw_input(stdscr, lines-1, 0, prompt_string)
    num = int(num)
    return num

def flash_message(stdscr, y, x, message, seconds=3):
    stdscr.addstr(y,x, message)
    reset_cursor(stdscr)
    time.sleep(seconds)
    clear_display(stdscr)


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
    stdscr.refresh()

def terminate(stdscr):
    stdscr.getch()
    curses.endwin()
    os.system('reset')
    


if __name__ == "__main__":
    stdscr = setup()

    prompt_string = ":"
    choice = my_raw_input(stdscr, lines-1, 0, prompt_string)

    clear_display(stdscr)
    x = cols - 9
    y = 0
    if choice == "check":
        flash_message(stdscr, y, x, "Checking!")
    elif choice == "bet":
        flash_message(stdscr, y, x, " Betting!") 
    else:
        
        stdscr.addstr(y, x," Invalid input") 


    terminate(stdscr)





