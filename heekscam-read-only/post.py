# coding=CP1252
#English language or it's variant detected in Microsoft Windows
import sys
sys.path.insert(0,'C:\\Dev\\HeeksCAM')
import math
sys.path.insert(0,'C:\\Dev\\HeeksCAM/Boolean')
import area
area.set_units(1)
from nc.nc import *
from nc.emc2b import *

output('C:\\Users\\Dan\\AppData\\Local\\Temp\\test.ngc')
program_begin(1, 'Program 1')
absolute()
metric()
set_plane(0)

#(3 mm Slot Cutter)
tool_defn( 1, '3 mm Slot Cutter', {'corner radius':0, 'cutting edge angle':0, 'cutting edge height':12, 'diameter':3, 'flat radius':0, 'material':1, 'tool length offset':127, 'type':3, 'name':'3 mm Slot Cutter'})
#(4 mm Drill Bit)
tool_defn( 2, '4 mm Drill Bit', {'corner radius':0, 'cutting edge angle':59, 'cutting edge height':50.8, 'diameter':4, 'flat radius':0, 'material':1, 'tool length offset':100, 'type':0, 'name':'4 mm Drill Bit'})
#(6 mm Slot Cutter)
tool_defn( 3, '6 mm Slot Cutter', {'corner radius':0, 'cutting edge angle':0, 'cutting edge height':30, 'diameter':6, 'flat radius':0, 'material':1, 'tool length offset':100, 'type':3, 'name':'6 mm Slot Cutter'})
program_end()
