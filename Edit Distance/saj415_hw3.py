from Tkinter import *
import tkMessageBox

class Application(Frame):

	def __init__(self, master):
		Frame.__init__(self, master)
		self.grid()
		self.editDistVar = BooleanVar() #Boolean variable for edit distance checkbox
		self.backtrackVar = BooleanVar() #Boolean variable for backtrack checkbox
		self.strAlignVar = BooleanVar() #Boolean variable for alignment checkbox
		self.create_widgets()
		self.editDistMatrix = '' #Global variable to store final edit distance matrix
		self.backtrackMatrix = '' #Global variable to store final backtracking matrix
		self.stringAlignment = '' #Global variable to store final string alignment

	def create_widgets(self):
		#Source text label
		self.firstStr_lbl = Label(self, text = "Source filename")
		self.firstStr_lbl.grid(row = 0, column = 0, sticky = W)
		#Source text entry
		self.firstStr_ent = Entry(self, width = 12)
		self.firstStr_ent.grid(row = 0, column = 1, sticky = E)
		#Target text label
		self.secondStr_lbl = Label(self, text = "Target filename")
		self.secondStr_lbl.grid(row = 1, column = 0, sticky = W)
		#Target text entry
		self.secondStr_ent = Entry(self, width = 12)
		self.secondStr_ent.grid(row = 1, column = 1, sticky = E)
		#Compute edit distance button
		self.compute = Button(self, text = "Compute", command = self.initialize)
		self.compute.grid(row = 0, column = 2, sticky = 'NEWS')
		#Clear button
		self.compute = Button(self, text = "Clear", command = self.clearOutputWindow)
		self.compute.grid(row = 1, column = 2, sticky = 'NEWS')
		#Cost option label
		self.costOpt_lbl = Label(self, text = "Cost Options:")
		self.costOpt_lbl.grid(row = 4, column = 0, sticky = W)
		#Cost of insertion label
		self.cins_lbl = Label(self, text = "Insertion")
		self.cins_lbl.grid(row = 5, column = 0, sticky = 'NEWS')
		#Cost of insertion scale
		self.cins_scale = Scale(self, orient=HORIZONTAL, from_ = 1, to = 10)
		self.cins_scale.grid(row = 5, column = 1, sticky = W)
		#Cost of deletion label
		self.cdel_lbl = Label(self, text = "Deletion")
		self.cdel_lbl.grid(row = 6, column = 0, sticky = 'NEWS')
		#Cost of deletion scale
		self.cdel_scale = Scale(self, orient=HORIZONTAL, from_ = 1, to = 10)
		self.cdel_scale.grid(row = 6, column = 1, sticky = W)
		#Cost of substitution label
		self.csub_lbl = Label(self, text = "Substitution")
		self.csub_lbl.grid(row = 7, column = 0, sticky = 'NEWS')
		#Cost of substitution scale
		self.csub_scale = Scale(self, orient=HORIZONTAL, from_ = 1, to = 10)
		self.csub_scale.grid(row = 7, column = 1, sticky = W)
		#Output options label
		self.outputOpt_lbl = Label(self, text = "Ouptut Options:")
		self.outputOpt_lbl.grid(row = 4, column = 2, sticky = W)
		#Edit distance matrix checkbox
		self.editDist = Checkbutton(self, text = "Edit Distance Matrix", variable = self.editDistVar)
		self.editDist.grid(row = 5, column = 2, sticky = W)
		#Backtrack matrix checkbox
		self.backtrack = Checkbutton(self, text = "Backtrack Matrix", variable = self.backtrackVar)
		self.backtrack.grid(row = 6, column = 2, sticky = W)
		#String alignment checkbox
		self.alignment = Checkbutton(self, text = "Alignment", variable = self.strAlignVar)
		self.alignment.grid(row = 7, column = 2, sticky = W)
		#Vertical scrollbar for the result window
		self.scroll = Scrollbar(self, orient=VERTICAL)
		#Output window
		self.output = Text(self, width = 125, height = 20, wrap = WORD, yscrollcommand = self.scroll.set)
		self.output.grid(row = 9, column = 0, columnspan = 6)
		self.scroll.grid(row = 9, column = 6, sticky = 'NEWS')
		self.scroll.config(command = self.output.yview)

	#Retrieves the values and options from the GUI and handles the output accordingly
	def initialize(self):
		#Retrieve user-input values
		sourceString = getFileString(self.firstStr_ent.get())
		targetString = getFileString(self.secondStr_ent.get())
		cins = int(self.cins_scale.get())
		cdel = int(self.cdel_scale.get())
		csub = int(self.csub_scale.get())

		if(sourceString is not None and targetString is not None):
			if(len(sourceString) != 0 and len(targetString) != 0 and sourceString[0] != '\n' and targetString[0] != '\n'):
				#Find the edit distance, backtracking matrix and string alignment matrix
				(distanceMat, backtrackMat) = findEditDistance(sourceString, targetString, cins, cdel, csub)
				self.editDistMatrix = convertEditDistanceMatrix(distanceMat, sourceString, targetString)
				self.backtrackMatrix = convertMatrix(backtrackMat, sourceString, targetString)		
				self.stringAlignment = getStringAlignment(backtrackMat, sourceString, targetString)
				#Append output to output window according to the options selected
				self.output.insert(END, '\n\n=================================================\n\n')
				self.output.insert(END, 'String edit distance value: ' + str(distanceMat[len(sourceString)][len(targetString)]) + '\n\n')
				if(self.editDistVar.get()):
					self.output.insert(END, '============= Edit Distance Matrix: ============= \n' + self.editDistMatrix + '\n')
				if(self.backtrackVar.get()):
					self.output.insert(END, '=============== Backtack Matrix: ================ \n' + self.backtrackMatrix + '\n')
				if(self.strAlignVar.get()):
					self.output.insert(END, '=============== String alignment: =============== \n' + self.stringAlignment + '\n')

	def clearOutputWindow(self):
		self.output.delete('1.0', END)

#Creates the edit distance matrix and backtrack Matrix from the user input strings
def findEditDistance(sString, tString, cins, cdel, csub):
	sLen = len(sString)
	tLen = len(tString)
	distanceMat = [[0 for i in range(tLen+1)] for j in range(sLen+1)]
	backtrackMat = [[0 for i in range(tLen+1)] for j in range(sLen+1)]
	for j in range(1, tLen+1):
		distanceMat[0][j] = distanceMat[0][j-1]+cins
		backtrackMat[0][j] = '-'
	for i in range(1, sLen+1):
		distanceMat[i][0] = distanceMat[i-1][0]+cdel
		backtrackMat[i][0] = '|'
	backTrackSym='\\|-'
	for j in range(1, tLen+1):
		for i in range(1, sLen+1):
				(distanceMat[i][j], idx)=getMinimumDist(sString, tString, distanceMat, i, j, cdel, cins, csub)
				backtrackMat[i][j] = backTrackSym[idx]
	return (distanceMat, backtrackMat)

#Get the minimum distance value for each comparison
def getMinimumDist(sStr, tStr, distMat, i, j, cdel, cins, csub):
	if (sStr[i-1] == tStr[j-1]):
		subCost = distMat[i-1][j-1]
	else:
		subCost = distMat[i-1][j-1]+csub
	delCost =  distMat[i-1][j]+cdel
	insCost = distMat[i][j-1]+cins
	return min([(subCost, 0), (delCost, 1), (insCost, 2)])

#Creates the alignment string from the source and target strings
def getStringAlignment(backtrackMat, sString, tString):
	i = len(sString)
	j = len(tString)
	firstLine = ''
	secondLine = ''
	thirdLine = ''
	while(backtrackMat[i][j] != 0):
		if (backtrackMat[i][j] == '\\'):
			firstLine = sString[i-1] + firstLine
			thirdLine = tString[j-1] + thirdLine
			i = i-1
			j = j-1
		elif (backtrackMat[i][j] == '-'):
			firstLine = '-'+firstLine
			thirdLine = tString[j-1]+thirdLine
			j = j-1
		elif (backtrackMat[i][j] == '|'):
			firstLine = sString[i-1]+firstLine
			thirdLine = '-'+thirdLine
			i = i-1
		if (firstLine[0] == thirdLine[0]):
			secondLine = '|'+secondLine
		else:
			secondLine = ' '+secondLine
	finalStringAlignment = firstLine+'\n'+secondLine+'\n'+thirdLine
	return finalStringAlignment

#Get the string from the file
def getFileString(fileName):
	try:
		fileString = open(fileName, 'r')
		lineString = fileString.readline()
		fileString.close()
		if(len(lineString) == 0 or lineString[0] == '\n'):
			tkMessageBox.showerror('Content Not Found', 'No content found in '+fileName)
		return lineString[0:len(lineString)]
	except IOError:
		tkMessageBox.showerror('File Access Error', fileName+' not found.')

#Convert the matrix to a printable version of string
def convertMatrix(matrix, sString, tString):	
	finalStr = '    '+' '.join(tString)+'\n'
	finalStr = finalStr+'  '+' '.join(str(i) for i in matrix[0])+'\n'
	for i in range(0, len(sString)):
		finalStr = finalStr+sString[i]+' '+' '.join(str(j) for j in matrix[i+1])+'\n'
	return finalStr

def convertEditDistanceMatrix(matrix, sString, tString):	
	finalStr = '\t\t'+'\t'.join(tString)+'\n'
	finalStr = finalStr+'\t'+'\t'.join(str(i) for i in matrix[0])+'\n'
	for i in range(0, len(sString)):
		finalStr = finalStr+sString[i]+'\t'+'\t'.join(str(j) for j in matrix[i+1])+'\n'
	return finalStr

root = Tk()
root.title("Edit Distance GUI")
app = Application(root)
root.mainloop()