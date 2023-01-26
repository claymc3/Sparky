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
# Last updates: January 26, 2023
#
#
# ------------------------------------------------------------------------------
#
Pseudo2Prot = {'AQB':['HB1', 'HB2', 'HB3'],'RQB':['HB2', 'HB3'],'RQG':['HG2', 'HG3'],'RQD':['HD2', 'HD3'],'RQH1':['HH11', 'HH12'],'RQH2':['HH21', 'HH22'],'NQB':['HB2', 'HB3'],'NQD2':['HD21', 'HD22'],'DQB':['HB2', 'HB3'],'CQB':['HB2', 'HB3'],'QQB':['HB2', 'HB3'],'QQG':['HG2', 'HG3'],'QQE2':['HE21', 'HE22'],'EQB':['HB2', 'HB3'],'EQG':['HG2', 'HG3'],'GQA':['HA2', 'HA3'],'HQB':['HB2', 'HB3'],'IQG1':['HG11', 'HG12', 'HG13'],'IQG2':['HG21', 'HG22', 'HG23'],'IQD1':['HD11', 'HD12', 'HD13'],'LQB':['HB2', 'HB3'],'LQD1':['HD11', 'HD12', 'HD13'],'LQD2':['HD21', 'HD22', 'HD23'],'KQG':['HG2', 'HG3'],'KQD':['HD2', 'HD3'],'KQE':['HE2', 'HE3'],'KQZ':['HZ2', 'HZ3'],'MQB':['HB2', 'HB3'],'MQG':['HG2', 'HG3'],'MQE':['HE1', 'HE2', 'HE3'],'FQB':['HB2', 'HB3'],'FQD':['HD1', 'HD2'],'FQE':['HE1', 'HE2'],'PQB':['HB2', 'HB3'],'PQG':['HG2', 'HG3'],'PQD':['HD2', 'HD3'],'SQB':['HB2', 'HB3'],'TQG2':['HG21', 'HG22', 'HG23'],'WQB':['HB2', 'HB3'],'YQB':['HB2', 'HB3'],'YQD':['HD1', 'HD2'],'YQE':['HE1', 'HE2'],'VQB':['HB2', 'HB3'],'VQG1':['HG11', 'HG12', 'HG13'],'VQG2':['HG21', 'HG22', 'HG23'],'AHB':['HB1', 'HB2', 'HB3'],'RHB':['HB2', 'HB3'],'RHG':['HG2', 'HG3'],'RHD':['HD2', 'HD3'],'RHH1':['HH11', 'HH12'],'RHH2':['HH21', 'HH22'],'NHB':['HB2', 'HB3'],'NHD2':['HD21', 'HD22'],'DHB':['HB2', 'HB3'],'HHB':['HB2', 'HB3'],'QHB':['HB2', 'HB3'],'QHG':['HG2', 'HG3'],'QNE2':['HE21', 'HE22'],'EHB':['HB2', 'HB3'],'EHG':['HG2', 'HG3'],'GHA':['HA2', 'HA3'],'HHB':['HB2', 'HB3'],'IHG1':['HG12', 'HG13'],'IHG2':['HG21', 'HG22', 'HG23'],'IHD1':['HD11', 'HD12', 'HD13'],'LHB':['HB2', 'HB3'],'LHD1':['HD11', 'HD12', 'HD13'],'LHD2':['HD21', 'HD22', 'HD23'],'KHG':['HG2', 'HG3'],'KHD':['HD2', 'HD3'],'KHE':['HE2', 'HE3'],'KHZ':['HZ2', 'HZ3'],'MHB':['HB2', 'HB3'],'MHG':['HG2', 'HG3'],'MHE':['HE1', 'HE2', 'HE3'],'FHB':['HB2', 'HB3'],'FHD':['HD1', 'HD2'],'FHE':['HE1', 'HE2'],'PHB':['HB2', 'HB3'],'PHG':['HG2', 'HG3'],'PHD':['HD2', 'HD3'],'SHB':['HB2', 'HB3'],'THG2':['HG21', 'HG22', 'HG23'],'WHB':['HB2', 'HB3'],'YHB':['HB2', 'HB3'],'YHD':['HD1','HD2'],'YHE':['HE1', 'HE2'],'VHB':['HB2', 'HB3'],'VHG1':['HG11', 'HG12', 'HG13'],'VHG2':['HG21', 'HG22', 'HG23']}
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
		tkutil.option_menu.__init__(self, parent, label ,self.names, self.default_spectrum_name())
		self.menu['postcommand'] = self.update_menu_cb

	# --------------------------------------------------------------------------
	#
	def spectrum_names(self):
		Names = []
		spectra = self.session.project.spectrum_list()
		for spectrum in spectra:
			if spectrum.dimension >= 3 and 'sim' not in spectrum.name:
				if '_cyana' not in spectrum.name:
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

NOESY_Specs = []

class assignment_distance_dialog(tkutil.Dialog, tkutil.Stoppable):

	# ------------------------------------------------------------------------------
	#
	def __init__(self, session):

		self.session = session
		self.selection_notice = None
		tkutil.Dialog.__init__(self, session.tk, 'Simulate 3D NOESY from PDB')

		explain = ('(last edits January 26, 2023)\n')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')

		explain = ('PDB does NOT need H, H treated with sum r-6')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')        
		ep = tkutil.file_field2(self.top, 'PDB file', 'Browse...', file_type=[('Protein Data Bank File', '.pdb')], default_ext='.pdb')
		self.pdb_path = ep.variable
		ep.frame.pack(side = 'top', anchor = 'w')

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

	## Reference Spectra Containing NOESY Assingments 
		w = Tkinter.Label(self.top, text = 'Select 2D Spectra Containing Assingments', justify = 'left')
		w.pack(side = 'top', anchor = 'w')
		self.HN_spectrum = spectrum_menu_2D(session, self.top, 'HN: ')
		self.HN_spectrum.frame.pack(side = 'top', anchor = 'w',pady = 2)
		self.Ali_spectrum = spectrum_menu_2D(session, self.top, 'Ali/Me: ')
		self.Ali_spectrum.frame.pack(side = 'top', anchor = 'w',pady = 2)
		self.Aro_spectrum = spectrum_menu_2D(session, self.top, 'Aromatic: ')
		self.Aro_spectrum.frame.pack(side = 'top', anchor = 'w',pady = 2)
		self.Other_spectrum = spectrum_menu_2D(session, self.top, 'Other: ')
		self.Other_spectrum.frame.pack(side = 'top', anchor = 'w',pady = 2)

		im = tkutil.checkbutton(self.top, 'Mono-mythyl', 0)
		im.button.pack(side = 'top', anchor = 'w')
		self.mono = im
		ha = tkutil.checkbutton(self.top, 'Use Heavy Atoms', 0)
		ha.button.pack(side = 'top', anchor = 'w')
		self.heavyatoms = ha
		progress_label = Tkinter.Label(self.top, anchor = 'nw')
		progress_label.pack(side = 'top', anchor = 'w',padx=2)

		br = tkutil.button_row(self.top,
								('Add NOESY', self.add_NOESY),
								('Generate peaklist', self.Generate_NOESY),
								('Close', self.close_cb),
								('Stop', self.stop_cb))
		br.frame.pack(side = 'top', anchor = 'w')

		tkutil.Stoppable.__init__(self, progress_label, br.buttons[3])

	# ------------------------------------------------------------------------------
	# 
	def add_NOESY(self):
		self.lf = Tkinter.LabelFrame(self.top, text = 'NOESY Settings')
		self.lf.pack(fill=Tkinter.X, pady=5, padx=5)
		noesyframe = Tkinter.Frame(self.lf)
		l1 = Tkinter.Label(noesyframe, text = '2D Editing:  ')
		l2 = Tkinter.Label(noesyframe, text = '     NOESY:  ')
		l1.grid(row = 2, column = 0)
		l2.grid(row = 3, column = 0)

		spectrum = spectrum_menu_3D(self.session,noesyframe, 'Spectrum: ')
		spectrum.frame.grid(row =0, column = 0, sticky = Tkinter.W, columnspan = 4)
		distance =  tkutil.entry_field(noesyframe, 'Distance Cutoff: ', '5', 5)
		max_dist = distance.variable
		distance.frame.grid(row = 1, column = 0, columnspan = 2)
		diagonal = tkutil.checkbutton2(noesyframe,'With Diagonal', 0,1,2)
		edim_nh = tkutil.checkbutton2(noesyframe, 'HN',  0,2,1)
		edim_ali = tkutil.checkbutton2(noesyframe, 'Ail/Me',  0,2,2)
		edim_aro = tkutil.checkbutton2(noesyframe, 'Aromatic', 0,2,3)
		edim_other = tkutil.checkbutton2(noesyframe,  'Other',  0,2,4)
		noe_nh = tkutil.checkbutton2(noesyframe,  'HN',  0,3,1)
		noe_ali = tkutil.checkbutton2(noesyframe,  'Ail/Me', 0,3,2)
		noe_aro = tkutil.checkbutton2(noesyframe, 'Aromatic', 0,3,3)
		noe_other = tkutil.checkbutton2(noesyframe, 'Other', 0,3,4)
		NOESY_Specs.append((spectrum, max_dist, diagonal ,edim_nh ,edim_ali ,edim_aro, edim_other, noe_nh, noe_ali,noe_aro, noe_other))
		noesyframe.pack(pady=5, padx = 5)

	# ------------------------------------------------------------------------------
	#

	def get_settings(self):

		settings = pyutil.generic_class()
		settings.HN_spectrum = self.HN_spectrum.spectrum()
		settings.Ali_spectrum = self.Ali_spectrum.spectrum()
		settings.Aro_spectrum = self.Aro_spectrum.spectrum()
		settings.Other_spectrum = self.Other_spectrum.spectrum()
		settings.pdb_path = self.pdb_path.get()
		settings.mono=self.mono.state()
		settings.chains = self.chains.get().replace(',','')
		settings.mnum = self.model_number.get()
		settings.heavyatoms = self.heavyatoms.state()
		print settings.HN_spectrum.name
		print settings.Ali_spectrum.name
		print settings.Aro_spectrum.name
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
		### Figure out if PDB is protonated
		protonated = False
		for line in open(s.pdb_path).readlines():
			if line[0:4] == "ATOM" and line[12:16].strip() == "HB2":
				protonated = True
				break
		if s.heavyatoms == True:
			protonated = False

		for (spectrum, max_dist, diagonal ,edim_nh ,edim_ali ,edim_aro, edim_other, noe_nh, noe_ali, noe_aro, noe_other) in NOESY_Specs:
			NOESY_Spectrum = spectrum.spectrum()
			ref_spectrum, noe_spectra = '', []
			if edim_nh.state(): ref_spectrum = s.HN_spectrum
			if edim_ali.state(): ref_spectrum = s.Ali_spectrum
			if edim_aro.state(): ref_spectrum = s.Aro_spectrum
			if edim_other.state(): ref_spectrum = s.Other_spectrum
			if noe_nh.state(): noe_spectra.append(s.HN_spectrum)
			if noe_ali.state(): noe_spectra.append(s.Ali_spectrum)
			if noe_aro.state(): noe_spectra.append(s.Aro_spectrum)
			if noe_other.state(): noe_spectra.append(s.Other_spectrum)

			Freq_dict = {}
			editing_atoms = []
			for peak in ref_spectrum.peak_list():
				if '?' not in peak.assignment:
					resn = peak.resonances()[0].group.name
					resi = peak.resonances()[0].group.number
					if isinstance(resi,int) == True and isinstance(resn[0],str) == True:
						ra1 = peak.resonances()[0].atom.name
						ra2 = peak.resonances()[1].atom.name
						if protonated == True:
							group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, ra2)
						if protonated == False:
							group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, ra1)
						editing_atoms.append([group,resn+ra1, resn+ra2])
						Freq_dict[resn+ra1] = peak.frequency[0]
						Freq_dict[resn+ra2] = peak.frequency[1]

			noe_atoms = []
			for noe_spectrum in noe_spectra:
				for peak in noe_spectrum.peak_list():
					if '?' not in peak.assignment:
						resn = peak.resonances()[0].group.name
						resi = peak.resonances()[0].group.number
						if isinstance(resi,int) == True and isinstance(resn[0],str) == True:
							resi2 = peak.resonances()[0].group.symbol +   str(int(peak.resonances()[0].group.number)+1000) ## for dimers
							na1 = peak.resonances()[0].atom.name
							na2 = peak.resonances()[1].atom.name
							if protonated == True:
								group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, na2)
							if protonated == False:
								group = '%s %s %s' %(peak.resonances()[0].group.symbol, resi, na1)
							if NOESY_Spectrum.nuclei[0] != '1H':
								noe_atoms.append([group,resn+na1])
								Freq_dict[resn+na1] = peak.frequency[0]
							if NOESY_Spectrum.nuclei[0] == '1H':
								noe_atoms.append([group,resn+na2])
								Freq_dict[resn+na2] = peak.frequency[1]
							if len(s.chains) == 2:
								if protonated == True:
									group2 = '%s %s %s' %(peak.resonances()[0].group.symbol, resi2, na2)
								if protonated == False:
									group2 = '%s %s %s' %(peak.resonances()[0].group.symbol, resi2, na1)
								if NOESY_Spectrum.nuclei[0] != '1H':
									noe_atoms.append([group2,resn2+na1])
									Freq_dict[resn2+na1] = peak.frequency[0]
								if NOESY_Spectrum.nuclei[0] == '1H':
									noe_atoms.append([group2,resn2+na2])
									Freq_dict[resn2+na2] = peak.frequency[1]
			## Check if simulation spectrum is present if not create one, if there is clear the peak list. 
			proj_spectra=self.session.project.spectrum_list()
			spectrum_ref_name=NOESY_Spectrum.name
			proj_spec_names = [spectrum.name for spectrum in self.session.project.spectrum_list()]

			if spectrum_ref_name+'_sim' in proj_spec_names:
				print('Found spectrum in project list')
				spectrum = sputil.name_to_spectrum(spectrum_ref_name+'_sim', self.session)
				for peak in spectrum .peak_list():
					peak.selected = 1
				self.session.command_characters("")

			if spectrum_ref_name+'_sim' not in proj_spec_names:
				save_path_new = str(NOESY_Spectrum.save_path+'SIM')
				save_new = open(save_path_new, 'w')
				save_content = open(NOESY_Spectrum.save_path, 'r')
				if 'condition' in open(NOESY_Spectrum.save_path).read():
					for line in save_content.readlines():
						line = line.replace('name ' + NOESY_Spectrum.name ,'name '+ NOESY_Spectrum.name + '_sim')
						if 'condition' in line:
							line = 'condition sim\n'
						if (line=='<end view>\n'): break
						save_new.write(line)
				if 'condition' not in open(NOESY_Spectrum.save_path).read():
					for line in save_content.readlines():
						if 'name ' + NOESY_Spectrum.name in line:
							line = 'condition sim\n' + line.replace('name ' + NOESY_Spectrum.name ,'name '+ NOESY_Spectrum.name + '_sim')
						if (line=='<end view>\n'): break
						save_new.write(line)
				save_new.write('<end view>\n<ornament>\n<end ornament>\n<end spectrum>\n')
				save_new.close()
				self.session.open_spectrum(save_path_new)

			out_spectrum = sputil.name_to_spectrum(spectrum_ref_name+'_sim', self.session)
			noe_peak_list = self.distances(s.pdb_path, pyutil.string_to_float(max_dist.get()), s.chains, s.mnum, diagonal.state(), s.mono, editing_atoms, noe_atoms)
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
				self.create_peak(assignment,frequency, note, color, out_spectrum)
				if d > 0.0: 
					print '------ '+str(tassignment.replace(w3,assignment[2][1]))+' ------'
					print "%14.1f" %d 
			for peak in out_spectrum.peak_list():
				peak.label.color = peak.color
				peak.color = "white"
				if peak.label.color == "cyan":
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

	def distances(self, path, Cutoff, chains, mnum, diagonal, mono, editing_atoms,noe_atoms):
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
					chainid = line[21]
					if chainid  == ' ':chainid = line[72]
					if line[17:20].strip() in AAA_dict.keys() and chainid == chains:
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
					chainid = line[21]
					if chainid  == ' ':chainid = line[72]
					if line[17:20].strip() in AAA_dict.keys() and chainid == chains[0]:
						if re.search('[1-9]', line[12:16].strip()[0]):
							atom = line[12:16].strip()[1:] + line[12:16].strip()[0]
						else: atom = line[12:16].strip()
						group = '%s %s %s' %(AAA_dict[line[17:20].strip()],line[22:26].strip(),line[12:16].strip())
						PDBdict[group]=[float(line[30:38].strip()),float(line[38:46].strip()),float(line[46:54].strip())]
						resids.append(AAA_dict[line[17:20].strip()]+line[22:26].strip())
					if line[17:20].strip() in AAA_dict.keys() and chainid == chains[1]:
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
		for (atom1,noew2,noew3) in editing_atoms:
			atoms1 = self.find_atoms(atom1, PDBdict)
			for (atom2,noew1) in noe_atoms:
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
			for (atom1,noew2,noew3) in editing_atoms:
				for (atom2,noew1) in noe_atoms:
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
