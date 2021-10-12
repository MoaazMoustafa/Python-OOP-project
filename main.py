import psycopg2
# I created another file with only one function which do nothing except returning a string with my password
from password import password

con = psycopg2.connect(database='postgres', user='postgres', password=password(),
                       host='127.0.0.1', port='5432')
print('Database opened successfully')
cur = con.cursor()
# creating the table


# cur.execute('''create table Employee(
#             id SERIAL PRIMARY KEY,
#             fname text not null,
#             lname text not null,
#             age int not null,
#             department varchar,
#             salary int not null,
#             mag_dept varchar
#             );''')
# con.commit()
# con.close()

class Employee:
    employee_names = []
    cur.execute('select * from Employee;')
    rows = cur.fetchall()
    for row in rows:
        employee_names.append({row[0]: row[1]+" "+row[2]})

    def __init__(self, id, fname, lname, age, dept, salary):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.age = age
        self.dept = dept
        self.salary = salary
        Employee.employee_names.append({id: fname+" "+lname})
        cur.execute('''Insert into Employee( id,fname, lname, age, department, salary)
            values(%s, %s, %s, %s, %s, %s)
            ''', (id, fname, lname, age, dept, salary))
        print('Record inserted successfully')
        con.commit()
        # con.close()

    @staticmethod
    def transfere(id, new_dept):
        cur.execute('''update Employee set department = %s 
                        where id = %s ;''', (new_dept, id))
        print("Data updated successfully")
        con.commit()

    @staticmethod
    def fire(id):
        cur.execute('''delete from employee where id = %s;''', (id,))
        print('Employee is fired.')
        con.commit()
        for emp in Employee.employee_names:
            for key in emp:
                if key == id:
                    Employee.employee_names.remove(emp)
        print(Employee.employee_names)

    @staticmethod
    def list_employees():
        cur.execute('select * from Employee;')
        rows = cur.fetchall()
        for row in rows:
            print(
                f"Employee id:{row[0]} his name is: {row[1]} {row[2]} and is {row[3]} years old working for {row[4]} department.")

    @staticmethod
    def show(id):
        cur.execute('select * from Employee where id = %s', (id,))
        rows = cur.fetchall()

        # checking if the user trying to accsess the manager information through the employee interface
        if rows[0][6]:
            print("You try to access a manager from an employee interface. ")
        else:
            print(
                f"""Employee id: {rows[0][0]} his name is: {rows[0][1]} {rows[0][2]} and he is {rows[0][3]} years old working for {rows[0][4]} department his salary : {rows[0][5]}""")


class Manager(Employee):
    def __init__(self, id, fname, lname, age, dept, salary, mgr_dept):
        super().__init__(id, fname, lname, age, dept, salary)
        self.mgr_dept = mgr_dept
        # updating the table with the manager department because I couldn't add it again cause i already added it through Employee __init__ function
        cur.execute(
            '''update employee set mag_dept = %s where id = %s''', (mgr_dept, id))
        print('Record inserted successfully')
        con.commit()

    def show(id):
        cur.execute('select * from Employee where id = %s', (id,))
        rows = cur.fetchall()
        # print(rows)
        print(f"""Employee id:{rows[0][1]} his name is: {rows[0][1]} {rows[0][2]} and is {rows[0][3]} years old working for {rows[0][4]} department his salary : confidintioal and managing department {rows[0][6]}""")


print(Employee.employee_names)

mgr_or_not = input(
    "Is the person a manager or an employee if manager type (m) if employee type (e) or type 'q' to exit: ").strip().lower()

if mgr_or_not == 'e':
    answer = input(
        "Please write your option 'add' 'transfere' 'fire' 'show' or 'list' 'q' to exit:  ").lower().strip()
    if answer == 'add':
        id = int(input("Enter the employee id: "))
        fname = input("Enter the employee first name: ")
        lname = input("Enter the employee last name: ")
        age = int(input("Enter the employee age: "))
        dept = input("Enter the employee department: ")
        salary = int(input("Enter the employee salary: "))
        new_emp = Employee(id, fname, lname, age, dept, salary)
    elif answer == 'transfere':
        id = int(input("Enter the employee id: "))
        new_dept = input("Enter the employee  new department: ")
        Employee.transfere(id, new_dept)
    elif answer == 'fire':
        id = int(input("Enter the employee id: "))
        Employee.fire(id)
    elif answer == 'list':
        Employee.list_employees()
    elif answer == 'show':
        id = int(input("Enter the employee id: "))
        Employee.show(id)
    elif answer == 'q':
        print("Thank you see you next time.")


elif mgr_or_not == 'm':
    answer = input(
        "Please write your option 'add' 'transfere' 'fire' 'show' or 'list' 'q' to exit:  ").lower().strip()
    if answer == 'add':
        id = int(input("Enter the manager id: "))
        fname = input("Enter the manager first name: ")
        lname = input("Enter the manager last name: ")
        age = int(input("Enter the manager age: "))
        dept = input("Enter the manager department: ")
        salary = int(input("Enter the manager salary: "))
        mgr_dept = input(
            "Enter the  department which the manager is managing: ")
        new_mgr = Manager(id, fname, lname, age, dept, salary, mgr_dept)
    elif answer == 'transfere':
        id = int(input("Enter the manager id: "))
        new_dept = input("Enter the manager  new department: ")
        Manager.transfere(id, new_dept)
    elif answer == 'fire':
        id = int(input("Enter the manager id: "))
        Manager.fire(id)
    elif answer == 'list':
        Manager.list_employees()
    elif answer == 'show':
        id = int(input("Enter the manager id: "))
        Manager.show(id)
    elif answer == 'q':
        print("Thank you see you next time.")
elif mgr_or_not == 'q':
    print("Thank you see you next time.")


con.close()


# mgr = Manager(6, 'Moustafa', 'Abbas', 62, 'company', 3000, "python")

# print(Employee.employee_names)

# print(Employee.employee_names)


# emp1 = Employee(1,"Moaaz", "Moustafa", 27, "python", 20000)
# print(emp1.lname)
# print(emp1.fname)
# print(emp1.age)
# print(emp1.salary)
# print(emp1.id)
# print(Employee.employee_names)
# emp1.transfere("full stack",1)
# emp1.fire(1)
# Employee.__init__( "Ahmed", "Moustafa", 29, "EHAF", 30000 )
