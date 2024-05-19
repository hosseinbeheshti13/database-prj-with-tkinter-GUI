import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox

save_index = 0
class Table:
    def __init__(self, root, lst):
        self.root = root
        self.lst = lst
        self.add_button = None

        # create image objects for the Edit and Delete buttons
        edit_icon = tk.PhotoImage(file='edit.png')
        delete_icon = tk.PhotoImage(file='delete.png')
        add_icon = tk.PhotoImage(file='add.png')
        product_icon = tk.PhotoImage(file='product.png')
        self.conn = psycopg2.connect(database="99463119", user="99463119", password="123456", host="78.38.35.219", port="5432")

        # create a cursor object to execute SQL queries
        self.cursor = self.conn.cursor()
         # execute a SELECT query to retrieve data from the "persons" table
        self.cursor.execute("SELECT * FROM persons")
        rows = self.cursor.fetchall()

        # convert the rows to a list of tuples
        self.lst = []
        for row in rows:
            self.lst.append(row)
        # code for creating table headers
        headers = ['First Name', 'Last Name', 'Email','Password', 'Phone','ID', 'Person Type', 'Address', 'actions', 'Product List']
        for j, header in enumerate(headers):
            label = ttk.Label(root, text=header, style='My.TLabel')
            label.grid(row=0, column=j, sticky='we')
            label.configure(background= '#ebebeb',font=('Arial', 16, 'bold'),padding=14)
            label.configure(borderwidth=1, relief='solid')

        # code for creating table rows
        for i, row in enumerate(self.lst):
            for j, value in enumerate(row):
                # create a label for each cell
                label = ttk.Label(root, text=value, style='My.TLabel')
                label.grid(row=i+1, column=j, sticky='we')
                label.configure(font=('Arial', 14), padding=27)
                label.configure(borderwidth=1, relief='solid')
                if j == 5:  # check if this is the ID column
                    label.configure(background='#a0ffff')  # set a different background color
                else:
                    label.configure(background='#fff')  # set the default background color

            # create a frame to hold the Edit and Delete buttons
            frame = ttk.Frame(root)
            frame.grid(row=i+1, column=len(headers)-2)
           
            # create an Edit button for each row
            edit_button = ttk.Button(frame, image=edit_icon, command=lambda i=i: self.edit_record(i) ,padding='40 0')
            edit_button.image = edit_icon  # assign the image to an instance variable to prevent garbage collection
            edit_button.grid(row=0, column=0)

            # create a Delete button for each row
            delete_button = ttk.Button(frame, image=delete_icon, command=lambda i=i: self.delete_record(i),padding='40 0')
            delete_button.image = delete_icon  # assign the image to an instance variable to prevent garbage collection
            delete_button.grid(row=1, column=0)
             # create a frame to hold the Edit, Delete, and Product List buttons
            frame = ttk.Frame(root)
            frame.grid(row=i+1, column=len(headers)-1)
            # create a Product List button for each row
            product_list_button = ttk.Button(frame, image=product_icon, text='Product List', command=lambda i=i: self.open_product_list(i), padding='50 12')
            product_list_button.image = product_icon
            product_list_button.grid(row=2, column=0)
        # create an Add button for adding new records
        self.add_button = ttk.Button(root, image=add_icon, text='Add', command=self.add_record ,padding='25 0')
        self.add_button.image = add_icon
        self.add_button.grid(row=len(self.lst)+1, column=len(headers)-1, pady=20)

    def add_record(self):
        # create a new window to enter data for the new record
        add_window = tk.Toplevel()
        add_window.title('Add Record')

        # create labels and entries for each column
        headers = ['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Password', 'Address', 'Person Type']
        for i, header in enumerate(headers):
            label = ttk.Label(add_window, text=header, style='My.TLabel')
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')
            entry = ttk.Entry(add_window, style='My.TEntry')
            entry.grid(row=i, column=1, padx=10, pady=10)

        # create a button to add the new record
        add_button = ttk.Button(add_window, text='Add', command=self.save_record)
        add_button.grid(row=len(headers), column=0, columnspan=2, pady=10)

        # save the entries as instance variables
        self.add_window = add_window
        self.entries = [e for e in add_window.children.values() if isinstance(e, ttk.Entry)]

    def save_record(self):
        # get the data from the entries
        data = [e.get() for e in self.entries]
    
        # convert the ID to an integer
        data[0] = int(data[0])

        # execute an INSERT query to add the new record to the database
        query = "INSERT INTO persons (id, f_name, l_name, email, phone, password, address, person_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, data)
        self.conn.commit()

        # update the table display
        self.add_window.destroy()
        self.add_button.destroy()
        self.__init__(self.root, self.lst)

    def edit_record(self, index):
        # create a new window to edit the record
        edit_window = tk.Toplevel()
        edit_window.title('Edit Record')
     
        # create labels and entries for each column
        headers = ['First Name', 'Last Name', 'Email', 'Password', 'Phone', 'id' , 'Person Type' , 'Address']
        for i, header in enumerate(headers):
            label = ttk.Label(edit_window, text=header, style='My.TLabel')
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')
            entry = ttk.Entry(edit_window, style='My.TEntry')
            entry.grid(row=i, column=1, padx=10, pady=10)
            entry.insert(0, self.lst[index][i]) 
        # populate the entries with the current values
        # current_row = self.lst[index]
        # for i, value in enumerate(current_row):
        #     self.entries[i].delete(0, tk.END)
        #     self.entries[i].insert(0, value)

        # create a button to save the changes
        save_button = ttk.Button(edit_window, text='Save', command=lambda: self.save_edit_record(index, edit_window))
        save_button.grid(row=len(headers), column=0, columnspan=2, pady=10)

        # save the entries as instance variables
        self.edit_window = edit_window
        self.entries = [e for e in edit_window.children.values() if isinstance(e, ttk.Entry)]

    def save_edit_record(self, index, window=None):
        # get the data from the entries
        data = [e.get() for e in self.entries]
        query = "UPDATE persons SET f_name = %s, l_name = %s, email = %s, password = %s, phone = %s , id = %s , person_type = %s, address = %s WHERE id = %s"
        print()
        self.cursor.execute(query, data + [self.lst[index][5]])
        self.conn.commit()
        # recreate the table with the updated data
        if window is not None:
            window.destroy()
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root, self.lst)

    def delete_record(self, index):
        # execute a DELETE query to remove the record from the database
        query = "DELETE FROM persons WHERE id = %s"
        self.cursor.execute(query, [self.lst[index][5]])
        self.conn.commit()
    
        # remove the row from the self.lst attribute
        del self.lst[index]
    
        # update the table display
        self.root.destroy()
        self.__init__(tk.Tk(), self.lst)
    
    def open_product_list(self, index):
        # Get the person's ID from the selected row
        person_id = self.lst[index][5]
        edit_icon = tk.PhotoImage(file='edit.png')
        delete_icon = tk.PhotoImage(file='delete.png')
        add_icon = tk.PhotoImage(file='productadd.png')
        try:
            #p.name , p.id, p.price, c.name Execute a SELECT query to retrieve product data for the person's ID JOIN catagory ON product.catagory_id = catagory.id  , catagory.name 
            query = "SELECT p.name , p.id, p.price, c.name FROM product p JOIN category c ON p.category_id = c.id WHERE p.user_id = %s"
            #  query = "SELECT FROM product "
            self.cursor.execute(query, (person_id,))
            product_rows = self.cursor.fetchall()
            # Create a new window to display the product list
            product_window = tk.Toplevel()
            product_window.title('Product List')

            self.product_rows = []
            for row in product_rows:
                self.product_rows.append(row)

            # Create table headers for the product list
            product_headers = ['Product Name','id', 'Price' , 'catagory name', 'Actions']
            for j, header in enumerate(product_headers):
                label = ttk.Label(product_window, text=header, style='My.TLabel')
                label.grid(row=0, column=j, sticky='we')
                label.configure(background='#ebebeb', font=('Arial', 16, 'bold'), padding=14)
                label.configure(borderwidth=1, relief='solid')

            # Display the product list rows
            for i, row in enumerate(self.product_rows):
                # Display product name and price
                for j, value in enumerate(row):
                    label = ttk.Label(product_window, text=value, style='My.TLabel')
                    label.grid(row=i+1, column=j, sticky='we')
                    label.configure(font=('Arial', 14), padding=27)
                    label.configure(borderwidth=1, relief='solid')
                    if j == 1:  # check if this is the ID column
                      label.configure(background='#a0ffff')  # set a different background color
                    else:
                      label.configure(background='#fff')  # set the default background color

                # create a frame to hold the Edit and Delete buttons
                frame = ttk.Frame(product_window)
                frame.grid(row=i+1, column=len(product_headers)-1)

                # create an Edit button for each row
                edit_button = ttk.Button(frame,image=edit_icon, text='Edit', command=lambda i=i: self.edit_product(i,person_id,product_window),padding='40 0')
                edit_button.image = edit_icon 
                edit_button.grid(row=0, column=0)

                # create a Delete button for each row
                delete_button = ttk.Button(frame,image=delete_icon, text='Delete', command=lambda i=i: self.delete_product(i,person_id,product_window),padding='40 0')
                delete_button.image = delete_icon
                delete_button.grid(row=1, column=0)

            # create an Add button for adding new products
            add_button = ttk.Button(product_window,image=add_icon, text='Add', command=lambda: self.add_product(person_id,product_window),padding='40 0')
            add_button.image = add_icon
            add_button.grid(row=len(product_rows)+1, column=len(product_headers)-1, pady=20)
        except psycopg2.Error as e:
            messagebox.showerror('Error', 'An error occurred while fetching the product data:\n' + str(e))

    def open_product_listAfterChange(self, person_id):
          # Get the person's ID from the selected row
          person_id = person_id
          edit_icon = tk.PhotoImage(file='edit.png')
          delete_icon = tk.PhotoImage(file='delete.png')
          add_icon = tk.PhotoImage(file='productadd.png')
          try:
              #p.name , p.id, p.price, c.name Execute a SELECT query to retrieve product data for the person's ID JOIN catagory ON product.catagory_id = catagory.id  , catagory.name 
              query = "SELECT p.name , p.id, p.price, c.name FROM product p JOIN category c ON p.category_id = c.id WHERE p.user_id = %s"
              #  query = "SELECT FROM product "
              self.cursor.execute(query, (person_id,))
              product_rows = self.cursor.fetchall()
              # Create a new window to display the product list
              product_window = tk.Toplevel()
              product_window.title('Product List')      
              self.product_rows = []
              for row in product_rows:
                  self.product_rows.append(row)     
              # Create table headers for the product list
              product_headers = ['Product Name','id', 'Price' , 'catagory name', 'Actions']
              for j, header in enumerate(product_headers):
                  label = ttk.Label(product_window, text=header, style='My.TLabel')
                  label.grid(row=0, column=j, sticky='we')
                  label.configure(background='#ebebeb', font=('Arial', 16, 'bold'), padding=14)
                  label.configure(borderwidth=1, relief='solid')        
              # Display the product list rows
              for i, row in enumerate(self.product_rows):
                  # Display product name and price
                  for j, value in enumerate(row):
                      label = ttk.Label(product_window, text=value, style='My.TLabel')
                      label.grid(row=i+1, column=j, sticky='we')
                      label.configure(font=('Arial', 14), padding=27)
                      label.configure(borderwidth=1, relief='solid')
                      if j == 1:  # check if this is the ID column
                        label.configure(background='#a0ffff')  # set a different background color
                      else:
                        label.configure(background='#fff')  # set the default background color      
                  # create a frame to hold the Edit and Delete buttons
                  frame = ttk.Frame(product_window)
                  frame.grid(row=i+1, column=len(product_headers)-1)        
                  # create an Edit button for each row
                  edit_button = ttk.Button(frame,image=edit_icon, text='Edit', command=lambda i=i: self.edit_product(i,person_id,product_window),padding='40 0')
                  edit_button.image = edit_icon 
                  edit_button.grid(row=0, column=0)     
                  # create a Delete button for each row
                  delete_button = ttk.Button(frame,image=delete_icon, text='Delete', command=lambda i=i: self.delete_product(i,person_id,product_window),padding='40 0')
                  delete_button.image = delete_icon
                  delete_button.grid(row=1, column=0)       
              # create an Add button for adding new products
             
              add_button = ttk.Button(product_window,image=add_icon, text='Add', command=lambda: self.add_product(person_id,product_window),padding='40 0')
              add_button.image = add_icon
              add_button.grid(row=len(product_rows)+1, column=len(product_headers)-1, pady=20)
          except psycopg2.Error as e:
              messagebox.showerror('Error', 'An error occurred while fetching the product data:\n' + str(e))        
 
    def add_product(self, person_id , window):
        # create a new window to enter data for the new product
        add_product_window = tk.Toplevel()
        add_product_window.title('Add Product')

        # create labels and entries for each column
        headers = ['id','Product Name', 'Price','catagory id' ]
        for i, header in enumerate(headers):
            label = ttk.Label(add_product_window, text=header, style='My.TLabel')
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')
            entry = ttk.Entry(add_product_window, style='My.TEntry')
            entry.grid(row=i, column=1, padx=10, pady=10)

        # create a button to add the new product
        add_product_button = ttk.Button(add_product_window, text='Add Product', command=lambda: self.save_product(person_id))
        add_product_button.grid(row=len(headers), column=0, columnspan=2, pady=10)

        # save the entries as instance variables
        self.add_product_window = add_product_window
        self.product_entries = [e for e in add_product_window.children.values() if isinstance(e, ttk.Entry)]
        window.destroy()

    def save_product(self, person_id):
        # get the data from the entries
        data = [e.get() for e in self.product_entries]
        person_id=int(person_id)
        # execute an INSERT query to add the new product to the database
        query = "INSERT INTO product (id, name , price,category_id,user_id) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, data + [person_id])
        self.conn.commit()

        # update the product list display
        self.add_product_window.destroy()
        self.open_product_listAfterChange(person_id)

    def edit_product(self, index ,  person_id ,window):
        # create a new window to edit the product
        edit_product_window = tk.Toplevel()
        edit_product_window.title('Edit Product')

        # create labels and entries for each column
        headers = ['Product Name', 'id', 'Price' , 'catagory id']
        for i, header in enumerate(headers):
            label = ttk.Label(edit_product_window, text=header, style='My.TLabel')
            label.grid(row=i, column=0, padx=10, pady=10, sticky='w')
            entry = ttk.Entry(edit_product_window, style='My.TEntry')
            entry.grid(row=i, column=1, padx=10, pady=10)
            entry.insert(0, self.product_rows[index][i])  # populate the entry with the current value

        # create a button to save the changes
        save_product_button = ttk.Button(edit_product_window, text='Save', command=lambda: self.save_edit_product(index,person_id, edit_product_window))
        save_product_button.grid(row=len(headers), column=0, columnspan=2, pady=10)

        # save the entries as instance variables
        self.edit_product_entries = [e for e in edit_product_window.children.values() if isinstance(e, ttk.Entry)]
        window.destroy()

    def save_edit_product(self, index, person_id , window):
        # get the data from the entries
        data = [e.get() for e in self.edit_product_entries]

        # execute an UPDATE query to update the product in the database
        query = "UPDATE product SET name = %s,  id = %s , price = %s , category_id  = %s WHERE id = %s"
        self.cursor.execute(query, data + [self.product_rows[index][1]])
        self.conn.commit()

        # recreate the product list with the updated data
        window.destroy()
        self.open_product_listAfterChange( person_id)

    def delete_product(self, index,person_id,window):
        # execute a DELETE query to remove the product from the database
        query = "DELETE FROM product WHERE id = %s"
        self.cursor.execute(query, [self.product_rows[index][1]])
        self.conn.commit()


        del self.product_rows[index]
        # update the product list displayadd_product_window.winfo_toplevel()
        window.destroy()
        self.open_product_listAfterChange( person_id)
        # self.root.destroy()
        # self.__init__(tk.Tk(), self.lst)
    
# create a Tkinter window
root = tk.Tk()
root.title('Table Example')
root.configure(background='#ebebeb')

# create style objects for the labels and entries
style = ttk.Style()
style.configure('My.TLabel', background='#ebebeb', font=('Arial', 16, 'bold'), padding=14)
style.configure('My.TEntry', background='white', font=('Arial', 14), padding=10)

# create a Table object to display the data
table = Table(root, [])

# run the Tkinter event loop
root.mainloop()