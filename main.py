from tkinter import *
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from random import choice
import pyscreenshot,time
import os

FILE_LOCATION = "./csv files"
BUTTON_FONT = ("Arial", 13, "bold")
LABEL_FONT = ("Arial", 20, "bold")
USER_FONT = ("Arial", 14, "bold")
INFO_FONT = ("Arial", 12, "bold")
SMALL_FONT = ("Arial", 12, "bold")
COLORS = ['green', 'red', 'purple', 'brown', 'blue']


class Visualization:
    def __init__(self, window):
        self.window = window
        self.window.title("Data Visualization GUI Application")
        self.window.geometry("1360x700")
        self.window.resizable(width=False, height=False)
        self.window.config(bg="black")

        # extra variables:
        self.df = pd.DataFrame()
        self.bar_x_label = StringVar()
        self.bar_y_label = StringVar()
        self.scatter_x_name = StringVar()
        self.scatter_y_name = StringVar()
        self.pie_value_name = StringVar()
        self.pie_group_name = StringVar()
        self.line_name = StringVar()

        # ================================ TOP FRAME ================================ #
        self.top_frame = Frame(self.window, bg="black", relief=RIDGE)
        self.top_frame.place(x=2, y=0, width=1363, height=40)

        self.build_chart = Label(self.top_frame, text="Matplotlib Dashboards", font=LABEL_FONT,
                                 fg="orange", bg="black")
        self.build_chart.place(x=610, y=2)

        # ================================ RIGHT FRAME ================================ #
        self.right_frame = Frame(self.window, bg="black")
        self.right_frame.place(x=1065, y=45, width=300, height=645)


        self.note = Label(self.right_frame, text="Write your own Notes", justify="center", font=USER_FONT,
                               bg="black",fg="orange")
        self.note.place(x=35, y=30)

        self.text=Text(self.right_frame,height=40,width=45)
        self.text.place(x=0,y=90)
        self.text.config(background="black",foreground="orange")

        self.ss=Button(self.right_frame,text="screen shot", justify="center", font=INFO_FONT, relief=RIDGE,
                                       bg="ivory", cursor="hand2", bd=2, width=10, command=self.screen_shot)
        self.ss.place(x=100,y=480)

        self.save_text=Button(self.right_frame,text="save_text",justify="center", font=INFO_FONT, relief=RIDGE,
                                       bg="ivory", cursor="hand2", bd=2, width=10, command=self.save_text)
        self.save_text.place(x=100,y=550)


        # ================================ DASHBOARD AREA ================================ #
        # top left canvas: -----------------------------------------------------------
        self.bar_heading = Label(self.window, text="Bar Chart", font=SMALL_FONT, bg="black",fg="orange")
        self.bar_heading.place(x=325, y=45, width=365, height=20)

        self.bar_info = Frame(self.window, bg="black")
        self.bar_info.place(x=325, y=65, width=365, height=70)

        self.x_label = Label(self.bar_info, text="XLabel", font=SMALL_FONT, bg="black",fg="orange", bd=1)
        self.x_label.grid(row=0, column=0, padx=10)

        self.y_label = Label(self.bar_info, text="YLabel", font=SMALL_FONT, bg="black",fg="orange", bd=1)
        self.y_label.grid(row=1, column=0, padx=10)

        self.x_box = ttk.Combobox(self.bar_info, font=SMALL_FONT, justify="center", state="readonly",
                                  textvariable=self.bar_x_label)
        self.x_box.grid(row=0, column=1)

        self.y_box = ttk.Combobox(self.bar_info, font=SMALL_FONT, justify="center", state="readonly",
                                  textvariable=self.bar_y_label)
        self.y_box.grid(row=1, column=1)

        self.bar_draw_button = Button(self.bar_info, text="draw", justify="center", font=INFO_FONT, relief=RIDGE, bd=2,
                                      bg="ivory", cursor="hand2", width=5, command=self.draw_bar_chart)
        self.bar_draw_button.grid(row=0, column=2, padx=10)

        self.bar_clear_button = Button(self.bar_info, text="clean", justify="center", font=INFO_FONT, relief=RIDGE,
                                       bg="ivory", cursor="hand2", bd=2, width=5, command=self.clear_bar)
        self.bar_clear_button.grid(row=1, column=2, padx=10)

        # bar diagram replacement:
        self.top_left = Frame(self.window, bg="black")
        self.top_left.place(x=325, y=135, width=365, height=230)
        self.canvas_1 = Canvas(self.top_left, width=365, height=250, bg="black", relief=RIDGE)
        self.canvas_1.pack()
        self.fig_1 = None
        self.output_1 = None

        # top right canvas: ----------------------------------------------------------
        self.scatter_heading = Label(self.window, text="Scatter Plot", font=SMALL_FONT, bg="black",fg="orange")
        self.scatter_heading.place(x=695, y=45, width=365, height=20)

        self.scatter_info = Frame(self.window, bg="black")
        self.scatter_info.place(x=695, y=65, width=365, height=70)

        self.scatter_x_label = Label(self.scatter_info, text="XLabel", font=SMALL_FONT,bg="black",fg="orange", bd=1)
        self.scatter_x_label.grid(row=0, column=0, padx=10)

        self.scatter_y_label = Label(self.scatter_info, text="YLabel", font=SMALL_FONT, bg="black",fg="orange", bd=1)
        self.scatter_y_label.grid(row=1, column=0, padx=10)

        self.scatter_x_box = ttk.Combobox(self.scatter_info, font=SMALL_FONT, justify="center", state="readonly",
                                          textvariable=self.scatter_x_name)
        self.scatter_x_box.grid(row=0, column=1)

        self.scatter_y_box = ttk.Combobox(self.scatter_info, font=SMALL_FONT, justify="center", state="readonly",
                                          textvariable=self.scatter_y_name)
        self.scatter_y_box.grid(row=1, column=1)

        self.scatter_draw_button = Button(self.scatter_info, text="draw", justify="center", font=INFO_FONT,
                                          relief=RIDGE, bd=2, bg="ivory", cursor="hand2", width=5,
                                          command=self.draw_scatter_chart)
        self.scatter_draw_button.grid(row=0, column=2, padx=10)

        self.scatter_clean_button = Button(self.scatter_info, text="clean", justify="center", font=INFO_FONT,
                                           relief=RIDGE, bg="ivory", cursor="hand2", bd=2, width=5,
                                           command=self.clear_scatter)
        self.scatter_clean_button.grid(row=1, column=2, padx=10)

        # diagram replacement:
        self.top_right = Frame(self.window, bg="black")
        self.top_right.place(x=695, y=135, width=365, height=230)
        self.canvas_2 = Canvas(self.top_right, width=365, height=265, bg="black", relief=RIDGE)
        self.canvas_2.pack()
        self.fig_2 = None
        self.output_2 = None

        # bottom left canvas: --------------------------------------------------------
        self.pie_heading = Label(self.window, text="Pie Chart", font=SMALL_FONT, bg="black",fg="orange")
        self.pie_heading.place(x=325, y=370, width=365, height=20)

        self.pie_info = Frame(self.window, bg="black")
        self.pie_info.place(x=325, y=390, width=365, height=70)

        self.pie_x_label = Label(self.pie_info, text="Values", font=SMALL_FONT, bg="black",fg="orange", bd=1)
        self.pie_x_label.grid(row=0, column=0, padx=10)

        self.pie_y_label = Label(self.pie_info, text="GroupBy", font=SMALL_FONT, bg="black",fg="orange", bd=1)
        self.pie_y_label.grid(row=1, column=0, padx=10)

        self.pie_value_box = ttk.Combobox(self.pie_info, font=SMALL_FONT, justify="center", state="readonly",
                                          textvariable=self.pie_value_name)
        self.pie_value_box.grid(row=0, column=1)

        self.pie_group_box = ttk.Combobox(self.pie_info, font=SMALL_FONT, justify="center", state="readonly",
                                          textvariable=self.pie_group_name)
        self.pie_group_box.grid(row=1, column=1)

        self.pie_draw_button = Button(self.pie_info, text="draw", justify="center", font=INFO_FONT, relief=RIDGE,
                                      bd=2, bg="ivory", cursor="hand2", width=5, command=self.draw_pie_chart)
        self.pie_draw_button.grid(row=0, column=2, padx=10)

        self.pie_clear_button = Button(self.pie_info, text="clean", justify="center", font=INFO_FONT, relief=RIDGE,
                                       bg="ivory", cursor="hand2", bd=2, width=5, command=self.clear_pie)
        self.pie_clear_button.grid(row=1, column=2, padx=10)

        self.bottom_left = Frame(self.window, bg="black")
        self.bottom_left.place(x=325, y=460, width=365, height=225)
        self.canvas_3 = Canvas(self.bottom_left, width=365, height=250, bg="black", relief=RIDGE)
        self.canvas_3.pack()
        self.fig_3 = None
        self.output_3 = None

        # bottom right canvas: ------------------------------------------------------
        self.line_heading = Label(self.window, text="Line Chart", font=SMALL_FONT, bg="black",fg="orange")
        self.line_heading.place(x=695, y=370, width=365, height=20)

        self.line_info = Frame(self.window, bg="black")
        self.line_info.place(x=695, y=390, width=365, height=70)

        self.line_box = ttk.Combobox(self.line_info, font=SMALL_FONT, justify="center", state="readonly",
                                     textvariable=self.line_name)
        self.line_box.grid(row=0, column=1)

        self.line_draw_button = Button(self.line_info, text="draw", justify="center", font=INFO_FONT, relief=RIDGE,
                                       bd=2, bg="ivory", cursor="hand2", command=self.draw_line_chart)
        self.line_draw_button.grid(row=0, column=0, padx=10, pady=20)

        self.line_clear_button = Button(self.line_info, text="clean", justify="center", font=INFO_FONT, relief=RIDGE,
                                        bg="ivory", cursor="hand2", bd=2, command=self.clear_line)
        self.line_clear_button.grid(row=0, column=2, padx=10, pady=20)

        self.bottom_right = Frame(self.window, bg="black")
        self.bottom_right.place(x=695, y=460, width=365, height=225)
        self.canvas_4 = Canvas(self.bottom_right, width=365, height=250, bg="black", relief=RIDGE)
        self.canvas_4.pack()
        self.fig_4 = None
        self.output_4 = None

        # =================================== LEFT FRAME ================================ #
        self.left_frame = Frame(self.window, bg="black", relief=RIDGE, bd=1)
        self.left_frame.place(x=2, y=45, width=320, height=645)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", backgroung="black", foreground="orange", rowheight=25, fieldbackground="black")
        style.map("Treeview", background=[("selected", "medium sea green")])
        style.configure("Treeview.Heading", background="black",foreground="orange", font=("Arial", 10, "bold"))

        self.my_table = ttk.Treeview(self.left_frame)

        scroll_x_label = ttk.Scrollbar(self.left_frame, orient=HORIZONTAL, command=self.my_table.xview)
        scroll_y_label = ttk.Scrollbar(self.left_frame, orient=VERTICAL, command=self.my_table.yview)
        scroll_x_label.pack(side=BOTTOM, fill=X)
        scroll_y_label.pack(side=RIGHT, fill=Y)

        # add menu bar:
        my_menu = Menu(self.window)
        self.window.config(menu=my_menu)
        self.file_menu = Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label="Available SpreadSheets", menu=self.file_menu)
        self.file_menu.add_command(label="open file", command=self.file_open)

    # ================================= FUNCTIONALITY =============================== #

    def file_open(self):
        file_name = filedialog.askopenfilename(
            initialdir=FILE_LOCATION,
            title="Open A File",
            filetypes=(("csv files", "*.csv"), ("All Files", "*.*"))
        )
        if file_name:
            try:
                file_name = f"{file_name}"
                self.df = pd.read_csv(file_name)
            except ValueError:
                self.error_info.config(text="file can not be opened!")
            except FileNotFoundError:
                self.error_info.config(text="file can not be found!")

        # clean existing data:
        self.clear_table_data()
        # from csv into dataframe:
        self.my_table["column"] = list(self.df.columns)
        self.my_table["show"] = "headings"
        for column in self.my_table["column"]:
            self.my_table.heading(column, text=column)
        # resize columns:
        for column_name in self.my_table["column"]:
            self.my_table.column(column_name, width=60)
        # fill rows with data:
        df_rows_old = self.df.to_numpy()
        df_rows_refreshed = [list(item) for item in df_rows_old]
        for row in df_rows_refreshed:
            self.my_table.insert("", "end", values=row)
        self.my_table.place(x=5, y=5, width=310, height=630)
        try:
            self.fill_scatter_box()
        except TclError:
            pass

        try:
            self.fill_bar_box()
        except TclError:
            pass

        try:
            self.fill_pie_box()
        except TclError:
            pass

        try:
            self.fill_line_box()
        except TclError:
            pass

    def clear_table_data(self):
        self.my_table.delete(*self.my_table.get_children())

    # ================================ FILL COMBOBOX METHODS ============================= #
    def fill_bar_box(self):
        columns = [item for item in self.df]
        x_labels = []
        y_labels = []
        for column in columns:
            if self.df[column].dtype == 'object':
                x_labels.append(column)
            elif self.df[column].dtype == 'int64' or self.df[column].dtype == 'float64':
                y_labels.append(column)
        self.x_box["values"] = tuple(x_labels)
        self.x_box.current(0)
        self.y_box["values"] = tuple(y_labels)
        self.y_box.current(0)

    def fill_scatter_box(self):
        columns = [item for item in self.df]
        x_labels = []
        y_labels = []
        for column in columns:
            if self.df[column].dtype == 'int64' or self.df[column].dtype == 'float64':
                x_labels.append(column)
                y_labels.append(column)
        self.scatter_x_box["values"] = tuple(x_labels)
        self.scatter_x_box.current(0)
        self.scatter_y_box["values"] = tuple(y_labels)
        self.scatter_y_box.current(0)

    def fill_pie_box(self):
        try:
            columns = [item for item in self.df]
            x_labels = []
            y_labels = []
            for column in columns:
                if self.df[column].dtype == 'object':
                    x_labels.append(column)
                elif self.df[column].dtype == 'int64' or self.df[column].dtype == 'float64':
                    y_labels.append(column)
            self.pie_group_box["values"] = tuple(x_labels)
            self.pie_group_box.current(0)
            self.pie_value_box["values"] = tuple(y_labels)
            self.pie_value_box.current(0)
        except:
            messagebox.showerror("Error!!")

    def fill_line_box(self):
        columns = [item for item in self.df]
        x_labels = []
        for column in columns:
            if self.df[column].dtype == 'int64' or self.df[column].dtype == 'float64':
                x_labels.append(column)
        self.line_box["values"] = tuple(x_labels)
        self.line_box.current(0)

    # =================================== DRAW CHARTS ============================ #
    def draw_bar_chart(self):
        self.fig_1 = Figure(figsize=(4, 3), dpi=100)
        axes = self.fig_1.add_subplot(111)
        axes.bar(self.df[f"{self.bar_x_label.get()}"], self.df[f"{self.bar_y_label.get()}"], color=choice(COLORS))
        self.output_1 = FigureCanvasTkAgg(self.fig_1, master=self.canvas_1)
        self.output_1.draw()
        self.output_1.get_tk_widget().pack()

    def clear_bar(self):
        if self.output_1:
            for child in self.canvas_1.winfo_children():
                child.destroy()
        self.output_1 = None

    def draw_scatter_chart(self):
        self.fig_2 = Figure(figsize=(4, 3), dpi=100)
        axes = self.fig_2.add_subplot(111)
        axes.scatter(self.df[f"{self.scatter_x_name.get()}"], self.df[f"{self.scatter_y_name.get()}"], c=choice(COLORS))
        self.output_2 = FigureCanvasTkAgg(self.fig_2, master=self.canvas_2)
        self.output_2.draw()
        self.output_2.get_tk_widget().pack()

    def clear_scatter(self):
        if self.output_2:
            for child in self.canvas_2.winfo_children():
                child.destroy()
        self.output_2 = None

    def draw_pie_chart(self):
        # prepare values:
        display = self.df.groupby([f"{self.pie_group_name.get()}"]).sum(numeric_only=True)
        display = display[f"{self.pie_value_name.get()}"].to_numpy()
        my_labels = list(self.df[f"{self.pie_group_name.get()}"].unique())
        # visualize:
        self.fig_3 = Figure(figsize=(4, 3), dpi=100)
        axes = self.fig_3.add_subplot(111)
        axes.pie(display, labels=my_labels, shadow=True)
        self.output_3 = FigureCanvasTkAgg(self.fig_3, master=self.canvas_3)
        self.output_3.draw()
        self.output_3.get_tk_widget().pack()

    def clear_pie(self):
        if self.output_3:
            for child in self.canvas_3.winfo_children():
                child.destroy()
        self.output_3 = None

    def draw_line_chart(self):
        self.fig_4 = Figure(figsize=(4, 3), dpi=100)
        axes = self.fig_4.add_subplot(111)
        axes.plot(self.df[f"{self.line_name.get()}"], c=choice(COLORS))
        self.output_4 = FigureCanvasTkAgg(self.fig_4, master=self.canvas_4)
        self.output_4.draw()
        self.output_4.get_tk_widget().pack()

    def clear_line(self):
        if self.output_4:
            for child in self.canvas_4.winfo_children():
                child.destroy()
        self.output_4 = None

    def screen_shot(self):
        pic = pyscreenshot.grab()
        pic.show()
        random = int(time.time())
        pic.save(str(random)+".png")
    def save_text(self):
        data=self.text.get("1.0",'end-1c')
        path=os.getcwd()+"/"+str(int(time.time()))+".txt"
        with open(path,'w') as f:
            f.write(data)
        f.close()

if __name__ == "__main__":
    app = Tk()
    Visualization(app)
    app.mainloop()
