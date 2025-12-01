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
        # visual theme vars (added)
        self.bg_color = "#f6f9fb"
        self.panel_color = "#ffffff"
        self.title_fg = "#0b3d91"
        self.text_fg = "#202124"
        self.btn_bg = "#0b6bd6"
        self.btn_active = "#0a57a8"
        self.entry_font = ("Arial", 12)
        self.label_font = ("Arial", 13)
        self.title_font = ("Arial", 20, "bold")

        self.frame_count=0
        self.B1 = Backend()
        self.B1.read_file()
        self.B1.find_prod_vol()
        self.root = tk.Tk()
        self.root.geometry("1000x600")
        self.root.title("Product Manager")

        # apply basic root styling
        self.root.configure(bg=self.bg_color)

        # configure ttk style for Treeview
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#0b6bd6", foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=26, fieldbackground=self.panel_color)
        style.map("Treeview", background=[('selected', '#bcd9ff')], foreground=[('selected', 'black')])

        # button stylizer (helper)
        def _style_btn(btn):
            try:
                btn.configure(bg=self.btn_bg, fg="white", activebackground=self.btn_active,
                              activeforeground="white", bd=0, relief="raised", padx=6, pady=6,
                              font=("Arial", 12))
            except Exception:
                pass
        self._style_btn = _style_btn

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

        self.menu = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        title = tk.Label(self.menu,text = "Menu",font = self.title_font, bg=self.bg_color, fg=self.title_fg)
        title.pack(padx=10,pady=10)

        sub_title = tk.Label(self.menu,text="Welcome to the Product Management System",font = ("Arial",14), bg=self.bg_color, fg=self.text_fg)
        sub_title.pack(padx=10,pady=10)

        menu_buttons = tk.Frame(self.menu, bg=self.bg_color)
        menu_buttons.columnconfigure(0,weight=1)
        menu_buttons.columnconfigure(1,weight=1)

        bt1 = tk.Button(menu_buttons,text="Add Product",font = ("Arial",14),command = self.add_product)
        bt1.grid(row=0,column=0,sticky='ew', padx=8, pady=8)
        self._style_btn(bt1)
        bt2 = tk.Button(menu_buttons,text="Delete Product",font = ("Arial",14),command= self.delete_product)
        bt2.grid(row=0,column=1,sticky='ew', padx=8, pady=8)
        self._style_btn(bt2)
        bt3 = tk.Button(menu_buttons,text="Inspect Inventory",font = ("Arial",14),command=self.inspect_inventory)
        bt3.grid(row=1,column=0,sticky='ew', padx=8, pady=8)
        self._style_btn(bt3)
        bt4 = tk.Button(menu_buttons,text="Warehouse Spacing",font = ("Arial",14),command=self.warehouse_spacing)
        bt4.grid(row=1,column=1,sticky='ew', padx=8, pady=8)
        self._style_btn(bt4)
        bt5 = tk.Button(menu_buttons,text="Search Product",font = ("Arial",14),command=self.search_product)
        bt5.grid(row=2,column=0,sticky='ew', padx=8, pady=8)
        self._style_btn(bt5)
        bt6 = tk.Button(menu_buttons,text="Sort By",font = ("Arial",14),command=self.sort_by)
        bt6.grid(row=2,column=1,sticky='ew', padx=8, pady=8)
        self._style_btn(bt6)

        menu_buttons.pack(pady=60,fill='x')

        self.menu.pack(fill='both', expand=True)

    def add_product(self):
        self.frame_count=1
        self.clear_screen(self.menu)

        self.add_prod = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        title = tk.Label(self.add_prod,text = "Add Product",font= self.title_font, bg=self.bg_color, fg=self.title_fg)
        title.grid(row=0,column=0,padx=10,pady=20,sticky='n')

        sub_title = tk.Label(self.add_prod,text="Please enter the fields below to add the product",font=("Arial",14), bg=self.bg_color, fg=self.text_fg)
        sub_title.grid(row=1,column=0,padx=10,pady=20,sticky='n')

        eb_1_input = StringVar()
        eb_1_txt = tk.Label(self.add_prod,text="Please enter name of the product",font= self.label_font, bg=self.bg_color, fg=self.text_fg)
        eb_1_txt.grid(row=2,column=0,padx=10,pady=10,sticky='w')
        self.eb_1 = tk.Entry(self.add_prod,textvariable=eb_1_input, font=self.entry_font, width=30)
        self.eb_1.grid(row=2,column=1,padx=10,pady=10,sticky='e')


        eb_2_input = StringVar()
        eb_2_txt = tk.Label(self.add_prod,text="Please enter price of the product",font= self.label_font, bg=self.bg_color, fg=self.text_fg)
        eb_2_txt.grid(row=3,column=0,padx=10,pady=10,sticky='w')
        self.eb_2 = tk.Entry(self.add_prod,textvariable=eb_2_input, font=self.entry_font, width=30)
        self.eb_2.grid(row=3,column=1,padx=10,pady=10,sticky='e')

        eb_3_input = StringVar()
        eb_3_txt = tk.Label(self.add_prod,text="Please enter quantity of the product",font= self.label_font, bg=self.bg_color, fg=self.text_fg)
        eb_3_txt.grid(row=4,column=0,padx=10,pady=10,sticky='w')
        self.eb_3 = tk.Entry(self.add_prod,textvariable=eb_3_input, font=self.entry_font, width=30)
        self.eb_3.grid(row=4,column=1,padx=10,pady=10,sticky='e')

        eb_4_input = StringVar()
        eb_4_txt = tk.Label(self.add_prod,text="Please enter volume(in L) of the product",font= self.label_font, bg=self.bg_color, fg=self.text_fg)
        eb_4_txt.grid(row=5,column=0,padx=10,pady=10,sticky='w')
        self.eb_4 = tk.Entry(self.add_prod,textvariable=eb_4_input, font=self.entry_font, width=30)
        self.eb_4.grid(row=5,column=1,padx=10,pady=10,sticky='e')

        enter_button = tk.Button(self.add_prod,text="Enter new product information",font=("Arial",14),command=self.enter_new_prod)
        enter_button.grid(row=6,column=0,padx=30,pady=20)
        self._style_btn(enter_button)

        back_button = tk.Button(self.add_prod,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.grid(row=7,column=0,padx=30,pady=10)
        self._style_btn(back_button)

        self.add_prod.pack(fill='both', expand=True)

    def inspect_inventory(self):
        self.frame_count=2
        self.clear_screen(self.menu)

        self.insp_inv = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        title = tk.Label(self.insp_inv,text = "Inspect Inventory",font= self.title_font, bg=self.bg_color, fg=self.title_fg)
        title.grid(row=0,column=0,padx=10,pady=10)

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
        table.grid(row=1,column=0, sticky='nsew', padx=6, pady=6)

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
        tt_table.grid(row=2,column=0, padx=6, pady=6)

        back_button = tk.Button(self.insp_inv,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.grid(row=3,column=0,padx=10,pady=10)
        self._style_btn(back_button)

        self.insp_inv.pack(fill='both', expand=True)

    def delete_product(self):
        self.frame_count=3
        self.clear_screen(self.menu)

        self.del_prod = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        title = tk.Label(self.del_prod,text="Delete Product",font=self.title_font, bg=self.bg_color, fg=self.title_fg)
        title.pack(padx=20,pady=16)
        sub_title = tk.Label(self.del_prod,text="Please enter the exact name of the product",font=self.label_font, bg=self.bg_color, fg=self.text_fg)
        sub_title.pack(padx=20,pady=6)

        question = tk.Label(self.del_prod,text="What is the name of the product?",font=self.label_font, bg=self.bg_color, fg=self.text_fg)
        question.pack(padx=20,pady=6)
        ans_var = ""
        self.ans = tk.Entry(self.del_prod,textvariable=ans_var, font=self.entry_font, width=35)
        self.ans.pack(padx=10,pady=10)

        enter_button = tk.Button(self.del_prod,text="Delete Product",font=("Arial",14),command=self.remove_prod)
        enter_button.pack(padx=10,pady=10)
        self._style_btn(enter_button)

        back_button = tk.Button(self.del_prod,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.pack(padx=10,pady=10)
        self._style_btn(back_button)

        self.del_prod.pack(fill='both', expand=True)

    def warehouse_spacing(self):
        self.frame_count=4
        self.clear_screen(self.menu)

        self.ware_spa = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        title = tk.Label(self.ware_spa,text="Warehouse Spacing",font=self.title_font, bg=self.bg_color, fg=self.title_fg)
        title.pack(padx=10,pady=20)

        lb_1 = tk.Label(self.ware_spa,text=f"The volume of your warehouse = {self.B1.warehouse}L",font=self.label_font, bg=self.bg_color, fg=self.text_fg)
        lb_1.pack(padx=10,pady=10)

        if self.B1.warehouse==0:
            self.add_warehouse()

        view_graph = tk.Button(self.ware_spa,text='View Graph',font=("Arial",14),command=self.show_graph)
        view_graph.pack(padx=10,pady=18)
        self._style_btn(view_graph)

        add_ware = tk.Button(self.ware_spa,text="Edit Warehouse",font=("Arial",14),command=self.add_warehouse)
        add_ware.pack(padx=10,pady=8)
        self._style_btn(add_ware)

        back_button = tk.Button(self.ware_spa,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.pack(padx=10,pady=6)
        self._style_btn(back_button)

        self.ware_spa.pack(fill='both', expand=True)

    def add_warehouse(self):
        self.frame_count = 5
        try:
            self.clear_screen(self.ware_spa)
        except Exception:
            pass

        self.add_ware = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        title = tk.Label(self.add_ware,text="Edit Warehouse",font=self.title_font, bg=self.bg_color, fg=self.title_fg)
        title.grid(row=0,column=0,padx=10,pady=10)

        eb_1_input = StringVar()
        eb_1_txt = tk.Label(self.add_ware,text="Please enter volume of the warehouse(in L)",font= self.label_font, bg=self.bg_color, fg=self.text_fg)
        eb_1_txt.grid(row=1,column=0,padx=10,pady=10,sticky='w')
        self.eb_1 = tk.Entry(self.add_ware,textvariable=eb_1_input, font=self.entry_font, width=30)
        self.eb_1.grid(row=1,column=1,padx=10,pady=10,sticky='e')

        enter_button = tk.Button(self.add_ware,text="Enter warehouse information",font=("Arial",14),command=self.enter_new_ware)
        enter_button.grid(row=3,column=0,padx=30,pady=20)
        self._style_btn(enter_button)

        self.add_ware.pack(fill='both', expand=True)

    def clear_screen(self,frame):
           frame.destroy()

    def search_product(self):
        self.frame_count = 6
        self.clear_screen(self.menu)

        self.search_prod = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        title = tk.Label(self.search_prod,text="Search Product",font=self.title_font, bg=self.bg_color, fg=self.title_fg)
        title.pack(padx=10,pady=20)

        question = tk.Label(self.search_prod,text="What is the name of the product?",font=self.label_font, bg=self.bg_color, fg=self.text_fg)
        question.pack(padx=20,pady=6)
        prod_name = ''
        self.enter_box = tk.Entry(self.search_prod,textvariable=prod_name, font=self.entry_font, width=35)
        self.enter_box.pack(padx=20,pady=8)

        add_ware = tk.Button(self.search_prod,text="Get Product Details",font=("Arial",14),command=self.search_inv)
        add_ware.pack(padx=10,pady=8)
        self._style_btn(add_ware)

        back_button = tk.Button(self.search_prod,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.pack(padx=10,pady=6)
        self._style_btn(back_button)

        self.search_prod.pack(fill='both', expand=True)

    def login_in(self):
        self.frame_count = 9

        self.login = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        title = tk.Label(self.login,text="Login",font=self.title_font, bg=self.bg_color, fg=self.title_fg)
        title.pack(padx=10,pady=20)

        question1 = tk.Label(self.login,text="Username",font=self.label_font, bg=self.bg_color, fg=self.text_fg)
        question1.pack(padx=20,pady=6)
        username = ''
        self.enter_box1 = tk.Entry(self.login,textvariable=username, font=self.entry_font, width=35)
        self.enter_box1.pack(padx=20,pady=6)

        question2 = tk.Label(self.login,text="Password",font=self.label_font, bg=self.bg_color, fg=self.text_fg)
        question2.pack(padx=20,pady=6)
        password = ''
        self.enter_box2 = tk.Entry(self.login,textvariable=password, font=self.entry_font, width=35, show="*")
        self.enter_box2.pack(padx=20,pady=6)

        login_button = tk.Button(self.login,text="Log in",font=("Arial",14),command=self.check)
        login_button.pack(padx=10,pady=10)
        self._style_btn(login_button)

        self.login.pack(fill='both', expand=True)

    def display_product(self,prod : Product):
        self.frame_count = 7
        try:
            self.clear_screen(self.search_prod)
        except Exception:
            pass

        self.dis_prod = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        title = tk.Label(self.dis_prod,text="Product",font=self.title_font, bg=self.bg_color, fg=self.title_fg)
        title.pack(padx=10,pady=20)

        name = tk.Label(self.dis_prod,text=f"Name of Product - {prod.name}",font=self.label_font, bg=self.bg_color, fg=self.text_fg)
        name.pack(padx=20,pady=8)
        quantity = tk.Label(self.dis_prod,text=f"Quantity of Product - {prod.quantity}",font=self.label_font, bg=self.bg_color, fg=self.text_fg)
        quantity.pack(padx=20,pady=8)
        price = tk.Label(self.dis_prod,text=f"Price of Product - {prod.price}",font=self.label_font, bg=self.bg_color, fg=self.text_fg)
        price.pack(padx=20,pady=8)
        volume = tk.Label(self.dis_prod,text=f"Volume of Product - {prod.volume}",font=self.label_font, bg=self.bg_color, fg=self.text_fg)
        volume.pack(padx=20,pady=8)

        back_button = tk.Button(self.dis_prod,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.pack(padx=10,pady=6)
        self._style_btn(back_button)

        self.dis_prod.pack(fill='both', expand=True)

    def sort_by(self):
        self.frame_count = 8
        self.clear_screen(self.menu)

        self.srt_by = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=10)
        title = tk.Label(self.srt_by,text = "Sort By",font = self.title_font, bg=self.bg_color, fg=self.title_fg)
        title.pack(padx=10,pady=10)

        sub_title = tk.Label(self.srt_by,text="Sort the items by",font = ("Arial",14), bg=self.bg_color, fg=self.text_fg)
        sub_title.pack(padx=10,pady=8)

        menu_buttons = tk.Frame(self.srt_by, bg=self.bg_color)
        menu_buttons.columnconfigure(0,weight=1)
        menu_buttons.columnconfigure(1,weight=1)

        bt1 = tk.Button(menu_buttons,text="Name",font = ("Arial",14),command = self.sb_n)
        bt1.grid(row=0,column=0,sticky='ew', padx=8, pady=8)
        self._style_btn(bt1)
        bt2 = tk.Button(menu_buttons,text="Price",font = ("Arial",14),command= self.sb_p)
        bt2.grid(row=0,column=1,sticky='ew', padx=8, pady=8)
        self._style_btn(bt2)
        bt3 = tk.Button(menu_buttons,text="Quantity",font = ("Arial",14),command=self.sb_q)
        bt3.grid(row=1,column=0,sticky='ew', padx=8, pady=8)
        self._style_btn(bt3)
        bt4 = tk.Button(menu_buttons,text="Volume",font = ("Arial",14),command=self.sb_v)
        bt4.grid(row=1,column=1,sticky='ew', padx=8, pady=8)
        self._style_btn(bt4)

        menu_buttons.pack(pady=40,fill='x')

        back_button = tk.Button(self.srt_by,text="Return to Main Menu",font=("Arial",14),command=self.menu_frame)
        back_button.pack(padx=10,pady=6)
        self._style_btn(back_button)

        self.srt_by.pack(fill='both', expand=True)

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
        read_str = read_str.decode("utf-8")
        read_str = read_str.split('\n')
        print(read_str)
        if read_str[0] == username and read_str[1] == password:
            self.clear_screen(self.login)
            self.menu_frame(True)
            messagebox.showinfo(title="Validated",message=f"Logged in\n Welcome, {username}")
        else:
            self.clear_screen(self.login)
            self.menu_frame(False)
            messagebox.showerror(title='Invalid',message="Wrong username or password")


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
