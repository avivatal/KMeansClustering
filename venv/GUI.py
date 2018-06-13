from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E
import tkFileDialog
import tkMessageBox
import pandas as pd
import matplotlib.pyplot as mat
import plotly.plotly as py
from Preprocessor import *
from KMeansRunner import *
from sklearn.cluster import KMeans
from PIL import Image, ImageTk


class GUI:

    df = pd.DataFrame()

    def __init__(self, master):
        self.master = master
        master.title("K-Means Clustering")

        self.numOfClustersVal = 0;
        self.numOfRunsVal = 0;
        self.hasProcessed=False

        #Browse File Input
        self.pathLabel = Label(master, text="Import data:")
        self.browse_button = Button(master, text="Browse", command=lambda: self.browse())
        self.pathInput = Entry(master, validate="key")

        #Num of Clusters
        self.numOfClustersLbl = Label(master, text="Num of Clusters:")
        self.numOfClustersVal = Entry(master, validate="key")

        #Num of Runs
        self.numOfRunsLbl = Label(master, text="Num of Runs:")
        self.numOfRunsVal = Entry(master, validate="key")

        #PreProcess
        self.preProcessBtn = Button(master, text="Preprocess", command=lambda : self.preProcess())

        #Cluster
        self.clusterBtn = Button(master, text="Cluster", command=lambda: self.cluster())


        # GUI LAYOUT

        #import data
        self.pathLabel.grid(row=0, column=1, sticky=W)
        self.pathInput.grid(row=0, column=2, sticky=W)
        self.browse_button.grid(row=0, column=3, sticky=W)

        #num of clusters
        self.numOfClustersLbl.grid(row=1, column=1, sticky=W)
        self.numOfClustersVal.grid(row=1, column=2, sticky=W)

        # num of runs
        self.numOfRunsLbl.grid(row=2, column=1, sticky=W)
        self.numOfRunsVal.grid(row=2, column=2, sticky=W)

        #preprocess
        self.preProcessBtn.grid(row=4, column=1, sticky=W)
        #cluster
        self.clusterBtn.grid(row=4, column=2, sticky=W)

    def browse(self):
        #open file dialog and get file name
        self.selectedPath = tkFileDialog.askopenfilename(filetypes=(("XLSX", "*.xlsx"), ("XLS", "*.xls")))
        #insert the path name into the path input textbox
        self.pathInput.insert(0, self.selectedPath)
        #read the selected file into a df and validate
        self.df = pd.read_excel(self.selectedPath)
        if(self.df.empty):
            tkMessageBox.showerror("K Means Clustering", "The Chosen File is Empty")
            return


    def preProcess(self):
        try:
            # preprocess the data and update df with the processed data
            preprocessor = Preprocessor(self.df)
            self.df = preprocessor.df
            self.hasProcessed=True
        except KeyError:
            tkMessageBox.showinfo("K Means Clustering", "The selected file is invalid")
            return
        #pop message to user
        tkMessageBox.showinfo("K Means Clustering", "Preprocessing completed successfully!")

    def cluster(self):
        if self.hasProcessed is False:
            tkMessageBox.showerror("K Means Clustering", "The data must be processed before clustering")
            return
        if self.numOfClustersVal.get()=="" or self.numOfRunsVal.get()=="":
            tkMessageBox.showerror("K Means Clustering", "Please submit all parameters before clustering")
            return
        if self.hasProcessed:
            numberOfClusters = int(self.numOfClustersVal.get())
            numberOfRuns = int(self.numOfRunsVal.get())

            #input validations
            if numberOfClusters < 0 :
                tkMessageBox.showerror("K Means Clustering", "Please choose at least 1 cluster")
                return
            if numberOfRuns < 0 :
                tkMessageBox.showerror("K Means Clustering", "Please choose at least 1 run")
                return
            if numberOfClusters > len(self.df) :
                tkMessageBox.showerror("K Means Clustering", "Please choose number of clusters that is less than number of records")
                return
            if numberOfRuns > 300 :
                tkMessageBox.showerror("K Means Clustering", "Please choose at most 300 runs")
                return

            kmeans = KMeansRunner(self.df, numberOfClusters, numberOfRuns)
            self.df = kmeans.df

            #display plots
            scatterImg = ImageTk.PhotoImage(Image.open('scatter.png'))
            self.lblscatter=Label(self.master,image=scatterImg)
            self.lblscatter.image=scatterImg
            self.lblscatter.grid(row=5, column=0, columnspan=10)

            horoplethImg = ImageTk.PhotoImage(Image.open('horopleth.png'))
            self.lblhoropleth = Label(self.master, image=horoplethImg)
            self.lblhoropleth.image = horoplethImg
            self.lblhoropleth.grid(row=5, column=10, columnspan=10)

            #pop up message
            tkMessageBox.showinfo("K Means Clustering", "Clustering completed successfully!")



root = Tk()
root.geometry("1500x800")
my_gui = GUI(root)
root.mainloop()
