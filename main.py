from colorama import Fore as Color
import re
from mysql.connector import connect, Error


def create_table(curs, name) -> None:
    curs.execute(f"""
    CREATE TABLE {name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(250),
        report VARCHAR(250),
        department_id INT,
        period INT,
        period_comment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP
    )
    """)


def get_names(curs, table) -> list:
    curs.execute(f"DESCRIBE {table};")
    result = curs.fetchall()
    return [x[0] for x in result]


def get_types(curs, table) -> list:
    curs.execute(f"DESCRIBE {table};")
    result = curs.fetchall()
    return [x[1] for x in result]


def read_table(curs, table) -> None:
    curs.execute(f"SELECT * FROM {table}")
    result = curs.fetchall()
    result = [x for x in result]
    for i in result:
        print(i)


def insert_data(curs, table) -> None:
    name_list = get_names(curs, table)
    curs.execute(f"DESCRIBE {table}")
    for string in curs:
        if string[-1] != '':
            name_list.remove(string[0])
    values = [input(f'{x}: ') for x in name_list]
    for i in range(len(values)):
        if re.search(r"\D", values[i]) and re.search(r"\D", values[i]).group():
            values[i] = "'"+values[i]+"'"
    curs.execute(f"INSERT {table} ({', '.join([x for x in name_list])}) VALUES ({', '.join(values)})")


def find(curs, table, condition) -> None:
    name_list = get_names(curs, table)
    curs.execute(f"SELECT {', '.join(name_list)} FROM {table}{condition}")
    old = [x for x in curs]
    for i in old:
        print(i)


def update_data(curs, table, condition) -> None:
    name_list = get_names(curs, table)
    curs.execute(f"DESCRIBE {table}")
    for string in curs:
        if string[-1] != '':
            name_list.remove(string[0])
    values = [input(f'{x}: ') for x in name_list]
    for i in range(len(values)):
        if re.search(r"\D", values[i]) and re.search(r"\D", values[i]).group():
            values[i] = "'" + values[i] + "'"
    new_data_list = []
    for i in range(len(values)):
        if values[i] != '':
            new_data_list.append(f"{name_list[i]} = {values[i]}")
    curs.execute(f"UPDATE {table} SET {', '.join([x for x in new_data_list])}{condition};")


def help_use():
    help_table = """
+--------------------------------------------+--------------------------------------------+
| command name                               | description                                |
+--------------------------------------------+--------------------------------------------+
| exit                                       | closes the program                         |
+--------------------------------------------+--------------------------------------------+
| read `table_name`                          | prints all values from the table           |
+--------------------------------------------+--------------------------------------------+
| add data `table_name`                      | adds data to the table                     |
+--------------------------------------------+--------------------------------------------+
| update data `table_name` where `condition` | updates data (if condition was performed)  |
+--------------------------------------------+--------------------------------------------+
| find data `table_name` where `condition`   | prints data (if condition was performed)   |
+--------------------------------------------+--------------------------------------------+
Example of condition: where i=0 (without SPACES)
"""
    print(Color.LIGHTYELLOW_EX + help_table)


def main_function():
    try:
        with connect(
            host="localhost",
            user=input(Color.MAGENTA + "user: "),
            password=input("password: "),
            database=input("database: ")
        ) as connection:
            with connection.cursor() as cursor:
                print(Color.LIGHTYELLOW_EX + "\nWelcome to MSWork v0.8.9!\n")
                while True:
                    user_input = input(Color.LIGHTYELLOW_EX + "-> ")
                    if user_input == "exit":
                        break
                    if user_input == "help":
                        help_use()
                    elif re.search(r"read \S*", user_input) and re.search(r"read \S*", user_input).group():
                        read_table(cursor, user_input.split()[1])
                        connection.commit()
                    elif re.search(r"add data \S*", user_input) and re.search(r"add data \S*", user_input).group():
                        insert_data(cursor, user_input.split()[2])
                        connection.commit()
                    elif re.search(r"update data \S* where \S*", user_input) and \
                            re.search(r"update data \S* where .*", user_input).group():
                        update_data(cursor, user_input.split()[2], re.search(r" where \S*", user_input).group())
                        connection.commit()
                    elif re.search(r"find data \S* where \S*", user_input) and \
                            re.search(r"find data \S* where .*", user_input).group():
                        find(cursor, user_input.split()[2], re.search(r" where \S*", user_input).group())
                        connection.commit()
    except Error as e:
        print(e)


if __name__ == "__main__":
    main_function()
