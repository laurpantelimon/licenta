import ttk
from Tkinter import *
import pypyodbc
import ScrolledText
import tkMessageBox
from PIL import ImageTk, Image
import json
from pprint import pprint

global json_index
json_index = 0

def db_schema():
    window = Toplevel(root)

    original = Image.open("D://robertv//Fac//Licenta//db_schema.png")
    resized = original.resize((1200, 800), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resized)

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

#Database conection
connection2 = pypyodbc.connect('Driver={SQL Server};'
                                'Server=.\SQLEXPRESS;'
                                'Database=NaturalSQL;'
                                'Trusted_Connection=yes;')
cursor2 = connection2.cursor()


#JSON immporter
with open('stackexchange_clean.json') as data_file:
    data = json.load(data_file)


#GUI Generator
root = Tk(className ="Insert queries")
root.title("CSD Update Error DB")
root.geometry('1200x800')
root.configure(background='dark grey')
makemenu(root)

'''Create scrolled list items'''
nlFrame = ttk.Frame(root)
nlFrame.pack(side = 'left',fill = Y)
scrollList = []
for i in range(11):

    scrollList.append(ScrolledText.ScrolledText(
    nlFrame,
    wrap   = 'word',  # wrap text rat full words only
    width  = 30,      # characters
    height = 4,       # text lines
    bg='light blue'   # background color of edit area)
    ))
    scrollList[i].pack(side='top', fill=Y)
scrollList[0].insert(INSERT,data[json_index]['title'])
scrollList[10].insert(INSERT,data[json_index]['url'])
scrollList[10].config(state=DISABLED)


l1 = Label(root, text="Natural Language Query",font = ("Helvetica",12))
l1.pack(side = 'left')

'''Create scrolled list'''
w2 =  ScrolledText.ScrolledText(
    wrap   = 'word',  # wrap text at full words only
    width  = 45,      # characters
    height = 5,       # text lines
    bg='light blue'   # background color of edit area)
)

w2.insert(INSERT,data[json_index]['snippet'])
w2.pack(side = 'right',fill = Y)

l1 = Label(root, text="SQL Query",font = ("Helvetica",12))
l1.pack(side = 'right')

'''Create name scrolled list'''
w3 =  ScrolledText.ScrolledText(
    wrap   = 'word',  # wrap text at full words only
    width  = 10,      # characters
    height = 3,       # text lines
    bg='light blue'   # background color of edit area)
)
w3.pack(side = 'top')

l2 = Label(root, text="Name",font = ("Helvetica",12))
l2.pack(side = 'top')

'''Change query value'''
def skip_command(w2,data,w3):
    global json_index
    result = tkMessageBox.askquestion("Skip query", "Are You Sure?", icon='warning')
    if result == 'yes':
        json_index += 1
        counter.set(json_index)
        w2.delete('1.0',END)
        w2.insert(INSERT,data[json_index]['snippet'])
        for i in range(10):
            w3[i].delete('1.0', END)
        w3[0].insert(INSERT, data[json_index]['title'])

'''Create checkbox'''
var1 = IntVar()
cb = Checkbutton(root, text="Complex query", variable=var1)
cb.pack(side = 'top',fill = Y)


'''Create index input'''
indexInputFrame = ttk.Frame(root)
indexInputFrame.pack(side = 'top', fill = Y)

'''Display current index'''
counter = IntVar()
counter.set(json_index)
l2 = Label(indexInputFrame, textvariable=counter,font = ("Helvetica",12))
l2.pack(side = 'top')


def set_index(index):
    global json_index
    json_index = int(index) - 1
    l2.config(text = index)
    skip_command(w2,data,scrollList)

indexEdit = Text(root, height=2, width=10)
indexEdit.pack(side = 'top')
jump = Button(indexInputFrame, text="JUMP",font = ("Helvetica",12),command=lambda : set_index(indexEdit.get('1.0', END)), height = 3, width = 10, bg = 'dark grey')
jump.pack(side = 'top')


'''Create buttons'''
buttonsFrame = ttk.Frame(root)
buttonsFrame.pack(side = 'bottom', fill = Y)

'''Make chages after insert'''
def next_command(w2,data,w3):
    global json_index
    json_index += 1
    counter.set(json_index)
    w2.delete('1.0',END)
    w2.insert(INSERT,data[json_index]['snippet'])
    for i in range(10):
        w3[i].delete('1.0', END)
    w3[0].insert(INSERT, data[json_index]['title'])

'''Insert values into database'''
def insert_command():
    result = tkMessageBox.askquestion("Insert values", "Are You Sure?", icon='warning')
    if result == 'yes':
        for i in range(10):
            if scrollList[i].get('1.0', END) != "\n":
                user_name = w3.get('1.0', END)
                difficult_query = int(var1.get())
                natural_query = scrollList[i].get('1.0', END)
                #print natural_query
                sql_query = w2.get('1.0', END)
                query_id = data[json_index]['url']

                queryForUpdate = "INSERT INTO dbo.Adnotation (QueryID,Input_User,Natural_Query,Sql_Query,Is_difficult) VALUES (?,?,?,?,?)"

                cursor2.execute(queryForUpdate,(query_id,user_name,natural_query,sql_query,difficult_query))
                cursor2.commit()
    next_command(w2,data,scrollList)

insert = Button(buttonsFrame, text="INSERT",font = ("Helvetica",15),command=insert_command, height = 5, width = 10, bg = 'dark grey')
insert.pack(side = 'left')
skip = Button(buttonsFrame, text="SKIP", font = ("Helvetica",15),command=lambda: skip_command(w2,data,scrollList), height = 5, width = 10, bg = 'dark grey')
skip.pack(side = 'left')





root.mainloop()
cursor2.close()
connection2.close()