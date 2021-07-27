from tkinter import *
from tkinter import ttk, filedialog, messagebox
from os import path, makedirs
from functions import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas

matplotlib.use('TkAgg')

if not path.exists('./Gráficos/'):
	makedirs('./Gráficos')


def center(win):
	win.update_idletasks()
	width = win.winfo_width()
	height = win.winfo_height()
	x = (win.winfo_screenwidth() // 2) - (width // 2)
	y = (win.winfo_screenheight() // 2) - (height // 2)
	win.geometry('+{}+{}'.format(x, y))

class Root(Tk):
	def __init__(self):
		super().__init__()
		self.title('Simulador de modelo de cristalização')
		self.iconbitmap('icon-cristal.ico')
		self.geometry('+40+10')
		self.protocol("WM_DELETE_WINDOW", self.quit_me)
		self.df_var = get_variables()
		self.default = dict(
							fig_config={
								'figsize': [8, 6],
								'dpi': 90,
								'line': 1.5},
							entrys={
								'comp1': 400,
								'lst1': [2000, 4000, 7000],
								't_resd': 10000,
								'lst2': [100, 150, 200, 300],
								'comp3': 250,
								'lst3': [2000, 4000, 6000, 8000]})

		# FRAME DAS VARIÁVEIS
		self.frm_var = LabelFrame(self, text='Seleção de Variáveis')
		self.frm_var.grid(row=0, column=0, sticky=N + S + E + W, padx=3)
		self.lst_var = list(self.df_var.index)
		self.var_selected = StringVar()
		self.var_selected.set(self.lst_var[0])
		self.opt_menu = OptionMenu(self.frm_var, self.var_selected, *self.lst_var)
		self.opt_menu.grid(row=0, column=0, sticky=W + E)
		Button(self.frm_var, text='Gerenciar dados',command=self.var_cfg).grid(row=1, column=0)

		# FRAME DE CONFIGURAÇÃO DOS GRÁFICOS E DIRETÓRIO DE SALVAMENTO
		frm_graph_cfg = LabelFrame(self, text='Opções de imagem')
		frm_graph_cfg.grid(row=0, column=1, sticky=N + S + E + W, padx=3)
		Label(frm_graph_cfg, text='Título da simulação: ').grid(row=0, column=0, sticky=W)
		self.graph_name = Entry(frm_graph_cfg, borderwidth=2)
		self.graph_name.grid(row=0, column=1, sticky=W + E)
		Button(frm_graph_cfg, text='Configurações\nde Imagem', command=self.graph_cfg).grid(row=0, column=2)
		Label(frm_graph_cfg, text='Salvar em: ').grid(row=1, column=0)
		self.directory = StringVar()
		self.directory.set(path.dirname(path.abspath(__file__)) + '/Gráficos')
		Label(frm_graph_cfg, textvariable=self.directory, bg='#f5f5f5', width=55,
			  font=('Arial', 10), bd=2, relief=SUNKEN, anchor='e').grid(row=1, column=1, pady=3, sticky=E)
		Button(frm_graph_cfg, text='Selecionar pasta',command=self.ask_save_dir, padx=5, pady=1).grid(row=1, column=2,padx=10)

		# FRAME DE CONFIGURAÇÕES ESPECÍFICAS DE CADA GRÁFICO
		frm_axis_cfg = LabelFrame(self, text='Config. Específicas')
		frm_axis_cfg.grid(row=1, column=0, sticky=N + S + E + W, padx=3)
		Label(frm_axis_cfg, text='Gráfico 1\nL máximo:').pack(anchor=W)
		self.comp1 = Entry(frm_axis_cfg, bd=2, width=20)
		self.comp1.pack(anchor=W)
		self.comp1.insert(END, self.default['entrys']['comp1'])
		Label(frm_axis_cfg, text='Lista de τ\'s').pack(anchor=W)
		self.lst1 = Entry(frm_axis_cfg, bd=2, width=20)
		self.lst1.pack(anchor=W)
		self.lst1.insert(END, list_int2str(self.default['entrys']['lst1']))
		self.ln1 = BooleanVar()
		Checkbutton(frm_axis_cfg, text='Plot semilog',
					variable=self.ln1, onvalue=True, offvalue=False).pack(anchor=W)
		self.save1 = BooleanVar()
		Checkbutton(
			frm_axis_cfg, text='Salvar gráfico 1', variable=self.save1, onvalue=True, offvalue=False).pack(anchor=W)

		ttk.Separator(frm_axis_cfg, orient=HORIZONTAL).pack(fill=X)

		Label(frm_axis_cfg, text='Gráfico 2\nτ máximo:').pack(anchor=W)
		self.t_resd = Entry(frm_axis_cfg, bd=2, width=20)
		self.t_resd.pack(anchor=W)
		self.t_resd.insert(END, self.default['entrys']['t_resd'])
		Label(frm_axis_cfg, text='Lista de L\'s').pack(anchor=W)
		self.lst2 = Entry(frm_axis_cfg, bd=2, width=20)
		self.lst2.pack(anchor=W)
		self.lst2.insert(END, list_int2str(self.default['entrys']['lst2']))
		self.save2 = BooleanVar()
		Checkbutton(
			frm_axis_cfg, text='Salvar gráfico 2', variable=self.save2, onvalue=True, offvalue=False).pack(anchor=W)

		ttk.Separator(frm_axis_cfg, orient=HORIZONTAL).pack(fill=X)

		Label(frm_axis_cfg, text='Gráfico 3\nL máximo:').pack(anchor=W)
		self.comp3 = Entry(frm_axis_cfg, bd=2, width=20)
		self.comp3.pack(anchor=W)
		self.comp3.insert(END, self.default['entrys']['comp3'])
		Label(frm_axis_cfg, text='Lista de τ\'s').pack(anchor=W)
		self.lst3 = Entry(frm_axis_cfg, borderwidth=2, width=20)
		self.lst3.pack(anchor=W)
		self.lst3.insert(END, list_int2str(self.default['entrys']['lst3']))
		self.save3 = BooleanVar()
		Checkbutton(
			frm_axis_cfg, text='Salvar gráfico 3', variable=self.save3, onvalue=True, offvalue=False).pack(anchor=W)

		# BOTÃO RUN
		ttk.Separator(frm_axis_cfg, orient=HORIZONTAL).pack(fill=X)
		Label(frm_axis_cfg, text='').pack()
		Button(frm_axis_cfg, text='Gerar Gráficos',command=self.run, bd=3).pack(fill=BOTH, anchor=S)

		# FRAME DE CANVAS
		frm_canvas = LabelFrame(self, text='Gráficos')
		frm_canvas.grid(row=1, column=1, sticky=N + S + E + W, padx=3)
		self.tab_control = ttk.Notebook(frm_canvas)
		self.tab1 = ttk.Frame(self.tab_control)
		self.graph1 = Figure(figsize=self.default['fig_config']['figsize'], dpi=self.default['fig_config']['dpi'])
		self.canvas1 = FigCanvas(self.graph1, master=self.tab1)
		self.canvas1.tkcanvas.grid(row=0, column=0)
		self.tab2 = ttk.Frame(self.tab_control)
		self.graph2 = Figure(figsize=self.default['fig_config']['figsize'], dpi=self.default['fig_config']['dpi'])
		self.canvas2 = FigCanvas(self.graph2, master=self.tab2)
		self.canvas2.tkcanvas.grid(row=0, column=0)
		self.tab3 = ttk.Frame(self.tab_control)
		self.graph3 = Figure(figsize=self.default['fig_config']['figsize'], dpi=self.default['fig_config']['dpi'])
		self.canvas3 = FigCanvas(self.graph3, master=self.tab3)
		self.canvas3.tkcanvas.grid(row=0, column=0)
		self.tab_control.add(self.tab1, text='1. Dens (n) x Comp (L)')
		self.tab_control.add(self.tab2, text='2. Dens (n) x T Resd (τ)')
		self.tab_control.add(self.tab3, text='3. N° cristais x Comp (L)')
		self.tab_control.pack(expand=1, fill='both')

	def var_cfg(self):
		Var_cfg_GUI(self)

	def graph_cfg(self):
		Graph_cfg_GUI(self)

	def ask_save_dir(self):
		save_folder=filedialog.askdirectory(initialdir=self.directory.get())
		if save_folder!='':
			self.directory.set(save_folder)

	def run(self):
		vrbls = self.df_var.loc[str(self.var_selected.get())].to_dict()
		try:
			entrys={
				'comp1': int(self.comp1.get()),
				'lst1': list_str2int(self.lst1.get()),
				't_resd': int(self.t_resd.get()),
				'lst2': list_str2int(self.lst2.get()),
				'comp3': int(self.comp3.get()),
				'lst3': list_str2int(self.lst3.get())
			}

			clear_canvas(self)
			self.graph1 = NxComp(vrbls,self.graph_name.get(),
									self.default['fig_config'],comprimento=entrys['comp1'], tempos=entrys['lst1'], ln=self.ln1.get(), save=self.save1.get(), directory=self.directory.get())
			self.graph2 = NxTrsd(vrbls, self.graph_name.get(),
								 self.default['fig_config'], T_resd=entrys['t_resd'], comprimentos=entrys['lst2'],
								 save=self.save2.get(), directory=self.directory.get())
			self.graph3 = Num_cristal(vrbls, self.graph_name.get(),
								 self.default['fig_config'], comprimento=entrys['comp3'], tempos=entrys['lst3'],
								 save=self.save3.get(), directory=self.directory.get())
			draw_canvas(self)
			self.canvas1=FigCanvas(self.graph1, master=self.tab1)
			self.canvas1.draw()
			self.canvas1.get_tk_widget().grid(row=0, column=0)
		except:
			messagebox.showwarning(
				title='Aviso', message='Parâmetros devem ser formados por números inteiros positivos.\n' +
									   ' -> L\'s e τ máximo, devem ser um número inteiro.\n' +
									   ' ->Listas devem ser conjuntos de números inteiros, separados por vírgulas.')

	def quit_me(self):
		self.quit()
		self.destroy()


class Var_cfg_GUI(Toplevel):
	def __init__(self, main_GUI):
		super().__init__(master=main_GUI)

		center(self)
		self.title('Gerenciamento de variáveis')
		self.transient()
		self.focus_force()
		self.grab_set()

		Label(self, text='Variáveis: ').grid(row=0, column=0, sticky=W)
		self.lstbox = Listbox(self, listvariable=StringVar(value=main_GUI.lst_var))
		self.lstbox.bind('<<ListboxSelect>>', self.show_selection)
		self.lstbox.grid(row=1, column=0, padx=3, pady=3)

		self.columnconfigure(1, minsize=150)
		frm_show = LabelFrame(self, text='Dataset Selecionado: ')
		frm_show.grid(row=1, column=1, ipadx=3, sticky=N + S + E + W)
		self.lbln0 = Label(frm_show, text='n0: ')
		self.lbln0.pack(anchor='w')
		self.lblDab = Label(frm_show, text='Dab: ')
		self.lblDab.pack(anchor='w')
		self.lblC0 = Label(frm_show, text='C0: ')
		self.lblC0.pack(anchor='w')
		self.lblCASS = Label(frm_show, text='CASS: ')
		self.lblCASS.pack(anchor='w')
		self.lblCAS = Label(frm_show, text='CAS: ')
		self.lblCAS.pack(anchor='w')
		self.lblCT = Label(frm_show, text='CT: ')
		self.lblCT.pack(anchor='w')

		frm_new_var = LabelFrame(self, text='Adicionar Dataset')
		frm_new_var.grid(row=1, column=2, sticky=N + S + E + W, padx=5)
		Label(frm_new_var, text='Nome: ').grid(row=0, column=0, sticky=W)
		self.var_title = Entry(frm_new_var, bd=2)
		self.var_title.grid(row=0, column=1)
		Label(frm_new_var, text='n0: ').grid(row=1, column=0, sticky=W)
		self.n0 = Entry(frm_new_var, bd=2)
		self.n0.grid(row=1, column=1)
		Label(frm_new_var, text='Dab: ').grid(row=2, column=0, sticky=W)
		self.Dab = Entry(frm_new_var, bd=2)
		self.Dab.grid(row=2, column=1)
		Label(frm_new_var, text='C0: ').grid(row=3, column=0, sticky=W)
		self.C0 = Entry(frm_new_var, bd=2)
		self.C0.grid(row=3, column=1)
		Label(frm_new_var, text='CASS: ').grid(row=4, column=0, sticky=W)
		self.CASS = Entry(frm_new_var, bd=2)
		self.CASS.grid(row=4, column=1)
		Label(frm_new_var, text='CAS: ').grid(row=5, column=0, sticky=W)
		self.CAS = Entry(frm_new_var, bd=2)
		self.CAS.grid(row=5, column=1)
		Label(frm_new_var, text='CT: ').grid(row=6, column=0, sticky=W)
		self.CT = Entry(frm_new_var, bd=2)
		self.CT.grid(row=6, column=1)

		Button(self, text='Adicionar novo Dataset', command=self.add_data).grid(row=2, column=2, sticky=W + E + N + S, padx=3)
		Button(self, text='Remover dados\nselecionados',
			   command=self.remove_data).grid(row=2, column=0, sticky=W + E + N + S, padx=3)
	def show_selection(self, event):
		widget=event.widget
		title=str(widget.get(widget.curselection()))
		self.lbln0['text'] = 'n0: ' + str(self.master.df_var.loc[title, 'n0']) + ' no/μm.L'
		self.lblDab['text'] = 'Dab: ' + \
							  str(self.master.df_var.loc[title, 'Dab']) + ' μm²/s'
		self.lblC0['text'] = 'C0: ' + str(self.master.df_var.loc[title, 'C0']) + ' Kmol/m³'
		self.lblCASS['text'] = 'CASS: ' + \
							   str(self.master.df_var.loc[title, 'CASS']) + ' Kmol/m³'
		self.lblCAS['text'] = 'CAS: ' + \
							  str(self.master.df_var.loc[title, 'CAS']) + ' Kmol/m³'
		self.lblCT['text'] = 'CT: ' + str(self.master.df_var.loc[title, 'CT']) + ' Kmol/m³'

	def add_data(self):
		try:
			new_var = {'title': str(self.var_title.get()),
					   'n0': [float(self.n0.get())],
					   'Dab': [float(self.Dab.get())],
					   'C0': [float(self.C0.get())],
					   'CASS': [float(self.CASS.get())],
					   'CAS': [float(self.CAS.get())],
					   'CT': [float(self.CT.get())]
					   }
			self.var_title.delete(0, 'end')
			self.n0.delete(0, 'end')
			self.Dab.delete(0, 'end')
			self.C0.delete(0, 'end')
			self.CASS.delete(0, 'end')
			self.CAS.delete(0, 'end')
			self.CT.delete(0, 'end')
			new_df = pd.DataFrame(data=new_var).set_index('title')
			self.master.df_var = pd.concat([self.master.df_var, new_df])
			self.master.lst_var = list(self.master.df_var.index)
			self.master.df_var.drop('Silva et al', axis=0).to_csv('variables_save.csv', sep=',')
			self.lstbox.insert('end', new_var['title'])
			self.master.opt_menu.destroy()
			self.master.opt_menu = OptionMenu(self.master.frm_var,self.master.var_selected,*self.master.lst_var)
			self.master.opt_menu.grid(row=0, column=0, sticky=W+E)

		except:
			messagebox.showwarning(
				title='Aviso',
				message='Todos os parâmetros devem ser preenchidos.\n\n' +
						'->Nome: texto, será o nome do novo conjunto de variáveis.\n' +
						'->Demais parâmetros: números', parent=self)

	def remove_data(self):
		n_var = self.lstbox.curselection()[0]
		try:
			self.master.df_var.drop(self.master.lst_var[n_var],axis=0,inplace=True)
			self.master.lst_var=list(self.master.df_var.index)
			self.master.df_var.drop('Silva et al', axis=0).to_csv('variables_save.csv', sep=',')
			self.lstbox.delete(self.lstbox.index(ACTIVE))
			self.master.opt_menu.destroy()
			self.master.opt_menu = OptionMenu(self.master.frm_var, self.master.var_selected, *self.master.lst_var)
			self.master.opt_menu.grid(row=0, column=0, sticky=W + E)
		except:
			messagebox.showwarning(
				title='Aviso',
				message='Os dados do trabalho original de Silva et al não podem ser removidos.', parent=self)

class Graph_cfg_GUI(Toplevel):
	def __init__(self, main_GUI):
		super().__init__(master=main_GUI)

		center(self)
		self.title('Configurações de imagem')
		self.transient()
		self.focus_force()
		self.grab_set()

		Label(self,text='Dimensões da figura: ').grid(row=0, column=0, sticky=W, padx=10)
		self.figsize=Entry(self,width=15)
		self.figsize.insert(END, str(self.master.default['fig_config']['figsize'][0])+','+ str(self.master.default['fig_config']['figsize'][1]))
		self.figsize.grid(row=1,column=0,sticky=W, padx=10)

		Label(self,text='DPI: ').grid(row=0,column=1, sticky=W, padx=10)
		self.dpi=Entry(self,width=15)
		self.dpi.insert(END, str(self.master.default['fig_config']['dpi']))
		self.dpi.grid(row=1,column=1,sticky=W,padx=10)

		Label(self,text='Espessura da linha: ').grid(row=0,column=3,sticky=W, padx=10)
		self.line=Entry(self,width=15)
		self.line.insert(END,str(self.master.default['fig_config']['line']))
		self.line.grid(row=1,column=3,sticky=W,padx=10)

		Button(self, text='OK', command=self.graph_cfg_OK).grid(row=2, column=1)

	def graph_cfg_OK(self):
		try:
			if len(list_str2int(self.figsize.get())) != 2:
				print('deu no if')
				messagebox.showwarning(
					title='Aviso', message='Parâmetro \"Tamanho da figura\" deve ser um' +
										   ' par de números inteiros, separados por vírgula.\nEx: 4,3', parent=self)

			else:
				self.master.default['fig_config']['figsize'] = list_str2int(self.figsize.get())
				self.master.default['fig_config']['line'] = float(self.line.get())
				self.master.default['fig_config']['dpi'] = int(self.dpi.get())
				self.destroy()

		except:
			messagebox.showwarning(
				title='Aviso',
				message='Os parâmetros devem ser números.\n\n' +
						'->Figure size: par de números inteiros, separados por virgula.\n' +
						'->DPI: número inteiro, apenas.\n' +
						'->Espessura da linha: número de ponto flutuante.', parent=self)

app = Root()
app.update()
app.mainloop()
