from __future__ import print_function

from PIL import Image, ImageFont, ImageDraw


class Carnet:

    _bg_img_path = 'data/front-bg.jpg'
    _font_path = 'data/DejaVuSans-Bold.ttf'
    _employee = None

    NAME_MAX_LENGHT = 18
    DEPARTMENT_MAX_LENGHT = 30
    POSITION_MAX_LENGHT = 18

    def __init__(self, emp=None):
        self._employee = emp

    def get_emp_photo(self):
        if self._employee:
            return 'output/%s.jpg' % self._employee.pid

    def create(self):
        imbg = Image.open(self._bg_img_path)
        imph = Image.open('output/pics/%s.jpg' % self._employee.pid)
        carnet_file = "output/carnets/%s.jpg" % self._employee.pid
        dpmt = self._employee.department.split("\n")

        draw = ImageDraw.Draw(imbg)
        font = ImageFont.truetype(self._font_path, size=16)
        font2 = ImageFont.truetype(self._font_path, size=18)
        font3 = ImageFont.truetype(self._font_path, size=32)

        line_size = 20

        idnum_xpos = 220
        idnum_ypos = 110

        name_xpos = 220
        name_ypos = 180

        surname_xpos = 220
        surname_ypos = 260

        dpto_xpos = 20
        dpto_ypos = 340

        position_xpos = 20
        position_ypos = 580

        draw.text(
            (idnum_xpos, idnum_ypos + line_size * 0),
            str(self._employee.pid),
            (0, 0, 0),
            font=font
        )

        draw.text(
            (name_xpos, name_ypos + line_size * 0),
            self._employee.name,
            (0, 0, 0),
            font=font
        )
        draw.text(
            (name_xpos, name_ypos + line_size * 1),
            self._employee.sname,
            (0, 0, 0),
            font=font
        )

        draw.text(
            (surname_xpos, surname_ypos + line_size * 0),
            self._employee.surname,
            (0, 0, 0),
            font=font
        )
        draw.text(
            (surname_xpos, surname_ypos + line_size * 1),
            self._employee.ssurname,
            (0, 0, 0),
            font=font
        )

        draw.text(
            (dpto_xpos, dpto_ypos + line_size * 0),
            dpmt[0],
            (0, 0, 0),
            font=font2
        )
        draw.text(
            (dpto_xpos, dpto_ypos + line_size * 1),
            dpmt[1],
            (0, 0, 0),
            font=font2
        )
        draw.text(
            (dpto_xpos, dpto_ypos + line_size * 2),
            dpmt[2],
            (0, 0, 0),
            font=font2
        )

        draw.text(
            (position_xpos, position_ypos),
            self._employee.position,
            (0, 0, 0),
            font=font3
        )

        photo_x1crop = 140
        photo_y1crop = 0
        photo_x2crop = 500
        photo_y2crop = 480

        photo_xpos = 20
        photo_ypos = 70
        photo_size = (180, 240)

        box = (photo_x1crop, photo_y1crop, photo_x2crop, photo_y2crop)
        region = imph.crop(box)
        region = region.resize(photo_size)

        imbg.paste(region, (photo_xpos, photo_ypos))

        imbg.save(carnet_file, 'JPEG')


if __name__ == "__main__":

    from employee import Employee
    c = Carnet(Employee(18084850))
    print(c.create())
