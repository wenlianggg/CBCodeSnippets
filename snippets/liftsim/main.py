# Wen Liang Goh - https://github.com/wenlianggg
# 18 April 2020
# Not a very good attempt at simulating lift movements

from tkinter import Tk
from gui import LiftSimGUI

TOTAL_FLOORS = 20
LIFTS_AVAIL = 3

root = Tk()
gui = LiftSimGUI(root, TOTAL_FLOORS, LIFTS_AVAIL)

root.mainloop()
