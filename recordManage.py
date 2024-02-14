import tkinter as tk
from tkinter import ttk
import customtkinter
import pandas as pd
from CTkMessagebox import CTkMessagebox
import os


def resetAble():
    for widget in win_dow.winfo_children():
        widget.destroy()
    createTable(win_dow)


def searchTable(table, query):
    
    for i in table.get_children():
        table.delete(i)
    df = pd.read_csv('./ImageDataset/facial_encodings_combined.csv')
    for _, row in df.iterrows():
        if query in str(row):
            table.insert("", "end", values=list(row))
            


def PopMenu(event,table):
   

    menu = tk.Menu(table, tearoff=0)
    menu.add_command(label="Delete", command=lambda: deleteRow(table))
    if(table.selection()!=()):
        menu.tk_popup(event.x_root, event.y_root)
    

def deleteRow(table):
    if(table.selection()!=()):
        msg=CTkMessagebox(title="Warning",icon='warning', message="All the Selected Face Encodings will be deleted",option_1="Cancel", option_2="Ok")
        if(msg.get()=='Ok'):    
            dfNew = pd.read_csv('./ImageDataset/facial_encodings_combined.csv')
            for i in table.selection():
                index = table.item(i)['values'][0]
        
                dfNew = dfNew.drop(dfNew[dfNew['ID.'] == index].index, axis=0)
        dfNew.to_csv('./ImageDataset/facial_encodings_combined.csv',index=False)
        resetAble()
    
        
        


    
    

    

def createTable(root):
    # Create a table
    df = pd.read_csv('./ImageDataset/facial_encodings_combined.csv')
    table = ttk.Treeview(root, columns=list(df.columns), show="headings")
    for col in df.columns:
        table.heading(col, text=col)
    for _, row in df.iterrows():
        table.insert("", "end", values=list(row))

    search = tk.Entry(root)
    l1 = customtkinter.CTkLabel(master=root, text="Search", font=("Arial", 14),text_color="white")
    l1.place(relx=0.4, rely=0.02, anchor=tk.CENTER)

    search.place(relx=0.5, rely=0.02, anchor=tk.CENTER)
    search.bind("<KeyRelease>", lambda e: searchTable(table, search.get()))

    table.bind("<Button-3>", lambda e: PopMenu(e,table))


    table.pack(fill="both", expand=True,pady=25)
    


    
        








win_dow = customtkinter.CTk()
win_dow.title("Manage Records")
win_dow.resizable(False, False)
createTable(win_dow)
win_dow.eval('tk::PlaceWindow . center')
win_dow.mainloop()
os.startfile('Homepage.py')