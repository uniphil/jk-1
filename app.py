import Tkinter as tk
import tkFont

class App(tk.Frame):
    totalcamFrames = 0
    totalproFrames = 0
    gridPos = 0
    contentsPos = -1
                
                        # Lists for modular interface
    modON = []          # Module On/Off toggle
    contentsCamF = []   # Input field camera frames
    contentsET = []     # Extposure time 
    mb = []             # Exposure time drop down menu
    camBack = []        # Camera direction toggle 
    contentsProF = []   # Input field projector frames 
    proBack = []        # Projector direction toggle
    cycles = []         # Module cycle count
    exp = 0

    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.layout()
        self.headWidgets()
        self.inputWidgets()
        self.footWidgets()
        
    def layout(self):
        self.seperatorHead_1 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperatorHead_1.grid(column=0, row=0, ipadx=10, padx=5, pady=5, sticky=tk.W)

        self.seperatorHead_2 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperatorHead_2.grid(column=1, row=0, ipadx=10, padx=5, pady=5, sticky=tk.E)
        
        self.seperatorBody_1 = tk.Frame(bd=3, relief=tk.RIDGE)
        self.seperatorBody_1.grid(column=0, row=1, padx=5, columnspan=2)
        
        self.seperatorFoot_1 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperatorFoot_1.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)

        self.seperatorFoot_2 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperatorFoot_2.grid(column=1, row=2, padx=5, pady=5, sticky=tk.E)

        self.seperatorFoot_3 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperatorFoot_3.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)

        self.seperatorFoot_4 = tk.Frame(bd=1, relief=tk.GROOVE)
        self.seperatorFoot_4.grid(column=1, row=3, padx=5, pady=5, sticky=tk.E)

                            
        
    def headWidgets(self):
        self.headFont = tkFont.Font(size=20)

        self.camTitle = tk.Label(self.seperatorHead_1, text='Current Camera Frame', width=30)
        self.camTitle.grid(column=0, row=0, columnspan=2)
        self.proTitle = tk.Label(self.seperatorHead_2, text='Current Projector Frame', width=30)
        self.proTitle.grid(column=2, row=0, columnspan=2)
        
        self.camReset = tk.Button(self.seperatorHead_1, text='reset', state=tk.NORMAL, command=self.camcountReset)
        self.camReset.grid(column=0, row=1)

        self.camFrames = tk.StringVar()
        self.camFrames.set(self.totalcamFrames)

        self.camCount = tk.Label(self.seperatorHead_1, font=self.headFont)
        self.camCount.grid(column=1, row=1, padx=5, sticky=tk.E)
        self.camCount["textvariable"] = self.camFrames

        self.proReset = tk.Button(self.seperatorHead_2, text='reset', state=tk.NORMAL, command=self.procountReset)
        self.proReset.grid(column=2, row=1)

        self.proFrames = tk.StringVar()
        self.proFrames.set(self.totalproFrames)

        self.proCount = tk.Label(self.seperatorHead_2, font=self.headFont)
        self.proCount.grid(column=3, row=1, padx=5, sticky=tk.E)
        self.proCount["textvariable"] = self.proFrames

        self.camFlabel = tk.Label(self.seperatorBody_1, text='Camera Frames:')
        self.camFlabel.grid(column=1, row=0, sticky=tk.W)

        self.EXlabel = tk.Label(self.seperatorBody_1, text='Exposure Time:')
        self.EXlabel.grid(column=3, row=0, sticky=tk.W)

        self.proFlabel = tk.Label(self.seperatorBody_1, text='Projector Frames:')
        self.proFlabel.grid(column=5, row=0, sticky=tk.W)

        self.cycleslabel = tk.Label(self.seperatorBody_1, text='Cycles:')
        self.cycleslabel.grid(column=7, row=0, sticky=tk.W)
        
    def inputWidgets(self):
        self.gridPos += 1
        self.contentsPos += 1
        
        self.modON.append(tk.IntVar())
        self.modCheck = tk.Checkbutton(self.seperatorBody_1, text = "ON/OFF", variable=self.modON[self.contentsPos], onvalue =1, offvalue = 0)
        self.modCheck.grid(column=0, row=self.gridPos, sticky=tk.W)
        
        self.contentsCamF.append(tk.IntVar())
        self.camFrames = tk.Entry(self.seperatorBody_1, justify=tk.RIGHT, textvariable=self.contentsCamF[self.contentsPos])
        self.camFrames.grid(column=1, row=self.gridPos)

        
        self.contentsET.append(tk.DoubleVar())
        self.mb.append(tk.Menubutton(self.seperatorBody_1, text='Default', relief=tk.RAISED))
        self.mb[self.contentsPos].grid(column=3, row=self.gridPos, padx=5, pady=3, sticky=tk.W)
        self.mb[self.contentsPos].menu = tk.Menu(self.mb[self.contentsPos], tearoff=0)
        self.mb[self.contentsPos]['menu'] = self.mb[self.contentsPos].menu

        
        self.mb[self.contentsPos].menu.add_radiobutton(label='Default', command=self.update, variable=self.contentsET[self.contentsPos], value=0)
        self.mb[self.contentsPos].menu.add_radiobutton(label='1/5', command=self.update, variable=self.contentsET[self.contentsPos], value=.25)
        self.mb[self.contentsPos].menu.add_radiobutton(label='1/4', command=self.update, variable=self.contentsET[self.contentsPos], value=0.75)
        self.mb[self.contentsPos].menu.add_radiobutton(label='0.3', command=self.update, variable=self.contentsET[self.contentsPos], value=0.125)
        self.mb[self.contentsPos].menu.add_radiobutton(label='0.4', command=self.update, variable=self.contentsET[self.contentsPos], value=0.225)
        self.mb[self.contentsPos].menu.add_radiobutton(label='0.5', command=self.update, variable=self.contentsET[self.contentsPos], value=0.325)
        self.mb[self.contentsPos].menu.add_radiobutton(label='0.6', command=self.update, variable=self.contentsET[self.contentsPos], value=0.425)
        self.mb[self.contentsPos].menu.add_radiobutton(label='0.8', command=self.update, variable=self.contentsET[self.contentsPos], value=0.625)
        self.mb[self.contentsPos].menu.add_radiobutton(label='1', command=self.update, variable=self.contentsET[self.contentsPos], value=0.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='1.3', command=self.update, variable=self.contentsET[self.contentsPos], value=1.125)
        self.mb[self.contentsPos].menu.add_radiobutton(label='1.6', command=self.update, variable=self.contentsET[self.contentsPos], value=1.425)
        self.mb[self.contentsPos].menu.add_radiobutton(label='2', command=self.update, variable=self.contentsET[self.contentsPos], value=1.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='2.5', command=self.update, variable=self.contentsET[self.contentsPos], value=2.325)
        self.mb[self.contentsPos].menu.add_radiobutton(label='3.2', command=self.update, variable=self.contentsET[self.contentsPos], value=3.025)
        self.mb[self.contentsPos].menu.add_radiobutton(label='4', command=self.update, variable=self.contentsET[self.contentsPos], value=3.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='5', command=self.update, variable=self.contentsET[self.contentsPos], value=4.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='6', command=self.update, variable=self.contentsET[self.contentsPos], value=5.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='8', command=self.update, variable=self.contentsET[self.contentsPos], value=7.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='10', command=self.update, variable=self.contentsET[self.contentsPos], value=9.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='13', command=self.update, variable=self.contentsET[self.contentsPos], value=12.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='15', command=self.update, variable=self.contentsET[self.contentsPos], value=14.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='20', command=self.update, variable=self.contentsET[self.contentsPos], value=19.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='25', command=self.update, variable=self.contentsET[self.contentsPos], value=24.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='30', command=self.update, variable=self.contentsET[self.contentsPos], value=29.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='35', command=self.update, variable=self.contentsET[self.contentsPos], value=34.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='40', command=self.update, variable=self.contentsET[self.contentsPos], value=39.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='45', command=self.update, variable=self.contentsET[self.contentsPos], value=44.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='50', command=self.update, variable=self.contentsET[self.contentsPos], value=49.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='55', command=self.update, variable=self.contentsET[self.contentsPos], value=55.825)
        self.mb[self.contentsPos].menu.add_radiobutton(label='60', command=self.update, variable=self.contentsET[self.contentsPos], value=59.825)
        
        self.camBack.append(tk.IntVar())
        self.camCheck = tk.Checkbutton(self.seperatorBody_1, text = "Reverse", variable=self.camBack[self.contentsPos], onvalue =1, offvalue = 0)
        self.camCheck.grid(column=4, row=self.gridPos, sticky=tk.W)

        self.contentsProF.append(tk.IntVar())
        self.proFrames = tk.Entry(self.seperatorBody_1, justify=tk.RIGHT, textvariable=self.contentsProF[self.contentsPos])
        self.proFrames.grid(column=5, row=self.gridPos)

        self.proBack.append(tk.IntVar())
        self.proCheck = tk.Checkbutton(self.seperatorBody_1, text = "Reverse", variable=self.proBack[self.contentsPos], onvalue =1, offvalue = 0)
        self.proCheck.grid(column=6, row=self.gridPos, sticky=tk.W)

        self.cycles.append(tk.IntVar())
        self.cycleBlock = tk.Entry(self.seperatorBody_1, justify=tk.RIGHT, textvariable=self.cycles[self.contentsPos])
        self.cycleBlock.grid(column=7, row=self.gridPos)    
    
    def footWidgets(self):  
        self.addButton = tk.Button(self.seperatorFoot_1, text='+',padx=1,pady=1, height=1, width=2, command=self.inputWidgets)
        self.addButton.grid(column=0, row=0, sticky=tk.W)

        self.runButton = tk.Button(self.seperatorFoot_3, text='RUN', fg='red', command=self.runProgram)
        self.runButton.grid(column=0, row=0, sticky=tk.W)

        self.testButton = tk.Button(self.seperatorFoot_3, text='test', fg='green', command=self.testProgram)
        self.testButton.grid(column=1, row=0, sticky=tk.W)

        self.totalcycleslabel = tk.Label(self.seperatorFoot_2, text='Total Cycles:')
        self.totalcycleslabel.grid(column=0, row=0)
        self.totalcycles = tk.IntVar()
        self.totalcycleBlock = tk.Entry(self.seperatorFoot_2, justify=tk.RIGHT, textvariable=self.totalcycles)
        self.totalcycleBlock.grid(column=1, row=0)

        self.man = tk.Button(self.seperatorFoot_4, text='Manual Mode', command=self.manual)
        self.man.grid(column=0, row=0)
        self.camFW = tk.Button(self.seperatorFoot_4, text='Camera FW', state=tk.NORMAL, command=self.camForward)
        self.camFW.grid(column=1, row=0)
        self.camBW = tk.Button(self.seperatorFoot_4, text='Camera BW', state=tk.NORMAL, command=self.camBackward)
        self.camBW.grid(column=2, row=0)
        self.proFW = tk.Button(self.seperatorFoot_4, text='Projector FW', state=tk.NORMAL, command=self.proForward)
        self.proFW.grid(column=3, row=0)
        self.proBW = tk.Button(self.seperatorFoot_4, text='Projector BW',state=tk.NORMAL, command=self.proBackward)
        self.proBW.grid(column=4, row=0, sticky=tk.W) 

    def update(self):
        lstLength = len(self.modON) #Determine number of modules in interface
        for a in range (0, lstLength):
            self.mb[a]["text"] = self.contentsET[a].get()+.175
    
    def manual(self):
        self.camReset ['state'] = tk.DISABLED
        self.proReset ['state'] = tk.DISABLED
        self.camFW ['state'] = tk.DISABLED
        self.camBW ['state'] = tk.DISABLED
        self.proFW ['state'] = tk.DISABLED
        self.proBW ['state'] = tk.DISABLED
        input_camButton = GPIO.input(15)
        input_proButton = GPIO.input(19)
        input_camFB = GPIO.input(23)
        input_proFB = GPIO.input(26)
        time.sleep(.5)
        while input_camButton or input_proButton == True:
            time.sleep(.5)
            input_camButton = GPIO.input(15)
            input_proButton = GPIO.input(19)
            input_camFB = GPIO.input(23)
            input_proFB = GPIO.input(26)
            if input_camButton == False:
                if input_camFB == False:
                    self.camBackward()
                else:
                    self.camForward()
            if input_proButton == False:
                if input_proFB == False:
                    self.proBackward()
                else:
                    self.proForward()
            if GPIO.input(21)== False:
                self.footWidgets()
                self.headWidgets()
                break

        
    def runProgram(self):        
        lstLength = len(self.modON) #Determine number of modules in interface
        for a in range(0, self.totalcycles.get()):
            if GPIO.input(21) == False:
                break
            index = 0
            for b in range(0, lstLength):
                for c in range(0, self.cycles[index].get()):
                    if GPIO.input(21)== False:
                        break
                    if self.modON[index].get() == 1:
                        for d in range(0, self.contentsCamF[index].get()):
                            self.exp = self.contentsET[index].get()
                            if self.camBack[index].get() == 0:
                                JK_Application.camForward(self)
                            else:
                                JK_Application.camBackward(self)
                            time.sleep(.5)
                        for e in range(0, self.contentsProF[index].get()):
                            if self.proBack[index].get() == 0:
                                JK_Application.proForward(self)
                            else:
                                JK_Application.proBackward(self)
                            time.sleep(.5)
                index+=1

    def testProgram(self):   

        grid1 = 10
        self.window_1=tk.Toplevel()

        self.canv = tk.Canvas(self.window_1, width=500, height=800, scrollregion=(0, 0, 0, 0))
        self.canv.grid()
        self.scrollY = tk.Scrollbar(self.window_1, orient=tk.VERTICAL, command=self.canv.yview)
        self.scrollY.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.canv['yscrollcommand'] = self.scrollY.set

        lstLength = len(self.modON) #Determine number of modules in interface

        self.lab1 = tk.Label(self.window_1, text='# of Modules: ')
        self.scrollWin = self.canv.create_window(110, grid1, window=self.lab1)
        self.lab2 = tk.Label(self.window_1, text=lstLength)
        self.scrollWin = self.canv.create_window(400, grid1, window=self.lab2)

        
        for a in range(0, self.totalcycles.get()):
           
            index=0
            grid1+=30
            
            self.lab3 = tk.Label(self.window_1, text='Main Loop: ')
            self.scrollWin = self.canv.create_window(110, grid1, window=self.lab3)
            self.lab4 = tk.Label(self.window_1, text=a+1)
            self.scrollWin = self.canv.create_window(400, grid1, window=self.lab4)

            for b in range(0, lstLength):
                grid1+=20
                
                self.lab5 = tk.Label(self.window_1, text='Module: ')
                self.scrollWin = self.canv.create_window(110, grid1, window=self.lab5)
                self.lab6 = tk.Label(self.window_1, text=index+1)
                self.scrollWin = self.canv.create_window(400, grid1, window=self.lab6)

                for c in range(0, self.cycles[index].get()):
                    if self.modON[index].get() == 1:
                        for d in range(0, self.contentsCamF[index].get()):

                            grid1+=20

                            if self.camBack[index].get() == 0:
                                
                                self.lab7 = tk.Label(self.window_1, text='Camera Forward, Exposure Time: ')
                                self.scrollWin = self.canv.create_window(110, grid1, window=self.lab7)
                                self.lab8 = tk.Label(self.window_1, text=self.contentsET[index].get()+.175)
                                self.scrollWin = self.canv.create_window(400, grid1, window=self.lab8)

                            else:

                                self.lab7 = tk.Label(self.window_1, text='Camera Backward, Exposure Time: ')
                                self.scrollWin = self.canv.create_window(110, grid1, window=self.lab7)
                                self.lab8 = tk.Label(self.window_1, text=self.contentsET[index].get()+.175)
                                self.scrollWin = self.canv.create_window(400, grid1, window=self.lab8)

                        for e in range(0, self.contentsProF[index].get()):

                            grid1+=20

                            if self.proBack[index].get() == 0:

                                self.lab9 = tk.Label(self.window_1, text='Projector Forward')
                                self.scrollWin = self.canv.create_window(110, grid1, window=self.lab9)

                            else:
                                self.lab10 = tk.Label(self.window_1, text='Projector Backward')
                                self.scrollWin = self.canv.create_window(110, grid1, window=self.lab10)
                    else:

                        grid1+=20

                        self.lab7 = tk.Label(self.window_1, text='Module Skipped')
                        self.scrollWin = self.canv.create_window(110, grid1, window=self.lab7)
                index+=1 
                self.canv['scrollregion'] = (0, 0, 0, grid1)
                
    def camForward(self):
        self.totalcamFrames+=1
        self.camFrames = tk.StringVar()
        self.camFrames.set(self.totalcamFrames)
        self.camCount["textvariable"] = self.camFrames
        GPIO.output(16, True)
        time.sleep(.025)
        input_camPos = GPIO.input(11)
        while input_camPos == True:
            input_camPos = GPIO.input(11)
            input_camET = GPIO.input(13)
            if input_camET == False:
                GPIO.output(16, False)
                time.sleep(self.exp)
                GPIO.output(16, True)
                time.sleep(.025)
            else:
                GPIO.output(16, True)   
        GPIO.output(16, False)

    def camBackward(self):
        self.totalcamFrames-=1
        self.camFrames = tk.StringVar()
        self.camFrames.set(self.totalcamFrames)
        self.camCount["textvariable"] = self.camFrames
 
        GPIO.output(12, True)
        time.sleep(.025)
        input_camPos = GPIO.input(11)
        while input_camPos == True:
            input_camPos = GPIO.input(11)
            input_camET = GPIO.input(13)
            if input_camET == False:
                GPIO.output(12, False)
                time.sleep(self.exp)
                GPIO.output(12, True)
                time.sleep(.025)
            else:
                GPIO.output(12, True)
        GPIO.output(12, False)
        
    def proForward(self):
        self.totalproFrames+=1
        self.proFrames = tk.StringVar()
        self.proFrames.set(self.totalproFrames)
        self.proCount["textvariable"] = self.proFrames
 
        GPIO.output(22, True)
        time.sleep(.025)
        input_camPos = GPIO.input(7)
        while input_camPos == True:
            input_camPos = GPIO.input(7)
            GPIO.output(22, True)
        GPIO.output(22, False)

    def proBackward(self):
        self.totalproFrames-=1
        self.proFrames = tk.StringVar()
        self.proFrames.set(self.totalproFrames)
        self.proCount["textvariable"] = self.proFrames
 
        GPIO.output(18, True)
        time.sleep(.025)
        input_camPos = GPIO.input(7)
        while input_camPos == True:
            input_camPos = GPIO.input(7)
            GPIO.output(18, True)
        GPIO.output(18, False)

    def camcountReset(self):
        self.totalcamFrames=0
        self.camFrames = tk.StringVar()
        self.camFrames.set(self.totalcamFrames)
        self.camCount["textvariable"] = self.camFrames
  
    def procountReset(self):
        self.totalproFrames=0
        self.proFrames = tk.StringVar()
        self.proFrames.set(self.totalproFrames)
        self.proCount["textvariable"] = self.proFrames


if __name__ == '__main__':
    app = App()
    app.master.title('Charlie Control')
    app.mainloop()
