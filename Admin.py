from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import StringVar
from tkinter import messagebox
from tkinter import messagebox as ms
import sqlite3, time, datetime, random
from PIL import Image, ImageTk
import os 


name_of_db='MainDb.db'
my_conn = sqlite3.connect(name_of_db)
c = my_conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS Admin (username TEXT NOT NULL PRIMARY KEY,password TEX NOT NULL,fullname TEX, contactNo TEX, HouseNo TEX, street TEX, town TEX, postcode TEX);')
my_conn.commit()
my_conn.close()

 

#Admin user class
    
class User:
    def __init__(self,n_username,n_password,n_fullname,n_contactno):
        self.n_username = n_username
        self.n_password = n_password
        self.n_fullname = n_fullname
        self.n_contactno = n_contactno

#admin adress class
class Address:
    def __init__(self,n_add_HouseNo,n_add_street,n_add_town,n_add_postcode):
        
        self.n_add_HouseNo = n_add_HouseNo
        self.n_add_street = n_add_street
        self.n_add_town = n_add_town
        self.n_add_postcode = n_add_postcode


# view recipe detail function and gui
def viewRecipe():
    fileName= "MainDb.db"

    listOfRecipe=[]
    #recipe class
    class RecipeClass:
        def __init__(self,id, Recipename,discription,cusine,MainIngrendens,taste,meal,ingredients,methodpreparation,date,userid):
            self.__id=id
            self.__Recipename=Recipename
            self.__discription=discription
            self.__cusine=cusine
            self.__MainIngrendens=MainIngrendens
            self.__taste=taste
            self.__meal= meal
            self.__ingredients = ingredients
            self.__methodpreparation=methodpreparation
            self.__date=date
            self.__userid=userid

        def getid(self):
            return self.__id
        def setid(self,id):
            self.__id=id
        def getrecipename(self):
            return self.__Recipename
        def setrecipename(self,Recipename):
            self.__Recipename=Recipename
        def getdiscription(self):
            return self.__discription
        def setdiscription(self,discription):
            self.__discription=discription
        def getcusine(self):
            return self.__cusine
        def setcusine(self,cusine):
            self.__cusine=cusine
        def getMainIngrendens(self):
            return self.__MainIngrendens
        def setMainIngrendens(self,MainIngrendens):
            self.__MainIngrendens=MainIngrendens
        def gettaste(self):
            return self.__taste
        def settaste(self,taste):
            self.__taste=taste
        def getmeal(self):
            return self.__meal
        def setmeal(self,meal):
            self.__meal= meal
        def getingredients(self):
            return self.__ingredients
        def setingredients(self,ingredients):
            self.__ingredients = ingredients
        def getmethodpreparation(self):
            return self.__methodpreparation
        def setmethodpreparation(self,methodpreparation):
            self.__methodpreparation=methodpreparation
        def getdate(self):
            return self.__date
        def setdate(self,date):
            self.__date=date
        def getuserid(self):
            return self.__userid
        def setuserid(self,userid):
            self.__userid=userid
    
    
    #load data function
    def loadData(fileName):
        db=sqlite3.connect(fileName)
        sql="select * from RecipeTab"
        db.row_factory = sqlite3.Row
        rows=db.execute(sql)
        RecipeLists = []
        
        for data in rows:
            RecipeList = RecipeClass(data['id'],data['Recipename'],data['description'],data['cuisine'],data['MainInge'],data['taste'],data['meal'],data['Ingeredient'],data['MethodPrep'],data['date'],data['userid'])
            RecipeLists.append(RecipeList)
        db.close()

        return RecipeLists

    


    #update Tree View of recipe
    def updateTreeView():
        #clear all items in the tree view
        for i in tree1.get_children():
            tree1.delete(i)
        i=0

        for tp in listOfRecipe:
            #bind the iid with the List item index
            tree1.insert("",i,text=tp.getrecipename(),iid=str(i))
            i+=1
        clearTextBoxes()

    def reloadData():
        global listOfRecipe
        listOfRecipe=loadData(fileName)
        updateTreeView()
        messagebox.showinfo("Data Load","Data Loaded!")

    #sort data function
    def sortbycusine():
        form2 = tk.Tk()
        form2.geometry("1200x800") 
        form2.title("Results sort by cuisine" )
        my_conn = sqlite3.connect(name_of_db)
        data_set=my_conn.execute("SELECT * FROM RecipeTab order by cuisine")
        output_data(data_set,form2)

    #sort by meal function
    def sortbyMeal():
        form2 = tk.Tk()
        form2.geometry("1200x800") 
        form2.title("Results sort by Meal" )
        my_conn = sqlite3.connect(name_of_db)
        data_set=my_conn.execute("SELECT * FROM RecipeTab order by meal")
        output_data(data_set,form2)



    def output_data(data_set,form2):
        i=0 # row value inside the loop 
        for recipeV in data_set: 
            for j in range(len(recipeV)):
                e = Entry(form2, width=15, fg='black') 
                e.grid(row=i, column=j) 
                e.insert(END, recipeV[j])
            i=i+1
        return form2

    #search and filter matching recipe
    def filterRecipName():
        #clear treeview items
        for i in tree1.get_children():
            tree1.delete(i)
        i=0
       # searchStr=txtNameFilter.get().upper()
        searchStr=entry1.get().upper()
        print(searchStr)
        

        for tp in listOfRecipe:
            #match substring
            if tp.getrecipename().upper().find(searchStr)>-1:
                #bind the iid with the List item index
                tree1.insert("",i,text=tp.getrecipename(),iid=str(i))
            i+=1
        clearTextBoxes()
        

    def clearTextBoxes():
        #clear text in textboxes
        #txtcusine.set("")

        textcusine.delete(0, END)
        textDate.delete(0, END)
        textDescription.delete(0, END)
        textingredients.delete(1.0, END)
        textMainIngrendens.delete(0, END)
        texttaste.delete(0, END)
        textmeal.delete(0, END)
        textmethodpreparation.delete(1.0, END)
        textuserid.delete(0, END)
        
        
    #update select item in text field
    def selectItem(e):

        curItem = tree1.selection()
        print(curItem[0]) #get the iid
        iid=int(curItem[0])
        print(listOfRecipe[iid].getrecipename())
        textcusine.delete(0, END)
        textDate.delete(0, END)
        textDescription.delete(0, END)
        textingredients.delete(1.0, END)
        textMainIngrendens.delete(0, END)
        texttaste.delete(0, END)
        textmeal.delete(0, END)
        textmethodpreparation.delete(1.0, END)
        textuserid.delete(0, END)

        textcusine.insert(END, listOfRecipe[iid].getcusine())  
        textDate.insert(END, listOfRecipe[iid].getdate())
        textDescription.insert(END, listOfRecipe[iid].getdiscription())
        textingredients.insert(END, listOfRecipe[iid].getingredients())
        textMainIngrendens.insert(END, listOfRecipe[iid].getMainIngrendens())
        texttaste.insert(END, listOfRecipe[iid].gettaste())
        textmeal.insert(END, listOfRecipe[iid].getmeal())
        textmethodpreparation.insert(END, listOfRecipe[iid].getmethodpreparation())
        textuserid.insert(END, listOfRecipe[iid].getuserid())
        #txtuserid.set(listOfRecipe[iid].getuserid())
    


    #view GUI
    window = tk.Tk()
    window.title("view Recipe")
    window.geometry(f"{width_value}x{height_value}+0+0")
    # allow resizing in the x or y direction
    window.resizable(True, True) 
    window.config(bg="#2c3e50")

    labelAppName=ttk.Label(window,text="View Recipes",padding=10)
    labelAppName.config(font=("Courier", 20))
    labelAppName.grid(row=0,column=1,columnspan=3)

    button1=ttk.Button(window,text='Reload Data',command=reloadData)
    button1.grid(row=1,column=1,pady=10)

    txtNameFilter=StringVar()
    entry1=ttk.Entry(window,textvariable=txtNameFilter,font=("Calibri", 16), width=30)
    entry1.grid(row=1,column=2)
    buttonSearch=ttk.Button(window,text='search',command=filterRecipName)
    buttonSearch.grid(row=1,column=3)


    lblsortby = Label(window, text="Sort By", font=("Calibri", 16), bg="#535c68", fg="white")
    lblsortby.grid(row=1, column=5, padx=10, pady=10, sticky="w")

    button2=ttk.Button(window,text='cuisine',command=sortbycusine)
    button2.grid(row=2,column=6,columnspan=3,pady=10)

    button4=ttk.Button(window,text='Meal',command=sortbyMeal)
    button4.grid(row=1,column=7,columnspan=3,pady=10)


    #treeview
    tree1=ttk.Treeview(window)
    tree1.heading("#0",text="Recipes")

    tree1.grid(row=2,column=0,columnspan=2,pady=15)
    tree1.bind('<ButtonRelease-1>', selectItem)

   
    labelDescription=ttk.Label(window,text="Description",padding=2)
    labelDescription.grid(row=3,column=1,sticky=tk.W)
    txtDescription=StringVar()
    textDescription=ttk.Entry(window,textvariable=txtDescription,width=50)
    textDescription.grid(row=3,column=2,pady=5,padx=10)

    labelcusine=ttk.Label(window,text="cuisine",padding=2)
    labelcusine.grid(row=3,column=3,sticky=tk.W)
    txtcusine=StringVar()
    textcusine=ttk.Entry(window,textvariable=txtcusine,width=50)
    textcusine.grid(row=3,column=4,pady=5,padx=10)

    labelMainIngrendens=ttk.Label(window,text="Main Ingrendens",padding=2)
    labelMainIngrendens.grid(row=4,column=1,sticky=tk.W)
    txtMainIngrendens=StringVar()
    textMainIngrendens=ttk.Entry(window,textvariable=txtMainIngrendens,width=50)
    textMainIngrendens.grid(row=4,column=2,pady=5)

    labeltaste=ttk.Label(window,text="Taste",padding=2)
    labeltaste.grid(row=4,column=3,sticky=tk.W)
    txttaste=StringVar()
    texttaste=ttk.Entry(window,textvariable=txttaste,width=50)
    texttaste.grid(row=4,column=4,pady=5)

    labelmeal=ttk.Label(window,text="Meal",padding=2)
    labelmeal.grid(row=5,column=1,sticky=tk.W)
    txtmeal=StringVar()
    textmeal=ttk.Entry(window,textvariable=txtmeal,width=50)
    textmeal.grid(row=5,column=2,pady=5)

    
    labeDate=ttk.Label(window,text="Date",padding=2)
    labeDate.grid(row=5,column=3,sticky=tk.W)
    txtdate=StringVar()
    textDate=ttk.Entry(window,textvariable=txtdate,width=50)
    textDate.grid(row=5,column=4,pady=5)

    labeluserid=ttk.Label(window,text="Recipe owner",padding=2)
    labeluserid.grid(row=6,column=1,sticky=tk.W)
    txtuserid=StringVar()
    textuserid=ttk.Entry(window,textvariable=txtuserid,width=50)
    textuserid.grid(row=6,column=2,pady=5)

    txtingredients=StringVar()
    labelingredients = Label(window, text="Ingredients")
    labelingredients.grid(row=7, column=1, pady=10, sticky="w")
    textingredients = Text(window,  width=60, height=5, font=("Calibri", 12))
    textingredients.grid(row=7, column=2, columnspan=4, padx=10,pady=10, sticky="w")

    txtmethodpreparation=StringVar()
    labemethodpreparation = Label(window, text="Method of prearation")
    labemethodpreparation.grid(row=8, column=1,  pady=10, sticky="w")
    textmethodpreparation = Text(window,  width=60, height=5, font=("Calibri", 12))
    textmethodpreparation.grid(row=8, column=2, columnspan=4, padx=10,pady=10, sticky="w")




    listOfRecipe=loadData(fileName)

    updateTreeView()

    window.mainloop() 



#manage admin recipe function
def myRecipeManage():
    
    root = Tk()
    root.title("My Recipe Management")
    root.geometry("1920x1080+0+0")
    root.config(bg="#2c3e50")
    root.state("zoomed")

    name_of_db='MainDb.db'
    my_conn = sqlite3.connect(name_of_db)
    cdb = my_conn.cursor()

#create recipe table
    def create_recipetable():
        cdb.execute('CREATE TABLE IF NOT EXISTS RecipeTab( id Integer Primary Key, Recipename text,description text,cuisine text,MainInge text, taste text, meal text, Ingeredient text,MethodPrep text,date text, userid text )')
        
    create_recipetable()

    
    tasteEn = StringVar()
    cuisineEn = StringVar()
    Description = StringVar()
    Main_Ingrendens = StringVar()
    type_of_meal= StringVar()
    currtime = time.time()
    date = datetime.datetime.fromtimestamp(currtime).strftime('%c')

  
    
    # Entries Frame
    entries_frame = Frame(root, bg="#535c68")
    entries_frame.pack(side=TOP, fill=X)
    title = Label(entries_frame, text="Manage Recipe", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
    title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

    lblName = Label(entries_frame, text="Recipe Name", font=("Calibri", 16), bg="#535c68", fg="white")
    lblName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    Recipname = StringVar()
    txtName = Entry(entries_frame, textvariable=Recipname, font=("Calibri", 16), width=30)
    txtName.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    lblDescription = Label(entries_frame, text="Description", font=("Calibri", 16), bg="#535c68", fg="white")
    lblDescription.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    txtDescription = Entry(entries_frame, textvariable=Description, font=("Calibri", 16), width=30)
    txtDescription.grid(row=1, column=3, padx=10, pady=10, sticky="w")

    lblCuisine = Label(entries_frame, text="Type of Cuisine", font=("Calibri", 16), bg="#535c68", fg="white")
    lblCuisine.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    comboCuisine = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=cuisineEn)
    comboCuisine['values'] = ("British cuisine","italian cuisine", "chinees cuisine","South Indian cuisine","North indian cuisine","Korean cuisine")
    comboCuisine.grid(row=2, column=1, padx=10, sticky="w")

    lblmeal = Label(entries_frame, text="Type of meal", font=("Calibri", 16), bg="#535c68", fg="white")
    lblmeal.grid(row=2, column=2, padx=10, pady=10, sticky="w")
    combomeal = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=type_of_meal)
    combomeal['values'] = ("Breakfast", "Lunch","Dinner","Dessert","Snack","Beverage")
    combomeal.grid(row=2, column=3, padx=10, sticky="w")

    lblTaste = Label(entries_frame, text="Type of Taste", font=("Calibri", 16), bg="#535c68", fg="white")
    lblTaste.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    comboTaste = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=tasteEn)
    comboTaste['values'] = ("spicy","sweet", "solty","sour","cool","hot","savory")
    comboTaste.grid(row=3, column=1, padx=10, sticky="w")

    lblMainIng = Label(entries_frame, text="Main Ingredients ", font=("Calibri", 16), bg="#535c68", fg="white")
    lblMainIng.grid(row=3, column=2, padx=10, pady=10, sticky="w")
    comboMainIng = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=Main_Ingrendens)
    comboMainIng['values'] = ("Meat/Protein","Chicken","Fish","Pasta","Dairy","Eggs","Rice","Vegetables","Beans","Fruits")
    comboMainIng.grid(row=3, column=3, padx=10, sticky="w")


    lblIngredients = Label(entries_frame, text="Ingredients", font=("Calibri", 16), bg="#535c68", fg="white")
    lblIngredients.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    txtIngredients = Text(entries_frame,  width=60, height=5, font=("Calibri", 12))
    txtIngredients.grid(row=5, column=0, columnspan=4, padx=10, sticky="w")

    lblMethodPrep = Label(entries_frame, text="Method of prearation", font=("Calibri", 16), bg="#535c68", fg="white")
    lblMethodPrep.grid(row=4, column=2, padx=10, pady=10, sticky="w")
    txtMethodPrep = Text(entries_frame,  width=60, height=5, font=("Calibri", 12))
    txtMethodPrep.grid(row=5, column=2, columnspan=4, padx=10, sticky="w")

    def getData(event):
        selected_row = tv.focus()
        data = tv.item(selected_row)
        global row
        row = data["values"]
        print(row)

        #Recipname.set(row[1])
        #Description.set(row[2])
        txtName.delete(0, END)
        txtName.insert(END, row[1])
        txtDescription.delete(0, END)
        txtDescription.insert(END, row[2])
        comboCuisine.delete(0, END)
        comboCuisine.insert(END, row[3])
        comboMainIng.delete(0, END)
        comboMainIng.insert(END, row[4])
        comboTaste.delete(0, END)
        comboTaste.insert(END, row[5])
        combomeal.delete(0, END)
        combomeal.insert(END, row[6])
        txtIngredients.delete(1.0, END)
        txtIngredients.insert(END, row[7])
        txtMethodPrep.delete(1.0, END)
        txtMethodPrep.insert(END, row[8])

        print(Recipname.get())

    def fetch():
        with my_conn:
            cdb.execute("SELECT * from RecipeTab WHERE userid=?", (userId,))
            rows = cdb.fetchall()
            # print(rows)
            return rows

    def dispalyAll():
        tv.delete(*tv.get_children())
        for row in fetch():
            tv.insert("", END, values=row)


    def add_Recipe():

        if txtName.get() == "" or txtDescription.get() == "" or comboCuisine.get() == "" or comboMainIng.get() == "" or comboTaste.get() == "" or combomeal.get() == "" or txtIngredients.get(1.0, END) == "" or txtMethodPrep.get(1.0, END) == "":       
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
        else: 
            with my_conn:
                cdb.execute("insert into RecipeTab(Recipename ,description ,cuisine ,MainInge , taste , meal , Ingeredient ,MethodPrep ,date , userid ) values (?,?,?,?,?,?,?,?,?,?)",
                         (txtName.get(), txtDescription.get() , comboCuisine.get() , comboMainIng.get() , comboTaste.get() , combomeal.get() , txtIngredients.get(1.0, END), txtMethodPrep.get(1.0, END),date,userId))
                my_conn.commit()
            messagebox.showinfo("Success", "Record Inserted")
        clearAll()
        dispalyAll()

 

    def update_recipe():
        if txtName.get() == "" or txtDescription.get() == "" or comboCuisine.get() == "" or comboMainIng.get() == "" or comboTaste.get() == "" or combomeal.get() == "" or txtIngredients.get(1.0, END) == "" or txtMethodPrep.get(1.0, END) == "":       
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
        else: 
            with my_conn:
                cdb.execute("update RecipeTab set Recipename=? ,description=? ,cuisine=? ,MainInge=? , taste=? , meal=? , Ingeredient=? ,MethodPrep=? ,date=? , userid=? where id=?",
                         (txtName.get(), txtDescription.get() , comboCuisine.get() , comboMainIng.get() , comboTaste.get() , combomeal.get() , txtIngredients.get(1.0, END), txtMethodPrep.get(1.0, END),date,userId,row[0]))
                my_conn.commit()
            messagebox.showinfo("Success", "Record Updated")
        clearAll()
        dispalyAll()




    def delete_recipe():
        with my_conn:
            cdb.execute("delete from RecipeTab where id=?", (row[0],))
            my_conn.commit()      
        clearAll()
        dispalyAll()

    def cancel_Manage():
        root.destroy()

    def clearAll():
        #firstEntry.delete(0, END)
        txtName.delete(0, END)     
        txtDescription.delete(0, END)
        comboCuisine.delete(0, END) 
        comboMainIng.delete(0, END)
        comboTaste.delete(0, END)
        combomeal.delete(0, END)
        txtIngredients.delete(1.0, END)
        txtMethodPrep.delete(1.0, END)
       


    btn_frame = Frame(entries_frame, bg="#535c68")
    btn_frame.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="w")
    btnAdd = Button(btn_frame, command=add_Recipe, text="Add Details", width=15, font=("Calibri", 16, "bold"), fg="white",
                    bg="#16a085", bd=0).grid(row=0, column=0)
    btnEdit = Button(btn_frame, command=update_recipe, text="Update Details", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#2980b9",
                    bd=0).grid(row=0, column=1, padx=10)
    btnDelete = Button(btn_frame, command=delete_recipe, text="Delete Details", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#c0392b",
                    bd=0).grid(row=0, column=2, padx=10)
    btnCancel = Button(btn_frame, command=cancel_Manage, text="Cancel", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#c0392b",
                    bd=0).grid(row=0, column=3, padx=10)
    
    

    # Table Frame
    tree_frame = Frame(root, bg="#ecf0f1")
    tree_frame.place(x=0, y=480, width=1980, height=400)
    style = ttk.Style()
    style.configure("mystyle.Treeview", font=('Calibri', 18),
                    rowheight=50)  # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))  # Modify the font of the headings
    tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13), style="mystyle.Treeview")
    tv.column("1", width=1)
    tv.heading("1", text="ID")
    tv.column("2", width=2)
    tv.heading("2", text="Recip Name")
    tv.column("3", width=2)
    tv.heading("3", text="Description")
    tv.column("4", width=2)
    tv.heading("4", text="Cusine")
    tv.column("5", width=2)
    tv.heading("5", text="Main Ing")
    tv.column("6", width=2)
    tv.heading("6", text="Taste")
    tv.column("7", width=2)
    tv.heading("7", text="Meal")
    tv.column("8", width=2)
    tv.heading("8", text="Ingeredient")
    tv.column("9", width=2)
    tv.heading("9", text="Method Prep")
    tv.column("10", width=2)
    tv.heading("10", text="Date")
    tv.column("11", width=10)
    tv.heading("11", text="userid")
    tv['show'] = 'headings'
    tv.bind("<ButtonRelease-1>", getData)
    tv.pack(fill=X)

    dispalyAll()
    root.mainloop()



def AlluserRecipeManage():
    
    root = Tk()
    root.title("My Recipe Management")
    root.geometry("1920x1080+0+0")
    root.config(bg="#2c3e50")
    root.state("zoomed")

    name_of_db='MainDb.db'
    my_conn = sqlite3.connect(name_of_db)
    cdb = my_conn.cursor()


    def create_recipetable():
        cdb.execute('CREATE TABLE IF NOT EXISTS RecipeTab( id Integer Primary Key, Recipename text,description text,cuisine text,MainInge text, taste text, meal text, Ingeredient text,MethodPrep text,date text, userid text )')
        
    create_recipetable()

    
    tasteEn = StringVar()
    cuisineEn = StringVar()
    Description = StringVar()
    Main_Ingrendens = StringVar()
    type_of_meal= StringVar()
    currtime = time.time()
    date = datetime.datetime.fromtimestamp(currtime).strftime('%c')

  
    
    # Entries Frame
    entries_frame = Frame(root, bg="#535c68")
    entries_frame.pack(side=TOP, fill=X)
    title = Label(entries_frame, text="Manage Recipe", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
    title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

    lblName = Label(entries_frame, text="Recipe Name", font=("Calibri", 16), bg="#535c68", fg="white")
    lblName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    Recipname = StringVar()
    txtName = Entry(entries_frame, textvariable=Recipname, font=("Calibri", 16), width=30)
    txtName.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    lblDescription = Label(entries_frame, text="Description", font=("Calibri", 16), bg="#535c68", fg="white")
    lblDescription.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    txtDescription = Entry(entries_frame, textvariable=Description, font=("Calibri", 16), width=30)
    txtDescription.grid(row=1, column=3, padx=10, pady=10, sticky="w")

    lblCuisine = Label(entries_frame, text="Type of Cuisine", font=("Calibri", 16), bg="#535c68", fg="white")
    lblCuisine.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    comboCuisine = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=cuisineEn)
    comboCuisine['values'] = ("British cuisine","italian cuisine", "chinees cuisine","South Indian cuisine","North indian cuisine","Korean cuisine")
    comboCuisine.grid(row=2, column=1, padx=10, sticky="w")

    lblmeal = Label(entries_frame, text="Type of meal", font=("Calibri", 16), bg="#535c68", fg="white")
    lblmeal.grid(row=2, column=2, padx=10, pady=10, sticky="w")
    combomeal = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=type_of_meal)
    combomeal['values'] = ("Breakfast", "Lunch","Dinner","Dessert","Snack","Beverage")
    combomeal.grid(row=2, column=3, padx=10, sticky="w")

    lblTaste = Label(entries_frame, text="Type of Taste", font=("Calibri", 16), bg="#535c68", fg="white")
    lblTaste.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    comboTaste = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=tasteEn)
    comboTaste['values'] = ("spicy","sweet", "solty","sour","cool","hot","savory")
    comboTaste.grid(row=3, column=1, padx=10, sticky="w")

    lblMainIng = Label(entries_frame, text="Main Ingredients", font=("Calibri", 16), bg="#535c68", fg="white")
    lblMainIng.grid(row=3, column=2, padx=10, pady=10, sticky="w")
    comboMainIng = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=Main_Ingrendens)
    comboMainIng['values'] = ("Meat/Protein","Chicken","Fish","Pasta","Dairy","Eggs","Rice","Vegetables","Beans","Fruits")
    comboMainIng.grid(row=3, column=3, padx=10, sticky="w")


    lblIngredients = Label(entries_frame, text="Ingredients", font=("Calibri", 16), bg="#535c68", fg="white")
    lblIngredients.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    txtIngredients = Text(entries_frame,  width=60, height=5, font=("Calibri", 12))
    txtIngredients.grid(row=5, column=0, columnspan=4, padx=10, sticky="w")

    lblMethodPrep = Label(entries_frame, text="Method of prearation", font=("Calibri", 16), bg="#535c68", fg="white")
    lblMethodPrep.grid(row=4, column=2, padx=10, pady=10, sticky="w")
    txtMethodPrep = Text(entries_frame,  width=60, height=5, font=("Calibri", 12))
    txtMethodPrep.grid(row=5, column=2, columnspan=4, padx=10, sticky="w")

    def getData(event):
        selected_row = tv.focus()
        data = tv.item(selected_row)
        global row
        row = data["values"]
        print(row)

        #Recipname.set(row[1])
        #Description.set(row[2])
        txtName.delete(0, END)
        txtName.insert(END, row[1])
        txtDescription.delete(0, END)
        txtDescription.insert(END, row[2])
        comboCuisine.delete(0, END)
        comboCuisine.insert(END, row[3])
        comboMainIng.delete(0, END)
        comboMainIng.insert(END, row[4])
        comboTaste.delete(0, END)
        comboTaste.insert(END, row[5])
        combomeal.delete(0, END)
        combomeal.insert(END, row[6])
        txtIngredients.delete(1.0, END)
        txtIngredients.insert(END, row[7])
        txtMethodPrep.delete(1.0, END)
        txtMethodPrep.insert(END, row[8])

        print(Recipname.get())

    def fetch():
        with my_conn:
            cdb.execute("SELECT * from RecipeTab ")
            rows = cdb.fetchall()
            # print(rows)
            return rows

    def dispalyAll():
        tv.delete(*tv.get_children())
        for row in fetch():
            tv.insert("", END, values=row)




    def delete_recipe():
        with my_conn:
            cdb.execute("delete from RecipeTab where id=?", (row[0],))
            my_conn.commit()      
        clearAll()
        dispalyAll()

    def cancel_Manage():
        root.destroy()

    def clearAll():
        #firstEntry.delete(0, END)
        txtName.delete(0, END)     
        txtDescription.delete(0, END)
        comboCuisine.delete(0, END) 
        comboMainIng.delete(0, END)
        comboTaste.delete(0, END)
        combomeal.delete(0, END)
        txtIngredients.delete(1.0, END)
        txtMethodPrep.delete(1.0, END)
       


    btn_frame = Frame(entries_frame, bg="#535c68")
    btn_frame.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="w")

    btnDelete = Button(btn_frame, command=delete_recipe, text="Delete Details", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#c0392b",
                    bd=0).grid(row=0, column=2, padx=10)
    btnCancel = Button(btn_frame, command=cancel_Manage, text="Cancel", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#c0392b",
                    bd=0).grid(row=0, column=3, padx=10)
    
    

    # Table Frame
    tree_frame = Frame(root, bg="#ecf0f1")
    tree_frame.place(x=0, y=480, width=1980, height=400)
    style = ttk.Style()
    style.configure("mystyle.Treeview", font=('Calibri', 18),
                    rowheight=50)  # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))  # Modify the font of the headings
    tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13), style="mystyle.Treeview")
    tv.column("1", width=1)
    tv.heading("1", text="ID")
    tv.column("2", width=2)
    tv.heading("2", text="Recip Name")
    tv.column("3", width=2)
    tv.heading("3", text="Description")
    tv.column("4", width=2)
    tv.heading("4", text="Cusine")
    tv.column("5", width=2)
    tv.heading("5", text="Main Ing")
    tv.column("6", width=2)
    tv.heading("6", text="Taste")
    tv.column("7", width=2)
    tv.heading("7", text="Meal")
    tv.column("8", width=2)
    tv.heading("8", text="Ingeredient")
    tv.column("9", width=2)
    tv.heading("9", text="Method Prep")
    tv.column("10", width=2)
    tv.heading("10", text="Date")
    tv.column("11", width=10)
    tv.heading("11", text="userid")
    tv['show'] = 'headings'
    tv.bind("<ButtonRelease-1>", getData)
    tv.pack(fill=X)

    dispalyAll()
    root.mainloop()


#manage ALL user function
def Manage_User():

    root = Tk()
    root.title("User Management")
    root.geometry("1920x1080+0+0")
    root.config(bg="#2c3e50")
    root.state("zoomed")

    name_of_db='MainDb.db'
    my_conn = sqlite3.connect(name_of_db)
    cdb = my_conn.cursor()


    def create_user():
        cdb.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEX NOT NULL,fullname TEX, contactNo TEX, HouseNo TEX, street TEX, town TEX, postcode TEX);')
        
    create_user()

    
    uUserId = StringVar()
    uFullName = StringVar()
    uHouseNo = StringVar()
    ucontactno = StringVar()
    uPostcode= StringVar()
    ustreet = StringVar()
    uTown = StringVar()
    


    
    entries_frame = Frame(root, bg="#535c68")
    entries_frame.pack(side=TOP, fill=X)
    title = Label(entries_frame, text="User Management", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
    title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

    lblUserId = Label(entries_frame, text="User Id", font=("Calibri", 16), bg="#535c68", fg="white")
    lblUserId.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    txtUserId = Entry(entries_frame, textvariable=uUserId, font=("Calibri", 16), width=30)
    txtUserId.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    lblFullName = Label(entries_frame, text="Full Name", font=("Calibri", 16), bg="#535c68", fg="white")
    lblFullName.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    txtFullName = Entry(entries_frame, textvariable=uFullName, font=("Calibri", 16), width=30)
    txtFullName.grid(row=1, column=3, padx=10, pady=10, sticky="w")


    lblContact = Label(entries_frame, text="Contact No", font=("Calibri", 16), bg="#535c68", fg="white")
    lblContact.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    txtContact = Entry(entries_frame, textvariable=ucontactno, font=("Calibri", 16), width=30)
    txtContact.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    lblHouseNo = Label(entries_frame, text="House No", font=("Calibri", 16), bg="#535c68", fg="white")
    lblHouseNo.grid(row=2, column=2, padx=10, pady=10, sticky="w")
    txtHouseNo = Entry(entries_frame, textvariable=uHouseNo, font=("Calibri", 16), width=30)
    txtHouseNo.grid(row=2, column=3, padx=10, pady=10, sticky="w")

    lblStreet = Label(entries_frame, text="Street", font=("Calibri", 16), bg="#535c68", fg="white")
    lblStreet.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    txtStreet = Entry(entries_frame, textvariable=ustreet, font=("Calibri", 16), width=30)
    txtStreet.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    lblTown = Label(entries_frame, text="Town", font=("Calibri", 16), bg="#535c68", fg="white")
    lblTown.grid(row=3, column=2, padx=10, pady=10, sticky="w")
    txtTown = Entry(entries_frame, textvariable=uTown, font=("Calibri", 16), width=30)
    txtTown.grid(row=3, column=3, padx=10, pady=10, sticky="w")

    lblPostcode = Label(entries_frame, text="Postcode", font=("Calibri", 16), bg="#535c68", fg="white")
    lblPostcode.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    txtPostcode = Entry(entries_frame, textvariable=uPostcode, font=("Calibri", 16), width=30)
    txtPostcode.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    def getData(event):
        selected_row = tv.focus()
        data = tv.item(selected_row)
        global row
        row = data["values"]
        print(row)

        #Recipname.set(row[1])
        #Description.set(row[2])
        txtUserId.delete(0, END)
        txtUserId.insert(END, row[0])
        txtFullName.delete(0, END)
        txtFullName.insert(END, row[1])
        txtContact.delete(0, END)
        txtContact.insert(END, row[2])
        txtHouseNo.delete(0, END)
        txtHouseNo.insert(END, row[3])
        txtStreet.delete(0, END)
        txtStreet.insert(END, row[4])
        txtTown.delete(0, END)
        txtTown.insert(END, row[5])
        txtPostcode.delete(0, END)
        txtPostcode.insert(END, row[6])
    

        

    def fetch():
        with my_conn:
            cdb.execute("SELECT username,fullname, contactNo, HouseNo, street, town, postcode from user ")
            rows = cdb.fetchall()
            # print(rows)
            return rows

    def dispalyAll():
        tv.delete(*tv.get_children())
        for row in fetch():
            tv.insert("", END, values=row)




    def delete_recipe():
        with my_conn:
            cdb.execute("delete from user where username=?", (row[0],))
            my_conn.commit()      
        clearAll()
        dispalyAll()



    def cancel_Manage():
        root.destroy()

    def clearAll():
        #firstEntry.delete(0, END)
        txtUserId.delete(0, END)
        
        txtFullName.delete(0, END)
        
        txtContact.delete(0, END)
        
        txtHouseNo.delete(0, END)
        
        txtStreet.delete(0, END)
      
        txtTown.delete(0, END)
        
        txtPostcode.delete(0, END)
       
       


    btn_frame = Frame(entries_frame, bg="#535c68")
    btn_frame.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="w")

    btnDelete = Button(btn_frame, command=delete_recipe, text="Delete Details", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#c0392b",
                    bd=0).grid(row=0, column=2, padx=10)
    btnCancel = Button(btn_frame, command=cancel_Manage, text="Cancel", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#c0392b",
                    bd=0).grid(row=0, column=3, padx=10)
    
    

    # Table Frame
    tree_frame = Frame(root, bg="#ecf0f1")
    tree_frame.place(x=0, y=480, width=1980, height=400)
    style = ttk.Style()
    style.configure("mystyle.Treeview", font=('Calibri', 18),
                    rowheight=50)  # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))  # Modify the font of the headings
    tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7,8,9), style="mystyle.Treeview")
    tv.column("1", width=1)
    tv.heading("1", text="userid")
    tv.column("2", width=2)
    tv.heading("2", text="Full Name")
    tv.heading("3", text="Full Name")
    tv.column("3", width=2)
    tv.heading("3", text="Phone no")
    tv.column("4", width=2)
    tv.heading("4", text="House no")
    tv.column("5", width=2)
    tv.heading("5", text="Street")
    tv.column("6", width=2)
    tv.heading("6", text="Town")
    tv.column("7", width=2)
    tv.heading("7", text="Post Code")
    
    
    tv['show'] = 'headings'
    tv.bind("<ButtonRelease-1>", getData)
    tv.pack(fill=X)

    dispalyAll()
    root.mainloop()




#main Class
class main:
    def __init__(self,master):
    	# Window 
        self.master = master
        # Some Usefull variables
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.n_fullname = StringVar()
        self.n_contactno = StringVar()
        self.n_add_HouseNo = StringVar()
        self.n_add_street = StringVar()
        self.n_add_town = StringVar()
        self.n_add_postcode = StringVar()
        
        #Create Widgets
        self.widgets()



    #Login Function
    def login(self):
    	#Establish Connection
        
        my_conn = sqlite3.connect(name_of_db)
        c = my_conn.cursor()

        #Find user If there is any take proper action
        find_user = ('SELECT * FROM Admin WHERE username = ? and password = ?' )
        c.execute(find_user,[(self.username.get()),(self.password.get())])
        result = c.fetchall()
        if result:
            global userId   
            userId =self.username.get()        
            ms.showinfo('Success!','Account login!')
            self.windo()
            
            

        else:
            ms.showerror('Oops!','something wrong.')
            
    def new_user(self):
    	#connect the db
        
        my_conn = sqlite3.connect(name_of_db)
        c = my_conn.cursor()
        if self.n_username == "" or self.n_password == "" :           
            ms.showerror('Error!','Please complete the required field!')
        else:
            #Find Existing username if any take proper action
            find_user = ('SELECT username FROM Admin WHERE username = ?')
            c.execute(find_user,[(self.n_username.get())])        
            if c.fetchall():
                ms.showerror('Error!','Admin Username Taken Try a Diffrent One.')
            else:
                ms.showinfo('Success!','Account Created!')
                
                self.log()
        #Create New Account 
            insert = 'INSERT INTO Admin(username,password,fullname ,contactNo ,HouseNo ,street , town , postcode) VALUES(?,?,?,?,?,?,?,?)'
            c.execute(insert,[(self.n_username.get()),(self.n_password.get()),(self.n_fullname.get()),(self.n_contactno.get()),(self.n_add_HouseNo.get()),(self.n_add_street.get()),(self.n_add_town.get()),(self.n_add_postcode.get())])        
            ('SELECT * FROM Admin WHERE username = ? and password = ? and fullname = ? and contactNo = ? and HouseNo = ? and street = ? and town = ? and postcode = ?')
         
            my_conn.commit()

        #Frame Packing Methords
    def log(self):
        self.username.set('')
        self.password.set('')
        self.windof.pack_forget()
        self.crf.pack_forget()
        self.head['text'] = 'ADMIN LOGIN'
        self.logf.pack()


    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.n_add_HouseNo.set('')
        self.n_add_postcode.set('')
        self.n_add_street.set('')
        self.n_contactno.set('')
        self.n_fullname.set('')
        self.n_add_town.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Admin Create Account'
        self.crf.pack()

    def windo(self):         
        self.logf.pack_forget()           
        self.head['text'] = ''
        self.windof.pack() 
 

    #Draw Widgets
    def widgets(self):
        self.head = Label(self.master,text = 'Wellcome to CookMe Admin !',font = ('',35),bg="#2c3e50", fg="white")     
        self.head.pack()
        self.logf = Frame(self.master,bg="#2c3e50")
        
        load = Image.open("home.jpg")
        render = ImageTk.PhotoImage(load)
        img = Label(self.logf, image=render)
        img.image = render
        img.place(x=0, y=0) 

        self.logf.pack(side=TOP, fill=X)
        title = Label(self.logf, text="Admin Login",bg="#89A9FF", fg="white", font=("Calibri", 30, "bold"))
        title.grid(row=0,column=2, columnspan=2,  pady=20, sticky="w")

        Button(self.logf, command=viewRecipe, text="View Recipe", width=22, font=("Calibri", 16, "bold"),
                    fg="white", bg="#c0392b",bd=0).grid(row=2, column=0, padx=250)
        Label(self.logf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(row=1,column=2,padx=10)
        Entry(self.logf,textvariable = self.username,bd = 5,font = ('',15)).grid(row=1,column=3,padx=10)
        Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(row=2,column=2)
        Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=2,column=3)
        Button(self.logf, command=self.login, text=' Login ', width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#008000",bd=0).grid(row=3,column=3, padx=10,pady=10)
        Button(self.logf, command=self.cr, text='Create Account', width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#008000",bd=0).grid(row=5,column=3, padx=10,pady=10)
        lblName1 = Label(self.logf, text="@Mythi ltd.", font=("Calibri", 9), bg= None, fg="white")
        lblName1.grid(row=6, column=3, padx=60, pady=150, sticky="w")
        
        self.logf.pack()
        
        


        self.crf = Frame(self.master,padx =10,pady = 10)
        
        Label(self.crf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.crf,text = 'Full Name: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_fullname,bd = 5,font = ('',15)).grid(row=1,column=1)
        Label(self.crf,text = 'Contact No: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_contactno,bd = 5,font = ('',15)).grid(row=2,column=1)
        Label(self.crf,text = 'Address:  ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Label(self.crf,text = 'House No:  ',font = ('',15),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_add_HouseNo,bd = 5,font = ('',15)).grid(row=4,column=1)
        Label(self.crf,text = 'Street :   ',font = ('',15),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_add_street,bd = 5,font = ('',15)).grid(row=5,column=1)
        Label(self.crf,text = 'Town:    ',font = ('',15),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_add_town,bd = 5,font = ('',15)).grid(row=6,column=1)
        Label(self.crf,text = 'Post Code: ',font = ('',15),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_add_postcode,bd = 5,font = ('',15)).grid(row=7,column=1)
        Label(self.crf,text = 'Password:  ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=8,column=1)
    
        Button(self.crf, command=self.new_user, text='Create Account', width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#008000",bd=0).grid(padx=10,pady=10)
        Label(self.crf,text = 'Already have Account ',font = ('',10),pady=5,padx=5).grid(sticky = W)
        Button(self.crf, command=self.log, text='Go to Login', width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#008000",bd=0).grid(padx=10,pady=10)


        self.windof = Frame(self.master) 
        load1 = Image.open("home.jpg")
        render = ImageTk.PhotoImage(load1)
        img1 = Label(self.windof, image=render)
        img1.image = render
        img1.place(x=0, y=0) 

        Label(self.windof,text = 'Admin Home Page',font = ("Calibri", 26, "bold"),bg="#89A9FF", fg="white").grid(row=0,column=0)
        Button(self.windof, command=AlluserRecipeManage, text='Manage All User Recipe', width=25, font=("Calibri", 16, "bold"),
                    fg="white", bg="#008000",bd=0).grid(row=1,column=1,padx=10,pady=20)
        Button(self.windof, command=myRecipeManage, text='Manage My Recipe', width=25, font=("Calibri", 16, "bold"),
                    fg="white", bg="#008000",bd=0).grid(row=2,column=1,padx=10,pady=20)
        Button(self.windof, command=viewRecipe, text='View All Recipes', width=25, font=("Calibri", 16, "bold"),
                    fg="white", bg="#008000",bd=0).grid(row=4,column=1,padx=10,pady=20)
        Button(self.windof, command=Manage_User, text='Manage User', width=25, font=("Calibri", 16, "bold"),
                    fg="white", bg="#008000",bd=0).grid(row=3,column=1,padx=10,pady=20)

        Label(self.windof,text = 'Enjoy Cooking with CookMe ! ',font = ("Calibri", 15, "bold"),bg="#89A9FF", fg="white").grid(row=5,column=1,padx=50,pady=80)
          
        Button(self.windof, command=self.log, text='Logout', width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="red",bd=0).grid(row=0,column=3,padx=10,pady=20)
        
        
        

mainroot = Tk()
width_value = mainroot.winfo_screenwidth()
height_value = mainroot.winfo_screenheight()
mainroot.geometry(f"{width_value}x{height_value}+0+0")
mainroot.resizable(True, True)
mainroot.title("Cook Me Admin")
mainroot.config(bg="#2c3e50")
main(mainroot)
mainroot.mainloop()


    
