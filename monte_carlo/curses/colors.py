""" Curses Clock: draw a colorful clock in the center of a terminal 
    		      and update it every second. Quit on first keystroke
		Bugs: handles window change (SIGWINCH) crudely
			  abends (exit code 1) if not curses.has_colors(), no error message
			  mouse events are so totally not working! 
			  	(may be cause of segfault?)
	by James T. Dennis <jimd at starshine.org> 
	Sun Mar 17 15:06:52 PST 2002
"""
import curses, time, random, string, sys

def main(w):
	w.keypad(1)
	w.leaveok(1) 
	w.immedok(0)
	w.nodelay(1) 
	w.scrollok(0)
	w.erase()
	norm = curses.A_NORMAL
	bold = curses.A_BOLD
	dim  = curses.A_DIM
	if curses.has_colors():
		colorlist = (("red", curses.COLOR_RED), 
					 ("green", curses.COLOR_GREEN),
					 ("yellow", curses.COLOR_YELLOW),
					 ("blue", curses.COLOR_BLUE),
					 ("cyan", curses.COLOR_CYAN),
					 ("magenta", curses.COLOR_MAGENTA),
					 ("black", curses.COLOR_BLACK),
					 ("white", curses.COLOR_WHITE))
		colors = {}
		colorpairs = 0
		for name,i in colorlist:
			colorpairs += 1 
			curses.init_pair(colorpairs, i, curses.COLOR_BLACK)
			colors[name]=curses.color_pair(i)
	else: 
		sys.exit(1)
	## (mousecap, mouseold) = curses.mousemask(0)
	## (mousecap, mouseold) = curses.mousemask(mouseold | mousecap)

	tpart = { "day":	 0, "month": 4, "date":	 8, "hour":	11,
			   "min":	14, "sec":	17, "year":	21 }
	key = 0		
	while 1:
		if key == 0 or key == 410:	# 410 is from SIGWINCH?
			w.erase()
			y,x=w.getmaxyx()
			mid = y / 2 
			ctr = x / 2 
			t = time.asctime()
			ctr -=  len(t) / 2 
		### k = w.getkey()
		### Warning: previous line causes segfault!
		key = w.getch()
		## if key == 410: continue
		if key == ord('q') or key == ord('Q'): 
			break
		else: 
			w.addstr(0, 0, "\t%s\t" % key, colors["yellow"])
			### w.addstr(0, 0, "\t%s\t" % curses.keyname(k), colors["yellow"])
			### Warning: previous line causes segfault!
		t = time.asctime()
		w.addstr(mid,ctr+tpart["day"],  t[0:3],colors["blue"]    | norm)
		w.addstr(mid,ctr+tpart["month"],t[4:8],colors["blue"]    | dim)
		w.addstr(mid,ctr+tpart["date"], t[8:11],colors["blue"]   | bold)
		w.addstr(mid,ctr+tpart["hour"], t[11:14],colors["red"]   | dim)
		w.addstr(mid,ctr+tpart["min"],  t[14:17],colors["red"]   | bold)
		w.addstr(mid,ctr+tpart["sec"],  t[17:20],colors["green"] | dim)
		w.addstr(mid,ctr+tpart["year"], t[20:],colors["magenta"] | dim)
		time.sleep(1)
	return key
	
if __name__ == "__main__":
	x = curses.wrapper(main)
	print x