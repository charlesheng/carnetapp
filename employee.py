import database as db


class Employee:

    pid = None
    name = None
    sname = None
    surname = None
    ssurname = None
    position = None
    department = None

    def __init__(self, employee_id):
        db.dbcursor.execute(
            "SELECT * FROM personal WHERE cedula = :pid",
            {
                "pid": employee_id
            })
        r = db.dbcursor.fetchone()
        if r is not None:
            self.pid = r['cedula']
            self.name = r['pnombre']
            self.sname = r['snombre']
            self.surname = r['papellido']
            self.ssurname = r['sapellido']
            self.position = r['cargo']
            self.department = r['dpto'] + "\n\n"


if __name__ == "__main__":
    e = Employee(18084850)
    print e.name, e.sname
