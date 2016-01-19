#!/usr/bin/python
from gi.repository import Gtk
from gi.repository import GLib
from os import system
import threading

from employee import Employee

# Use threads                                       
GLib.threads_init()

## FOR COMMON USE
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
## FOR COMMON USE


class MyWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="ID Card Generator - By Erick Birbe")

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)
        self.add(self.grid)

        self.lbl_search = Gtk.Label("ID")
        self.txt_search = Gtk.SearchEntry()
        self.txt_search.connect('activate', self.on_txt_search_activate)

        self.lbl_name = Gtk.Label("Name:")
        self.txt_name = Gtk.Entry()
        self.txt_name.set_editable(False)
        
        self.txt_name1 = Gtk.Entry()
        self.txt_name1.set_editable(False)

        self.lbl_surname = Gtk.Label("Surname:")
        self.txt_surname = Gtk.Entry()
        self.txt_surname.set_editable(False)
        
        self.txt_surname1 = Gtk.Entry()
        self.txt_surname1.set_editable(False)

        self.lbl_position = Gtk.Label("Position:")
        self.txt_position = Gtk.TextView()
        self.txt_position.set_editable(True)

        self.lbl_department = Gtk.Label("Department:")
        self.txt_department = Gtk.TextView()
        self.txt_department.set_editable(True)
        self.txt_department.set_wrap_mode(Gtk.WrapMode.WORD)

        self.btn_process = Gtk.Button("Process!")
        self.btn_process.connect('clicked', self.on_btn_process_clicked)
        
        self.btn_take_picture = Gtk.Button("Take a Picture")
        self.btn_take_picture.connect('clicked', self.on_btn_take_picture_clicked)
        
        self.image = Gtk.Image()

        self.grid.add(self.lbl_search)
        self.grid.attach(self.txt_search, 1, 0, 1, 1)
        
        self.grid.attach(self.lbl_name, 0, 1, 1, 1)
        self.grid.attach(self.txt_name, 1, 1, 1, 1)
        self.grid.attach(self.txt_name1, 1, 2, 1, 1)

        self.grid.attach(self.lbl_surname, 0, 3, 1, 1)
        self.grid.attach(self.txt_surname, 1, 3, 1, 1)
        self.grid.attach(self.txt_surname1, 1, 4, 1, 1)

        self.grid.attach(self.lbl_position, 0, 5, 1, 1)
        self.grid.attach(self.txt_position, 1, 5, 1, 3)

        self.grid.attach(self.lbl_department, 0, 8, 1, 1)
        self.grid.attach(self.txt_department, 1, 8, 1, 3)

        self.grid.attach(self.btn_process, 0, 11, 2, 1)
        self.grid.attach(self.btn_take_picture, 0, 12, 2, 1)

        self.clear_form()
        
    def clear_form(self):
        widgets = [
            self.txt_name,
            self.txt_name1,
            self.txt_surname,
            self.txt_surname1,
            self.txt_position.get_buffer(),
            self.txt_department.get_buffer(),
        ]
        for w in widgets:
            w.set_text('')
        self.load_image('data/front-bg-white.png')

    def load_image(self, path):
        self.image.destroy()
        self.image = Gtk.Image.new_from_file(path)
        self.grid.attach(self.image, 3, 0, 1, 20)
        self.image.show()

    def on_btn_process_clicked(self, widget):
        self.load_image('output/carnets/%s.jpg' % self.txt_search.get_text())
        
    def on_txt_search_activate(self, widget):
        self.clear_form()
        e = Employee(widget.get_text())
        self.txt_name.set_text(e.name)
        self.txt_name1.set_text(e.sname)
        self.txt_surname.set_text(e.surname)
        self.txt_surname1.set_text(e.ssurname)
        self.txt_position.get_buffer().set_text(e.position)
        self.txt_department.get_buffer().set_text(e.department)
        self.btn_process.do_activate(self.btn_process)
        
    def on_btn_take_picture_clicked(self, widget):
        execute_cmd("python camera.py %s" % 17936784)

if __name__ == "__main__":
	win = MyWindow()
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()
