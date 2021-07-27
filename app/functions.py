from math import exp, sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas
import pandas as pd

def NxComp(var, title, fig_config, comprimento, tempos, ln, save, directory):
	global df_var
	# Densidade x comprimento
	L = np.linspace(0, comprimento, 1000)  # Comprimento do cristal
	t = tempos  # Tempo de residência
	n = [0] * len(L)

	fig1, ax1 = plt.subplots(num=1, figsize=fig_config['figsize'], dpi=80)

	for tempo in t:
		G = 0.5643 * ((sqrt(var['Dab'])) / (
			sqrt(tempo) * sqrt((var['C0'] ** 2 / var['CT'] ** 2) * (var['CASS'] - var['CT']) ** 2))) * (
			var['CASS'] - var['CAS'])
		for k in range(0, len(L), 1):
			n[k] = var['n0'] * exp(-L[k] / (G * tempo))
		if ln == True:
			ax1.semilogy(L, n, label='Tempo= {} s'.format(tempo),
						 linewidth=fig_config['line'], basey=np.e)
		else:
			plt.plot(L, n, label='Tempo= {} s'.format(
				tempo), linewidth=fig_config['line'])

	if ln == True:
		def ticks(y, pos):
			return r'${:.0f}$'.format(np.log(y))

		plt.ylim(bottom=exp(0))  # , top=exp(10))
		ax1.yaxis.set_major_formatter(tck.FuncFormatter(ticks))
		plt.ylabel('ln(n)')
		plt.title('Densidade de população vs Comprimento dos cristais\n (Semilog)')
	else:
		plt.ylabel('Densidade de população\n(nº de cristais/μm.L)')
		plt.title('Densidade de população vs Comprimento dos cristais')
	plt.xlabel('Comprimento (μm)')
	plt.legend()
	plt.grid()
	fig1.set_tight_layout(True)
	if save == True:
		nomearq = title + ' - Densidade vs Comprimento'
		figname = directory + '/' + nomearq + '.png'
		plt.savefig(figname, dpi=fig_config['dpi'])
	return fig1


def NxTrsd(var, title, fig_config, T_resd, comprimentos, save, directory):
	# Densidade x tempo

	L = comprimentos
	t = np.linspace(1, T_resd, 20)
	n = [0] * len(t)
	fig2, ax2 = plt.subplots(num=2, figsize=fig_config['figsize'], dpi=80)

	for l in L:
		for k in range(0, len(t), 1):
			G = 0.5643 * ((sqrt(var['Dab'])) / (
				sqrt(t[k]) * sqrt((var['C0'] ** 2 / var['CT'] ** 2) * (var['CASS'] - var['CT']) ** 2))) * (
				var['CASS'] - var['CAS'])
			n[k] = var['n0'] * exp(-l / (G * t[k]))
		plt.plot(t, n, label='Comprimento= {} μm'.format(
			l), linewidth=fig_config['line'])
	# plt.xticks(np.arange(0,t[-1]+1,1000))
	plt.ylabel('Densidade de população\n(nº de cristais/μm.L)')
	plt.xlabel('Tempo de residência (s)')
	plt.legend()
	plt.grid()
	plt.title('Densidade de população vs Tempo de residência')
	fig2.set_tight_layout(True)
	if save == True:
		nomearq = title + ' - Densidade vs Tempo'
		figname = directory + '/' + nomearq + '.png'
		plt.savefig(figname, dpi=fig_config['dpi'])
	return fig2


def Num_cristal(var, title, fig_config, comprimento, tempos, save, directory):
	# Densidade x comprimento
	L = np.linspace(0, comprimento, 1000)  # Comprimento do cristal
	t = tempos  # Tempo de residência
	num_cristal = [0] * len(L)

	fig3, ax3 = plt.subplots(num=3, figsize=fig_config['figsize'], dpi=80)

	for tempo in t:
		G = 0.5643 * ((sqrt(var['Dab'])) / (
			sqrt(tempo) * sqrt((var['C0'] ** 2 / var['CT'] ** 2) * (var['CASS'] - var['CT']) ** 2))) * (
			var['CASS'] - var['CAS'])
		for k in range(0, len(L), 1):
			num_cristal[k] = var['n0'] * exp(-L[k] / (G * tempo)) * L[k]

		plt.plot(L, num_cristal, label='Tempo= {} s'.format(
			tempo), linewidth=fig_config['line'])

	plt.ylabel('Nº de cristais')
	plt.xlabel('Comprimento (μm)')
	plt.title('Número de Cristais vs Comprimento dos cristais')
	plt.legend()
	plt.grid()
	fig3.set_tight_layout(True)
	if save == True:
		nomearq = title + ' - Tamanho dominante'
		figname = directory + '/' + nomearq + '.png'
		plt.savefig(figname, dpi=fig_config['dpi'])
	return fig3


# FUNÇÕES AUXILIARES

def list_str2int(lst):

	lstsplit = lst.split(',')

	if len(lstsplit) == 1:
		num = int(lstsplit[0])
		return num
	else:
		intlist = [int(val) for val in lstsplit]

		return intlist


def list_int2str(lst):
	string = str()
	for n in lst:
		if n == lst[-1]:
			string += str(n)
		else:
			string += str(n) + ','
	return string


def clear_canvas(master):
	tabs=[master.tab1, master.tab2, master.tab3]
	graphs=[master.graph1, master.graph2, master.graph3]

	for i in range(0,3):
		graphs[i].clf()
		graphs[i].set_size_inches(master.default['fig_config']['figsize'])
		for w in tabs[i].winfo_children():
			w.destroy()

def draw_canvas(master):
	tabs=[master.tab1, master.tab2, master.tab3]
	graphs=[master.graph1, master.graph2, master.graph3]
	canvas=[master.canvas1, master.canvas2, master.canvas3]

	for i in range(0,3):
		canvas[i]=FigCanvas(graphs[i], master=tabs[i])
		canvas[i].draw()
		canvas[i].get_tk_widget().grid(row=0, column=0)


def get_variables():
	df = pd.read_csv('variables_save.csv', sep=',')
	silva = {'title': 'Silva et al',
			 'n0': [325215.956],  # (no/μm.L) # Quantidade de núcleos iniciais
			 'Dab': [355],  # (μm²/s) # Difusividade
			 'C0': [4.64],  # (Kmol/m³) # Concentração do cristal
			 # (Kmol/m³) # Concentração de supersaturação da solução
			 'CASS': [2.82],
			 # (Kmol/m³) # Concentração na superfície do cristal
			 'CAS': [2.64],
			 'CT': [26.13]  # (Kmol/m³) # Concentração molar da solução
			 }
	silvadf = pd.DataFrame(data=silva)
	df = pd.concat([silvadf, df]).set_index('title')
	return df


