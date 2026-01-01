import sqlite3
from datetime import date, timedelta
from tabulate import tabulate 

# ---------------- DATABASE INITIALIZATION ---------------- #

def create_tables():
    try:
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Member(
            Member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Email TEXT,
            Phone TEXT,
            Role TEXT,
            JoinDate DATE
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            User_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT,
            Password TEXT,
            Role TEXT
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books(
            Book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Author TEXT,
            Publisher TEXT,
            Genre TEXT,
            Year INTEGER,
            Total_copies INTEGER,
            Available_copies INTEGER
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Issued_Books(
            Issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Member_id INTEGER,
            Book_id INTEGER,
            Issue_date DATE,
            Due_date DATE,
            Return_date DATE
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Fine_Table(
            Fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Issue_id INTEGER,
            Amount INTEGER,
            Status TEXT
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Book_Request(
            Request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Member_id INTEGER,
            Request_date DATE,
            Status TEXT
        )''')

        conn.commit()

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        conn.close()



def admin():
    conn=sqlite3.connect('LibrarySystem.db')
    cursor=conn.cursor()
    cursor.execute('''
    INSERT INTO Users(User_id,Username,Password,Role)
                   VALUES(1,'Admin','Admin123','Admin')
                ''')
    conn.commit()
    conn.close()
# admin()
# ---------------- USER FUNCTIONS ---------------- #


def Register():
    try:
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()

        Name = input("Name: ")
        Email = input("Email: ")
        Phone = input("Phone: ")
        Role = input("Role (Teacher/Student): ")
        Username = input("Username: ")
        Password = input("Password: ")

        cursor.execute('''
        INSERT INTO Member(Name,Email,Phone,Role,JoinDate)
        VALUES (?,?,?,?,?)
        ''', (Name, Email, Phone, Role, date.today().isoformat()))  

        cursor.execute('''
        INSERT INTO Users(Username,Password,Role)
        VALUES (?,?,?)
        ''', (Username, Password, Role))

        conn.commit()
        print("✅ Registration successful")

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        conn.close()


def Login():
    try:
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()

        u = input("Username: ")
        p = input("Password: ")

        cursor.execute('''
        SELECT Role FROM Users WHERE Username=? AND Password=?
        ''', (u, p))

        data = cursor.fetchone()
        if data:
            print("✅ Login successful")
            return data[0]
        else:
            print("❌ Invalid login")

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        conn.close()


# ---------------- ADMIN FUNCTIONS ---------------- #

def InsertBook():
    try:
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()

        Title = input("Title: ")
        Author = input("Author: ")
        Publisher = input("Publisher: ")
        Genre = input("Genre: ")
        Year = int(input("Year: "))
        Total = int(input("Total copies: "))
        Available = int(input("Available copies: "))

        cursor.execute('''
        INSERT INTO Books VALUES (NULL,?,?,?,?,?,?,?)
        ''', (Title, Author, Publisher, Genre, Year, Total, Available))

        conn.commit()
        print("✅ Book added")

    except ValueError:
        print("❌ Numeric values required")
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        conn.close()


def ViewBooks():
    conn = sqlite3.connect('LibrarySystem.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    data = cursor.fetchall()
    print(tabulate(data, headers=["ID","Title","Author","Publisher","Genre","Year","Total","Available"], tablefmt="grid"))
    conn.close()


def ViewMember():
    conn = sqlite3.connect('LibrarySystem.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Member")
    data = cursor.fetchall()
    print(tabulate(data, headers=["ID","Name","Email","Phone","Role","JoinDate"], tablefmt="grid"))
    conn.close()


def ViewRequest():
    conn = sqlite3.connect('LibrarySystem.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Book_Request")
    data = cursor.fetchall()
    print(tabulate(data, headers=["ReqID","Title","MemberID","Date","Status"], tablefmt="grid"))
    conn.close()


def IssueBook():
    try:
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()

        rid = int(input("Request ID: "))

        cursor.execute("SELECT Title,Member_id FROM Book_Request WHERE Request_id=? AND Status='Pending'", (rid,))
        req = cursor.fetchone()
        if not req:
            print("❌ Invalid request")
            return

        title, mid = req

        cursor.execute("SELECT Book_id,Available_copies FROM Books WHERE Title=?", (title,))
        book = cursor.fetchone()
        if not book or book[1] == 0:
            print("❌ Book unavailable")
            return

        cursor.execute("UPDATE Books SET Available_copies=Available_copies-1 WHERE Book_id=?", (book[0],))
        cursor.execute("UPDATE Book_Request SET Status='Approved' WHERE Request_id=?", (rid,))
        issue_date=date.today()
        due_date=issue_date+timedelta(days=14)
        cursor.execute("INSERT INTO Issued_Books VALUES (NULL,?,?,?, ?,NULL)",
                       (mid, book[0], issue_date.isoformat(), due_date.isoformat()))  

        conn.commit()
        print("✅ Book issued")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()




def EditMember():
     
     conn=sqlite3.connect('LibrarySystem.db')
     cursor=conn.cursor()

     char=int(input('Press 1 for Edit/Update \n 2 for Delete a member-->'))
     
     if char==1:

          Member_id=int(input('Enter Member_id-->'))
          Name=input('Enter member name-->')
          Email=input('Enter your Email Address-->')
          Phone=input('Enter your Contact Number-->')
          Role=input('Enter your Role (Teacher/Student)-->')
          JoinDate=date.today()

          cursor.execute('''
          UPDATE Member SET Name=?,Email=?,Phone=?,Role=?,JoinDate=? WHERE Member_id=?
          ''',(Name,Email,Phone,Role,JoinDate,Member_id))

          conn.commit()
          print('Member details updated✅')
     if char==2:
          Member_id=int(input('Enter Member_id-->'))
          cursor.execute('''
          DELETE FROM Member WHERE Member_id=?
     ''',(Member_id,))
          conn.commit()
          print('Deleted Member details')
     conn.close()
   





def EditBook():
     conn=sqlite3.connect('LibrarySystem.db')
     cursor=conn.cursor()
     char=int(input('Press 1 for Edit/Update \n 2 for Delete a Book-->'))
     if char==1:
          Book_id=int(input('Enter Book_id-->'))
          Title=input('Enter Title-->')
          Publisher=input('Enter Publisher name-->')
          Year=int(input('Enter published year-->'))
          Total_copies=int(input('Enter Total number or copies-->'))
          Available_copies=int(input('Enter available copies-->'))
          cursor.execute('''
               UPDATE  Books SET Title=?,Publisher=?,Year=?,Total_copies=?,Available_copies=? WHERE Book_id=?
          ''',(Title,Publisher,Year,Total_copies,Available_copies,Book_id))
          conn.commit()
          print('Updated book details✅')
     if char==2:
          Book_id=int(input('Enter Book_id -->'))
          cursor.execute('''
          DELETE FROM Books WHERE Book_id=?
          ''',(Book_id,))
          conn.commit()
          print('Deleted Book details..')
     conn.close()


def ViewFineAdmin():
     conn=sqlite3.connect('LibrarySystem.db')
     cursor=conn.cursor()

     cursor.execute('''
          SELECT * FROM Fine_Table
     ''')
     alldata=cursor.fetchall()
     print(tabulate(alldata,headers=["Fine_ID","Issue_ID","Amount","Status"],tablefmt="grid"))
     conn.close()

# ---------------- MEMBER FUNCTIONS ---------------- #

def SearchBookByGenre():
    conn = sqlite3.connect('LibrarySystem.db')
    cursor = conn.cursor()
    genre = input("Genre: ")
    cursor.execute("SELECT * FROM Books WHERE Genre=?", (genre,))
    data = cursor.fetchall()
    print(tabulate(data, headers=["ID","Title","Author","Publisher","Genre","Year","Total","Available"], tablefmt="grid"))
    conn.close()

def SearchBook():
    conn=sqlite3.connect('LibrarySystem.db')
    cursor=conn.cursor()

    name=input('Enter Book Title -->')

    cursor.execute('''
        SELECT * FROM Books WHERE Title=?
    ''',(name,))
    Value=cursor.fetchall()
   
    if Value:                            
        print('Book found')
        print(tabulate(Value, headers=["ID","Title","Author","Publisher","Genre","Year","Total","Available"], tablefmt="grid"))
    else:
         print('No such Book Available')
    conn.commit()
    conn.close()


def RequestBook():
    try:
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()

        mid = int(input("Member ID: "))
        title = input("Book Title: ")

        cursor.execute("SELECT COUNT(*) FROM Issued_Books WHERE Member_id=? AND Return_date IS NULL", (mid,))
        if cursor.fetchone()[0] >= 3:
            print("❌ Max 3 books allowed")
            return

        cursor.execute("""
        SELECT SUM(Amount) FROM Fine_Table WHERE Status='Unpaid'
        AND Issue_id IN (SELECT Issue_id FROM Issued_Books WHERE Member_id=?)
        """, (mid,))
        fine = cursor.fetchone()[0]
        if fine and fine > 300:
            print("❌ Fine > ₹300. Clear dues first")
            return

        cursor.execute("INSERT INTO Book_Request VALUES (NULL,?,?,?,'Pending')", (title, mid, date.today().isoformat())) 
        conn.commit()
        print("✅ Request placed")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

def MyIssuedBook():
    
    conn = sqlite3.connect('LibrarySystem.db')
    cursor = conn.cursor()

    member_id = int(input('Enter member ID-->'))
    cursor.execute('''
        SELECT Issue_id, Book_id, Issue_date, Due_date, Return_date
        FROM Issued_Books
        WHERE Member_id=?
    ''', (member_id,))

    data = cursor.fetchall()
    print(tabulate(
        data,
        headers=["Issue_id","Book_id","Issue_date","Due_date","Return_date"],
        tablefmt="grid"
    ))
    conn.close()




def ReturnBook():
    try:
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()

        mid = int(input("Member ID: "))
        bid = int(input("Book ID: "))

        cursor.execute("""
        SELECT Issue_id,Due_date FROM Issued_Books
        WHERE Member_id=? AND Book_id=? AND Return_date IS NULL OR Return_date=''
        """, (mid, bid))
        data = cursor.fetchone()
        if not data:
            print("❌ No issued book")
            return

        issue_id, due = data
        cursor.execute("UPDATE Issued_Books SET Return_date=? WHERE Issue_id=?", (date.today().isoformat(), issue_id))
        cursor.execute("UPDATE Books SET Available_copies=Available_copies+1 WHERE Book_id=?", (bid,))

        
        today = date.today()
        due_date = date.fromisoformat(due)

        late = (today - due_date).days

        if late > 0:
            cursor.execute("INSERT INTO Fine_Table VALUES (NULL,?,?, 'Unpaid')", (issue_id, late*10))
            print("Returned with fine")
        else:
            print("Returned successfully")

        conn.commit()

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def PayFine():
    try:
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()

        fid = int(input("Fine ID: "))
        cursor.execute("SELECT Amount,Status FROM Fine_Table WHERE Fine_id=?", (fid,))
        data = cursor.fetchone()
        if not data:
            print("❌ Invalid Fine ID")
            return

        if data[1] == 'Paid':
            print("Already paid")
            return

        cursor.execute("UPDATE Fine_Table SET Status='Paid' WHERE Fine_id=?", (fid,))
        conn.commit()
        print("✅ Payment successful")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

#FINE DETAILS FOR MEMBER
def ViewFineMember():
     
    try:
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()

        member_id = int(input('Enter your Member_id --> '))

        cursor.execute('''
        SELECT 
            FT.Fine_id,
            FT.Issue_id,
            FT.Amount,
            FT.Status
        FROM Fine_Table FT
        JOIN Issued_Books IB ON FT.Issue_id = IB.Issue_id
        WHERE IB.Member_id = ?
        ''', (member_id,))

        fines = cursor.fetchall()

        if fines:
            print(tabulate(
                fines,
                headers=["Fine ID", "Issue ID", "Amount", "Status"],
                tablefmt="grid"
            ))
        else:
            print("✅ No fines found for this member")

    except Exception as e:
        print("Error while fetching fine details:", e)

    finally:
        conn.close()

def ViewByGenre():
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()
        genre=input('Enter the Genre of books you want to search-->')

        cursor.execute('''
        SELECT * FROM Books WHERE genre=?
        ''',(genre,))

        data=cursor.fetchall()
        
        if data:
            print(tabulate(data,headers=["Book_ID","Title","Author","Publisher","Genre","Year","Total_copies","Available_copies"],tablefmt="grid"))
        else:
            print(f'No books Found in Genre {genre}')
        conn.commit()
        conn.close()




def ViewAllGenre():
        conn = sqlite3.connect('LibrarySystem.db')
        cursor = conn.cursor()

        cursor.execute('''
                SELECT DISTINCT TRIM(LOWER(Genre)) AS Genre FROM Books WHERE Genre IS NOT NULL AND Genre !=''
                    ''')
        data=cursor.fetchall()
        if data:
            print(tabulate(data,headers=["Genre"],tablefmt="grid"))
        else:
            print('No Genre Found')
        conn.commit()
        conn.close()
        
    

# ---------------- MAIN MENU ---------------- #

def main():
    create_tables()

    while True:
        print("\n1.Register\n2.Login\n3.Exit")
        ch = input("Choice: ")

        if ch == '1':
            Register()
        elif ch == '2':
            role = Login()
            if role == 'Admin':
                while True:
                    print("\n1.Add Book\n2.View Books\n3.View Members\n4.Edit Member\n5.View Requests\n6.Edit Books\n7.Issue Book\n8.View Fine Status\n9.Exit")
                    c = input("Choice: ")
                    if c == '1': InsertBook()
                    elif c == '2': ViewBooks()
                    elif c == '3': ViewMember()
                    elif c == '4': EditMember()
                    elif c == '5': ViewRequest()
                    elif c == '6': EditBook()
                    elif c == '7': IssueBook()
                    elif c == '8': ViewFineAdmin()
                    else: break
            elif role == 'Teacher' or role == 'Student':
                while True:
                    print("\n1.View Books\n2.Search by Genre\n3.Search Book by name\n4.Request Book\n5.My Issued Books\n6.Return Book\n7.View Fine details\n8.Pay Fine\n9. View All Genre\n10.View All Books In same Genre\n11.Exit")
                    c = input("Choice: ")
                    if c == '1': ViewBooks()
                    elif c == '2': SearchBookByGenre()
                    elif c == '3': SearchBook()
                    elif c == '4': RequestBook()
                    elif c == '5': MyIssuedBook()
                    elif c == '6': ReturnBook()
                    elif c == '7': ViewFineMember()
                    elif c == '8': PayFine()
                    elif c == '9': ViewAllGenre()
                    elif c == '10': ViewByGenre()
                    else: break
            else: print('Wrong Username OR Password')
        else:
            break


main()
