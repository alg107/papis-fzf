import curses
import os


f=open("/dev/tty")
os.dup2(f.fileno(), 0)

def print_lst(stdscr, lst, selected):
    idxs = [i[1] for i in lst]
    filt_idx = 0
    try:
        filt_idx = idxs.index(selected)
    except:
        pass
    y0,x0 = stdscr.getyx()
    curses.init_pair(1,curses.COLOR_RED,-1)
    curses.init_pair(2,curses.COLOR_YELLOW,-1)
    curses.init_pair(3,curses.COLOR_CYAN,-1)
    i = k = 1
    while i < min(curses.LINES-1, len(lst)*2):
        for j,l in enumerate(lst[k-1][0].split("\n")[::-1]):
            if k-1==filt_idx:
                stdscr.addstr(curses.LINES-1-i,0,"  "+l,curses.color_pair(3))
            else:
                stdscr.addstr(curses.LINES-1-i,0,"  "+l,curses.color_pair(j+1))
            i+=1
        k += 1
    stdscr.move(y0,x0)

def filter_lst(query, lst, selected):
    filtered = list(filter(lambda x: "".join(x[0].split()).lower().find(query.lower().strip())!=-1, lst))
    idxs = [i[1] for i in filtered]
    if selected not in idxs and len(filtered) != 0:
        selected = filtered[0][1]
    return filtered ,selected

def main(stdscr, lst):
    lst = list(zip(lst, range(len(lst))))
    stdscr.clear()
    stdscr.refresh()
    curses.start_color()
    curses.use_default_colors()
    stdscr.keypad(True)
    query = ""
    filtered = lst
    selected =0 
    print_lst(stdscr,lst,selected)
    stdscr.move(curses.LINES-1,0)
    while True:
        ch = stdscr.getkey()
        if ch == "KEY_BACKSPACE":
            if query == "":
                continue
            else:
                query = query[:-1]
                y,x = stdscr.getyx()
                stdscr.delch(y,x-1)
        elif ch == '\n':
            return lst[selected][0]
        elif ch == "KEY_UP":
            linesused = min(curses.LINES//2, len(filtered))
            idxs = [i[1] for i in filtered]
            selected = filtered[(idxs.index(selected)+1)%linesused][1]
        elif ch == "KEY_DOWN":
            linesused = min(curses.LINES//2, len(filtered))
            idxs = [i[1] for i in filtered]
            selected = filtered[(idxs.index(selected)-1)%linesused][1]
        else:
            query += ch
        stdscr.clear()
        stdscr.refresh()
        filtered,selected = filter_lst(query, lst, selected)
        print_lst(stdscr,filtered, selected)
        stdscr.addstr(curses.LINES-1,0, "> "+query)

def picker(lst):
    return curses.wrapper(main,lst)
