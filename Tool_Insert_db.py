import ttk
from Tkinter import *
import pypyodbc
import ScrolledText
import tkMessageBox
from PIL import ImageTk, Image

def db_schema():
    window = Toplevel(root)
    img = ImageTk.PhotoImage(Image.open("D://robertv//Fac//Licenta//db_schema.png"))
    panel = Label(window, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.wait_window(window)

def makemenu(win):
    top = Menu(win)  # win=top-level window
    win.config(menu=top)  # set its menu option

    edit = Menu(top, tearoff=0)
    top.add_cascade(label='Tool', menu=edit, underline=0)

    submenu = Menu(edit, tearoff=0)
    submenu.add_command(label='Database Schema', command=db_schema, underline=0)
    submenu.add_command(label='Exit', command=exit, underline=0)
    edit.add_cascade(label='Actions', menu=submenu, underline=0)

def skip_command():
    result = tkMessageBox.askquestion("Skip query", "Are You Sure?", icon='warning')
    if result == 'yes':
        print "SKIP"
    else:
        print "Don't skip"

#Database conection
connection2 = pypyodbc.connect('Driver={SQL Server};'
                                'Server=.\SQLEXPRESS;'
                                'Database=NaturalSQL;'
                                'Trusted_Connection=yes;')
cursor2 = connection2.cursor()

#GUI Generator
root = Tk(className ="Insert queries")
root.title("CSD Update Error DB")
root.geometry('1200x800')
root.configure(background='dark grey')
makemenu(root)

nlFrame = ttk.Frame(root)
nlFrame.pack(side = 'left',fill = Y)

scrollList = []


for i in range(10):

    scrollList.append(ScrolledText.ScrolledText(
    nlFrame,
    wrap   = 'word',  # wrap text rat full words only
    width  = 30,      # characters
    height = 4,       # text lines
    bg='light blue'   # background color of edit area)
    ))
    scrollList[i].pack(side='top', fill=Y)



l1 = Label(root, text="Natural Language Query",font = ("Helvetica",12))
l1.pack(side = 'left')

w2 =  ScrolledText.ScrolledText(
    wrap   = 'word',  # wrap text at full words only
    width  = 45,      # characters
    height = 5,       # text lines
    bg='light blue'   # background color of edit area)
)
w2.pack(side = 'right',fill = Y)


l1 = Label(root, text="SQL Query",font = ("Helvetica",12))
l1.pack(side = 'right')

w3 =  ScrolledText.ScrolledText(
    wrap   = 'word',  # wrap text at full words only
    width  = 10,      # characters
    height = 3,       # text lines
    bg='light blue'   # background color of edit area)
)
w3.pack(side = 'top')

l2 = Label(root, text="Name",font = ("Helvetica",12))
l2.pack(side = 'top')

var1 = IntVar()
cb = Checkbutton(root, text="Complex query", variable=var1)
cb.pack(side = 'top',fill = Y)


#Insert values in database
def act():

    for i in range(10):

        difficult_query = var1.get()
        natural_query = scrollList[i].get('1.0', END)
        sql_query = w2.get('1.0', END)
        query_name = w3.get('1.0', END)
        natural_query = '"' + natural_query + '"'
        sql_query = '"' + sql_query + '"'
        query_name = '"' + query_name + '"'
        queryForUpdate = """INSERT INTO dbo.Adnotation (Query_Name,Sql_Query,Natural_query) VALUES (%s, %s, %s);""" % (query_name, sql_query, natural_query)

        cursor2.execute(queryForUpdate)
        cursor2.commit()

buttonsFrame = ttk.Frame(root)
buttonsFrame.pack(side = 'bottom', fill = Y)


insert = Button(buttonsFrame, text="INSERT",font = ("Helvetica",15),command=act, height = 5, width = 10, bg = 'dark grey')
insert.pack(side = 'left')
skip = Button(buttonsFrame, text="SKIP", font = ("Helvetica",15),command=skip_command, height = 5, width = 10, bg = 'dark grey')
skip.pack(side = 'left')

root.mainloop()
cursor2.commit()
cursor2.close()
connection2.close()