#!/usr/bin/python3

import sys
import re
import curses
from curses import wrapper


def addstrWordWrap(w, contents):
    (height, width) = w.getmaxyx()
    x, y = 0, 0
    wordlist = re.split(r"(\s)", contents)
    for word in wordlist:
        if height - y <= 10:
            w.resize(height + 10, width)
            height += 10

        if word.isspace():
            if word == "\n":
                x = 0
                y += 1
                continue
            if word == "\r":
                x = 0
                continue
            if word == " ":
                if x == width:
                    x = 0
                    y += 1
                elif x != 0:
                    x += 1
                continue

        if word == "":
            continue

        if len(word) > width:
            w.addstr(y, x, word)
            y += (x + len(word)) // width
            x = (x + len(word)) % width
        elif x + len(word) > width:
            w.addstr(y+1, 0, word)
            y += 1
            x = len(word)
        else:
            w.addstr(y, x, word)
            x += len(word)


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()


    (lines, cols) = stdscr.getmaxyx()

    margin = 1

    stdscr.border()

    p = curses.newpad(10, cols - 2 * (1 + 2 * margin))

    addstrWordWrap(p, contents)

    stdscr.refresh()
    r = 0
    while(True):
        if r < 0:
            r = 0
        try:
            p.refresh( r,0, 1 + margin,1+2*margin, lines-(2+margin),cols-(2+2*margin))
        except curses.error:
            pass
        c = stdscr.getch()
        if c == curses.KEY_DOWN:
            r += 1
        elif c == curses.KEY_UP:
            r -= 1
        elif c == curses.KEY_RESIZE:
            stdscr.clear()
            stdscr.border()
            stdscr.refresh()
            (lines, cols) = stdscr.getmaxyx()
            p.erase()
            p.resize(10, cols - 2 * (1 + 2 * margin))
            addstrWordWrap(p, contents)
        elif c == ord('q'):
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cursestest.py file")
        sys.exit(0)
    filename = sys.argv[1]
    try:
        with open(filename, 'rt') as f:
            contents = f.read()
    except IOError as e:
        print(f"{filename}: {e.strerror}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"UnicodeDecodeError: could not decode {filename} as string")
        sys.exit(1)
    except:
        print(f"Unexpected error: {sys.exc_info()[0]}")
        sys.exit(1)

    wrapper(main)
