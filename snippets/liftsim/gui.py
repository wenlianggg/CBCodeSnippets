# Wen Liang Goh - https://github.com/wenlianggg
# 18 April 2020
# Not a very good attempt at simulating lift movements


from tkinter import Label, Button, Text, Checkbutton


class LiftSimGUI:
    def __init__(self, master, numFloors, numLifts):
        # Lift Logic
        # --------------------
        self.lifts = [1] * numLifts

        # Window items go here
        # --------------------
        self.window = master
        self.window.title("Lift Simulator")
        self.window.grid_columnconfigure(1, minsize=50)
        self.window.grid_columnconfigure(numLifts + 2, minsize=50)
        self.window.grid_rowconfigure(numFloors + 3, minsize=50)

        titleLbl = Label(self.window, text="Lift Simulator", fg="red", font=("Arial", 12))
        titleLbl.grid(column=0, row=0)

        liftInputBox = [0] * numLifts
        for liftNum in range(numLifts):
            # Lift Status - Lift x
            liftStatus = Label(self.window, text=f"Lift {liftNum + 1}")
            liftStatus.grid(column=liftNum + 1, row=1)
            # Text box for entering lift destination
            liftInputBox[liftNum] = Text(self.window, height=1, width=5)
            liftInputBox[liftNum].grid(column=liftNum + 1, row=2)

        self.checkBtn = [[0] * (numFloors + 1) for _ in range(numLifts)]
        floorName = [0] * (numFloors + 1)
        self.btnUp = [0] * (numFloors + 1)
        self.btnDown = [0] * (numFloors + 1)

        # Generate UI
        for floorNum in range(numFloors, 0, -1):
            print(f'Generating level: {floorNum}')
            rowNumber = numFloors - floorNum + 3

            floorName[floorNum] = Label(self.window, text=f'Level: {floorNum}')
            floorName[floorNum].grid(column=0, row=rowNumber)

            # Generate check buttons
            for i in range(numLifts):
                self.checkBtn[i][floorNum] = Checkbutton(self.window)
                self.checkBtn[i][floorNum].grid(column=i + 1, row=rowNumber)
                # Lifts to be stationed at first floor
                if floorNum == 1:
                    self.checkBtn[i][floorNum].select()

            # Generate lift request UP buttons, except for the top floor
            if floorNum != numFloors:
                self.btnUp[floorNum] = Button(self.window, text="▲", command=lambda floorNum=floorNum: self.GoUp(floorNum))
                self.btnUp[floorNum].grid(column=numLifts + 1, row=rowNumber)

            # Generate lift request DOWN buttons, except for the bottom floor
            if floorNum != 1:
                self.btnDown[floorNum] = Button(self.window, text="▼", command=lambda floorNum=floorNum: self.GoDown(floorNum))
                self.btnDown[floorNum].grid(column=numLifts + 2, row=rowNumber)

    def moveLift(self, liftNum, dest):
        currentFloor = self.lifts[liftNum]
        print(f"Lift number {liftNum} going to level {dest}. Currently at {currentFloor}")
        if currentFloor > dest:
            self.checkBtn[liftNum][currentFloor].deselect()
            self.checkBtn[liftNum][currentFloor - 1].select()
            self.lifts[liftNum] = currentFloor - 1
            self.window.after(500, self.moveLift, liftNum, dest)
        if currentFloor < dest:
            self.checkBtn[liftNum][currentFloor].deselect()
            self.checkBtn[liftNum][currentFloor + 1].select()
            self.lifts[liftNum] = currentFloor + 1
            self.window.after(500, self.moveLift, liftNum, dest)
        if currentFloor == dest:
            self.lifts[liftNum] = dest

    def findClosestLift(self, floorNum):
        print(f"Finding closest lift to level {floorNum}")
        closestLift = self.lifts.index(min(self.lifts, key=lambda x: abs(x - floorNum)))
        return closestLift  # Find closest value

    def GoUp(self, floorNum: int):
        print(f"Going up requested from floor {floorNum}!")
        closestLift = self.findClosestLift(floorNum)
        self.moveLift(closestLift, floorNum)

    def GoDown(self, floorNum: int):
        print(f"Going down requested from floor {floorNum}!")
        closestLift = self.findClosestLift(floorNum)
        self.moveLift(closestLift, floorNum)

    def GoDest(self, floorNum: int, dest: int):
        print(f"Going from level {floorNum} to {dest}")
