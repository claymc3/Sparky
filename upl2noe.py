from tkinter import *
import tkinter
import types
import re
import math as m
import pyutil
import sparky
import sputil
import tkutil
import tkMessageBox
from numpy import median

# ------------------------------------------------------------------------------
#
# Updated by : Mary Clay PhD
# e-mail: mary.clay@stjude.org
# St Jude Children's Research Hospital 
# Department of Structural Biology Memphis, TN 
#
# Last updates: February 21, 2023
#
#
# ------------------------------------------------------------------------------
#
Pseudo2Prot = {'AQB':['HB1', 'HB2', 'HB3'],'RQB':['HB2', 'HB3'],'RQG':['HG2', 'HG3'],'RQD':['HD2', 'HD3'],'RQH1':['HH11', 'HH12'],'RQH2':['HH21', 'HH22'],'NQB':['HB2', 'HB3'],'NQD2':['HD21', 'HD22'],'DQB':['HB2', 'HB3'],'CQB':['HB2', 'HB3'],'QQB':['HB2', 'HB3'],'QQG':['HG2', 'HG3'],'QQE2':['HE21', 'HE22'],'EQB':['HB2', 'HB3'],'EQG':['HG2', 'HG3'],'GQA':['HA2', 'HA3'],'HQB':['HB2', 'HB3'],'IQG1':['HG11', 'HG12', 'HG13'],'IQG2':['HG21', 'HG22', 'HG23'],'IQD1':['HD11', 'HD12', 'HD13'],'LQB':['HB2', 'HB3'],'LQD1':['HD11', 'HD12', 'HD13'],'LQD2':['HD21', 'HD22', 'HD23'],'KQG':['HG2', 'HG3'],'KQD':['HD2', 'HD3'],'KQE':['HE2', 'HE3'],'KQZ':['HZ2', 'HZ3'],'MQB':['HB2', 'HB3'],'MQG':['HG2', 'HG3'],'MQE':['HE1', 'HE2', 'HE3'],'FQB':['HB2', 'HB3'],'FQD':['HD1', 'HD2'],'FQE':['HE1', 'HE2'],'PQB':['HB2', 'HB3'],'PQG':['HG2', 'HG3'],'PQD':['HD2', 'HD3'],'SQB':['HB2', 'HB3'],'TQG2':['HG21', 'HG22', 'HG23'],'WQB':['HB2', 'HB3'],'YQB':['HB2', 'HB3'],'YQD':['HD1', 'HD2'],'YQE':['HE1', 'HE2'],'VQB':['HB2', 'HB3'],'VQG1':['HG11', 'HG12', 'HG13'],'VQG2':['HG21', 'HG22', 'HG23'],'AHB':['HB1', 'HB2', 'HB3'],'RHB':['HB2', 'HB3'],'RHG':['HG2', 'HG3'],'RHD':['HD2', 'HD3'],'RHH1':['HH11', 'HH12'],'RHH2':['HH21', 'HH22'],'NHB':['HB2', 'HB3'],'NHD2':['HD21', 'HD22'],'DHB':['HB2', 'HB3'],'HHB':['HB2', 'HB3'],'QHB':['HB2', 'HB3'],'QHG':['HG2', 'HG3'],'QNE2':['HE21', 'HE22'],'EHB':['HB2', 'HB3'],'EHG':['HG2', 'HG3'],'GHA':['HA2', 'HA3'],'HHB':['HB2', 'HB3'],'IHG1':['HG12', 'HG13'],'IHG2':['HG21', 'HG22', 'HG23'],'IHD1':['HD11', 'HD12', 'HD13'],'LHB':['HB2', 'HB3'],'LHD1':['HD11', 'HD12', 'HD13'],'LHD2':['HD21', 'HD22', 'HD23'],'KHG':['HG2', 'HG3'],'KHD':['HD2', 'HD3'],'KHE':['HE2', 'HE3'],'KHZ':['HZ2', 'HZ3'],'MHB':['HB2', 'HB3'],'MHG':['HG2', 'HG3'],'MHE':['HE1', 'HE2', 'HE3'],'FHB':['HB2', 'HB3'],'FHD':['HD1', 'HD2'],'FHE':['HE1', 'HE2'],'PHB':['HB2', 'HB3'],'PHG':['HG2', 'HG3'],'PHD':['HD2', 'HD3'],'SHB':['HB2', 'HB3'],'THG2':['HG21', 'HG22', 'HG23'],'WHB':['HB2', 'HB3'],'YHB':['HB2', 'HB3'],'YQD':['HD1','HD2'],'YQE':['HE1', 'HE2'],'VHB':['HB2', 'HB3'],'VHG1':['HG11', 'HG12', 'HG13'],'VHG2':['HG21', 'HG22', 'HG23']}
Prot2Pseudo = {'AHB':['QB','HB*'],'CHB2':['QB','HB*'],'CHB3':['QB','HB*'],'DHB2':['QB','HB*'],'DHB3':['QB','HB*'],'EHB2':['QB','HB*'],'EHB3':['QB','HB*'],'EHG2':['QG2', 'HG*'],'FHB2':['QB','HB*'],'FHB3':['QB','HB*'],'FHD':['HD1','HD2'],'FHD1':['QD','HD*'],'FHD2':['QD','HD*'],'FHE1':['QE','HE*'],'FHE2':['QE','HE*'],'GHA2':['QA','HA*'],'GHA3':['QA','HA*'],'HHB2':['QB','HB*'],'HHB3':['QB','HB*'],'IHG1':['QG1','HG1*'],'IHG2':['QG2','HG2*'],'IHD1':['QD1','HD1*'],'KHD2':['QD','HD*'],'KHD3':['QD','HD*'],'KHE2':['QE','HE*'],'KHE3':['QE','HE*'],'KHG2':['QG','HG*'],'KHG3':['QG','HG*'],'KHZ2':['QZ','HZ*'],'KHZ3':['QZ','HZ*'],'LHB2':['QB','HB*'],'LHB3':['QB','HB*'],'LHD1':['QD1', 'HD1*'],'LHD2':['QD2', 'HD2*'],'MHB2':['QB','HB*'],'MHB3':['QB','HB*'],'MHE':['QE', 'HE'],'MHG2':['QG','HG*'],'MHG3':['QG','HG*'],'NHB2':['QB','HB*'],'NHB3':['QB','HB*'],'NHD21':['QD2','HD2*'],'NHD22':['QD2','HD2*'],'PHB':['HB2', 'HB3'],'PHB2':['QB','HB*'],'PHB3':['QB','HB*'],'PHD2':['QD','HD*'],'PHD3':['QD','HD*'],'PHG2':['QG','HG*'],'PHG3':['QG','HG*'],'QHB2':['QB','HB*'],'QHB3':['QB','HB*'],'QHG2':['QG','HG*'],'QHG3':['QG','HG*'],'QHE21':['QE2','HE2*'],'QHE22':['QE2','HE2*'],'RHB2':['QB','HB*'],'RHB3':['QB','HB*'],'RHD2':['QD','HD*'],'RHD3':['QD','HD*'],'RHG2':['QG','HG*'],'RHG3':['QG','HG*'],'RHH11':['QH1','HH1*'],'RHH12':['QH1','HH1*'],'RHH21':['QH2','HH2*'],'RHH22':['QH2','HH2*'],'SHB2':['QB','HB*'],'SHB3':['QB','HB*'],'THG2':['QG2', 'HG2*'],'VHB2':['QB','HB*'],'VHB3':['QB','HB*'],'VHG1':['QG1', 'HG1*'],'VHG2':['QG2', 'HG2*'],'WHB2':['QB','HB*'],'WHB3':['QB','HB*'],'YHB2':['QB','HB*'],'YHB3':['QB','HB*'],'YHD1':['QD','HD*'],'YHD2':['QD','HD*'],'YHE1':['QE','HE*'],'YHE2':['QE','HE*']}
Pseudo2Prot = {'AQB':['HB'],'CQB':['HB2', 'HB3'],'DHB':['HB2', 'HB3'],'DQB':['HB2', 'HB3'],'EHB':['HB2', 'HB3'],'EHG':['HG2', 'HG3'],'EQB':['HB2', 'HB3'],'EQG':['HG2', 'HG3'],'FHB':['HB2', 'HB3'],'FHD':['HD1', 'HD2'],'FHE':['HE1', 'HE2'],'FQB':['HB2', 'HB3'],'FQD':['HD1', 'HD2'],'FQE':['HE1', 'HE2'],'GHA':['HA2', 'HA3'],'GQA':['HA2', 'HA3'],'HHB':['HB2', 'HB3'],'HHB':['HB2', 'HB3'],'HQB':['HB2', 'HB3'],'IHG1':['HG12', 'HG13'],'IQD1':['HD1'],'IQG1':['HG1'],'IQG2':['HG2'],'KHD':['HD2', 'HD3'],'KHE':['HE2', 'HE3'],'KHG':['HG2', 'HG3'],'KHZ':['HZ2', 'HZ3'],'KQD':['HD2', 'HD3'],'KQE':['HE2', 'HE3'],'KQG':['HG2', 'HG3'],'KQZ':['HZ2', 'HZ3'],'LHB':['HB2', 'HB3'],'LQB':['HB2', 'HB3'],'LQD1':['HD1'],'LQD2':['HD2'],'MHB':['HB2', 'HB3'],'MHG':['HG2', 'HG3'],'MQB':['HB2', 'HB3'],'MQE':['HE'],'MQG':['HG2', 'HG3'],'NHB':['HB2', 'HB3'],'NHD2':['HD21', 'HD22'],'NQB':['HB2', 'HB3'],'NQD2':['HD21', 'HD22'],'PHB':['HB2', 'HB3'],'PHD':['HD2', 'HD3'],'PHG':['HG2', 'HG3'],'PQB':['HB2', 'HB3'],'PQD':['HD2', 'HD3'],'PQG':['HG2', 'HG3'],'QE2':['HE21', 'HE22'],'QHB':['HB2', 'HB3'],'QHG':['HG2', 'HG3'],'QQB':['HB2', 'HB3'],'QQE2':['HE21', 'HE22'],'QQG':['HG2', 'HG3'],'RHB':['HB2', 'HB3'],'RHD':['HD2', 'HD3'],'RHG':['HG2', 'HG3'],'RHH1':['HH11', 'HH12'],'RHH2':['HH21', 'HH22'],'RQB':['HB2', 'HB3'],'RQD':['HD2', 'HD3'],'RQG':['HG2', 'HG3'],'RQH1':['HH11', 'HH12'],'RQH2':['HH21', 'HH22'],'SHB':['HB2', 'HB3'],'SQB':['HB2', 'HB3'],'TQG2':['HG2'],'VHB':['HB2', 'HB3'],'VQB':['HB2', 'HB3'],'VQG1':['HG1'],'VQG2':['HG2'],'WHB':['HB2', 'HB3'],'WQB':['HB2', 'HB3'],'YHB':['HB2', 'HB3'],'YHD':['HD1', 'HD2'],'YHE':['HE1', 'HE2'],'YQB':['HB2', 'HB3'],'YQD':['HD1', 'HD2'],'YQD':['HD1','HD2'],'YQE':['HE1', 'HE2'],'YQE':['HE1', 'HE2']}

AAA_dict = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
 "GLU": "E", "GLN": "Q", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L",
 "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T",
 "TRP": "W", "TYR": "Y", "VAL": 'V', "MSE":'M', "PTR":'Y', "TPO":"T", "SEP":'S','CYSS':'C', 'HIST':'H'}
 
class spectrum_menu_2D(tkutil.option_menu):

	def __init__(self, session, parent, label, allow_no_choice = 0):

		self.session = session
		self.allow_no_choice = allow_no_choice
		self.names = self.spectrum_names()
		tkutil.option_menu.__init__(self, parent, label,
																self.names, self.default_spectrum_name())
		self.menu['postcommand'] = self.update_menu_cb

	# --------------------------------------------------------------------------
	#
	def spectrum_names(self):

		Names = []
		spectra = self.session.project.spectrum_list()
		for spectrum in spectra:
			if spectrum.dimension == 2:
				Names.append(spectrum)
		names = pyutil.attribute_values(Names, 'name')
		if self.allow_no_choice:
			names = ('',) + names
		return names
	# --------------------------------------------------------------------------
	def default_spectrum_name(self):
		return pyutil.attribute(self.session.selected_spectrum(), 'name', '')
	# --------------------------------------------------------------------------
	def update_menu_cb(self):

		current_names = self.spectrum_names()
		if current_names != self.names:
			self.names = current_names
			self.remove_all_entries()
			for name in self.names:
				self.add_entry(name)
			if not self.get() in self.names:
				self.set(self.default_spectrum_name())
	# --------------------------------------------------------------------------
	def spectrum(self):

		return sputil.name_to_spectrum(self.get(), self.session)

# --------------------------------------------------------------------------
class spectrum_menu_3D(tkutil.option_menu):

	def __init__(self, session, parent, label, allow_no_choice = 0):

		self.session = session
		self.allow_no_choice = allow_no_choice
		self.names = self.spectrum_names()
		tkutil.option_menu.__init__(self, parent, label,
																self.names, self.default_spectrum_name())
		self.menu['postcommand'] = self.update_menu_cb

	# --------------------------------------------------------------------------
	#
	def spectrum_names(self):
		Names = []
		spectra = self.session.project.spectrum_list()
		for spectrum in spectra:
			if spectrum.dimension == 3 and 'sim' not in spectrum.name:
				Names.append(spectrum)
		names = pyutil.attribute_values(Names, 'name')
		if self.allow_no_choice:
			names = ('',) + names
		return names

	# --------------------------------------------------------------------------
	#
	def default_spectrum_name(self):

		return pyutil.attribute(self.session.selected_spectrum(), 'name', '')

	# --------------------------------------------------------------------------
	#
	def update_menu_cb(self):

		current_names = self.spectrum_names()
		if current_names != self.names:
			self.names = current_names
			self.remove_all_entries()
			for name in self.names:
				self.add_entry(name)
			if not self.get() in self.names:
				self.set(self.default_spectrum_name())
	# --------------------------------------------------------------------------
	#
	def spectrum(self):

		return sputil.name_to_spectrum(self.get(), self.session)

class obj:
	pass

class assignment_distance_dialog(tkutil.Dialog, tkutil.Stoppable):

	# ------------------------------------------------------------------------------
	#
	def __init__(self, session):

		self.session = session
		self.selection_notice = None
		tkutil.Dialog.__init__(self, session.tk, 'Simulate NOESY from UPL')

		explain = ('(last edits Febraury 21, 2023)\n')
		w = tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')

		ep = tkutil.file_field2(self.top, 'UPL file', 'Browse...', file_type=[('CYANA upper limit file', '.upl')], default_ext='.pdb')
		self.upl_path = ep.variable
		ep.frame.pack(side = 'top', anchor = 'w')

		explain = ('Median Distance (dref')
		w = tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')
		e = tkutil.entry_field(self.top, 'dref: ', '4.0', 5)
		self.median_dist = e.variable
		e.frame.pack(side = 'top', anchor = 'w')

		explain = ('Select NOESY Spectrum')
		w = tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')    
		self.spectrum_choice_3DNOESY = spectrum_menu_3D(session, self.top, '3D NOESY:    ')
		self.spectrum_choice_3DNOESY.frame.pack(side = 'top', anchor = 'w')

	# Reference Spectrum defines w2, w3 of 3D NOESY
		explain = ('Select 2D spectrum which defines the w2, w3 dimensions of NOESY')
		w = tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')
		self.spectrum_choice_ref = spectrum_menu_2D(session, self.top, '2D editing: ')
		self.spectrum_choice_ref.frame.pack(side = 'top', anchor = 'w')

	# NOE SPECTRUM defines atoms found in noe (w1) dimension of 3DNOESY
		explain = ('Select 2D spectra that contain assignments\n that can be assigned to w1 of NOESY spectrum')
		w = tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')    
		self.sc = self.spectrum_choice_table(self.top)
		self.sc.pack(side = 'top', anchor = 'w')

		eh = tkinter.Label(self.top, text = 'Omit peak if note has a word from:')
		eh.pack(side = 'top', anchor = 'w')
		ef = tkutil.entry_field(self.top, '', width = 30)
		ef.frame.pack(side = 'top', anchor = 'w')
		self.note_words = ef
		et = tkinter.Label(self.top, text = '(comma separated list of words)\n')
		et.pack(side = 'top', anchor = 'w')
		et = tkinter.Label(self.top, text = 'note = tag upl [ ]; spec [ ]\n tag:\n   spec - upl > 0.5 bad; spec - upl <= 0.5 long\n   spec - upl < -0.5 good; spec - upl > -0.5 short\n\n upl [ ] =  value from input upl\n spec [ ] = distance calculated from peak intensity\n',justify = 'left')
		et.pack(side = 'top', anchor = 'w')

		progress_label = tkinter.Label(self.top, anchor = 'nw')
		progress_label.pack(side = 'top', anchor = 'w',padx=2)

		br = tkutil.button_row(self.top,
								('Generate peaklist', self.Generate_NOESY),
								('Close', self.close_cb),
								('Stop', self.stop_cb))
		br.frame.pack(side = 'top', anchor = 'w')

		tkutil.Stoppable.__init__(self, progress_label, br.buttons[2])
	# ------------------------------------------------------------------------------
	#
	def spectrum_choice_table(self, parent):

		headings = ('')
		st = sputil.spectrum_table(self.session, parent, headings, self.add_spectrum, self.remove_spectrum)
		st.spectrum_to_checkbutton = {}
		st.chosen_spectra = []
		st.spectrum_epeak_menus = {}
		st.axis_order_menu = {}
		self.spectrum_table = st
		
		spectra = self.session.project.spectrum_list()
		for spectrum in spectra:
			if spectrum.dimension == 2:
				st.add_spectrum(spectrum)
		return st.frame

	def add_spectrum(self, spectrum, table, row):

		# Make spectrum checkbutton
		if spectrum.dimension == 2:
			cb = tkutil.checkbutton(table.frame, spectrum.name, 0)
			#cb.button['selectcolor'] = sputil.spectrum_color(spectrum)
			choose_cb = pyutil.precompose(sputil.choose_spectrum_cb, spectrum, table.chosen_spectra)
			cb.add_callback(choose_cb)
			cb.button.grid(row = row, column = 0, sticky = 'w')
			table.spectrum_to_checkbutton[spectrum] = cb

	def remove_spectrum(self, spectrum, table):

		cb = table.spectrum_to_checkbutton[spectrum]
		cb.set_state(0)
		cb.button.destroy()
		del table.spectrum_to_checkbutton[spectrum]

		table.spectrum_epeak_menus[spectrum].frame.destroy()
		del table.spectrum_epeak_menus[spectrum]

		table.axis_order_menu[spectrum].frame.destroy()
		del table.axis_order_menu[spectrum]

	def get_settings(self):
	
		settings = pyutil.generic_class()
		settings.spectrum_ref = self.spectrum_choice_ref.spectrum()   
		settings.spectrum_3DNOESY = self.spectrum_choice_3DNOESY.spectrum()    
		spectra = self.spectrum_table.chosen_spectra
		settings.spectrum_noe_list=[spectrum for spectrum in spectra]
		settings.upl_path = self.upl_path.get()
		settings.dref = float(self.median_dist.get())
		settings.note_words = self.note_words.variable.get().split(',')
		return settings


	# ------------------------------------------------------------------------------
	# 
	def Generate_NOESY(self):
		s = self.get_settings()
		self.stoppable_call(self.Generate_NOESY_cb)
		message = ('Created %d new cross peaks\nLast run %s' % (self.count, self.time))
		self.progress_report(message)


	# ------------------------------------------------------------------------------
	# 
	def Generate_NOESY_cb(self):

		s = self.get_settings()
		self.session.unselect_all_ornaments()
		for peak in self.session.selected_peaks():
			if peak.label: peak.label.selected = 0
			peak.selected = 0

		Freq_dict = {}
		ref_atoms = {}
		for peak in s.spectrum_ref.peak_list():
			if '?' not in peak.assignment:
				resn = peak.resonances()[0].group.name
				resi = peak.resonances()[0].group.number
				ra1 = peak.resonances()[0].atom.name
				ra2 = peak.resonances()[1].atom.name
				group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, ra2)
				ref_atoms[group] = [resn+ra1, resn+ra2]
				group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, ra1)
				ref_atoms[group] = [resn+ra1, resn+ra2]
				Freq_dict[resn+ra1] = peak.frequency[0]
				Freq_dict[resn+ra2] = peak.frequency[1]

		noe_atoms = {}
		for noe_spectrum in s.spectrum_noe_list:
			for peak in noe_spectrum.peak_list():
				if '?' not in peak.assignment:
					resn = peak.resonances()[0].group.name
					resi = peak.resonances()[0].group.number
					resi2 = peak.resonances()[0].group.symbol +   str(int(peak.resonances()[0].group.number)+1000) ## for dimers
					na1 = peak.resonances()[0].atom.name
					na2 = peak.resonances()[1].atom.name
					if s.spectrum_3DNOESY.nuclei[0] != '1H':
						group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, na1)
						noe_atoms[group]= resn+na1
						group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, na2)
						noe_atoms[group]= resn+na1
						Freq_dict[resn+na1] = peak.frequency[0]
					if s.spectrum_3DNOESY.nuclei[0] == '1H':
						group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, na1)
						noe_atoms[group]= resn+na2
						group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, na2)
						noe_atoms[group]= resn+na2
						Freq_dict[resn+na2] = peak.frequency[1]

## Check if simulation spectrum is present if not create one, if there is clear the peak list. 
		proj_spectra=self.session.project.spectrum_list()
		spectrum_ref_name=s.spectrum_3DNOESY.name
		proj_spec_names = [spectrum.name for spectrum in self.session.project.spectrum_list()]
		if spectrum_ref_name+'_sim' in proj_spec_names:
			print 'Found spectrum in project list'
			spectrum = sputil.name_to_spectrum(spectrum_ref_name+'_sim', self.session)
			for peak in spectrum .peak_list():
				peak.selected = 1
			self.session.command_characters("")
		if spectrum_ref_name+'_sim' not in proj_spec_names:
			save_path_new = str(s.spectrum_3DNOESY.save_path+'SIM')
			save_new = open(save_path_new, 'w')
			save_content = open(s.spectrum_3DNOESY.save_path, 'r')
			if 'condition' in open(s.spectrum_3DNOESY.save_path).read():
				for line in save_content.readlines():
					line = line.replace('name ' + s.spectrum_3DNOESY.name ,'name '+ s.spectrum_3DNOESY.name + '_sim')
					if 'condition' in line:
						line = 'condition sim\n'
					if (line=='<end view>\n'): break
					save_new.write(line)
			if 'condition' not in open(s.spectrum_3DNOESY.save_path).read():
				for line in save_content.readlines():
					if 'name ' + s.spectrum_3DNOESY.name in line:
						line = 'condition sim\n' + line.replace('name ' + s.spectrum_3DNOESY.name ,'name '+ s.spectrum_3DNOESY.name + '_sim')
					if (line=='<end view>\n'): break
					save_new.write(line)
			save_new.write('<end view>\n<ornament>\n<end ornament>\n<end spectrum>\n')
			save_new.close()
			self.session.open_spectrum(save_path_new)

		import re
		Heights,passpeaks = [], []
		for x in range(len(s.spectrum_3DNOESY.peak_list())):
			peak = s.spectrum_3DNOESY.peak_list()[x]
			if len(s.note_words[0]) > 0 and len(peak.note) > 0:
				for words in s.note_words:
					if re.search(words.lower().strip(),peak.note.lower()):
						passpeaks.append(x)
		for x in range(len(s.spectrum_3DNOESY.peak_list())):
			if x not in passpeaks:
				peak = s.spectrum_3DNOESY.peak_list()[x]
				Heights.append(peak.data_height)

		Calcnst = float(median(Heights) * (s.dref**6))
		noise = s.spectrum_3DNOESY.noise
		spectrum = sputil.name_to_spectrum(spectrum_ref_name+'_sim', self.session)
		noe_peak_list = self.restraints(s.upl_path, ref_atoms, noe_atoms)
		print 'Calibration constant for peak list: {:3.2E}'.format(Calcnst)
		for (tassignment,w1,w2,w3,d) in noe_peak_list:
			assignment = sputil.parse_assignment(tassignment)
			frequency = [Freq_dict[w1],Freq_dict[w2],Freq_dict[w3]]
			note = str(d)
			self.create_peak(assignment,frequency, note, "white", spectrum)
		for peak in spectrum.peak_list():
			upl = float(peak.note)
			peak_height = peak.data_height
			SNR = peak_height/noise
			if peak_height <= 0.0: 
				peak.color = 'darkred'
				peak.label.color = peak.color
				peak.note = '    missing'
				pass 
			else: 
				obsD = (Calcnst/abs(peak_height))**(1.0/6.0)
				if SNR > 10:
					peak.note = '    upl {:} ;spec {:3.2f}'.format(peak.note,obsD)
					if obsD - upl > 0.0:
						if obsD - upl <= 0.5:
							peak.color = 'darkorange'
							peak.label.color = peak.color
							peak.note = '     long {:}'.format(peak.note)
						if obsD - upl > 0.5:
							peak.color = 'red'
							peak.label.color = peak.color
							peak.note = '      bad {:}'.format(peak.note)
					if obsD - upl < 0.0: 
						if abs(obsD - upl) <= 0.5:
							peak.color = 'gold'
							peak.label.color = peak.color
							peak.note = '    short {:}'.format(peak.note)
						if abs(obsD - upl) > 0.5:
							peak.color = 'darkgreen'
							peak.label.color = peak.color
							peak.note = '    good {:}'.format(peak.note)
				if SNR <= 10:
					peak.color = 'darkred'
					peak.label.color = peak.color
					peak.note = '    missing: SNR < 10'

		import datetime as time
		self.count = len(noe_peak_list)
		self.time = time.datetime.now().strftime("%m-%d-%y %H:%M")
		message = ('Created %d new cross peaks\nLast run %s' % (self.count, self.time))
		self.progress_report(message)
		# tkMessageBox.showinfo('Task Complete', "Finished Simulating NOESY")
	# ------------------------------------------------------------------------------
	# return atoms_list entry containing expansion of pseudo atoms for entries 
	# found in the PDB 
	# ------------------------------------------------------------------------------

	def get_groups(self, resi, resn, a1):
		groups = []
		if resn in AAA_dict.keys():
			ra = AAA_dict[resn] + a1.replace('*','')
		if ra in Pseudo2Prot.keys():
			for atom in Pseudo2Prot[ra]:
				groups.append('{:} {:} {:}'.format(AAA_dict[resn], resi, atom))
		if ra not in Pseudo2Prot.keys():
			groups.append('{:} {:} {:}'.format(AAA_dict[resn], resi, a1))
		return groups

	# ------------------------------------------------------------------------------
	# Look for Restraints 
	# 
	def restraints(self, path, ref_atoms, noe_atoms):
	# 471 ASP  N      475 GLU  N       5.48
		NOESY3D_peaklist = []
		for line in open(path).readlines():
			if line.strip()[0] != '#':
				resi1, resn1, atom1, resi2, resn2, atom2, dist = line.split()[0:7]
				groups1 = self.get_groups(resi1, resn1, atom1)
				groups2 = self.get_groups(resi2, resn2, atom2)
				for group1 in groups1:
					for group2 in groups2:
						if group1 in ref_atoms.keys() and group2 in noe_atoms.keys():
							a2, a3 = ref_atoms[group1]
							a1 = noe_atoms[group2]
							NOESY3D_peaklist.append([a1+'-'+a2+'-'+a3, a1, a2, a3, float(dist)])
						if group2 in ref_atoms.keys() and group1 in noe_atoms.keys():
							a2, a3 = ref_atoms[group2]
							a1 = noe_atoms[group1]
							NOESY3D_peaklist.append([a1+'-'+a2+'-'+a3, a1, a2, a3, float(dist)])

		if len(NOESY3D_peaklist) < 2:
			tkMessageBox.showinfo('Input Error', "No NOESY entries generated \nCheck input selections and try again")
			return
		return tuple(NOESY3D_peaklist)

# -----------------------------------------------------------------------------
#
	def create_peak(self, assignment, frequency, note, color, spectrum):

		peak = spectrum.place_peak(frequency)
		self.move_peak_onto_spectrum(peak)

		assigned = 0
		for a in range(spectrum.dimension):
			group_name, atom_name = assignment[a]
			if group_name or atom_name:
				peak.assign(a, group_name, atom_name)
				assigned = 1
		if assigned:
			peak.show_assignment_label()

		if color:
			peak.color = color

		if note:
			peak.note = note
		return
	def move_peak_onto_spectrum(self, peak):

		freq = peak.frequency
		pos = sputil.alias_onto_spectrum(freq, peak.spectrum)
		if pos != freq:
			peak.position = pos
			peak.alias = pyutil.subtract_tuples(freq, pos)

def show_dialog(session):
	sputil.the_dialog(assignment_distance_dialog,session).show_window(1)
