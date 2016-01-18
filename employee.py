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
		db.dbcursor.execute("SELECT * FROM personal WHERE pid = :pid", {"pid":employee_id})
		r = db.dbcursor.fetchone()
		if not r == None:
			self.pid = r['pid']
			self.name = r['name']
			self.sname = r['sname']
			self.surname = r['surname']
			self.ssurname = r['ssurname']
			self.position = r['position']
			self.department = r['department'] + "\n\n"


if __name__ == "__main__":
	e = Employee(18084850)
	print e.name, e.sname
