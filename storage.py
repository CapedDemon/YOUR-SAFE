from fileinput import filename
import sqlite3

def whileLoop(conn, cur):
    # main loop
    choice = None
    while choice != 'Q':
        print('"""\nQ = QUIT\nR = RETRIEVE DATA\nI = INSERT NEW DATA\nM = CREATE NEW SAFE\nC = CHANGE CURRENT SAFE\n"""\n')
        choice = input()
        if choice == 'I':

            # taking the path of the file
            path = input("Enter the path of the file: ")
            name = input(
                "Put the name with which you want to store the file: ")
            passwordFile = input("Enter the password of your file: ")

            with open(path, 'rb') as f:
                m = f.read()
            cur.execute("""
                INSERT INTO my_table (name, data, password) VALUES (?, ?, ?)""", (name, m, passwordFile))
            conn.commit()

        if choice == 'R':
            # retrieving the data
            ext = input("Enter the extenstion of your file(txt, png, etc..): ")
            name = input("Enter the name of your file: ")
            passwordFile = input("Enter the password of your file: ")
            passwordFileCheck = None
            mainFileBinary = None
            recData = cur.execute("""
                SELECT * FROM my_table
                """)

            for x in recData:
                if x[0] == name:
                    mainFileBinary = x[1]
                    passwordFileCheck = x[2]
            if passwordFileCheck != passwordFile:
                print("INVALID PASSWORD!!")
            else:
                finalName = name+'.' + ext
                with open(finalName, 'wb') as f:
                    f.write(mainFileBinary)
        
        else:
            break


def mainFunction(storage, masterPassword, ownerChoice, creatORexist):

    conn = sqlite3.connect(storage)
    cur = conn.cursor()

    if ownerChoice == "YES":
        if creatORexist == 'E':
            m = cur.execute("""
            SELECT * FROM my_table
            """)
            i = 0
            for x in m:
                if i == 0:
                    passwordCheck = x[0]

                i = i+1
                
            if passwordCheck == masterPassword:
                whileLoop(conn, cur)
            else:
                print("INVALID!!!")
        else:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS my_table (name TEXT, data BLOB, password TEXT)
            """)
            cur.execute("""
                    INSERT INTO my_table (name, data, password) VALUES (?, ?, ?)""", (masterPassword, "*", "*"))
            conn.commit()
            whileLoop(conn, cur)

    if ownerChoice == "NO":
        cur.execute("""
        CREATE TABLE IF NOT EXISTS my_table (name TEXT, data BLOB, password TEXT)
        """)
        cur.execute("""
                INSERT INTO my_table (name, data, password) VALUES (?, ?, ?)""", (masterPassword, "*", "*"))
        conn.commit()
        whileLoop(conn, cur)
        

    cur.close()
    conn.close()

# welcome statement


def main():
    ownerChoice = None
    while ownerChoice != 'Q':
        print('WELCOME TO YOUR SAFE\nHERE YOU CAN STORE YOUR PRECIOUS FILES WITH A PASSWORD.\n')

        print("DO YOU HAVE A SAFE PREVIOUSLY OR NOT. TYPE 'YES' FOR THE EXISTING SAFE OR 'NO' IF YOU ARE NEW YOU CAN PRESS 'Q' TO EXIT: ")
        ownerChoice = input()

        if ownerChoice == "YES":
            creatORexist = input("DO YOU WANT TO OPEN A NEW SAFE (TYPE 'N') OR OPEN AN EXISTING SAFE (TYPE 'E'): ")
            if creatORexist == 'E':
                storage = input("ENTER THE NAME OF YOUR SAFE: ")
                masterPassword = input("ENTER THE MASTER PASSWORD OF YOUR SAFE: ")
                mainFunction(storage, masterPassword, ownerChoice, creatORexist)
            else:
                storage = input("ENTER THE NAME OF YOUR NEW SAFE: ")
                masterPassword = input("ENTER THE MASTER PASSWORD OF YOUR NEW SAFE: ")
                mainFunction(storage, masterPassword, ownerChoice, creatORexist)

        elif ownerChoice == "NO":
            storage = input(
                "ENTER A BEAUTIFUL NAME OF YOUR SAFE WITH .db (Ex- safe.db, mongo.db): ")
            masterPassword = input("ENTER A MASTER PASSWORD OF YOUR SAFE: ")
            mainFunction(storage, masterPassword, ownerChoice, None)

if __name__ == "__main__":
    main()