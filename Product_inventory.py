import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
from cryptography.fernet import Fernet
class Product():
    def __init__(self,name,price,quantity,volume):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.volume = volume
        self.table_format = (name,price,quantity,volume,price*quantity,volume*quantity)
    def __str__(self):
        return f"{self.name}_{self.price}_{self.quantity}_{self.volume}<>\\"
class GUI:
    def __init__(self):
        self.frame_count=0
        self.B1 = Backend()
        self.B1.read_file()
        self.B1.find_prod_vol()
        self.root = tk.Tk()
        self.root.geometry("1000x600")
        self.root.title("Product Manager")
        self.menu_frame(False)

        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.root.mainloop()

    def menu_frame(self,logged_in = True):
        if logged_in==False:
            self.login_in()
            return
        
        if self.frame_count==1:
            self.clear_screen(self.add_prod)
        elif self.frame_count==2:
            self.clear_screen(self.insp_inv)
        elif self.frame_count==3:
            self.clear_screen(self.del_prod)
        elif self.frame_count==4:
            self.clear_screen(self.ware_spa)
        elif self.frame_count==5:
            self.clear_screen(self.add_ware)
        elif self.frame_count==6:
            self.clear_screen(self.search_prod)
        elif self.frame_count==7:
            self.clear_screen(self.dis_prod)
        elif self.frame_count==8:
            self.clear_screen(self.srt_by)
        self.menu = tk.Frame(self.root)
        title = tk.Label(self.menu,text = "Menu",font = ("Arial",20))
        title.pack(padx=10,pady=10)

        sub_title = tk.Label(self.menu,text="Welcome to the Product Management System",font = ("Arial",14))
        sub_title.pack(padx=10,pady=10)

        menu_buttons = tk.Frame(self.menu)
        menu_buttons.columnconfigure(0,weight=1)
        menu_buttons.columnconfigure(1,weight=1)

        bt1 = tk.Button(menu_buttons,text="Add Product",font = ("Arial",14),command = self.add_product)
        bt1.grid(row=0,column=0,sticky='ew')
        bt2 = tk.Button(menu_buttons,text="Delete Product",font = ("Arial",14),command= self.delete_product)
        bt2.grid(row=0,column=1,sticky='ew')
        bt3 = tk.Button(menu_buttons,text="Inspect Inventory",font = ("Arial",14),command=self.inspect_inventory)
        bt3.grid(row=1,column=0,sticky='ew')
        bt4 = tk.Button(menu_buttons,text="Warehouse Spacing",font = ("Arial",14),command=self.warehouse_spacing)
        bt4.grid(row=1,column=1,sticky='ew')
        bt5 = tk.Button(menu_buttons,text="Search Product",font = ("Arial",14),command=self.search_product)
        bt5.grid(row=2,column=0,sticky='ew')
        bt5 = tk.Button(menu_buttons,text="Sort By",font = ("Arial",14),command=self.sort_by)
        bt5.grid(row=2,column=1,sticky='ew')

        menu_buttons.pack(pady=150,fill='x')

        self.menu.pack()

        
    
    def add_product(self):
        self.frame_count=1
        self.clear_screen(self.menu)

        self.add_prod = tk.Frame(self.root)
        title = tk.Label(self.add_prod,text = "Add Product",font= ("Arial",20))
        title.grid(row=0,column=0,padx=10,pady=20,sticky='n')

        sub_title = tk.Label(self.add_prod,text="Please enter the fields below to add the product",font=("Arial",14))
        sub_title.grid(row=1,column=0,padx=10,pady=50,sticky='n')

        eb_1_input = StringVar()
        eb_1_txt = tk.Label(self.add_prod,text="Please enter name of the product",font= ("Arial",14))
        eb_1_txt.grid(row=2,column=0,padx=10,pady=10,sticky='w')
        self.eb_1 = tk.Entry(self.add_prod,textvariable=eb_1_input)
        self.eb_1.grid(row=2,column=1,padx=10,pady=10,sticky='e')
        
        
        eb_2_input = StringVar()
        eb_2_txt = tk.Label(self.add_prod,text="Please enter price of the product",font= ("Arial",14))
        eb_2_txt.grid(row=3,column=0,padx=10,pady=10,sticky='w')
        self.eb_2 = tk.Entry(self.add_prod,textvariable=eb_2_input)
        self.eb_2.grid(row=3,column=1,padx=10,pady=10,sticky='e')
        
        eb_3_input = StringVar()
        eb_3_txt = tk.Label(self.add_prod,text="Please enter quantity of the product",font= ("Arial",14))
        eb_3_txt.grid(row=4,column=0,padx=10,pady=10,sticky='w')
        self.eb_3 = tk.Entry(self.add_prod,textvariable=eb_3_input)
        self.eb_3.grid(row=4,column=1,padx=10,pady=10,sticky='e')

        eb_4_input = StringVar()
        eb_4_txt = tk.Label(self.add_prod,text="Please enter volume(in L) of the product",font= ("Arial",14))
        eb_4_txt.grid(row=5,column=0,padx=10,pady=10,sticky='w')
        self.eb_4 = tk.Entry(self.add_prod,textvariable=eb_4_input)
        self.eb_4.grid(row=5,column=1,padx=10,pady=10,sticky='e')


        enter_button = tk.Button(self.add_prod,text="Enter new product information",font=("Arial",14),command=self.enter_new_prod)
        enter_button.grid(row=6,column=0,padx=30,pady=40)

        back_button = tk.Button(self.add_prod,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.grid(row=7,column=0,padx=30)

        self.add_prod.pack()
    def inspect_inventory(self):
        self.frame_count=2
        self.clear_screen(self.menu)

        self.insp_inv = tk.Frame(self.root)
        title = tk.Label(self.insp_inv,text = "Inspect Inventory",font= ("Arial",20))
        title.grid(row=0,column=0,padx=10,pady=20)
        
        scroll_bar = tk.Scrollbar(self.insp_inv,orient="vertical")

        columns = ("Product","Price","Quantity","Volume","Total_Price","Total_Volume")
        table = ttk.Treeview(self.insp_inv,columns=columns,show="headings",yscrollcommand=scroll_bar.set)
        table.heading("Product",text="Product")
        table.heading("Price",text="Price")
        table.heading("Quantity",text="Quantity") 
        table.heading("Volume",text="Volume(in L)")
        table.heading("Total_Price",text="Total Price")
        table.heading("Total_Volume",text="Total Volume(in L)")


        scroll_bar.grid(row=1,column=1,pady=10,sticky='ens')
        scroll_bar.config(command=table.yview)
        
        tt_price=0
        tt_volume=0
        table.column("Product", width=210)  
        table.column("Price", width=118)  
        table.column("Quantity", width=164)  
        table.column("Volume", width=164)  
        table.column("Total_Price", width=164)  
        table.column("Total_Volume", width=164)
        for product in self.B1.products:
            table.insert('',tk.END,values=product.table_format)
            tt_price=tt_price+product.table_format[4]
            tt_volume=tt_volume+product.table_format[5]
        table.grid(row=1,column=0)

        column = ("tt_price_volume"," ","tt_price","tt_volume")
        tt_table = ttk.Treeview(self.insp_inv,columns=column,show="headings",height=0)
        tt_table.heading("tt_price_volume",text="Total Price and Volume")
        tt_table.heading(" ",text="")
        tt_table.heading("tt_price",text=str(tt_price))
        tt_table.heading("tt_volume",text=str(tt_volume))

        tt_table.column("tt_price_volume", width=210)  
        tt_table.column(" ", width=446)    
        tt_table.column("tt_price", width=164)  
        tt_table.column("tt_volume", width=164)
        tt_table.grid(row=2,column=0)

        back_button = tk.Button(self.insp_inv,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.grid(row=3,column=0,padx=10,pady=10)

        self.insp_inv.pack()
    def delete_product(self):
        self.frame_count=3
        self.clear_screen(self.menu)

        self.del_prod = tk.Frame(self.root)
        title = tk.Label(self.del_prod,text="Delete Product",font=('Arial',20))
        title.pack(padx=20,pady=20)
        sub_title = tk.Label(self.del_prod,text="Please enter the exact name of the product",font=('Arial',14))
        sub_title.pack(padx=20,pady=10)

        question = tk.Label(self.del_prod,text="What is the name of the product?",font=('Arial',14))
        question.pack(padx=20,pady=10)
        ans_var = ""
        self.ans = tk.Entry(self.del_prod,textvariable=ans_var)
        self.ans.pack(padx=10,pady=10)

        enter_button = tk.Button(self.del_prod,text="Delete Product",font=('Arial',14),command=self.remove_prod)
        enter_button.pack(padx=10,pady=10)

        back_button = tk.Button(self.del_prod,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.pack(padx=10,pady=10)

        self.del_prod.pack()
    def warehouse_spacing(self):
        self.frame_count=4
        self.clear_screen(self.menu)

        self.ware_spa = tk.Frame(self.root)
        title = tk.Label(self.ware_spa,text="Warehouse Spacing",font=("Arial",20))
        title.pack(padx=10,pady=50)

        lb_1 = tk.Label(self.ware_spa,text=f"The volume of your warehouse = {self.B1.warehouse}L",font=("Arial",14))
        lb_1.pack(padx=10,pady=20)

        if self.B1.warehouse==0:
            self.add_warehouse()

        view_graph = tk.Button(self.ware_spa,text='View Graph',font=("Arial",14),command=self.show_graph)
        view_graph.pack(padx=10,pady=80)
        

        add_ware = tk.Button(self.ware_spa,text="Edit Warehouse",font=('Arial',14),command=self.add_warehouse)
        add_ware.pack(padx=10,pady=10)

        back_button = tk.Button(self.ware_spa,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.pack(padx=10,pady=5)

        self.ware_spa.pack()
    def add_warehouse(self):
        self.frame_count = 5
        self.clear_screen(self.ware_spa)

        self.add_ware = tk.Frame(self.root)
        title = tk.Label(self.add_ware,text="Edit Warehouse",font=("Arial",20))
        title.grid(row=0,column=0,padx=10,pady=10)

        eb_1_input = StringVar()
        eb_1_txt = tk.Label(self.add_ware,text="Please enter volume of the warehouse(in L)",font= ("Arial",14))
        eb_1_txt.grid(row=1,column=0,padx=10,pady=10,sticky='w')
        self.eb_1 = tk.Entry(self.add_ware,textvariable=eb_1_input)
        self.eb_1.grid(row=1,column=1,padx=10,pady=10,sticky='e')

        enter_button = tk.Button(self.add_ware,text="Enter warehouse information",font=("Arial",14),command=self.enter_new_ware)
        enter_button.grid(row=3,column=0,padx=30,pady=50)

        self.add_ware.pack()
    def clear_screen(self,frame):
           frame.destroy()
    def search_product(self):
        self.frame_count = 6
        self.clear_screen(self.menu)

        self.search_prod = tk.Frame(self.root)
        title = tk.Label(self.search_prod,text="Search Product",font=("Arial",20))
        title.pack(padx=10,pady=50)

        question = tk.Label(self.search_prod,text="What is the name of the product?",font=('Arial',14))
        question.pack(padx=20,pady=10)
        prod_name = ''
        self.enter_box = tk.Entry(self.search_prod,textvariable=prod_name)
        self.enter_box.pack(padx=20,pady=10)

        add_ware = tk.Button(self.search_prod,text="Get Product Details",font=('Arial',14),command=self.search_inv)
        add_ware.pack(padx=10,pady=10)

        back_button = tk.Button(self.search_prod,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.pack(padx=10,pady=5)

        self.search_prod.pack()
    def login_in(self):
        self.frame_count = 9

        self.login = tk.Frame(self.root)
        title = tk.Label(self.login,text="Login",font=("Arial",20))
        title.pack(padx=10,pady=50)

        question1 = tk.Label(self.login,text="Username",font=('Arial',14))
        question1.pack(padx=20,pady=10)
        username = ''
        self.enter_box1 = tk.Entry(self.login,textvariable=username)
        self.enter_box1.pack(padx=20,pady=10)

        question2 = tk.Label(self.login,text="Password",font=('Arial',14))
        question2.pack(padx=20,pady=10)
        password = ''
        self.enter_box2 = tk.Entry(self.login,textvariable=password)
        self.enter_box2.pack(padx=20,pady=10)

        login_button = tk.Button(self.login,text="Log in",font=('Arial',14),command=self.check)
        login_button.pack(padx=10,pady=10)


        self.login.pack()
    def display_product(self,prod : Product):
        self.frame_count = 7
        self.clear_screen(self.search_prod)

        self.dis_prod = tk.Frame(self.root)
        title = tk.Label(self.dis_prod,text="Product",font=("Arial",20))
        title.pack(padx=10,pady=50)

        name = tk.Label(self.dis_prod,text=f"Name of Product - {prod.name}",font=('Arial',14))
        name.pack(padx=20,pady=10)
        quantity = tk.Label(self.dis_prod,text=f"Quantity of Product - {prod.quantity}",font=('Arial',14))
        quantity.pack(padx=20,pady=10)
        price = tk.Label(self.dis_prod,text=f"Price of Product - {prod.price}",font=('Arial',14))
        price.pack(padx=20,pady=10)
        volume = tk.Label(self.dis_prod,text=f"Volume of Product - {prod.volume}",font=('Arial',14))
        volume.pack(padx=20,pady=10)


        back_button = tk.Button(self.dis_prod,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.pack(padx=10,pady=5)

        self.dis_prod.pack()
    def sort_by(self):
        self.frame_count = 8
        self.clear_screen(self.menu)

        self.srt_by = tk.Frame(self.root)
        title = tk.Label(self.srt_by,text = "Sort By",font = ("Arial",20))
        title.pack(padx=10,pady=10)

        sub_title = tk.Label(self.srt_by,text="Sort the items by",font = ("Arial",14))
        sub_title.pack(padx=10,pady=10)

        menu_buttons = tk.Frame(self.srt_by)
        menu_buttons.columnconfigure(0,weight=1)
        menu_buttons.columnconfigure(1,weight=1)

        bt1 = tk.Button(menu_buttons,text="Name",font = ("Arial",14),command = self.sb_n)
        bt1.grid(row=0,column=0,sticky='ew')
        bt2 = tk.Button(menu_buttons,text="Price",font = ("Arial",14),command= self.sb_p)
        bt2.grid(row=0,column=1,sticky='ew')
        bt3 = tk.Button(menu_buttons,text="Quantity",font = ("Arial",14),command=self.sb_q)
        bt3.grid(row=1,column=0,sticky='ew')
        bt4 = tk.Button(menu_buttons,text="Volume",font = ("Arial",14),command=self.sb_v)
        bt4.grid(row=1,column=1,sticky='ew')

        menu_buttons.pack(pady=150,fill='x')

        back_button = tk.Button(self.srt_by,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.pack(padx=10,pady=5)

        self.srt_by.pack()
    def enter_new_prod(self):
        if (float(self.eb_3.get())*float(self.eb_4.get()))+self.B1.prod_vol>self.B1.warehouse:
                messagebox.showerror(title='Error',message="You do not have enough space in the warehouse for adding this item")
                self.menu_frame()
                return
        name = self.eb_1.get()
        i = 0
        for prod in self.B1.products:
            if prod.name.lower()==name.lower() and prod.price==float(self.eb_2.get()) and prod.volume==float(self.eb_4.get()):
                self.B1.products[i] = Product(prod.name,prod.price,prod.quantity + float(self.eb_3.get()),prod.volume)
                self.B1.find_prod_vol()
                self.menu_frame()
                messagebox.showinfo(title="Information",message="Similar product found: Quantity updated")
                return
            i+=1
        prod = Product(self.eb_1.get(),float(self.eb_2.get()),float(self.eb_3.get()),float(self.eb_4.get()))
        self.B1.add_prod(prod)
        self.B1.find_prod_vol()
        self.menu_frame()
        messagebox.showinfo(title="Information",message="Product added successfully")
    def remove_prod(self):
        ans = self.ans.get().lower()
        for prod in self.B1.products:
            if ans.lower()==prod.name.lower():
                if messagebox.askyesno(title="Delete Product",message="Are you sure you want to delete this product?"):
                    self.B1.products.remove(prod)
                    self.B1.find_prod_vol()
                    messagebox.showinfo(title="Info",message="Product Removed")
                    self.menu_frame()
                    return
                else:
                    self.menu_frame()
                    return
        messagebox.showerror(title="Error",message="Could not find specified product")
        self.menu_frame()
    def enter_new_ware(self):
        volume = float(self.eb_1.get())
        self.B1.find_prod_vol()
        if volume < self.B1.prod_vol:
            messagebox.showerror(title="Error",message="Your products require a bigger warehouse!")
            self.menu_frame()
            return
        self.B1.warehouse = volume
        self.menu_frame()
    def show_graph(self):
        arr_vol = []
        for prod in self.B1.products:
            arr_vol.append(prod.table_format[5])
        arr_vol.append(self.B1.warehouse-self.B1.prod_vol)
        arr_vol = np.array(arr_vol)

        arr_name = []
        for prod in self.B1.products:
            arr_name.append(prod.name)
        arr_name.append('Empty')

        plt.pie(arr_vol,labels=arr_name,labeldistance=0.7)
        plt.show()
    def search_inv(self):
        prod_name = self.enter_box.get()
        print(prod_name)
        prod = self.B1.find_prod(prod_name)
        if type(prod) !=int:
            self.display_product(prod)

    def on_closing(self):
        if messagebox.askyesno(title="Quit?",message="Do ya wanna quit?"):
            if messagebox.askyesno(title="Save",message="Do you wanna save your work?"):
                self.B1.save_file()
            self.root.destroy()
    def sb_p(self):
        self.B1.sort_by('price')
        self.menu_frame()
        messagebox.showinfo(title="Sorted",message="Your products are successfully sorted!")
    def sb_q(self):
        self.B1.sort_by('quantity')
        self.menu_frame()
        messagebox.showinfo(title="Sorted",message="Your products are successfully sorted!")
    def sb_n(self):
        self.B1.sort_by('name')
        self.menu_frame()
        messagebox.showinfo(title="Sorted",message="Your products are successfully sorted!")
    def sb_v(self):
        self.B1.sort_by('volume')
        self.menu_frame()
        messagebox.showinfo(title="Sorted",message="Your products are successfully sorted!")
    def check(self):
        username = self.enter_box1.get()
        password = self.enter_box2.get()
        try:
            file = open('password.txt','r')
        except (FileNotFoundError):
            file = open('password.txt','a')
            file.close()
            file = open('password.txt','r')
        read_str = file.read()
        f = Fernet('TqthRTNy9yr-kQF4YzmrckCwoJb6KGCvWdn5GKBlejA=')
        read_str = f.decrypt(read_str)
        type(read_str)
        




class Backend():
    def __init__(self):
        self.products = []
        self.warehouse = 0
        self.prod_vol = 0
    def add_prod(self,prod):
        self.products.append(prod)
        for items in self.products:
            print(items)
    def save_file(self):
        file = open('product_info.txt','w')
        save_str =""
        for products in self.products:
            save_str = save_str+str(products)
        save_str = save_str +'\n\n'+'<>\\'+str(self.warehouse)
        file.write(save_str)
        file.close()
    def read_file(self):
        try:
            file = open('product_info.txt','r')
        except (FileNotFoundError):
            file = open('product_info.txt','a')
            file.close()
            file = open('product_info.txt','r')
        read_str = file.read()
        list_prod = read_str.split("<>\\")
        flag= False
        for prod in list_prod:
            list_var_prod = prod.split("_")
            if list_var_prod[0] != '' :
                if "\n\n"==list_var_prod[0]:
                    flag = True
                elif "\n\n"!=list_var_prod[0] and flag==False :
                    P1 = Product(list_var_prod[0],float(list_var_prod[1]),float(list_var_prod[2]),float(list_var_prod[3]))
                    self.products.append(P1)   
                else:
                    self.warehouse = float(prod)        
        file.close()
    def find_prod_vol(self):
        self.prod_vol = 0
        for prod in self.products:
            self.prod_vol = self.prod_vol+prod.table_format[5]
    def find_prod(self,name):
        i = 0
        for prod in self.products:
            print(type(prod))
            if name.lower() == prod.name.lower():
                return self.products[i]
            i+=1
        messagebox.showerror(title='Error',message='No products found')
        return 0


    def sort_by(self,what: str):
        temp = 0
        t = 0
        for i in range(0,len(self.products)-1):
            temp = i
            for j in range(i+1,len(self.products)):
                if getattr(self.products[temp],what) > getattr(self.products[j],what):
                    temp = j
            t = self.products[i]
            self.products[i] = self.products[temp]
            self.products[temp] = t
            



            
            

G1 = GUI()

