import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import ttk, Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Tkinter import *
import matplotlib.pyplot as plt
from pandas import DataFrame

DB_FILE = "../recruit.db"
APP_TITLE = "MassMutual Life Insurance Sales"

data_points = ["race", "education_level", "home_owner", "state", "is_smoker", "is_exerciser", "has_insurance", "income", "travel_spending", "sports_leisure_spending", "economic_stability", "insurance_segment", "youtube_user_rank", "facebook_user_rank", "gender"]
hist_data_points = ["income", "travel_spending", "sports_leisure_spending"]

try:

    def do_tab(ntbk, being_counted, use_hist):
	connection = sqlite3.connect(DB_FILE)
        print("START: " + being_counted);
        being_counted_formatted = being_counted.replace("_", " ").title()
        the_query = "select " + being_counted + ", count(*) as count FROM (SELECT race_code, race.value as race, education_id, education.value as education_level, home_owner, state, is_smoker, is_exerciser, has_insurance, income, travel_spending, sports_leisure_spending, economic_stability, insurance_segment_id, insurance_segment.value as insurance_segment, youtube_user_rank, facebook_user_rank, gender FROM customer, race, education, insurance_segment where customer.race_code = race.code and customer.education_id = education.id and customer.insurance_segment_id = insurance_segment.id) group by " + being_counted + " order by " + being_counted
        print(the_query);
        result_df = pd.read_sql(the_query, connection)
        tabFrame = Tkinter.Frame(nb, name = being_counted)
        result_counts = result_df["count"]
        labels = result_df[being_counted]
        fig, ax = plt.subplots()
        fig.tight_layout()
        y_pos = np.arange(len(labels))

        if(use_hist):
            ax.hist(result_df[being_counted].dropna(), color="#26386a")
        else:
            ax.bar(y_pos, result_counts, align='center', color='#26386a', ecolor='black')        
            ax.set_xticks(y_pos)
            ax.set_xticklabels(labels)

	ax.set_xlabel(being_counted_formatted)
	ax.set_ylabel('Customer Count')
        
        ax.set_title(being_counted_formatted)
        canvas = FigureCanvasTkAgg(fig, master=tabFrame)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.draw()
        ntbk.add(tabFrame, text = being_counted_formatted)
        print("DONE: " + being_counted);
        
    mainWindow = Tkinter.Tk()
    mainWindow.configure(background='white')
    w, h = mainWindow.winfo_screenwidth(), mainWindow.winfo_screenheight()
    mainWindow.geometry("%dx%d+0+0" % (w, h))
    img = PhotoImage(file="../_resources/img/logo.gif")
    imgLabel = Label(image = img)
    imgLabel.pack()

    mainFrame = Tkinter.Frame(mainWindow, name = 'main-frame')
    mainFrame.pack(fill = Tkinter.BOTH, expand=True)

    nb = ttk.Notebook(mainFrame, name = 'nb')
    nb.pack(fill = Tkinter.BOTH, expand=True)

    for point in data_points:
        do_tab(nb, point, point in hist_data_points)

    mainWindow.mainloop()

except Exception as e:
    print("Unexpected error:", e)
else:
    connection.close()