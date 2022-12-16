import random
import threading
import tkinter as tk
import time


class TypeSpeedGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Typing SPeed Test Application')
        self.root.geometry('800x600')

        self.texts = open('sentences.txt', 'r').read().split('\n')

        self.frame = tk.Frame(self.root)

        self.HeadingLabel = tk.Label(
            self.frame, text="Speed Type Test", font=('Segoe Script', 34), fg='#CC3636')
        self.HeadingLabel.grid(row=0, column=0, columnspan=2)

        self.sampleLabel = tk.Label(self.frame, text=random.choice(
            self.texts), font=('Helvetica', 18), height=2)
        self.sampleLabel.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.inputEntry = tk.Entry(
            self.frame, width=40, font=('Helvetica', 24))
        self.inputEntry.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.inputEntry.bind('<KeyRelease>', self.start)

        self.speedLabel = tk.Label(
            self.frame, text="Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM", font=('Helvetica', 18))
        self.speedLabel.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.resetButton = tk.Button(
            self.frame, text="Reset", command=self.reset)
        self.resetButton.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False

        self.root.mainloop()

    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.timeThread)
                t.start()
        if not self.sampleLabel.cget('text').startswith(self.inputEntry.get()):
            self.inputEntry.config(fg='#F57328')
        else:
            self.inputEntry.config(fg='black')

        if self.inputEntry.get() == self.sampleLabel.cget('text'):
            self.running = False
            self.inputEntry.config(fg='#367E18')

    def timeThread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.inputEntry.get()) / self.counter
            cpm = cps * 60
            wps = len(self.inputEntry.get().split(' ')) / self.counter
            wpm = wps * 60
            self.speedLabel.config(
                text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM\n{wps:.2f} WPS\n{wpm:.2f} WPM")

    def reset(self):
        self.running = False
        self.counter = 0
        self.speedLabel.config(
            text='Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM')
        self.sampleLabel.config(text=random.choice(self.texts))
        self.inputEntry.delete(0, tk.END)


TypeSpeedGUI()
