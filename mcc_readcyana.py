# -----------------------------------------------------------------------------
# Read a peak list from cyana and create peaks directly onto a spectrum
# (Dec 14, 2019)
# Last updated 08/11/2022
# -----------------------------------------------------------------------------
#
# Originated from Enrico Morelli's code
#
# -----------------------------------------------------------------------------
#
import string
import re
import tkinter
import pyutil
import sparky
import sputil
import cyana
import tkutil
import os
import tkinter.messagebox
import tkMessageBox 
# -----------------------------------------------------------------------------
#
AAA_dict = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
			'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
			'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
			'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M', 
			'ADE': 'A', 'GUA': 'G', 'CYT': 'C', 'URA': 'U', 'THY': 'T','HIST':'H', 'HISE':'H'}
amino = {'ALA' : 'A', 'CYS' : 'C', 'CYSS' : 'C','ASP' : 'D', 'ASP-' : 'D',
				 'GLU' : 'E', 'GLU-' : 'E', 'PHE' : 'F', 'GLY' : 'G', 'HIS' : 'H',
				 'HIS+' : 'H','HEM' : 'H', 'ILE' : 'I', 'LYS' : 'K', 'LYS+' : 'K',
				 'LEU' : 'L', 'ASN' : 'N', 'MET' : 'M', 'PRO' : 'P', 'GLN' : 'Q',
				 'ARG' : 'R', 'ARG+' : 'R','SER' : 'S', 'THR' : 'T', 'VAL' : 'V',
				 'TRP' : 'W', 'TYR' : 'Y'}

# -----------------------------------------------------------------------------
#
class read_cyana_peaks_dialog(tkutil.Dialog, tkutil.Stoppable):

	def __init__(self, session):

		self.session = session
		self.selection_notice = None

		tkutil.Dialog.__init__(self, session.tk, 'Read Cyana peak list')

		## Get the sequence for the protein, if one does not exist prompt user to load one 
		try:
			persist_path = self.session.project.save_path + '.seq'
		except:
			persist_path = ''
		seq_dict = {} #key = index, value = group
		# If the session.project.save_path + '.seq' file exist then produce seq_dct = idx:szAidx
		if os.path.exists(persist_path):
			pszLines =[line.rstrip() for line in open(persist_path).readlines() if line.rstrip() and ">" not in line and "#" not in line]
			for line in pszLines:
				if line.split()[0] in AAA_dict.keys():
					seq_dict[line.split()[1]] = AAA_dict[line.split()[0]] + str(line.split()[1])

		if not os.path.exists(persist_path):
			tkMessageBox.showinfo('Input Error', "No Sequence file was found\n Please load a sequence using 'sq' command\nSave the project and relaunch MAGIC-Act")

		self.fseq = seq_dict

		plp = tkutil.file_field2(self.top, 'Cyana output peak file: ', 'peaklist', file_type=[('cyana peak list', '.peaks')], default_ext='.peaks')
		plp.frame.pack(side = 'top', anchor = 'e')
		self.peak_list_path = plp

		prt = tkutil.file_field2(self.top, 'Cyana prot file: ', 'prot', file_type=[('cyana prot file', '.prot')], default_ext='.prot')
		prt.frame.pack(side = 'top', anchor = 'w')
		self.prot_path = prt

		explain = ('Condition to set in save files (def: cyana):')
		w = tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')

		cn_nam = tkutil.entry_field(self.top, 'Condition: ', 'CYANA', 12)
		self.cond_name = cn_nam.variable
		cn_nam.frame.pack(side = 'top', anchor = 'w')

		order=('xy','yx','xyz','xzy','yxz','yzx','zxy','zyx')
		initial=order[2]
		self.order = tkutil.option_menu(self.top, "Select output order", order, initial)
		self.order.frame.pack(side = 'top', anchor = 'w')  

		sc = sputil.spectrum_menu(session, self.top, 'Spectrum: ')
		sc.frame.pack(side = 'top', anchor = 'w')
		self.spectrum_choice = sc

		progress_label = tkinter.Label(self.top, anchor = 'nw')
		progress_label.pack(side = 'top', anchor = 'w')

		br = tkutil.button_row(self.top,
				('Create peaks', self.read_cb),
				('Stop', self.stop_cb),
				('Close', self.close_cb),
				('Help', sputil.help_cb(session, 'ReadPeaks')),
				)
		br.frame.pack(side = 'top', anchor = 'w')

		tkutil.Stoppable.__init__(self, progress_label, br.buttons[1])

		#self.settings = self.get_settings()
	# ---------------------------------------------------------------------------
	#
	def read_cb(self):

		condition_name = self.cond_name.get()
		fin = self.peak_list_path.get()
		fpath = fin.replace(fin.split('/')[-1], '')
		fprot = self.prot_path.get()
		seq_dict = self.fseq
		calc = os.path.join(fpath, 'CALC.cya')
		fupl = os.path.join(fpath, 'final.upl')
		fovw = fupl.replace('.upl','.ovw')
		spectrum = self.spectrum_choice.spectrum()
		order = self.order.get()
		self.order.get()
		if fin and seq_dict and spectrum:
			self.stoppable_call(self.read_peaks, fin, fprot, seq_dict, fupl, fovw, calc, spectrum, order, condition_name)
			message = ('Transfered %d peaks\n Last run %s' % (self.count, self.time))
			self.progress_report(message)

	# ---------------------------------------------------------------------------
	#

	def read_peaks(self, fin, fprot, seq_dict, fupl, fovw, calc, spectrum, order, condition_name):

		inspec = spectrum 
		save_path_new = str(spectrum.save_path+condition_name)
		save_new = open(save_path_new, 'w')
		save_content = open(spectrum.save_path, 'r')
		proj_spec_names = [spec.name for spec in self.session.project.spectrum_list()]
		self.session.unselect_all_ornaments()
		if inspec.name + '_' + condition_name in proj_spec_names:
			cyaspectrum = sputil.name_to_spectrum(inspec.name+ '_' + condition_name, self.session)
			for peak in cyaspectrum .peak_list():
				peak.selected = 1
			self.session.command_characters("")
		if inspec.name + '_' + condition_name not in proj_spec_names:
			if 'condition' in open(inspec.save_path).read():
				for line in save_content.readlines():
					if 'name ' + inspec.name in line:
						line = line.replace('name ' + inspec.name ,'name '+ inspec.name + '_' + condition_name)
					if 'condition' in line:
						line = line.replace('\n',condition_name + '\n')
					if (line=='<end view>\n'): break
					save_new.write(line)
			if 'condition' not in open(inspec.save_path).read():
				for line in save_content.readlines():
					if 'name ' + inspec.name in line:
						line = 'condition ' + condition_name + '\n' + line.replace('name ' + inspec.name ,'name '+ inspec.name + '_' + condition_name)
					if (line=='<end view>\n'): break
					save_new.write(line)
			save_new.write('<end view>\n<ornament>\n<end ornament>\n<end spectrum>\n')
			save_new.close()
			self.session.open_spectrum(save_path_new)
		
		cyaspectrum = sputil.name_to_spectrum(inspec.name + '_' + condition_name, self.session)
		CYANAplist = self.cyana_peak_list(fin, fprot, seq_dict, cyaspectrum, self.get_dist(calc, fupl, fin), self.get_viols(calc, fovw, fin), order)
		self.count = 0 
		for (assignment, frequency, note, pcolor, lcolor) in CYANAplist:
			self.count = self.count +1 
			self.create_peak(assignment, frequency, note, pcolor, lcolor, cyaspectrum)
		import datetime as time
		self.time = time.datetime.now().strftime("%m-%d-%y %H:%M")

	# ---------------------------------------------------------------------------
	#
	def get_dist(self, calc, fupl, fin):
		dist = {}
		cya_plist = [line.strip() for line in open(calc).readlines() if line.strip() and 'peaks' in line][0].split()[2].split(',')
		for x in range(len(cya_plist)):
			if cya_plist[x].replace('.peaks','-cycle7.peaks') == fin.split('/')[-1]:
				lupl = [line.strip() for line in open(fupl).readlines() if line.strip() and 'plist '+ str(x+1) in line]
				for upl in lupl:
					d = upl.split()[6]
					pkn = upl.split()[8]
					dist[pkn] = d 
		return dist

	# ---------------------------------------------------------------------------
	#
	def get_viols(self, calc, fovw, fin):
		viols = {}
		cya_plist = [line.strip() for line in open(calc).readlines() if line.strip() and 'peaks' in line][0].split()[2].split(',')
		for x in range(len(cya_plist)):
			if cya_plist[x].replace('.peaks','-cycle7.peaks') == fin.split('/')[-1]:
				fovwl = [line.strip() for line in open(fovw).readlines() if line.strip() and 'list '+ str(x+1) in line]
				for viol in fovwl:
					pkn = viol[viol.find('peak')+4:viol.find('list')].strip()
					vmax = viol[58:62]
					viols[pkn] = 'viol ' + viol[40:44] + '+' + viol[58:62]
		return viols

	def cyana_peak_list(self, fin, fprot, seq_dict, spectrum, dist, viols, order):

		# >>>> Open Cyana Peak list file remove any commented out lines and blank lines <<<<

		cyplines = [line.strip().replace("#",'') for line in open(fin).readlines() if line.strip() and line[0] != "#"]

		protlines= [line.strip() for line in open(fprot).readlines() if line.strip() and line[0] != "#"]

		# Create dictionaries to convert sequence index value to group (20 to A20), 
		# translate CYANA numerical code to sparky group-atom, and indicate which 
		# chain the residue is in

		cyntrans = {} #key = cyana #code; value = [sparky group-atom, chain]
		for line in protlines:
			cyntrans[line.split()[0]]= seq_dict[line.split()[4]] + line.split()[3]

		# -----------------------------------------------------------------------------
		# Fill in missing information for ambiguous assignments and create peak entries
		# -----------------------------------------------------------------------------
		stype = str(str(spectrum.dimension)+'D')
		pldim = int(open(fin).readline()[-2])
		print pldim

		peakslist = []
		for i in range(len(cyplines)):
			if stype == '2D' and len(cyplines[i].split()) >= 10:## Unambiguous/Unassigned 2D
				peakslist.append(cyplines[i])
			if stype == '2D' and  len(cyplines[i].split()) < 10:## Ambiguous 2D
				cyplines[i] = peakslist[i-1][0:peakslist[i-1].find(' U ')+35] + ' ' + cyplines[i]
				peakslist.append(cyplines[i])
			if stype == '3D' and len(cyplines[i].split()) >= 12:## Unambiguous/Unassigned 3D
				peakslist.append(cyplines[i])
			if stype == '3D' and  len(cyplines[i].split()) < 12:## Ambiguous 3D
				cyplines[i] = peakslist[i-1][0:peakslist[i-1].find(' U ')+35] + ' ' + cyplines[i]
				peakslist.append(cyplines[i])

		# -----------------------------------------------------------------------------
		# Use filled in cyan peak list (pline) to generate new colored coded cross peaks
		# green = unambiguous = green
		# white = unassigned = white
		# magenta = ambiguous = magenta
		# purple = inter molecular = beige
		# -----------------------------------------------------------------------------

		CYANA_peak_list = []
		for x in range(len(peakslist)):
			pline = peakslist[x].split()
			peak_id = pline[0]
			idx = pline.index('U') + 2
			note = '    %4s;  '%peak_id
			if peakslist[x].split()[0] in dist.keys():
				if peakslist[x].split()[0] in viols.keys():
					note =  note  + viols[peakslist[x].split()[0]] 
					lcolor,pcolor = "red","red"
				if peakslist[x].split()[0] not in viols.keys():
					note = note + dist[peakslist[x].split()[0]]
			if stype == '2D':
				## Assigned
				if order == 'xy':a1,a2,f1,f2 = 3,4,1,2
				if order == 'yx':a1,a2,f1,f2 = 4,3,2,1
				if pline[idx+3] != "0":
					assignment = sputil.parse_assignment(cyntrans[pline[idx+a1]] + '-' + cyntrans[pline[idx+a2]])
					frequency = [float(pline[f1]), float(pline[f2])]
					## Ambiguous 
					if "VC" in pline:
						note = note + peakslist[x][peakslist[x].find('VC'):peakslist[x].find('VC') + 8].strip() + ' '
						if peakslist[x].find('QU') > 0:
							note = note + peakslist[x][peakslist[x].find('QU'):peakslist[x].find('QU') + 8].strip()
							if float(pline[pline.index('QU')+1]) >= 0.85: 
								lcolor,pcolor = "orange","orange"
							if float(pline[pline.index('QU')+1]) < 0.85: 
								lcolor,pcolor = "DarkOrange","DarkOrange"
						if peakslist[x].find('QU') < 0:
							note = note + peakslist[x][peakslist[x].find('SUP'):peakslist[x].find('SUP') + 9].strip()
							if float(pline[pline.index('SUP')+1]) >= 0.85: 
								lcolor,pcolor = "orange","orange"
							if float(pline[pline.index('SUP')+1]) < 0.85: 
								lcolor,pcolor = "DarkOrange","DarkOrange"
						if pline[0] == peakslist[x-1].split()[0]:
							pcolor = "DarkOrange1"
					## Unambiguous 
					if "VC" not in pline:
						if peakslist[x].find('QU') > 0:
							note = peakslist[x][peakslist[x].find('QU'):].strip()
							if float(pline[pline.index('QU')+1]) >= 0.85: 
								lcolor,pcolor  = "DarkGreen","DarkGreen"
							if float(pline[pline.index('QU')+1]) < 0.85: 
								lcolor,pcolor = "LightGoldenrod","LightGoldenrod"
						if peakslist[x].find('QU') < 0:
							note = peakslist[x][peakslist[x].find('SUP'):].strip()
							if float(pline[pline.index('SUP')+1]) >= 0.85: 
								lcolor,pcolor  = "DarkGreen","DarkGreen"
							if float(pline[pline.index('SUP')+1]) < 0.85: 
								lcolor,pcolor = "LightGoldenrod","LightGoldenrod"
					CYANA_peak_list.append([assignment, frequency, note, lcolor, pcolor])
				## Unassigned
				if pline[idx+9][0] == "0":
					assignment = sputil.parse_assignment('?-?')
					lcolor,pcolor = "white","white"
					frequency = [float(pline[f1]), float(pline[f2])]
					CYANA_peak_list.append([assignment, frequency, note, lcolor, pcolor])

			if stype == '3D':
				## Assigned
				if order == 'xyz':a1,a2,a3,f1,f2,f3 = 3,4,5,1,2,3
				if order == 'xzy':a1,a2,a3,f1,f2,f3 = 3,5,4,1,3,2
				if order == 'yxz':a1,a2,a3,f1,f2,f3 = 4,3,5,2,1,3
				if order == 'yzx':a1,a2,a3,f1,f2,f3 = 4,5,3,2,3,1
				if order == 'zxy':a1,a2,a3,f1,f2,f3 = 5,3,4,3,1,2
				if order == 'zyx':a1,a2,a3,f1,f2,f3 = 5,4,3,3,2,1
				if pline[idx+3] != "0":
					assignment = sputil.parse_assignment(cyntrans[pline[idx+a1]] + '-' + cyntrans[pline[idx+a2]] + '-' + cyntrans[pline[idx+a3]])
					frequency = [float(pline[f1]), float(pline[f2]), float(pline[f3])]
					## Ambiguous 
					if "VC" in pline:
						note = note + peakslist[x][peakslist[x].find('VC'):peakslist[x].find('VC') + 8].strip() + ' '
						if peakslist[x].find('QU') > 0:
							note = note + peakslist[x][peakslist[x].find('QU'):peakslist[x].find('QU') + 8].strip()
							if float(pline[pline.index('QU')+1]) >= 0.85: 
								lcolor,pcolor = "orange","orange"
							if float(pline[pline.index('QU')+1]) < 0.85: 
								lcolor,pcolor = "DarkOrange","DarkOrange"
						if peakslist[x].find('QU') < 0:
							note = note + peakslist[x][peakslist[x].find('SUP'):peakslist[x].find('SUP') + 9].strip()
							if float(pline[pline.index('SUP')+1]) >= 0.85: 
								lcolor,pcolor = "orange","orange"
							if float(pline[pline.index('SUP')+1]) < 0.85: 
								lcolor,pcolor = "DarkOrange","DarkOrange"
						if pline[0] == peakslist[x-1].split()[0]:
							pcolor = "DarkOrange1"
					## Unambiguous 
					if "VC" not in pline:
						if peakslist[x].find('QU') > 0:
							note = note + peakslist[x][peakslist[x].find('QU'):peakslist[x].find('QU') + 8].strip()
							if float(pline[pline.index('QU')+1]) >= 0.85: 
								lcolor,pcolor  = "DarkGreen","DarkGreen"
							if float(pline[pline.index('QU')+1]) < 0.85: 
								lcolor,pcolor = "LightGoldenrod","LightGoldenrod"
						if peakslist[x].find('QU') < 0:
							note = note + peakslist[x][peakslist[x].find('SUP'):peakslist[x].find('SUP') + 9].strip()
							if float(pline[pline.index('SUP')+1]) >= 0.85: 
								lcolor,pcolor  = "DarkGreen","DarkGreen"
							if float(pline[pline.index('SUP')+1]) < 0.85: 
								lcolor,pcolor = "LightGoldenrod","LightGoldenrod"

					CYANA_peak_list.append([assignment, frequency, note, pcolor, lcolor])
				## Unassigned 
				if pline[idx+3] == "0":
					assignment = sputil.parse_assignment('?-?-?')
					lcolor,pcolor = "white", "white"
					frequency = [float(pline[f1]), float(pline[f2]), float(pline[f3])]
					CYANA_peak_list.append([assignment, frequency, note, pcolor, lcolor])
		return tuple(CYANA_peak_list)
	# -----------------------------------------------------------------------------
	#
	def create_peak(self, assignment, frequency, note, pcolor, lcolor, spectrum):

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

		peak.color = pcolor
		if peak.label:
			peak.label.color = lcolor
		if note:
			peak.note = note

		return

	# ---------------------------------------------------------------------------
	# If the peak is off the edge of the spectrum, fold it onto the spectrum
	# and set the alias to keep its frequency the same.
	#
	def move_peak_onto_spectrum(self, peak):

		freq = peak.frequency
		pos = sputil.alias_onto_spectrum(freq, peak.spectrum)
		if pos != freq:
			peak.position = pos
			peak.alias = pyutil.subtract_tuples(freq, pos)

# -----------------------------------------------------------------------------
#
def read_cyana_peak_list(session):
	sputil.the_dialog(read_cyana_peaks_dialog,session).show_window(1)
