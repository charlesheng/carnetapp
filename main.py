#!/usr/bin/python
from gi.repository import Gtk
from os import system
from PIL import Image
import StringIO, cairo

from carnet import Carnet
from employee import Employee


# ---- FOR COMMON USE
def execute_cmd(cmd_string):
    # system("clear")
    a = system(cmd_string)
    print ""
    if a == 0:
        pass  # print "Command executed correctly"
    else:
        print "Command terminated with error"
        raw_input("Press enter")
    print ""

    return a
# ---- FOR COMMON USE


class MyWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="ID Card Generator - By Erick Birbe")

        self.employee = None

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
        self.btn_take_picture.connect(
            'clicked', self.on_btn_take_picture_clicked)

        self.btn_print = Gtk.Button("Print")
        self.btn_print.connect('clicked', self.on_btn_print_clicked)

        self.image = Gtk.Image()

        self.grid.add(self.lbl_search)
        self.grid.attach(self.txt_search, 1, 0, 1, 1)

        self.grid.attach(self.lbl_name, 0, 1, 1, 1)
        self.grid.attach(self.txt_name, 1, 1, 1, 1)
        self.grid.attach(self.txt_name1, 1, 2, 1, 1)

        self.grid.attach(self.lbl_surname, 0, 3, 1, 1)
        self.grid.attach(self.txt_surname, 1, 3, 1, 1)
        self.grid.attach(self.txt_surname1, 1, 4, 1, 1)

        self.grid.attach(self.lbl_department, 0, 5, 1, 1)
        self.grid.attach(self.txt_department, 1, 5, 1, 3)

        self.grid.attach(self.lbl_position, 0, 8, 1, 1)
        self.grid.attach(self.txt_position, 1, 8, 1, 3)

        self.grid.attach(self.btn_process, 0, 11, 2, 1)
        self.grid.attach(self.btn_take_picture, 0, 12, 2, 1)
        self.grid.attach(self.btn_print, 0, 13, 2, 1)

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
        self.load_image()

    def load_image(self, file_name=None):

        print "Filename = %s" % file_name

        self.image.destroy()

        if file_name is None:
            self.image = Gtk.Image.new_from_file('data/front-bg-white.png')
        else:
            self.image = Gtk.Image.new_from_file(
                'output/carnets/%s.png' % file_name)

        self.grid.attach(self.image, 3, 0, 1, 20)
        self.image.show()

    def set_employee(self, pid):
        if self.employee is None or self.employee.pid != pid:
            self.employee = Employee(pid)
            self.txt_name.set_text(self.employee.name)
            self.txt_name1.set_text(self.employee.sname)
            self.txt_surname.set_text(self.employee.surname)
            self.txt_surname1.set_text(self.employee.ssurname)
            self.txt_position.get_buffer().set_text(self.employee.position)
            self.txt_department.get_buffer().set_text(self.employee.department)

    def update_employee(self):

        start, end = self.txt_position.get_buffer().get_bounds()
        self.employee.position = self.txt_position.get_buffer().get_text(start, end, False)

        start, end = self.txt_department.get_buffer().get_bounds()
        self.employee.department = self.txt_department.get_buffer().get_text(start, end, False)

        carnet = Carnet(self.employee)
        carnet.create()

    def on_btn_process_clicked(self, widget):

        if self.employee is None:
            return

        self.update_employee()
        self.load_image(self.employee.pid)

    def on_txt_search_activate(self, widget):
        self.clear_form()
        try:
            self.set_employee(widget.get_text())
            self.load_image(self.employee.pid)
        except Exception, excp:
            print excp
            self.clear_form()

    def on_btn_take_picture_clicked(self, widget):
        status = execute_cmd("python camera.py %s" % self.employee.pid)
        if status == 0:
            carnet = Carnet(self.employee)
            carnet.create()
            self.load_image(self.employee.pid)

    def on_btn_print_clicked(self, widget):
        self.pd = Gtk.PrintOperation()
        self.pd.set_n_pages(1)
	self.pd.set_use_full_page(True)
        self.pd.connect("draw_page", self.draw_page)
        result = self.pd.run(
            Gtk.PrintOperationAction.PRINT_DIALOG, None)

        print result  # handle errors etc.

    def draw_page(self, operation=None, context=None, page_nr=None):

	psettings = self.pd.get_print_settings()
	psize = psettings.get_paper_size()
	psize.set_size(10, 10, Gtk.Unit.MM)
	psettings.set_paper_size(psize)
	self.pd.set_print_settings(psettings)

	w = int(context.get_width())
	h = int(context.get_height())

	#page_setup = context.get_page_setup()
	#paper_size = page_setup.get_paper_size()
	#paper_size.set_size(10, 10, Gtk.Unit.INCH)
	#page_setup.set_paper_size(paper_size)

	# Getting JPG image
        im = Image.open("output/carnets/%s.png" % self.employee.pid)
	im = im.resize((w,h), Image.ANTIALIAS)
        buf = StringIO.StringIO()
        im.save(buf, format="PNG")
        buf.seek(0)

	surface = cairo.ImageSurface.create_from_png(buf)
        ctx = context.get_cairo_context()
	print surface.get_width(), surface.get_height()
	ctx.set_source_surface(surface, 0.0, 0.0)
        ctx.paint()

if __name__ == "__main__":
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
