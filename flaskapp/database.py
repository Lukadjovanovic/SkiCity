import csv
import os

import pymysql


def load_password():
    path = os.path.join(os.path.expanduser("~"), "i211s25-password.txt")
    with open(path) as fh:
        return fh.read().strip()


DB_PASSWORD = load_password()


def get_connection():
    return pymysql.connect(
        host="db.luddy.indiana.edu",
        user="i211s25_ljovanov",
        password=DB_PASSWORD,
        database="i211s25_ljovanov",
        cursorclass=pymysql.cursors.DictCursor,
    )

def initialize_db():
    conn = get_connection()
    _equipment = """
    create table equipment (
        id int auto_increment primary key,
        name varchar(50),
        quantity int,
        maxquantity int,
        category varchar(50)
    ) engine=InnoDB;
    """
    _people = """
    create table people (
        id int auto_increment primary key,
        name varchar(50),
        email varchar(100),
        height int(30),
        shoesize decimal(5,1),   
        checkedin bit default 0,
        pass_type varchar(50),
        boot_size varchar(10),
        ski_size varchar(10),
        pole_size varchar(10)
    ) engine=InnoDB 
    """
    with conn.cursor() as curr:
        curr.execute("drop table if exists people")
        curr.execute("drop table if exists equipment")
        curr.execute(_people)
        curr.execute(_equipment)
    conn.commit()
    conn.close()



def add_person(person: dict):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            """
            insert into people
                (name, email, height, shoesize)
            values
                (%s, %s, %s, %s)
            """,
            (person["name"], person["email"], person["height"], person["shoesize"])
        )
    conn.commit()
    conn.close()

def update_person(person: dict):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            """
            update people
            set name=%s,email=%s,height=%s,shoesize=%s
            where id = %s    
            """,
            (person["name"], person["email"], person["height"], person["shoesize"],person['id'])
        )
    conn.commit()
    conn.close()

def add_equipment(equipment: dict):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute(
            """
            insert into equipment
                (name, quantity, maxquantity, category)
            values 
                (%s, %s, %s, %s)
            """,
            (equipment["name"], equipment["quantity"], equipment["maxquantity"], equipment["category"])
        )
    conn.commit()
    conn.close()

def get_people() -> list[dict]:
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("select * from people  ")
        people = curr.fetchall()
    conn.close()
    return people

def get_equipment() -> list[dict]:
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("select * from equipment")
        equipment = curr.fetchall()
    conn.close()
    return equipment

def get_one_person(rid: int) -> dict:
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("""select * from people
        where id = %s""", (rid,))
        person = curr.fetchone()
    conn.close()
    return person


if __name__ == "__main__":
    initialize_db()
    with open("equipment.csv") as csvf:
        for row in list(csv.DictReader(csvf)):
            add_equipment(row)
    with open('people.csv') as csvf:
        for row in list(csv.DictReader(csvf)):
            add_person(row)


#New workspace for v1
'''def checkin_person(id,):
    conn = get_connection()
  #  _checkin = '''
  #  UPDATE people
 #   SET checkedin = 1
 #   WHERE id = %s;
''',(id)
    with conn.cursor() as curr:
        curr.execute(_checkin)
    conn.commit()
    conn.close()
'''
def checkout_person(id):
    conn = get_connection()
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM people WHERE id = %s", (id,))
        person = curr.fetchone()

        curr.execute("UPDATE people SET checkedin = 0 WHERE id = %s", (id,))

        if person["pass_type"] in ["Lift Ticket", "Lodge Pass"]:
            curr.execute('''
                UPDATE equipment
                SET quantity = quantity + 1
                WHERE name = %s;
            ''', (person["pass_type"],))
            curr.execute(
                '''
                UPDATE people
                SET pass_type = NULL
                WHERE id = %s;
                ''',
                (person["id"],))
        curr.execute('''
            UPDATE people
                SET pass_type = null,
                boot_size = null,
                ski_size = null,
                pole_size = null
                WHERE id = %s;
                ''', (person['id'],))

        for col in ["boot_size", "ski_size", "pole_size"]:
            item = person.get(col)
            if item:
                curr.execute('''
                    UPDATE equipment
                    SET quantity = quantity + 1
                    WHERE name = %s;
                ''', (item,))

        conn.commit()
    conn.close()


def checkin_person(id, pass_type, rent, boot, ski, pole):
    conn = get_connection()
    with conn.cursor() as curr:
        boot = boot if rent else ""
        ski = ski if rent else ""
        pole = pole if rent else ""
        curr.execute('''
            UPDATE people
            SET checkedin = 1,
                pass_type = %s,
                boot_size = %s,
                ski_size = %s,
                pole_size = %s
            WHERE id = %s;
        ''', (pass_type, boot, ski, pole, id))

        if pass_type in ["Lift Ticket", "Lodge Pass"]:
            curr.execute('''
                UPDATE equipment
                SET quantity = quantity - 1
                WHERE name = %s AND quantity > 0;
            ''', (pass_type,))

        if rent:
            for item in [boot, ski, pole]:
                if item:
                    curr.execute('''
                        UPDATE equipment
                        SET quantity = quantity - 1
                        WHERE name = %s AND quantity > 0;
                    ''', (item,))

        conn.commit()
    conn.close()

def get_checkin_people( ): 
    conn = get_connection()
    _get_checkin = '''
    SELECT * FROM people
    WHERE checkedin = 0;
    '''
    with conn.cursor() as curr:
        curr.execute(_get_checkin)
        checkin_people=curr.fetchall()
    conn.commit()
    conn.close()
    return checkin_people
'''
def checkout_person(id):
    conn = get_connection()
    _checkout = '''#
    #UPDATE people
    #SET checkedin = 0
    #WHERE id = %s;
''',(id)
    with conn.cursor() as curr:
        curr.execute(_checkout)
    conn.commit()
    conn.close()
'''
def get_checkout_people(): 
    conn = get_connection()
    _get_checkout = '''
    SELECT * FROM people
    WHERE checkedin = 1;
    '''
    with conn.cursor() as curr:
        curr.execute(_get_checkout)
        checkout_people=curr.fetchall()
    conn.commit()
    conn.close()
    return checkout_people

def get_available_boot_sizes():
    conn = get_connection()
    _query = """
    SELECT DISTINCT name FROM equipment
    WHERE category = 'boots' AND quantity > 0
    """
    with conn.cursor() as curr:
        curr.execute(_query)
        result = [row["name"] for row in curr.fetchall()]
    conn.close()
    return result

def get_available_ski_sizes():
    conn = get_connection()
    _query = """
    SELECT DISTINCT name FROM equipment
    WHERE category = 'skis' 
    """
    with conn.cursor() as curr:
        curr.execute(_query)
        result = [row["name"] for row in curr.fetchall()]
    conn.close()
    return result

def get_available_pole_sizes():
    conn = get_connection()
    _query = """
    SELECT DISTINCT name FROM equipment
    WHERE category = 'poles'
    """
    with conn.cursor() as curr:
        curr.execute(_query)
        result = [row["name"] for row in curr.fetchall()]
    conn.close()
    return result
