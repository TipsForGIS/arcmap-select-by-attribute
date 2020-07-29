# Ahmad Aburizaiza
# GGS 650
# Project

from Tkinter import * # This module is used to deal with graphics.
import tkFileDialog # This module is used to enable the use of file dialogs.
from tkMessageBox import * # This module is used to generate message boxes.
import arcgisscripting


#----------------------------------------------------------
# This is the first button in the main menu "Select by Attribute"
#----------------------------------------------------------
def SAButClick():

  windowsCreated = FALSE
  for i in windows:
    if i == "s a":
      windowsCreated = TRUE

  if windowsCreated == TRUE:
    pass
  else:
    global sARoot
    sARoot = Tk()
    sARoot.geometry("600x340+470+30")
    sARoot.title("Select by attribute")
    sARoot.resizable(0, 0)
    sARoot.protocol("WM_DELETE_WINDOW", closeSA)
    foundInWindows = FALSE
    for i in windows:
      if i == "s a":
        foundInWindows = TRUE
    
    if foundInWindows == FALSE:
      windows.append("s a")

    # Create 6 frames to organize the compoenents
    layerFrame = Frame(sARoot)
    fieldsFrame = Frame(sARoot)
    uniqueFrame = Frame(sARoot)
    commandFrame = Frame(sARoot)
    whereClauseFrame = Frame(sARoot)
    butFrame = Frame(sARoot)

    # The layer frame
    global layerLabel
    layerLabel = Label(layerFrame,text="Layer",font=("Verdana", 16))
    layerLabel.pack(side=LEFT)

    global layerBut
    layerBut = Button(layerFrame, text="Open Layer", command = openLayer,font=("Verdana", 12))
    layerBut.pack(side=RIGHT)

    global layerText
    layerText = Entry(layerFrame, font=("Verdana", 12))
    layerText.pack(fill=X)

    # Generate and pack the fields frame
    global fieldsLabel
    fieldsLabel = Label(fieldsFrame,text="Fields",font=("Verdana", 16))
    fieldsLabel.pack(side=LEFT)
    fieldsLabel['state'] = DISABLED

    global fieldBut
    fieldBut = Button(fieldsFrame, text="selectField", command = selectField,font=("Verdana", 12))
    fieldBut.pack(side=RIGHT)
    fieldBut['state'] = DISABLED

    global fieldsLBox
    fieldsLBox = Listbox(fieldsFrame,selectmode=SINGLE,exportselection=0, height=5)
    fieldsLBox['state'] = DISABLED
    fieldsLBox.pack(fill=X)

    #Generate and pack uniqueFrame
    global uniqueLabel
    uniqueLabel = Label(uniqueFrame,text="Unique values",font=("Verdana", 16))
    uniqueLabel.pack(side=LEFT)
    uniqueLabel['state'] = DISABLED

    global uniqueLBox
    uniqueLBox = Listbox(uniqueFrame, selectmode=SINGLE,exportselection=0, height=5)
    uniqueLBox['state'] = DISABLED
    uniqueLBox.pack(fill=X)

    # The command frame
    global commandLabel
    commandLabel = Label(commandFrame,text="Commands",font=("Verdana", 16))
    commandLabel.pack(side=LEFT)
    commandLabel['state'] = DISABLED

    global commandsLBox
    commandsLBox = Listbox(commandFrame,selectmode=SINGLE,exportselection=0, height=5)
    commandsLBox['state'] = DISABLED
    commandsLBox.pack(fill=X)

    # The whereClause frame
    global whereClauseLabel
    whereClauseLabel = Label(whereClauseFrame,text="Where Clause",font=("Verdana", 16))
    whereClauseLabel.pack(side=LEFT)
    whereClauseLabel['state'] = DISABLED

    global whereClauseText
    whereClauseText = Entry(whereClauseFrame,font=("Verdana", 12))
    whereClauseText.pack(fill=X)
    whereClauseText['state'] = DISABLED

    # The but frame
    global createExpBut
    createExpBut = Button(butFrame, text="Create Expression", command = createExp,font=("Verdana", 12))
    createExpBut.pack(side=LEFT)
    createExpBut['state'] = DISABLED

    global clearWCBut
    clearWCBut = Button(butFrame, text="Clear", command = clearWClause,font=("Verdana", 12))
    clearWCBut.pack(side=LEFT)
    clearWCBut['state'] = DISABLED

    global closeSABut
    closeSABut = Button(butFrame, text="Close", command = closeSA,font=("Verdana", 12))
    closeSABut.pack(side=RIGHT)

    global createLayerBut
    createLayerBut = Button(butFrame, text="Create Layer", command = createLayer,font=("Verdana", 12))
    createLayerBut.pack(side=RIGHT)
    createLayerBut['state'] = DISABLED

    # Pack the layer into the root
    layerFrame.pack(fill=X)
    fieldsFrame.pack(fill=X)
    uniqueFrame.pack(fill=X)
    commandFrame.pack(fill=X)
    whereClauseFrame.pack(fill=X)
    butFrame.pack(side=TOP)

    
    # Run the window
    sARoot.mainloop()

# The below function runs the open layer button in "select by attribute". It gets the name of the shapefile from a the open file dialog.
# It also generates the fields names in the appropriate listbox and enables it with its button.
def openLayer():
  
  global myShpFile
  global mySelectedShpFile
  myShpFile = tkFileDialog.askopenfilename(title="Select a shape file", initialdir=".",filetypes=[('Shape Files','*.shp'),('Shape Files','*.SHP')])
  fieldBut['state'] = NORMAL
  fieldsLabel['state'] = NORMAL
  fieldsLBox['state'] = NORMAL
  mySelectedShpFile = myShpFile.replace(".shp","_SA.shp")
  layerText.insert(0,myShpFile)

  gp = arcgisscripting.create()
  gp.OverwriteOutput = 1
  fields = gp.listfields(myShpFile)
  field = fields.Next()
  global listOfFields
  listOfFields = []
  while field:
    if field.name != 'Shape':
      listOfFields.append(field.Name)
    field = fields.Next() 

  fieldsLBox.delete(0, END)
  for i in listOfFields:
    fieldsLBox.insert(END, i)

  fieldsLBox.selection_set(first=0)

# The below function runs the select field button in "select by attribute". It generates the unique values of a field into its listbox.
# It also enables the rest of the components in the window including the where clause text.
def selectField():

  uniqueLBox['state'] = NORMAL
  uniqueLabel['state'] = NORMAL
  commandLabel['state'] = NORMAL
  commandsLBox['state'] = NORMAL
  whereClauseLabel['state'] = NORMAL
  whereClauseText['state'] = NORMAL
  createExpBut['state'] = NORMAL
  clearWCBut['state'] = NORMAL
  createLayerBut['state'] = NORMAL
  
  gp = arcgisscripting.create()
  gp.OverwriteOutput = 1
  # create empty list
  global listOfUVals
  listOfUVals = []
  rows = gp.SearchCursor(myShpFile)
  row = rows.Next()
  while row:
    # pulling value from row
    rowvalue = row.GetValue(fieldsLBox.get('active'))
    if rowvalue not in listOfUVals:
        listOfUVals.append(rowvalue)
    else:
        pass
    row = rows.Next()

  uniqueLBox.delete(0, END)
  for i in listOfUVals:
    uniqueLBox.insert(END, i)

  uniqueLBox.selection_set(first=0)
  
  listOfCommands = ["=", "<", ">", "<=",">=","<>"]

  commandsLBox.delete(0, END)
  for i in listOfCommands:
    commandsLBox.insert(END, i)
  commandsLBox.selection_set(first=0)
  #sARoot.update()

# This function runs the "create expression" button. It generates the where clause and add it to its textbox. 
def createExp():
  whereClauseText.delete(0,END)
  global whereCExp
  if is_numeric(uniqueLBox.get('active')):
    whereCExp = '"' + fieldsLBox.get('active') + '" ' + commandsLBox.get('active') + ' ' + str(uniqueLBox.get('active'))
  else:
    whereCExp = '"' + fieldsLBox.get('active') + '" ' + commandsLBox.get('active') + " \'" + str(uniqueLBox.get('active')) + "\'" 

  whereClauseText.insert(0,whereCExp)

# This function runs th clear button to clear the where clause text.
def clearWClause():
  whereClauseText.delete(0,END)

# This runs the create layer button. It creates an output shapefile based on the where clause statement.
def createLayer():
  gp = arcgisscripting.create()
  gp.OverwriteOutput = 1
  # For shapefile expression, fields are double quoted (") and text values are single quoted (')
  gp.select_analysis(myShpFile , mySelectedShpFile, whereCExp)
  showinfo("Selection Created", "A new shapefile was created succefully named:\n" + mySelectedShpFile + "\nfrom the shapefile:\n" + myShpFile + "\nusing the where clause:\n" + whereCExp)

# This function checks if a string value is a valid number
def is_numeric(value):
  return str(value).replace(".", "").replace("-", "").isdigit()

# The close button for "select by attribute" where it makes sure that the window is removed from the windows list when clicked.
def closeSA():

  for i in windows:
    if i == "s a":
      windows.remove(i)
  sARoot.destroy() 


#----------------------------------------------------------
# This is the second button in the main menu "Select by Location"
#----------------------------------------------------------
def SLButClick():
  windowsCreated = FALSE
  for i in windows:
    if i == "s l":
      windowsCreated = TRUE

  if windowsCreated == TRUE:
    pass
  else: 
    global sLRoot
    sLRoot = Tk()
    sLRoot.geometry("600x110+470+30")
    sLRoot.title("Select by location")
    sLRoot.resizable(0, 0)
    sLRoot.protocol("WM_DELETE_WINDOW", closeSL)
    foundInWindows = FALSE
    for i in windows:
      if i == "s l":
        foundInWindows = TRUE
    if foundInWindows == FALSE:
      windows.append("s l")

    inputLayerFrame = Frame(sLRoot, width = 100)
    maskLayerFrame = Frame(sLRoot, width = 100)
    maskButFrame = Frame(sLRoot, width = 100)

    # The input layer frame
    global inputLayerLabel
    inputLayerLabel = Label(inputLayerFrame,text="Layer",font=("Verdana", 16))
    inputLayerLabel.pack(side=LEFT)

    global inputBut
    inputBut = Button(inputLayerFrame, text="Open Input Layer", command = inputBut,font=("Verdana", 12))
    inputBut.pack(side=RIGHT)
    
    global inputLayerText
    inputLayerText = Entry(inputLayerFrame, font=("Verdana", 12))
    inputLayerText.pack(fill=X)


    # The mask layer frame
    global maskLayerLabel
    maskLayerLabel = Label(maskLayerFrame,text="Layer",font=("Verdana", 16))
    maskLayerLabel.pack(side=LEFT)

    global maskBut
    maskBut = Button(maskLayerFrame, text="Open Mask Layer", command = maskBut,font=("Verdana", 12))
    maskBut.pack(side=RIGHT)
    
    global maskLayerText
    maskLayerText = Entry(maskLayerFrame, font=("Verdana", 12))
    maskLayerText.pack(fill=X)


    # The mask buttons frame
    global runBut
    runBut = Button(maskButFrame, text="Run", command = runRect,font=("Verdana", 12))
    runBut.pack(side=LEFT)
    runBut['state'] = DISABLED

    global closeSLBut
    closeSLBut = Button(maskButFrame, text="Close", command = closeSL,font=("Verdana", 12))
    closeSLBut.pack(side=LEFT)

    inputLayerFrame.pack(fill=X)
    maskLayerFrame.pack(fill=X)
    maskButFrame.pack(side=BOTTOM)

# The layer input button loads the shapefile name from an open file dialog
def inputBut():

  global myShpFileI
  myShpFileI = tkFileDialog.askopenfilename(title="Select a shape file", initialdir=".",filetypes=[('Shape Files','*.shp'),('Shape Files','*.SHP')])
  global myShpFileO
  myShpFileO = myShpFileI.replace(".shp","_SL.shp")
  inputLayerText.insert(0,myShpFileI)

  if maskLayerText.get() == '':
    pass
  else:
    runBut['state'] = NORMAL

# The mask input button loads the shapefile name from an open file dialog
def maskBut():
  global myShpFileR
  myShpFileR = tkFileDialog.askopenfilename(title="Select a shape file", initialdir=".",filetypes=[('Shape Files','*.shp'),('Shape Files','*.SHP')])
  maskLayerText.insert(0,myShpFileR)

  if inputLayerText.get() == '':
    pass
  else:
    runBut['state'] = NORMAL

# The run button creates an output shapefile from the input and mask shapefiles.
def runRect():

  gp = arcgisscripting.create()
  gp.OverwriteOutput = 1
  #parts = myShpFileI.rpartition("/")
  #folderName = parts[0]

  gp.MakeFeatureLayer(myShpFileI,"inputLayer")
  gp.MakeFeatureLayer(myShpFileR,"rectLayer")

  gp.SelectLayerByLocation("inputLayer","intersect", "rectLayer")
  gp.CopyFeatures("inputLayer",myShpFileO)

  showinfo("Selection Created", "A new shapefile was created succefully named:\n" + myShpFileO + "\nfrom the shapefile:\n" + myShpFileI)

# The close button for "select by location" where it makes sure that the window is removed from the windows list when clicked.
def closeSL():

  for i in windows:
    if i == "s l":
      windows.remove(i)
  sLRoot.destroy()
  
#----------------------------------------------------------
# This is the third button in the main menu "Close Application"
#----------------------------------------------------------
def closeApp():

  for i in windows:
    if i == "s a":
      sARoot.destroy()
    elif i == "s l":
      sLRoot.destroy()
    else:
      mainRoot.destroy()

#----------------------------------------------------------
# Main program
#----------------------------------------------------------

mainRoot = Tk()
global windows
windows = []
mainRoot.geometry("450x270+3+30")
mainRoot.resizable(0, 0)
mainRoot.protocol("WM_DELETE_WINDOW", closeApp)
mainRoot.title("Select by attribute or location")

foundInWindows = FALSE
for i in windows:
  if i == "main":
    foundInWindows = TRUE

if foundInWindows == FALSE:
  windows.append("main")


mainLabelFrame = Frame(mainRoot, width = 100)
mainButtonsFrame = Frame(mainRoot, width = 100)
mainButtonsFrame2 = Frame(mainRoot, width = 100)

mainLabel = Label(mainLabelFrame,text="This script creates a selection layer\nby either attribute or location\n\nGGS GMU - GGS 650\nCreated by\nAhmad Aburizaiza\n",font=("Verdana", 16))
mainLabel.pack()

openSABut = Button(mainButtonsFrame, text="Select by attribute", command = SAButClick,font=("Verdana", 16))
openSABut.pack(side=LEFT)

openSLBut = Button(mainButtonsFrame, text="Select by location", command = SLButClick,font=("Verdana", 16))
openSLBut.pack(side=RIGHT)

closeAppBut = Button(mainButtonsFrame2, text="Close Application", command = closeApp,font=("Verdana", 12))
closeAppBut.pack()

mainLabelFrame.pack()
mainButtonsFrame.pack()
mainButtonsFrame2.pack()

mainRoot.mainloop()
