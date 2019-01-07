from tkinter import *

WIN_START_WIDTH = 500
WIN_START_HEIGHT = 500


FIGURES=[]
LINES = []

#вопросы к учителю я пометил с помощью ###




class Dot:
	RADIUS = 30
	OUTLINE_COLOR = 'red'
	FILL_COLOR = 'purple'

	def __init__(self, canvas, x, y):
		self.canvas=canvas
		self.x=x
		self.y=y
		self.CursorIn = False
		self.lines=[]
		#нам надо сказать, что figure есть, иначе будет ошибка
		self.figure = None
		FIGURES.append(self)



	def binds(self):
		self.canvas.tag_bind(self.figure, '<B1-Motion>', self.dnd)	
		self.canvas.tag_bind(self.figure, '<Enter>', self.CursorInFigure)
		self.canvas.tag_bind(self.figure, '<Leave>', self.CursorOutFigure)
		self.canvas.tag_bind(self.figure, '<3>', self.Remove_figure_and_override_lines)


	def dnd(self, event):
		self.canvas.move(self.figure,
			event.x-self.canvas.coords(self.figure)[0]-self.RADIUS,
			event.y-self.canvas.coords(self.figure)[1]-self.RADIUS )
		self.x = event.x
		self.y = event.y
		for line in self.lines:
			line.dnd()

	def CursorInFigure(self, event):
		self.CursorIn = True

	def CursorOutFigure(self, event):
		self.CursorIn = False

	def Remove_figure(self, *args):
		global FIGURES
		FIGURES.remove(self)
		self.canvas.tag_unbind(self.figure, '<B1-Motion>')
		self.canvas.tag_unbind(self.figure, '<Enter>')
		self.canvas.tag_unbind(self.figure, '<Leave>')
		self.canvas.delete(self.figure)


	def Remove_figure_and_override_lines(self, *args):
		self.Remove_figure()
		override_lines()

	def Get_dot(self):
		return self.x, self.y

	def Add_line(self, line):
		self.lines.append(line)

	def Remove_line(self, line):
		self.lines.remove(line)

class Line:
	WIDTH = 2
	COLOR = 'black'
	def __init__(self, canvas, dot1, dot2):
		global LINES
		dot1.Add_line(self)
		dot2.Add_line(self)
		self.canvas = canvas
		self.dot1 = dot1
		self.dot2 = dot2
		self.x1, self.y1 = dot1.Get_dot()
		self.x2, self.y2 = dot2.Get_dot()
		self.line = self.canvas.create_line(self.x1, self.y1,
			self.x2, self.y2,
			width = self.WIDTH, fill = self.COLOR)
		LINES.append(self)

	def Remove_line(self):
		global LINES
		LINES.remove(self)
		self.dot1.Remove_line(self)
		self.dot2.Remove_line(self)
		self.canvas.delete(self.line)

	def dnd(self):
		self.x1, self.y1 = self.dot1.Get_dot()
		self.x2, self.y2 = self.dot2.Get_dot()
		self.canvas.coords(self.line,
			self.x1, self.y1,
			self.x2, self.y2)





class Oval(Dot):

	def __init__(self, canvas, x, y):
		super().__init__(canvas, x, y)
		self.canvas.delete(self.figure)
		self.figure = self.canvas.create_oval(
			self.x-self.RADIUS, self.y-self.RADIUS,
			self.x+self.RADIUS, self.y+self.RADIUS,
			fill = self.FILL_COLOR, outline = self.OUTLINE_COLOR)
		super().binds()

class Rectangle(Dot):
	def __init__(self, canvas, x, y):
		super().__init__(canvas, x, y)
		self.canvas.delete(self.figure)
		self.figure = self.canvas.create_rectangle(
			self.x-self.RADIUS, self.y-self.RADIUS,
			self.x+self.RADIUS, self.y+self.RADIUS,
			fill = self.FILL_COLOR, outline = self.OUTLINE_COLOR)
		super().binds()

class Triangle(Dot):
	def __init__(self, canvas, x, y):
		super().__init__(canvas, x, y)
		self.canvas.delete(self.figure)
		self.figure=self.canvas.create_polygon(
			self.x, self.y-self.RADIUS,
			self.x+int(self.RADIUS*0.866//1), self.y+self.RADIUS/2,
			self.x-int(self.RADIUS*0.866//1), self.y+self.RADIUS/2,
			fill = self.FILL_COLOR, outline = self.OUTLINE_COLOR)
		super().binds()

	def dnd(self, event):
		self.canvas.move(self.figure,
			event.x-self.canvas.coords(self.figure)[0],
			event.y-self.canvas.coords(self.figure)[1]-self.RADIUS )
		self.x = event.x
		self.y = event.y
		for line in self.lines:
			line.dnd()



AVAILABLE_FORMS = {
	'Oval'			:Oval,
	'Rectangle'		:Rectangle,
	'Triangle'		:Triangle
}





def new_figure(event):
	global canvas, ACT
	#обработка события
	check = True
	for figure in FIGURES:
		if figure.CursorIn == True:
			check = False
			break
	if check:
		#точка
		figure = ACT(canvas, int(event.x//1), int(event.y//1) )
		#линия
		override_lines()







def Change_the_form():
	global canvas, ACT
	form = figure_form.get()
	ACT = AVAILABLE_FORMS[form]
	new_figures=[]
	for line in LINES:
		line.Remove_line()
	#массив будет меняться, потому выкручиваюсь как могу
	#i использоваться не будет, потому i
	for i in range(len(FIGURES)):
		x, y = FIGURES[0].Get_dot()
		FIGURES[0].Remove_figure()
		new_figure = ACT(canvas, x, y)
	override_lines()

#такая функция будет вызвана не раз, потому запишу её отдельно
def override_lines():
	###оно не хочет работать с правильными формулами
	global canvas, ACT
	for line in LINES:
		line.Remove_line()#для переопределения
	dots={
		'x':[],
		'y':[]
	}
	for figure in FIGURES:
		x, y = figure.Get_dot()
		dots['x'].append(int(x))
		dots['y'].append(int(y))

	#я долго пытался написать это всё на for
	#но в итоге получилось на while
	#исправлять лень
	id1, id2, id3 = 0, 0, 0
	while len(dots['x'])>id1 and len(dots['x'])>3:
		x1 = dots['x'][id1]
		y1 = dots['y'][id1]
		while len(dots['x'])>id2:
			if id2!=id1:
				x2 = dots['x'][id2]
				y2 = dots['y'][id2] 
				if x1==x2:
					k=0
				else:
					k = (y2-y1)/(x2-x1)
				b = y1-x1*k
				bigger = True
				less = True
				while len(dots['x'])>id3:
					if id3!=id1 and id3!=id2:
						x3 = dots['x'][id3]
						y3 = dots['y'][id3]
						if (y3>(k*x3+b)) and bigger:
							less = False
						elif (y3<(k*x3+b)) and less:
							bigger = False
						else:
							bigger = False
							less = False
						if not bigger and not less:
							break
					id3+=1
				if bigger or less:
					new_line = Line(canvas, FIGURES[id1], FIGURES[id2])
			id3=0
			id2+=1
		id2=0
		id1+=1	





root = Tk()

root.minsize(width = WIN_START_WIDTH, height = WIN_START_HEIGHT)
root.title('Drag&Drop')



menu = Menu(root)
root.configure(menu = menu)
Options = Menu(menu, tearoff = 0)
menu.add_cascade(label = 'Options', menu = Options)
Change_figures = Menu(Options)
Options.add_cascade(label = 'Change figure(s)', menu = Change_figures)

figure_form = StringVar()
figure_form.set('Oval')
Change_figures.add_radiobutton(label = 'Oval', variable = figure_form,
	value = 'Oval', command = Change_the_form)
Change_figures.add_radiobutton(label = 'Rectangle', variable = figure_form,
	value = 'Rectangle', command = Change_the_form)
Change_figures.add_radiobutton(label = 'Triangle', variable = figure_form,
	value = 'Triangle', command = Change_the_form)





canvas = Canvas(root, bg='white')
canvas.focus_set()
canvas.pack(expand=YES, fill=BOTH)

ACT = AVAILABLE_FORMS['Oval']
WIN_START_WIDTH, WIN_START_HEIGHT
figure = ACT(canvas, int(WIN_START_WIDTH/2//1),int(WIN_START_HEIGHT/2//1))

canvas.bind('<1>', new_figure)






root.mainloop()