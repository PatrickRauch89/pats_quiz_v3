
import tkinter as tk
from tkinter import ttk
import functions as func



class ThemeStyle(ttk.Style):
    def __init__(self):
        super().__init__()

        self.theme_create("quiz_theme", parent="clam", settings={
            "TFrame":{
                "configure": {
                    "background": "#c3e3e2"
                }
            },
            "TLabel":{
                "configure": {
                    "background": "#d9eae2",
                    "foreground": "#333333",
                    "font": ("Helvetica", 10),
                    "padding": 10,
                    "relief": "groove"
                },
                "map":{
                    "background": [("active", "#a4cdcc"), ("disabled", "#d9eae2")],
                    "foreground": [("disabled", "#A9A9A9")] 
                }
            },
            "TButton":{
            "configure": {
                    "background": "#d9eae2",
                    "foreground": "#FFFFFF",
                    "font": ("Helvetica", 12, "bold"),  
                    "padding": 10
                },
                "map": {
                    "background": [("active", "#36ca83"), ("disabled", "#d9eae2")],
                    "foreground": [("disabled", "#A9A9A9")] 
                }
             },
            "TEntry": {
                "configure": {
                    "background": "#FFFFFF",
                    "foreground": "#333333",
                    "font": ("Helvetica", 50),
                    "padding": 5,
                    "relief": "sunken",
                    "borderwidth": 2
                },
                "map": {
                    "background": [("active", "#c3e3e2")],
                    "foreground": [("disabled", "#A9A9A9")]
                }
            }                                
        })


        

class LabelStyle(ThemeStyle):
    font = "Arial"
    
    def __init__(self):
        super().__init__()

        self.theme_use("quiz_theme")
        self.configure("main_title.TLabel", anchor="center", relief="flat")
        self.configure("main_quiz.TLabel", background="#c3e3e2", anchor="center")
        self.configure("quiz_title.TLabel", background="#c3e3e2", anchor="center", relief="flat")
        self.configure("quiz_option.TLabel", background="#c3e3e2", anchor="center")
        self.configure("abbreviation_submit.TLabel", background="#c3e3e2", anchor="center")
        self.configure("abbreviation_button.TLabel", background="#c3e3e2", anchor="center")
        self.configure("under_menu.TLabel", background="#c3e3e2", anchor="center")



    
    def main_font_size(self, event):
        if event.width >= 1500 and event.height >= 900:
            new_size_main = 40
            new_size_quiz = 25
            new_size_quiz_title = 35
            new_size_entry = 40
            new_wraplength = 1300
        elif event.width < 750 or event.height < 483:
            new_size_main = 15
            new_size_quiz = 10
            new_size_quiz_title = 15
            new_size_entry = 15
            new_wraplength = 500
        else:
            new_size_main = 25
            new_size_quiz = 15
            new_size_quiz_title = 20
            new_size_entry = 50
            new_wraplength = 700
        
        self.configure("main_title.TLabel", font=(self.font, new_size_main, "bold"))
        self.configure("main_quiz.TLabel", font=(self.font, new_size_main, "bold"))
        self.configure("quiz_title.TLabel",  font=(self.font, new_size_quiz_title, "bold"), wraplength=new_wraplength)
        self.configure("quiz_option.TLabel", font=(self.font, new_size_quiz, "bold"), wraplength=new_wraplength)
        self.configure("abbreviation_submit.TLabel", font=(self.font, new_size_quiz, "bold"))
        self.configure("abbreviation_button.TLabel", font=(self.font, new_size_quiz, "bold"))
        self.configure("under_menu.TLabel", font=(self.font, new_size_quiz, "bold"))
        


    # BG Color Buttons Main
    @staticmethod
    def on_enter(event):
        event.widget.configure(background="#a4cdcc")

    @staticmethod
    def on_leave(event):
        event.widget.configure(background="#c3e3e2")
    # ----



class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.style = LabelStyle()
        self.current_table = None
        self.current_container = None

        self.title("Pat's Quiz")
        self.geometry("900x800+400+100")
        self.minsize(width=676, height=459)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frames = {}
        self.data_to_file = func.DataToFile()
        self.read_data = func.Randomizer()

        main_window = MainFrame(self, self)
        main_window.grid(row=0, column=0, sticky="NSEW")

        self.quiz_window_basic = QuizFrameBasic(self)
        self.quiz_window_basic.grid(row=0, column=0, sticky="NSEW")

        quiz_window_abbre = QuizFrameAbbre(self)
        quiz_window_abbre.grid(row=0, column=0, sticky="NSEW")

        self.frames[MainFrame] = main_window
        self.frames[QuizFrameBasic] = self.quiz_window_basic
        self.frames[QuizFrameAbbre] = quiz_window_abbre

        
        self.change_window(MainFrame)    

    def change_window(self, container):
        frame = self.frames[container]
        frame.tkraise()
    # Hier die read_data aktualisieren
    def change_to_window(self, table, container):
        self.current_table = table
        self.current_container = container
        self.data_to_file.load_data(table)
        self.refresh_quiz_basic(container)

    
    def refresh_quiz_basic(self, container):
        if container == QuizFrameBasic:
            self.quiz_window_basic.destroy()
            self.quiz_window_basic = QuizFrameBasic(self)
            self.quiz_window_basic.grid(row=0, column=0, sticky="NSEW")
        elif container== QuizFrameAbbre:
            self.quiz_window_basic.destroy()
            self.quiz_window_basic = QuizFrameAbbre(self)
            self.quiz_window_basic.grid(row=0, column=0, sticky="NSEW")



class MainFrame(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, style="TFrame", **kwargs)

        self.bind("<Configure>", self.on_configure)

        main_title_label = ttk.Label(self, text="Willkommen bei Pat's Quiz", style="main_title.TLabel", anchor="center")
        main_title_label.place(relx=0.5, rely=0.05, relwidth=0.8, relheight=0.1, anchor="center")

        quiz_selection_label_basic = ttk.Label(self, text="Basic Quiz", style="main_quiz.TLabel", anchor="center")
        quiz_selection_label_basic.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.1, anchor="center")
        quiz_selection_label_basic.bind("<Button-1>", lambda event: controller.change_to_window("base", QuizFrameBasic))

        quiz_selection_label_python = ttk.Label(self, text="Python Quiz", style="main_quiz.TLabel", anchor="center")
        quiz_selection_label_python.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.1, anchor="center")
        quiz_selection_label_python.bind("<Button-1>", lambda event: controller.change_to_window("python", QuizFrameBasic))

        quiz_selection_label_english = ttk.Label(self, text="Englisch Quiz", style="main_quiz.TLabel", anchor="center")
        quiz_selection_label_english.place(relx=0.3, rely=0.6, relwidth=0.4, relheight=0.1, anchor="center")
        quiz_selection_label_english.bind("<Button-1>", lambda event: controller.change_to_window("english_hardware", QuizFrameBasic))

        quiz_selection_label_english_voc = ttk.Label(self, text="Englisch Vokabeln", style="main_quiz.TLabel", anchor="center")
        quiz_selection_label_english_voc.place(relx=0.7, rely=0.6, relwidth=0.4, relheight=0.1, anchor="center")
        quiz_selection_label_english_voc.bind("<Button-1>", lambda event: controller.change_to_window("english_voc", QuizFrameBasic))

        quiz_selection_label_abbre = ttk.Label(self, text="Kürzel Quiz", style="main_quiz.TLabel", anchor="center")
        quiz_selection_label_abbre.place(relx=0.5, rely=0.8, relwidth=0.8, relheight=0.1, anchor="center")
        quiz_selection_label_abbre.bind("<Button-1>", lambda event: controller.change_to_window("abbreviation", QuizFrameAbbre))
        
        for label in [quiz_selection_label_basic, quiz_selection_label_python, quiz_selection_label_english, quiz_selection_label_english_voc, quiz_selection_label_abbre]:
            label.bind("<Enter>", self.master.style.on_enter)
            label.bind("<Leave>", self.master.style.on_leave)

    def on_configure(self, event):
        self.master.style.main_font_size(event)


class QuizFrameBasic(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, style="TFrame", **kwargs)

        self.quiz_label_reaction = []
        table = self.master.current_table

        random_data = func.Randomizer()
        term, answers, answer1, explanation = random_data.read_data(table)
        self.correct_answer = answer1

        basic_title_label = ttk.Label(self, text=f"Wozu passt:    {term}", style="quiz_title.TLabel", anchor="center")
        basic_title_label.place(relx=0.5, rely=0.05, relwidth=0.8, relheight=0.18, anchor="center")

        quiz_top_label_basic = ttk.Label(self, text=answers[0], style="quiz_option.TLabel", anchor="center", padding=10)
        quiz_top_label_basic.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.18, anchor="center")
        self.quiz_label_reaction.append(quiz_top_label_basic)

        quiz_middle_label_basic = ttk.Label(self, text=answers[1], style="quiz_option.TLabel", anchor="center")
        quiz_middle_label_basic.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.18, anchor="center")
        self.quiz_label_reaction.append(quiz_middle_label_basic)

        quiz_bottom_label_basic = ttk.Label(self, text=answers[2], style="quiz_option.TLabel", anchor="center")
        quiz_bottom_label_basic.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.18, anchor="center")
        self.quiz_label_reaction.append(quiz_bottom_label_basic)

        under_menu = UnderMenu(self, controller=self.master, style=self.master.style, current_container=self.master.current_container)
        under_menu.place(relx=0.5, rely=0.9, relwidth=1, relheight=0.1, anchor="center")


        for label in self.quiz_label_reaction:
            label.bind("<Button-1>", lambda event, l=label: self.clicked_answer(event, l, explanation))
            label.bind("<Enter>", self.master.style.on_enter)
            label.bind("<Leave>", self.master.style.on_leave)       


    def clicked_answer(self, event, label, explanation):
        if explanation != "":
            quiz_python_label_basic = ttk.Label(self, text=explanation, style="quiz_option.TLabel", anchor="center")
            quiz_python_label_basic.place(relx=0.5, rely=0.77, relwidth=0.8, relheight=0.14, anchor="center")
        for label in self.quiz_label_reaction:
            selected = label.cget("text")
            if selected == self.correct_answer:
                label.configure(background="#7DDA58", foreground="#333333")
            else:
                label.configure(background="#E4080A", foreground="#333333")
        
        for lbl in self.quiz_label_reaction:
            lbl.unbind("<Enter>")
            lbl.unbind("<Leave>")
            lbl.unbind("<Button-1>")
        
        self.update_idletasks()
        
    
class QuizFrameAbbre(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, style="TFrame", **kwargs)     

        table = self.master.current_table
        random_data = func.Randomizer()
        term, answers, self.answer1, explanation = random_data.read_data(table)

        self.tip = ""
        self.counter_tip = 0
        self.accuracy = ""

        abbreviation_title_label = ttk.Label(self, text=f"Was bedeutet:\n       {term}", style="quiz_title.TLabel", anchor="center")
        abbreviation_title_label.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.18, anchor="center")

        self.abbreviation_entry_var = tk.StringVar()
        abbreviation_entry = ttk.Entry(self, font=("Arial", 25, "bold"), textvariable=self.abbreviation_entry_var)
        abbreviation_entry.place(relx=0.39, rely=0.3, relwidth=0.6, relheight=0.1, anchor="center")
        abbreviation_entry.bind("<Return>", lambda event: self.check_answer())

        abbreviation_submit_label = ttk.Label(self, text="Absenden", style="abbreviation_submit.TLabel", anchor="center")
        abbreviation_submit_label.place(relx=0.81, rely=0.3, relwidth=0.2, relheight=0.1, anchor="center")
        abbreviation_submit_label.bind("<Button-1>", lambda event: self.check_answer())

        abbreviation_tip_button = ttk.Label(self, text="Hinweis", style="abbreviation_submit.TLabel", anchor="center")
        abbreviation_tip_button.place(relx=0.81, rely=0.5, relwidth=0.2, relheight=0.1, anchor="center")
        abbreviation_tip_button.bind("<Button-1>", lambda event: self.clicked_tip())

        self.abbreviation_show_tip_label = ttk.Label(self, text=self.tip, style="quiz_title.TLabel", anchor="center")
        self.abbreviation_show_tip_label.place(relx=0.38, rely=0.5, relwidth=0.62, relheight=0.18, anchor="center")

        self.abbreviation_answer_accuracy_label = ttk.Label(self, text=self.accuracy, style="quiz_title.TLabel", anchor="center")
        self.abbreviation_answer_accuracy_label.place(relx=0.5, rely=0.7, relwidth=0.8, relheight=0.15, anchor="center")

        under_menu = UnderMenu(self, controller=self.master, style=self.master.style, current_container=self.master.current_container)
        under_menu.place(relx=0.5, rely=0.9, relwidth=1, relheight=0.1, anchor="center")

        for label in [abbreviation_submit_label, abbreviation_tip_button]:
            label.bind("<Enter>", self.master.style.on_enter)
            label.bind("<Leave>", self.master.style.on_leave)
    
    def clicked_tip(self):
        self.counter_tip += 1
        self.counter_dots = ""
        if len(self.tip) < len(self.answer1):
            self.counter_dots = "..."
        else:
            self.counter_dots = ""
        self.tip = str(self.answer1[0:(self.counter_tip * 3)]) + str(self.counter_dots)
        self.abbreviation_show_tip_label.config(text=self.tip)
    
    def check_answer(self):
        if self.answer1.lower().replace("-", " ") in self.abbreviation_entry_var.get().lower().replace("-", " "):
            self.accuracy = "Richtig!"
            self.abbreviation_answer_accuracy_label.config(text=self.accuracy, background="#7DDA58", foreground="#333333")
        if self.answer1.lower().replace("-", " ") not in self.abbreviation_entry_var.get().lower().replace("-", " "):
            self.accuracy = "Leider Falsch"
            self.abbreviation_answer_accuracy_label.config(text=self.accuracy, background="#E4080A", foreground="#333333")


class UnderMenu(ttk.Frame):
    def __init__(self, container, controller, style, current_container,  **kwargs):
        super().__init__(container, **kwargs)

        self.container = container
        self.controller = controller
        self.style = style
        self.current_container = current_container
    

        main_menu = ttk.Label(self, text="Hauptmenü", style="under_menu.TLabel", anchor="center")
        main_menu.place(relx=0.2, rely=0.5, relwidth=0.3, relheight=0.8, anchor="center")
        main_menu.bind("<Button-1>", lambda event: self.controller.change_window(MainFrame))

        next = ttk.Label(self, text="Weiter", style="under_menu.TLabel", anchor="center")
        next.place(relx=0.8, rely=0.5, relwidth=0.3, relheight=0.8, anchor="center")
        next.bind("<Button-1>", lambda event: self.controller.refresh_quiz_basic(current_container))

        for label in [main_menu, next]:
                    label.bind("<Enter>", self.style.on_enter)
                    label.bind("<Leave>", self.style.on_leave)





root = MainWindow()


root.mainloop()