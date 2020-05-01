import json, os, csv
import tkinter as TK
from tkinter.filedialog import askopenfilename 
import functools
import tkinter.ttk as ttk
# import time
from tkinter import messagebox

global pbar_det


#<!--------Program Helper Functions----------------->
def clear(event):
    "'Window cleaning'"
    for element in root.winfo_children():
        element.destroy()

def percentageCalculator(x, y, case=1):
    """Calculate percentages
       Case1: What is x% of y?
       Case2: x is what percent of y?
       Case3: What is the percentage increase/decrease from x to y?
    """
    if case == 1:
        #Case1: What is x% of y?
        r = x/100*y
        return r
    elif case == 2:
        #Case2: x is what percent of y?
        r = x/y*100
        return r
    elif case == 3:
        #Case3: What is the percentage increase/decrease from x to y?
        r = (y-x)/x*100
        return r
    else:
        raise Exception("Only case 1,2 and 3 are available!")
#<!--------Program Helper Functions End------------->


#<!---------OTHER FUNCTIONS-------->
def browse_file(window):
            
    files = [
                ('CSV Files', '*.csv'), 
                ('Excel Files', '*.xlsm')
            ]
    data_path = askopenfilename(filetypes=files, defaultextension = files)
    base_name = os.path.basename(data_path)
    size = os.path.getsize(data_path)
    name, ext = os.path.splitext(base_name)
    if(data_path == ""):
        Error_label = TK.Label(
                root,
                text = "No file selected",
                font = ("Comic sans MS", 11, "bold"),
                fg='red',
                wraplength=300, 
                background = "#ffffff",
            )
        Error_label.place(x=99, y=25)
    elif(ext != ".csv"):
        print(ext)
        Error_label = TK.Label(
                root,
                text = "Only CSV files are accepted",
                font = ("Comic sans MS", 11, "bold"),
                fg='red',
                wraplength=300, 
                background = "#ffffff",
            )
        Error_label.place(x=99, y=25)
    elif(size <= 2):
        Error_label = TK.Label(
                root,
                text = "CSV File is empty",
                font = ("Comic sans MS", 11, "bold"),
                fg='red',
                wraplength=300, 
                background = "#ffffff",
            )
        Error_label.place(x=99, y=25)

    else:
        window.destroy()
        display_data(data_path, name)


def count_rows(file):
    with open(file) as j:
        total = sum(1 for line in j)
    return total


def empty_cell(file):
    dict_count = {}
    count = 0
    sum = 0
    with open(file) as k:
        reader = csv.DictReader(k)
        data = list(reader)
        # fields = reader.fieldnames

    for record in data:
        for f,r in record.items():
            if r == "" or r == "0":
                if f in dict_count:
                    tot = int(dict_count[f]) + 1
                else:
                    tot = count + 1
                dict_count[f] = str(tot)

    if len(dict_count) != 0:
        for b in dict_count:
            sum += int(dict_count[b])  
        return sum
    else:
        return "None"


def duplicate_row(path):
    count = 0
    seen = set()
    duplicate = set()
    with open(path) as cu:
        for line in cu:
            if line in seen:
                count = count + 1
                duplicate.add(line)
            else:
                seen.add(line)
    return count


def row_classification(path):
    dict_county = {}
    seen = set()

    with open(path) as file:
        reader = csv.DictReader(file)
        data = list(reader)
        for j in data:
            count = 0
            if j["class"] in seen:
                 dict_county[j["class"]] = int(dict_county[j["class"]]) + 1
            else:
                seen.add(j["class"])
                count = count + 1
                dict_county[j["class"]] = count

    if len(dict_county) != 0:
        out = []
        sum = 0
        for b in dict_county:
            sum += int(dict_county[b]) 
        out.append(dict_county)
        out.append(sum)
        out.append(len(dict_county))
        return out
    else:
        return "None"


def row_percent_classifier(dicty, sum):
    new_dicty = {}
    for b in dicty:
        key = b
        val = dicty[b]
        new_dicty[key] = (val/sum) * 100
    return new_dicty


def row_pat_input(min_value, max_value, classy, percentage_classy, path, header, root_tree):   
    root_input = TK.Toplevel(root_tree)
    root_input.title('Row Partitioning')
    root_input.geometry('500x200')
    # root_input.iconbitmap("images/halo_shield.ico")
    root_input['bg'] = 'blue'
    global rowPat_entry

    rowPat_Label = TK.Label(
        root_input, 
        text='Enter No. of rows ('+ str(min_value) + "-" + str(max_value) + ")", 
        font = ("Comic sans MS", 10, "bold"),
        bg='blue'
    )
    rowPat_Label.place(x=170, y=65)

    rowPat_no = TK.StringVar()
    rowPat_entry = TK.Entry(
        root_input, 
        textvariable= rowPat_no, 
        font = ('Bookman Old Styles', 12),
        width=50
    )
    rowPat_entry.place(x=20, y=95)

    percent = TK.Label(
        root_input,
        text="",
        anchor=TK.S,
        font = ("Comic sans MS", 9, "bold"),
        bg='blue'
    )
    # progress = ttk.Progressbar(
    #     root_input, 
    #     length=450, 
    #     mode='determinate'
    # )    
    status = TK.Label(
        root_input, 
        text="Click Partition to start process..", 
        relief= TK.SUNKEN, 
        anchor=TK.W, 
        bd=2
    )

    pat_button = TK.Button(
        root_input, 
        bg='light yellow', 
        activebackground='light yellow', 
        text='Partition',
        command=functools.partial(partition, min_value, max_value, percentage_classy, path, header, root_input, root_tree, status)
    )
    pat_button.place(x=220, y=135)

    percent.pack()
    # progress.pack()
    status.pack(side=TK.BOTTOM, fill=TK.X)



    rowPat_entry.focus_force()
    root_input.transient(root_tree)
    root_input.grab_set()
    root_tree.wait_window(root_input)
    # root_input.mainloop()


def col_pat_input(path, header, root_tree):
    root_input = TK.Toplevel(root_tree)
    root_input.title('Row Partitioning')
    root_input.geometry('500x200')
    # root_input.iconbitmap("images/halo_shield.ico")
    root_input['bg'] = 'blue'
    global colPat_entry

    colPat_Label = TK.Label(
        root_input, 
        text='Enter No. of columns (1'+ "-" + str(len(header)) + ")", 
        font = ("Comic sans MS", 10, "bold"),
        bg='blue'
    )
    colPat_Label.place(x=170, y=65)

    colPat_no = TK.StringVar()
    colPat_entry = TK.Entry(
        root_input, 
        textvariable= colPat_no, 
        font = ('Bookman Old Styles', 12),
        width=50
    )
    colPat_entry.place(x=20, y=95)

    status = TK.Label(
        root_input, 
        text="Click Partition to start process..", 
        relief= TK.SUNKEN, 
        anchor=TK.W, 
        bd=2
    )

    pat_button = TK.Button(
        root_input, 
        bg='light yellow', 
        activebackground='light yellow', 
        text='Partition',
        command=functools.partial(partition_col, path, header, root_input, root_tree, status)
    )
    pat_button.place(x=220, y=135)

    status.pack(side=TK.BOTTOM, fill=TK.X)

    colPat_entry.focus_force()
    root_input.transient(root_tree)
    root_input.grab_set()
    root_tree.wait_window(root_input)


def partition (min_v, max_v, percentage_class, path, header, window1, window2, status):
    no = rowPat_entry.get()
    no = int(no)
    su = 0
    mini = int(min_v)
    maxy = int(max_v) -1
         
        
    if (no < mini) or (no >= maxy):
        Error_label = TK.Label(
                window1,
                text = "Number entered must be greater than or equal to {0} and less than {1}".format(min_v, max_v),
                font = ("Comic sans MS", 11, "bold"),
                fg='red',
                wraplength=300, 
                background = "#ffffff",
        )
        Error_label.place(x=97, y=15)
    else:
        new_dic = {}
        count_dic = {}
        part = 0
        part_arr = []
        tipy = maxy
        
        for l in percentage_class:
            percent = percentage_class[l]
            new_dic[l] = round((percent * no)/100)
            count_dic[l] = 0
        print(new_dic)

        for y in new_dic:
            su += new_dic[y]
                
        with open(path) as file:
            reader = csv.DictReader(file)
            data = list(reader)
            new_data_part = list()
            remaining = list()
            det = maxy
            while det >= su:
                # unit = percentageCalculator(part, det, case=2)
                for f in count_dic:
                    count_dic[f] = 0

                for j in data:
                    if count_dic[j["class"]] != new_dic[j["class"]] and len(part_arr) == 0:
                        new_data_part.append(j)
                        tipy -= 1
                        count_dic[j["class"]] += 1
                    else:
                        for party in part_arr:
                            if count_dic[j["class"]] != new_dic[j["class"]] and j not in party:
                                new_data_part.append(j)
                                tipy -= 1
                                count_dic[j["class"]] += 1
                            else:
                                
                                remaining.append(j)

                part_arr.append(new_data_part)
                part += 1
                new_data_part = list()
                det -= su
                # time.sleep(0.1)
                step = "Working on {}".format(det) 
                status['text'] = "{}".format(step)
                window1.update()

            if det < su and tipy != 0:
                for j in remaining:
                    if len(remaining) != 0:
                        new_data_part.append(j)
                    else:
                        break
                if len(new_data_part) != 0:
                    part_arr.append(new_data_part)

        # step = "Working on {}".format(det) 
        # status['text'] = "{}".format(step)
        # window1.update()
        print(str(len(part_arr)) + " New Partitions created")
        complete = partition_writer(part_arr, header,)
        window1.destroy()
        partition_list(complete, window2)


def partition_col (path, header, window1, window2, status):
    no = colPat_entry.get()
    no = int(no)
    maxy = len(header)

    if (no < 1) or (no >= maxy):
        Error_label = TK.Label(
                window1,
                text = "Number entered must be greater than or equal to {0} and less than {1}".format(1, maxy),
                font = ("Comic sans MS", 11, "bold"),
                fg='red',
                wraplength=300, 
                background = "#ffffff",
        )
        Error_label.place(x=97, y=15)
    else:
        part = 0
        list2_part = []
        check_dict = {}
        det = maxy
        fir = 0
        back = no
        col_arr = []
        print("once")

        for j in header:
            check_dict[j] = 0
        while det >= no:
            with open(path) as ji:
                reader = csv.reader(ji)
                for row in reader:
                    list2_part.append(row[fir:back])
                  
                col_arr.append(list2_part)
                part += 1
                list2_part = []
                det -= no
                fir += no
                back += no
                step = "Working on {}".format(det) 
                status['text'] = "{}".format(step)
                window1.update()
                print(col_arr)

        if (det != 0):
            back -= no
            with open(path) as ji:
                reader = csv.reader(ji)
                for row in reader:
                    list2_part.append(row[back:])
                    step = "Working on {}".format(det) 
                    status['text'] = "{}".format(step)
                    window1.update()
                col_arr.append(list2_part)

        print(str(len(col_arr)) + " New Partitions created")
        complete = partition_col_writer(col_arr)
        window1.destroy()
        partition_list(complete, window2)


def partition_col_writer(raster):
    part = 1
    partition_paths = []
    for rast in raster:
        file_c = "column_partition/" + tname + "_partition" + str(part) + ".csv"
        partition_paths.append(file_c)
        with open(file_c, "w", newline='') as yir:
            rit = csv.writer(yir)
            for f in rast:
                rit.writerow(f)
            part += 1
    return partition_paths

                    
def partition_writer(raster, header):
    part = 1
    partiton_paths = []
    for rast in raster:
        file_w = "row_partition/" + tname + "_partition" + str(part) + ".csv"
        partiton_paths.append(file_w)
        with open(file_w, "w", newline='') as filey:
            fieldnames = header
            writer = csv.DictWriter(filey, fieldnames=fieldnames)

            writer.writeheader()
            for ily in rast:
                ruby = dict(ily)
                writer.writerow(ruby)

            part += 1

    return partiton_paths
   

def partition_list(file_paths, window2):
    window2.destroy()
    root = TK.Tk()
    root.title("Partition Selection")
    width = 400
    height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)
    # root.iconbitmap("images/halo_shield.ico")

    partition_listbox = TK.Listbox(
        root,
        width=58, 
        height=7, 
        bg='light yellow', 
        selectbackground='SkyBlue4'
    )
    partition_listbox.place(x=28, y=10)

    for f in range(len(file_paths)):
        partition = f
        partition_listbox.insert(1, file_paths[partition])
        partition_listbox.bind("<Double-Button-1>", OnDouble)

    # btnPartitionSelection = TK.Button(
    #     root,
    #     text='Open', 
    #     background='light yellow', 
    #     activebackground='light yellow', 
    #    command=functools.partial(OnDouble, event)
    # )
    # btnPartitionSelection.place(x=170, y=160)


def OnDouble(event):
    widget = event.widget
    selection=widget.curselection()
    value = widget.get(selection[0])
    dir_fol = value.split("/")
    print("selection:", selection, ": '%s'" % value)
    display_data(value, dir_fol[1])


def wrap(string):
    return '|________________________________'.join(string)


def display_data(path, ty_name):
    # clear(window)
    root_tree = TK.Tk()
    root_tree.title("Dataset Display Table")
    width = 1400
    height = 700
    screen_width = root_tree.winfo_screenwidth()
    screen_height = root_tree.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root_tree.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root_tree.resizable(0, 0)
    global tname 
    tname = ty_name

    TableMargin = TK.Frame(root_tree, width=1000)
    TableMargin.pack(side=TK.LEFT)
    clockFrame = TK.Frame(TableMargin, width=400, background="#ffffff")
    clockFrame.pack(side=TK.RIGHT)
    scrollbarx = TK.Scrollbar(TableMargin, orient=TK.HORIZONTAL)
    scrollbary = TK.Scrollbar(TableMargin, orient=TK.VERTICAL)

    with open(path) as f:
        reader = csv.reader(f, delimiter=',')
        header = next(reader)
        fr = tuple(header)
        total = count_rows(path)
        empty = empty_cell(path)
        duplicate = duplicate_row(path)
        if "class" in header:
            arr = row_classification(path)
            classifier = arr[0]
            tot_class = arr[1]
            min_value = arr[2]
            percentage_classifier = row_percent_classifier(classifier, tot_class)


        
        tree = ttk.Treeview(
            TableMargin,
            columns = (fr),
            height=400, 
            selectmode="extended", 
            yscrollcommand=scrollbary.set, 
            xscrollcommand=scrollbarx.set
        )
        
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=TK.RIGHT, fill=TK.Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=TK.BOTTOM, fill=TK.X)
        for head in header:
            tree.heading(head, text=head, )
            

        tree.column('#0', stretch=TK.NO, minwidth=0, width=0)
        # tree.grid(row=1,column=0,padx=5,pady=5)
        tree.pack(ipadx=30)
            

        for row in reader:
            tree.insert("", total, values=(row), tag = "red")

        tree.tag_configure('red', background='#cccccc')
 
    tInfo_label = TK.Label(
        clockFrame,
        text = "..........Table Information..........",
        font = ("Comic sans MS", 24, "bold"),
        background = "#ffffff",
        height = 2
    )

    tName_label = TK.Label(
        clockFrame,
        text = "Table Name : " + tname,
        font = ("Comic sans MS", 12, "bold"),
        background = "#ffffff",
        height = 2
    )

    empty_label = TK.Label(
        clockFrame,
        text = "Number of Empty Fields: " + str(empty),
        font = ("Comic sans MS", 12, "bold"),
        background = "#ffffff",
        height = 2
    )

    duplicate_label = TK.Label(
        clockFrame,
        text = "Number of Duplicate Rows: " + str(duplicate),
        font = ("Comic sans MS", 12, "bold"),
        background = "#ffffff",
        height = 2
    )

    spacing_label = TK.Label(
        clockFrame,
        text = "",
        font = ("Comic sans MS", 12, "bold"),
        background = "#ffffff",
        height = 9
    )

    if "class" in header:
        row_patBtn = TK.Button(
            clockFrame, 
            bg='light yellow', 
            activebackground='light yellow', 
            text='Partition By Row',
            font = ("Comic sans MS", 10, "bold"), 
            height = 2,
            command=functools.partial(row_pat_input, min_value, total, classifier, percentage_classifier, path, header, root_tree)
        )

        col_patBtn = TK.Button(
            clockFrame, 
            bg='light yellow', 
            activebackground='light yellow', 
            text='Partition By Column', 
            font = ("Comic sans MS", 10, "bold"),
            height = 2,
            command=functools.partial(col_pat_input,path,header, root_tree)
        )

        exit_Btn = TK.Button(
            clockFrame, 
            bg='light yellow', 
            activebackground='light yellow', 
            text='Exit', 
            font = ("Comic sans MS", 10, "bold"),
            height = 2,
            command=root_tree.destroy
        )


    tInfo_label.pack(side=TK.TOP)
    tName_label.pack()
    empty_label.pack()
    duplicate_label.pack()
    if "class" in header:
        for t in classifier:
            TK.Label(
                clockFrame,
                text = t + ":" + str(classifier[t]),
                font = ("Comic sans MS", 12, "bold"),
                background = "#ffffff",
                # height = 4
            ).pack()
    spacing_label.pack()
    if "class" in header:
        row_patBtn.place(x=20, y=470)
        col_patBtn.place(x=149, y=470)
        exit_Btn.place(x=520, y=470)
    
        
        
    root_tree.mainloop()





#<!------ Program starts here------->
root = TK.Tk()
root.title("Open Dataset")
width = 400
height = 170
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
# root.geometry("400x170")
root.config(background="#ffffff")
# root.iconbitmap("images/halo_shield.ico")
root.resizable(0,0)



hello_label = TK.Label(
      root,
      text = "Choose a Dataset file to work with",
      font = ("Comic sans MS", 11, "bold"),
      background = "#ffffff",
)
hello_label.place(x=80, y=55)

btnBrowse = TK.Button(
    root,
    text = "Browse",
    relief = TK.FLAT,
    command = functools.partial(browse_file, root)

)
btnBrowse.place(x=170, y=120)


root.mainloop()
