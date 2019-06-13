#!/usr/bin/env python3

import os
import curses
import sys

HEIGHT = 600
WIDTH = 800
TIMEOUT = 0


class Cda:

    def __init__(self):
        # init
        
        self.currentDir = os.getcwd()
        self.listDir = os.listdir(self.currentDir)
        self.selection = 0
        self.event = -1
        self.quit = 0
        self.scroll =  1
        # display init
        self.screen = curses.initscr()
        self.h, self.w = self.screen.getmaxyx()
        self.sh, self.sw = self.screen.getmaxyx()
        self.window = curses.newwin(self.h, self.w, 0, 0)
        self.window.timeout(TIMEOUT)
        self.window.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        self.window.border(0)
        self.pad = curses.newpad(self.h,2000)
    def changeDir(self, newDir):
        self.currentDir = newDir
        os.chdir(self.currentDir)
        self.listDir = os.listdir(self.currentDir)
        self.selection = 0
    
    def exit(self):
        curses.endwin()
        os.system("/bin/bash")
        self.quit = 1
        sys.exit()
    
    def stop(self):
        curses.endwin()
        self.quit = 1
        sys.exit()

    def display(self):
        self.window.clear()
        printString = "Current Directory: {}" .format(self.currentDir)
   #     self.window.addstr(10, 50, "sh: {}" .format(self.sh))
   #     self.window.addstr(9, 50, "se: {}" .format(self.selection))
   #     self.window.addstr(8, 50, "sc: {}" .format(self.scroll))
        if(len(printString) > self.w):
            self.w = len(printString) + 10
        if(len(self.listDir) + 1 > self.h):
            self.h = len(self.listDir) + 11
        self.window.resize(self.h, self.w)
        self.window.addstr(0, 0, printString, curses.A_BOLD)
        for i in range(len(self.listDir)):
            if (self.scroll + i < 1):
                continue
            elif i == self.selection:
                if(os.path.isfile(os.path.join(self.currentDir, self.listDir[i]))):
                    self.window.addstr(self.scroll + i, 5, "{}" .format(self.listDir[i]), curses.A_STANDOUT)
                else:
                    self.window.addstr(self.scroll + i, 5, "▶  {}/" .format(self.listDir[i]), curses.A_STANDOUT)
            else:
                if(os.path.isfile(os.path.join(self.currentDir, self.listDir[i]))):
                    self.window.addstr(self.scroll + i, 5, "{}" .format(self.listDir[i]))
                else:
                    self.window.addstr(self.scroll + i, 5, "▶  {}/" .format(self.listDir[i]))
    def getInput(self):
        while(self.event == -1):
            self.event = self.window.getch()

    def takeAction(self):

        if self.event == curses.KEY_RESIZE:
            self.sh, self.sw = self.screen.getmaxyx()

        elif self.event == curses.KEY_UP:
            self.selection -= 1
            if self.selection <= 0 - self.scroll:
                self.scroll += 1

        elif self.event == curses.KEY_DOWN:
            if self.selection > self.sh - 2 - self.scroll:
                self.scroll -= 1
            self.selection += 1
                #self.scroll = 1 - ((self.selection) - (self.sh-2))

        elif self.event == curses.KEY_RIGHT:
            if(not os.path.isfile(os.path.join(self.currentDir, self.listDir[self.selection]))):
                self.changeDir(os.path.join(self.currentDir, self.listDir[self.selection]))
                self.selection = 0
                self.scroll = 1

        elif self.event == curses.KEY_LEFT:
            if not (self.currentDir == os.path.abspath(os.path.join(self.currentDir, os.pardir))):
                self.changeDir(os.path.abspath(os.path.join(self.currentDir, os.pardir)))
                self.selection = 0
                self.scroll = 1

        elif self.event == 10:
            self.exit()

        elif self.event == 27:
            self.stop()

        if self.selection < 0:
            self.scroll -= 1
            self.selection += len(self.listDir)
            if self.selection > self.sh - 2:
                self.scroll -= self.selection - (self.sh - 2)
        if self.selection >= len(self.listDir):
            self.selection -= len(self.listDir)
            self.scroll = 1 - self.selection
        pass

    def start(self):

        while not self.quit:
            self.display()
            self.event  = -1
            self.getInput()
            self.takeAction()


if __name__ == '__main__':
    instance = Cda()
    instance.start()
