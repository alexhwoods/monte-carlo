import curses
import os

sz = os.get_terminal_size()
# these are accurate
cols = sz.columns
lines = sz.lines

def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    text = stdscr.getstr(r, c + len(prompt_string), 20)
    text = text.lower()
    text = str(text).split('\'')[1]
    return str(text)  #       ^^^^  reading input at next line


if __name__ == "__main__":
    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.addstr(0,0, "Type 'check' to call or check, 'bet' to bet" + 
        ", or 'q' to quit")
    prompt_string = ":"
    choice = my_raw_input(stdscr, lines-1, 0, prompt_string)
    stdscr.clear()
    stdscr.addstr(lines-1, 0, prompt_string)
    stdscr.addstr(0,0, "Type 'check' to call or check, 'bet' to bet" + 
        ", or 'q' to quit")
    x = cols - 9
    y = 0
    if choice == "check":
        stdscr.addstr(y,x,"Checking!")
    elif choice == "bet":
        stdscr.addstr(y, x," Betting!") 
    else:
        print(choice)
        stdscr.addstr(y, x," Invalid input") 

    stdscr.refresh()
    # move the cursor back to the prompt
    stdscr.move(lines-1, 1)

    
    # waits for you to press something on the keyboard and
    # then exits the program.
    stdscr.getch()
    curses.endwin()





