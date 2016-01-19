#!/usr/bin/env python

from os import system
import curses
import locale

from employee import Employee
from carnet import Carnet

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


def addstr_bold(y, x, text):
    screen.attron(curses.A_BOLD)
    screen.addstr(y, x, text)
    screen.attroff(curses.A_BOLD)


def get_param(prompt_string):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, prompt_string)
    screen.refresh()
    input = screen.getstr(10, 10, 60)
    return input


def execute_cmd(cmd_string):
    system("clear")
    a = system(cmd_string)
    print ""
    if a == 0:
        pass  # print "Command executed correctly"
    else:
        print "Command terminated with error"
        raw_input("Press enter")
    print ""

    return a

x = 0

while x != ord('4'):

    screen = curses.initscr()

    screen.clear()
    screen.border(0)
    screen.addstr(1, 1, "Please enter a number...")
    screen.addstr(4, 4, "1 - Search for a person")
    screen.addstr(7, 4, "4 - Exit")
    screen.refresh()

    x = screen.getch()

    if x == ord('1'):
        person_id = get_param("Enter the person ID:")

        emp = Employee(person_id)

        if emp.pid is not None:

            screen.clear()
            screen.border(0)
            screen.addstr(2, 4, "Name:")
            addstr_bold(2, 14, emp.name.encode(code))
            screen.addstr(3, 4, "Surname:")
            addstr_bold(3, 14, emp.surname.encode(code))
            screen.addstr(7, 4, "Press any key to cotinue...")
            screen.refresh()
            screen.getch()

            curses.endwin()
            status = execute_cmd("python camera.py %s" % person_id)

            if status == 0:
                carnet = Carnet(emp)
                carnet.create()

curses.endwin()
