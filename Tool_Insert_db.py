import ttk
from Tkinter import *
import pypyodbc
import ScrolledText
import json
from pprint import pprint


# #Database conection
# connection2 = pypyodbc.connect('Driver={SQL Server};'
#                                'Server=.\SQLEXPRESS;'
#                                'Database=NaturalSQL;'
#                                'Trusted_Connection=yes;')
# cursor2 = connection2.cursor()

#JSON immporter
with open('stackexchange_clean.json') as data_file:
    data = json.load(data_file)
pprint(data)

#GUI Generator
root = Tk(className ="Insert queries")
root.title("CSD Update Error DB")
root.geometry('1200x800')
root.configure(background='dark grey')

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

#Insert values in database
def act():

    for i in range(10):

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
skip = Button(buttonsFrame, text="SKIP", font = ("Helvetica",15),command=act, height = 5, width = 10, bg = 'dark grey')
skip.pack(side = 'left')

root.mainloop()
# cursor2.close()
# connection2.close()