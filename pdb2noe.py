import Tkinter
import types
import re
import math as m
import pyutil
import sparky
import sputil
import tkutil
import tkMessageBox

# ------------------------------------------------------------------------------
#
# Updated by : Mary Clay PhD
# e-mail: mary.clay@stjude.org
# St Jude Children's Research Hospital 
# Department of Structural Biology Memphis, TN 
#
# Last updates: August 12, 2022
#
#
# ------------------------------------------------------------------------------
#
Pseudo2Prot = {'AQB':['HB1', 'HB2', 'HB3'],'RQB':['HB2', 'HB3'],'RQG':['HG2', 'HG3'],'RQD':['HD2', 'HD3'],'RQH1':['HH11', 'HH12'],'RQH2':['HH21', 'HH22'],'NQB':['HB2', 'HB3'],'NQD2':['HD21', 'HD22'],'DQB':['HB2', 'HB3'],'CQB':['HB2', 'HB3'],'QQB':['HB2', 'HB3'],'QQG':['HG2', 'HG3'],'QQE2':['HE21', 'HE22'],'EQB':['HB2', 'HB3'],'EQG':['HG2', 'HG3'],'GQA':['HA2', 'HA3'],'HQB':['HB2', 'HB3'],'IQG1':['HG11', 'HG12', 'HG13'],'IQG2':['HG21', 'HG22', 'HG23'],'IQD1':['HD11', 'HD12', 'HD13'],'LQB':['HB2', 'HB3'],'LQD1':['HD11', 'HD12', 'HD13'],'LQD2':['HD21', 'HD22', 'HD23'],'KQG':['HG2', 'HG3'],'KQD':['HD2', 'HD3'],'KQE':['HE2', 'HE3'],'KQZ':['HZ2', 'HZ3'],'MQB':['HB2', 'HB3'],'MQG':['HG2', 'HG3'],'MQE':['HE1', 'HE2', 'HE3'],'FQB':['HB2', 'HB3'],'FQD':['HD1', 'HD2'],'FQE':['HE1', 'HE2'],'PQB':['HB2', 'HB3'],'PQG':['HG2', 'HG3'],'PQD':['HD2', 'HD3'],'SQB':['HB2', 'HB3'],'TQG2':['HG21', 'HG22', 'HG23'],'WQB':['HB2', 'HB3'],'YQB':['HB2', 'HB3'],'YQD':['HD1', 'HD2'],'YQE':['HE1', 'HE2'],'VQB':['HB2', 'HB3'],'VQG1':['HG11', 'HG12', 'HG13'],'VQG2':['HG21', 'HG22', 'HG23'],'AHB':['HB1', 'HB2', 'HB3'],'RHB':['HB2', 'HB3'],'RHG':['HG2', 'HG3'],'RHD':['HD2', 'HD3'],'RHH1':['HH11', 'HH12'],'RHH2':['HH21', 'HH22'],'NHB':['HB2', 'HB3'],'NHD2':['HD21', 'HD22'],'DHB':['HB2', 'HB3'],'HHB':['HB2', 'HB3'],'QHB':['HB2', 'HB3'],'QHG':['HG2', 'HG3'],'QNE2':['HE21', 'HE22'],'EHB':['HB2', 'HB3'],'EHG':['HG2', 'HG3'],'GHA':['HA2', 'HA3'],'HHB':['HB2', 'HB3'],'IHG1':['HG12', 'HG13'],'IHG2':['HG21', 'HG22', 'HG23'],'IHD1':['HD11', 'HD12', 'HD13'],'LHB':['HB2', 'HB3'],'LHD1':['HD11', 'HD12', 'HD13'],'LHD2':['HD21', 'HD22', 'HD23'],'KHG':['HG2', 'HG3'],'KHD':['HD2', 'HD3'],'KHE':['HE2', 'HE3'],'KHZ':['HZ2', 'HZ3'],'MHB':['HB2', 'HB3'],'MHG':['HG2', 'HG3'],'MHE':['HE1', 'HE2', 'HE3'],'FHB':['HB2', 'HB3'],'FHD':['HD1', 'HD2'],'FHE':['HE1', 'HE2'],'PHB':['HB2', 'HB3'],'PHG':['HG2', 'HG3'],'PHD':['HD2', 'HD3'],'SHB':['HB2', 'HB3'],'THG2':['HG21', 'HG22', 'HG23'],'WHB':['HB2', 'HB3'],'YHB':['HB2', 'HB3'],'YHD1':['HD1'],'YHD2':['HD2'],'YHE1':['HE1', 'HE2'],'VHB':['HB2', 'HB3'],'VHG1':['HG11', 'HG12', 'HG13'],'VHG2':['HG21', 'HG22', 'HG23']}
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
		tkutil.Dialog.__init__(self, session.tk, 'Simulate 3D NOESY from PDB')

		explain = ('(last edits August 9, 2022)\n')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')

		explain = ('PDB does NOT need H, H treated with sum r-6')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')        
		ep = tkutil.file_field2(self.top, 'PDB file', 'Browse...', file_type=[('Protein Data Bank File', '.pdb')], default_ext='.pdb')
		self.pdb_path = ep.variable
		ep.frame.pack(side = 'top', anchor = 'w')

		explain = ('Distance threshold for het. atom to het. atom')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')
		e = tkutil.entry_field(self.top, 'distance cutoff: ', '', 5)
		self.max_dist = e.variable
		e.frame.pack(side = 'top', anchor = 'w')

		explain = ('Specify which chain(s) should be used,limit 2')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')
		ch = tkutil.entry_field(self.top, 'Use Chain(s): ', 'A', 5)
		self.chains = ch.variable
		ch.frame.pack(side = 'top', anchor = 'w')

		explain = ('Specify which model number should be used,limit 1')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')
		mn = tkutil.entry_field(self.top, 'Use Model: ', '', 5)
		self.model_number = mn.variable
		mn.frame.pack(side = 'top', anchor = 'w')

		explain = ('Select NOESY Spectrum')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')    
		self.spectrum_choice_3DNOESY = spectrum_menu_3D(session, self.top, '3D NOESY:    ')
		self.spectrum_choice_3DNOESY.frame.pack(side = 'top', anchor = 'w')

	# Reference Spectrum defines w2, w3 of 3D NOESY
		explain = ('Select 2D spectrum wich defines the w2, w3 dimensions of NOESY')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')
		self.spectrum_choice_ref = spectrum_menu_2D(session, self.top, '2D editing: ')
		self.spectrum_choice_ref.frame.pack(side = 'top', anchor = 'w')

	# NOE SPECTRUM defines atoms found in noe (w1) dimension of 3DNOESY
		explain = ('Select 2D spectra that contain assignments\n that can be assigned to w1 of NOESY spectrum')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')    
		self.sc = self.spectrum_choice_table(self.top)
		self.sc.pack(side = 'top', anchor = 'w')

		ib = tkutil.checkbutton(self.top, 'With diagonal peaks?', 0)
		ib.button.pack(side = 'top', anchor = 'w')
		self.diagonal = ib

		im = tkutil.checkbutton(self.top, 'Mono-mythyl', 0)
		im.button.pack(side = 'top', anchor = 'w')
		self.mono = im

		ha = tkutil.checkbutton(self.top, 'Use Heavy Atoms', 0)
		ha.button.pack(side = 'top', anchor = 'w')
		self.heavyatoms = ha

		progress_label = Tkinter.Label(self.top, anchor = 'nw')
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
		settings.pdb_path = self.pdb_path.get()   
		settings.diagonal=self.diagonal.state()
		settings.mono=self.mono.state()
		settings.max_distance = pyutil.string_to_float(self.max_dist.get())
		settings.chains = self.chains.get().replace(',','')
		settings.mnum = self.model_number.get()
		settings.heavyatoms = self.heavyatoms.state()
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
		for peak in self.session.selected_peaks():
			if peak.label: peak.label.selected = 0
			peak.selected = 0
		### Figure out if PDB is protonated
		protonated = False
		for line in open(s.pdb_path).readlines():
			if line[0:4] == "ATOM" and line[12:16].strip() == "HB2":
				protonated = True
				break
		if s.heavyatoms == True:
			protonated = False

		Freq_dict = {}
		atoms_list_ref = []
		for peak in s.spectrum_ref.peak_list():
			if '?' not in peak.assignment:
				resn = peak.resonances()[0].group.name
				resi = peak.resonances()[0].group.number
				ra1 = peak.resonances()[0].atom.name
				ra2 = peak.resonances()[1].atom.name
				if protonated == True:
					group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, ra2)
				if protonated == False:
					group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, ra1)
				atoms_list_ref.append([group,resn+ra1, resn+ra2])
				Freq_dict[resn+ra1] = peak.frequency[0]
				Freq_dict[resn+ra2] = peak.frequency[1]

		atoms_list_noe = []
		for noe_spectrum in s.spectrum_noe_list:
			for peak in noe_spectrum.peak_list():
				if '?' not in peak.assignment:
					resn = peak.resonances()[0].group.name
					resi = peak.resonances()[0].group.number
					resi2 = peak.resonances()[0].group.symbol +   str(int(peak.resonances()[0].group.number)+1000) ## for dimers
					na1 = peak.resonances()[0].atom.name
					na2 = peak.resonances()[1].atom.name
					if protonated == True:
						group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, na2)
					if protonated == False:
						group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, na1)
					if s.spectrum_3DNOESY.nuclei[0] != '1H':
						atoms_list_noe.append([group,resn+na1])
						Freq_dict[resn+na1] = peak.frequency[0]
					if s.spectrum_3DNOESY.nuclei[0] == '1H':
						atoms_list_noe.append([group,resn+na2])
						Freq_dict[resn+na2] = peak.frequency[1]
					if len(s.chains) == 2:
						if protonated == True:
							group2 = '%s %s %s' %(peak.resonances()[0].group.symbol, resi2, na2)
						if protonated == False:
							group2 = '%s %s %s' %(peak.resonances()[0].group.symbol, resi2, na1)
						if s.spectrum_3DNOESY.nuclei[0] != '1H':
							atoms_list_noe.append([group2,resn2+na1])
							Freq_dict[resn2+na1] = peak.frequency[0]
						if s.spectrum_3DNOESY.nuclei[0] == '1H':
							atoms_list_noe.append([group2,resn2+na2])
							Freq_dict[resn2+na2] = peak.frequency[1]

## Check if simulation spectrum is present if not create one, if there is clear the peak list. 
		proj_spectra=self.session.project.spectrum_list()
		spectrum_ref_name=s.spectrum_3DNOESY.name
		proj_spec_names = [spectrum.name for spectrum in self.session.project.spectrum_list()]
		if spectrum_ref_name+'_sim' in proj_spec_names:
			print('Found spectrum in project list')
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

		spectrum = sputil.name_to_spectrum(spectrum_ref_name+'_sim', self.session)
		noe_peak_list = self.distances(s.pdb_path, s.max_distance, s.chains, s.mnum, s.diagonal, s.mono, atoms_list_ref, atoms_list_noe)
		for (tassignment,w1,w2,w3,d) in noe_peak_list:
			assignment = sputil.parse_assignment(tassignment)
			frequency = [Freq_dict[w1],Freq_dict[w2],Freq_dict[w3]]
			note = str(d)
			if d == 0.0:
				color = "cyan"
			if d <= 4.0 and d != 0.0:
				color = 'green'
			if d > 4.0: 
				color = "white"
			self.create_peak(assignment,frequency, note, color, spectrum)
			if d > 0.0: 
				print '------ '+str(tassignment.replace(w3,assignment[2][1]))+' ------'
				print "%14.1f" %d 
		for (label, peak) in zip(spectrum.label_list(), spectrum.peak_list()):
			label.color = peak.color
			peak.color = "white"
			if label.color == "cyan":
				peak.color = "cyan"
		import datetime as time
		self.count = len(noe_peak_list)
		self.time = time.datetime.now().strftime("%m-%d-%y %H:%M")
		message = ('Created %d new cross peaks\nLast run %s' % (self.count, self.time))
		self.progress_report(message)

	# ------------------------------------------------------------------------------
	# return atoms_list entry containing expansion of pseudo atoms for entries 
	# found in the PDB 
	# ------------------------------------------------------------------------------

	def find_atoms(self, inatom, PDBdict):
		resn1, resi1, name1 = inatom.split()
		atoms = []
		if resn1+name1 in Pseudo2Prot.keys():
			for atomid in ['%s %s %s'%(resn1,resi1,atom) for atom in Pseudo2Prot[resn1+name1]]:
				if atomid in PDBdict.keys():
					atoms.append(atomid)
		if resn1+name1 not in Pseudo2Prot.keys():
			if inatom in PDBdict.keys():
				atoms.append(inatom)
		return atoms

	# ------------------------------------------------------------------------------
	# Read in PDB file line by line, and build two list of values:
	# PDB_lines_ref : list based on assignments in 2D editing spectrum 
	#                 (rgroup,rw1,rw2,rx,ry,rz) 
	#                 rgroup = the sequence specific identity of heavy atom,
	#                 rw1 = Freq_dict key for w2 frequency in 3D NOESY,
	#                 rw2 = Freq_dict key for w3 frequency in 3D NOESY,
	#                 rx,ry,rz = Cartesian coordinates of heavy atoms) 
	#
	# PDB_lines_noe : list based on assignments in 2D spectra containing assignments 
	#                 for nuclei with which NOEs occur (w1 dimension of 3D NOESY)
	#                 (ngroup,nw,nx,ny,nz)
	#                 ngroup = the sequence specific identity of heavy atom,
	#                 nw = Freq_dict key for w1 frequency in 3D NOESY,
	#                 nx,ny,nz = Cartesian coordinates of heavy atoms) 
	#
	# If dimer is used then 1000 is added to the index of residues found in second
	# chain. These residues are only added to PDB_lines_noe, so that intra molecular
	# contacts are not doubled, and intra molecular contacts can be found easily
	# 
	# Returns: 
	# NOESY3D_peaklist :list of  new peak entry for ref and noe heavy atoms within  
	#                   the user specified distance cutoff 
	#                   (Assignment, nw, rw1, rw2, distance)
	#
	# ------------------------------------------------------------------------------
	def getDistance(self, donor, acceptor,PDBdict):
		d = 0.0
		for a1 in donor:
			for a2 in acceptor:
				(x1,y1,z1) = PDBdict[a1]
				(x2,y2,z2) = PDBdict[a2]
				d = d + m.pow(m.pow((m.pow((x1-x2),2) + m.pow((y1-y2),2) + m.pow((z1-z2),2)),0.5),-6)
		reff = round(m.pow(d, -1/6.0), 2)
		return reff

	def distances(self, path, Cutoff, chains, mnum, diagonal, mono, atoms_list_ref,atoms_list_noe):
		resids = []
		if len(mnum) != 0:
			model = 'MODEL' + '%9s\n' %mnum
			start = open(path).readlines().index(model)
		if len(mnum) == 0:
			start = 0
		PDBdict ={}
		if len(chains) == 1:
			for line in open(path).readlines()[start:]:
				if line == 'ENDMDL\n': break
				if line[0:4] == "ATOM" or line[0:4] == 'HETA':
					if line[17:20].strip() in AAA_dict.keys() and line[21] == chains:
						if re.search('[1-9]', line[12:16].strip()[0]):
							atom = line[12:16].strip()[1:] + line[12:16].strip()[0]
						else: atom = line[12:16].strip()
						group = '%s %s %s' %(AAA_dict[line[17:20].strip()],line[22:26].strip(),atom)
						PDBdict[group]=[float(line[30:38].strip()),float(line[38:46].strip()),float(line[46:54].strip())]
						resids.append(AAA_dict[line[17:20].strip()]+line[22:26].strip())
		if len(chains) == 2:
			for line in open(path).readlines()[start:]:
				if line == 'ENDMDL\n': break
				if line[0:4] == "ATOM" or line[0:4] == 'HETA':
					if line[17:20].strip() in AAA_dict.keys() and line[21] == chains[0]:
						if re.search('[1-9]', line[12:16].strip()[0]):
							atom = line[12:16].strip()[1:] + line[12:16].strip()[0]
						else: atom = line[12:16].strip()
						group = '%s %s %s' %(AAA_dict[line[17:20].strip()],line[22:26].strip(),line[12:16].strip())
						PDBdict[group]=[float(line[30:38].strip()),float(line[38:46].strip()),float(line[46:54].strip())]
						resids.append(AAA_dict[line[17:20].strip()]+line[22:26].strip())
					if line[17:20].strip() in AAA_dict.keys() and line[21] == chains[1]:
						if re.search('[1-9]', line[12:16].strip()[0]):
							atom = line[12:16].strip()[1:] + line[12:16].strip()[0]
						else: atom = line[12:16].strip()
						group = '%s %s %s' %(AAA_dict[line[17:20].strip()],str(int(line[22:26].strip()) + 1000),line[12:16].strip())
						PDBdict[group]=[float(line[30:38].strip()),float(line[38:46].strip()),float(line[46:54].strip())]
						resids.append(AAA_dict[line[17:20].strip()]+str(int(line[22:26].strip()) + 1000))
		if len(PDBdict) < 2:
			tkMessageBox.showinfo('Input Error', "No PDB entries found \n Check input selections try again")
			return
		NOESY3D_peaklist = []
		for (atom1,noew2,noew3) in atoms_list_ref:
			atoms1 = self.find_atoms(atom1, PDBdict)
			for (atom2,noew1) in atoms_list_noe:
				atoms2 = self.find_atoms(atom2, PDBdict)
				if len(atoms1) != 0 and len(atoms2) != 0 and atom1 != atom2:
					if mono == True:
						if atom1.split()[1] != atom2.split()[1]:
							d = self.getDistance(atoms1, atoms2, PDBdict)
					if mono != True:
						d = self.getDistance(atoms1, atoms2, PDBdict)
					if d <= Cutoff:
						NOESY3D_peaklist.append([noew1+"-"+noew2+"-"+noew3, noew1, noew2, noew3, d])
		if len(NOESY3D_peaklist) < 2:
			tkMessageBox.showinfo('Input Error', "No NOESY entries generated \n Check input selections and try again")
			return
		if diagonal == True:
			for (atom1,noew2,noew3) in atoms_list_ref:
				for (atom2,noew1) in atoms_list_noe:
					if atom1 == atom2:
						NOESY3D_peaklist.append([noew1+"-"+noew2+"-"+noew3, noew1, noew2, noew3, 0.0])

		return tuple(NOESY3D_peaklist)
#
#
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
