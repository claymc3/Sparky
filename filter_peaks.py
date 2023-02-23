import Tkinter
import pyutil
import sparky
import sputil
import tkutil
import tkMessageBox
import expectedpeaks

# ------------------------------------------------------------------------------
#
# Updated by : Mary Clay PhD
# e-mail: mary.clay@stjude.org
# St Jude Children's Research Hospital 
# Department of Structural Biology Memphis, TN 
#
# Last updates: February 9, 2023
#
#
# ------------------------------------------------------------------------------
#
# Generate w2w3 2D pull down menu, using only 2D spectra found in project
#
class spectrum_menu_2D(tkutil.option_menu):

	def __init__(self, session, parent, label, allow_no_choice = 0):

		self.session = session
		self.allow_no_choice = allow_no_choice
		self.names = self.spectrum_names()
		tkutil.option_menu.__init__(self, parent, label,
																self.names, self.default_spectrum_name())
		self.menu['postcommand'] = self.update_menu_cb

	# --------------------------------------------------------------------------
	# Select for only 2D spectra 
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
	# Get parent spectrum name, so duplicate views are not used 
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
#
# ---------------------------------------------------------------------------
#
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

class filter_peaks_dialog(tkutil.Dialog, tkutil.Stoppable):

	# ------------------------------------------------------------------------------
	#
	def __init__(self, session):

		self.session = session
		self.selection_notice = None
		tkutil.Dialog.__init__(self, session.tk, 'Filter 3D peak list')

		explain = ('Colors cross peaks red which have frequencies not found reference 2Ds\n'+ 
							 'User can use pC command to select these peaks and delete them\n'
							'(last edits February 9, 2023)\n')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')

		self.spectrum_choice_3D = sputil.spectrum_menu(session, self.top, '3D Spectrum:    ')
		self.spectrum_choice_3D.frame.pack(side = 'top', anchor = 'w')

	# SPECTRUM Type Options
		w = Tkinter.Label(self.top, text = '3D Spectrum Type', justify = 'left')
		w.pack(side = 'top', anchor = 'w')

		noesycb = tkutil.checkbutton(self.top, 'NOESY 3D', 1)
		noesycb.button.pack(side = 'top', anchor = 'w')
		self.noesy = noesycb
		HNCocb = tkutil.checkbutton(self.top, 'HNCo', 0)
		HNCocb.button.pack(side = 'top', anchor = 'w')
		self.HNCo = HNCocb
		HNCAcb = tkutil.checkbutton(self.top, 'HNCA/HNcoCA', 0)
		HNCAcb.button.pack(side = 'top', anchor = 'w')
		self.HNCA = HNCAcb
		HNCACBcb = tkutil.checkbutton(self.top, 'HNCACB', 0)
		HNCACBcb.button.pack(side = 'top', anchor = 'w')
		self.HNCACB = HNCACBcb
		HNcoCACBcb = tkutil.checkbutton(self.top, 'HNCoCACB', 0)
		HNcoCACBcb.button.pack(side = 'top', anchor = 'w')
		self.HNcoCACB = HNcoCACBcb
		CBCAcoNHcb = tkutil.checkbutton(self.top, 'CBCAcoNH', 0)
		CBCAcoNHcb.button.pack(side = 'top', anchor = 'w')
		self.CBCAcoNH = CBCAcoNHcb

	# 2D spectrum defining w2, w3 of 3D
		explain = ('\n2D spectrum defining w2, w3 of 3D spectrum')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')
		self.w2w3_spectrum_choice = spectrum_menu_2D(session, self.top, '2D editing: ')
		self.w2w3_spectrum_choice.frame.pack(side = 'top', anchor = 'w')

	# NOE SPECTRUM defines atoms found in noe (w1) dimension of 3DNOESY
		explain = ('\nSelect all 2D spectra that contain assignments\n that can be assigned to w1 of NOESY spectrum')
		w = Tkinter.Label(self.top, text = explain, justify = 'left')
		w.pack(side = 'top', anchor = 'w')    
		self.sc = self.spectrum_choice_table(self.top)
		self.sc.pack(side = 'top', anchor = 'w')

		br = tkutil.button_row(self.top,
													 ('Filter peaklist', self.Filter_cb),
													 ('Close', self.close_cb),
													 ('Stop', self.stop_cb))
		br.frame.pack(side = 'top', anchor = 'w')
		er = tkutil.entry_row(self.top, 'PPM tolerance: ',
																		('1H', '0.01', 5),
																		('13C', '0.10', 5),
																		('15N', '0.10', 5),
																		('NOE', '0.20', 5))
		er.frame.pack(side = 'top', anchor = 'w')
		self.ppm_range = er

		progress_label = Tkinter.Label(self.top, anchor = 'nw')
		progress_label.pack(side = 'top', anchor = 'w')
		self.settings = self.get_settings()
		tkutil.Stoppable.__init__(self, progress_label, br.buttons[2])

	# ------------------------------------------------------------------------------
	#
	def spectrum_choice_table(self, parent):

		headings = ('')
		st = sputil.spectrum_table(self.session,parent,headings,self.add_spectrum, self.remove_spectrum)
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
		settings.w2w3_spectrum = self.w2w3_spectrum_choice.spectrum()   
		settings.spectrum_3D = self.spectrum_choice_3D.spectrum()    
		spectra = self.spectrum_table.chosen_spectra
		settings.spectrum_w1_list=[spectrum for spectrum in spectra]
		settings.noesy = self.noesy.state()
		settings.HNCo = self.HNCo.state()
		settings.HNCA = self.HNCA.state()
		settings.HNCACB = self.HNCACB.state()
		settings.HNcoCACB = self.HNcoCACB.state()
		settings.CBCAcoNH = self.CBCAcoNH.state()
		settings.tolerance={'1H':float(self.ppm_range.variables[0].get()),'13C':float(self.ppm_range.variables[1].get()),'15N':float(self.ppm_range.variables[2].get()),'NOE':float(self.ppm_range.variables[3].get())}
		
		return settings

	# ------------------------------------------------------------------------------
	# 
	def Filter_cb(self):
		settings = self.get_settings()
		if settings.noesy == True:
			self.stoppable_call(self.Filter_NOESY)
			message = (' Checked %d peaks of %d peaks' % (self.checked, self.numpeaks))
			self.progress_report(message)
		if settings.HNCo == True or settings.HNCA == True or settings.CBCAcoNH == True:
			self.stoppable_call(self.Filter_BackBone_sp)
			message = (' Checked %d peaks of %d peaks' % (self.checked, self.numpeaks))
			self.progress_report(message)
		if settings.HNCACB == True or settings.HNcoCACB == True:
			self.stoppable_call(self.Filter_BackBone_tp)
			message = (' Checked %d peaks of %d peaks' % (self.checked, self.numpeaks))
			self.progress_report(message)
	# ------------------------------------------------------------------------------
	# 

	def Filter_NOESY(self):
		s = self.get_settings()
		spectrum = s.spectrum_3D
		if spectrum == None:
			return
		if len(s.spectrum_w1_list) == 0:
			tkMessageBox.showinfo('Input Error', "Please Select 2D spectra containing w1 frequencies of NOESY")
			return
		## Get identity nuclei of each dimension in 3D noesy
		w1nuc = s.spectrum_3D.nuclei[0]
		w2nuc = s.spectrum_3D.nuclei[1]
		w3nuc = s.spectrum_3D.nuclei[2]
		## Get dimension index in w2w3 2D spectrum corresponding to w2 and w3 nuclei in 3D NOESY
		w2idx = s.w2w3_spectrum.nuclei.index(w2nuc)
		w3idx = s.w2w3_spectrum.nuclei.index(w3nuc)
		## Make a list of all possible values of w1 in 3D NOESY
		w1_freqs = []
		for w1_spectrum in s.spectrum_w1_list:
			w1idex = w1_spectrum.nuclei.index(w1nuc)
			for peak in w1_spectrum.peak_list():
				w1_freqs.append(peak.frequency[w1idex])
		## Generate a list of peak in NOESY that have acceptable values of w1, w2, and w3. 
		peaks = s.spectrum_3D.peak_list()
		self.numpeaks = len(peaks)
		Keep_list = []
		w2w3_keep = []
		w2w3_peaks = s.w2w3_spectrum.peak_list()

		for i in range(len(peaks)):
			self.checked = i + 1
			peak = peaks[i] ## this allows for count to be shown in progress label 
			for w2w3 in w2w3_peaks:
				if (abs(peak.frequency[1] - w2w3.frequency[w2idx]) < s.tolerance[w2nuc]) and (abs(peak.frequency[2] - w2w3.frequency[w3idx]) < s.tolerance[w3nuc]) and i not in w2w3_keep:
					w2w3_keep.append(i)
			message = (' Checked %d peaks of %d peaks for w2w3 consistency' % (self.checked , self.numpeaks))
			self.progress_report(message)
		self.checked = 0
		for x in w2w3_keep:
			self.checked = x + 1
			peak = peaks[x]
			for w1 in w1_freqs:
				if abs(peak.frequency[0] - w1) < s.tolerance['NOE'] and x not in Keep_list:
					Keep_list.append(x)
			message = (' Checked %d peaks of %d peaks for w1 consistency' % (self.checked , self.numpeaks))
			self.progress_report(message)

		for i in range(len(peaks)):
			peak = peaks[i]
			note = peak.note
			if i not in Keep_list:
				peak.color = 'red'
				if 'Bad w1 frequency;' not in note:
					peak.note = 'Bad w1 frequency; ' + note
				peak.selected = 1
				if i not in w2w3_keep:
					peak.color = 'red'
					if 'Bad w2 w3 frequencies;' not in note:
						peak.note = 'Bad w2 w3 frequencies; ' + note
					peak.selected = 1
		for x in Keep_list:
			peak = peaks[x]
			if peak.color == 'red' and 'Bad w' in peak.note:
				peak.color = 'white'
				peak.note = peak.note.replace('Bad w1 frequency; ', '').replace('Bad w2 w3 frequencies; ', '')
			peak.selected = 0
		if w1nuc == w2nuc:
			for x in Keep_list:
				peak = peaks[x]
				if abs(peak.frequency[0] - peak.frequency[1]) < s.tolerance[w2nuc]:
					peak.color = 'cyan'
					peak.note = 'diagonal; ' + peak.note
		if w1nuc == w3nuc:
			for x in Keep_list:
				peak = peaks[x]
				if abs(peak.frequency[0] - peak.frequency[2]) < s.tolerance[w3nuc]:
					peak.color = 'cyan'
					peak.note = 'diagonal; ' + peak.note

		tkMessageBox.showinfo("Filter Peaks", "Found %s bad peaks in original %s peaks" % (len(peaks) -len(Keep_list), len(peaks)))


	def Filter_BackBone_tp(self):
		s = self.get_settings()
		spectrum = s.spectrum_3D
		if spectrum == None:
			return
		## Get identity nuclei of each dimension in 3D noesy
		w1nuc = s.spectrum_3D.nuclei[0]
		w2nuc = s.spectrum_3D.nuclei[1]
		w3nuc = s.spectrum_3D.nuclei[2]
		## Get dimension index in w2w3 2D spectrum corresponding to w2 and w3 nuclei in 3D NOESY
		w2idx = s.w2w3_spectrum.nuclei.index(w2nuc)
		w3idx = s.w2w3_spectrum.nuclei.index(w3nuc)
		## Make a list of all possible values of w1 in 3D NOESY
		w1_freqs = []
		peaks = s.spectrum_3D.peak_list()
		self.numpeaks = len(peaks)
		Keep_list = []
		w2w3_peaks = s.w2w3_spectrum.peak_list()
		for i in range(len(peaks)):
			self.checked = i + 1
			peak = peaks[i] ## this allows for count to be shown in progress label 
			original_color = peak.color ## in case user has colored peaks
			peak.color = 'red'
			peak.selected = 1
			## Pass any peak with frequencies less than 42ppm and a negative intensity 
			if peak.frequency[0] <= 48.0 and peak.data_height < 0.0:
				for w2w3 in w2w3_peaks:
					if (abs(peak.frequency[1] - w2w3.frequency[w2idx]) < s.tolerance[w2nuc]) and (abs(peak.frequency[2] - w2w3.frequency[w3idx]) < s.tolerance[w3nuc]) and peak not in Keep_list:
						print 'peak # %d passed w2w3 filter' %i
						print 'peak w1 = %f' %peak.frequency[0]
						print 'peak data_height = %1.2E' %peak.data_height
						Keep_list.append(peak)
						peak.color = original_color ## rest peak color to original user defined color
						peak.selected= 0
			## Pass any peak with frequencies between 42ppm and 67ppm with a positive intensity
			if peak.frequency[0] >= 42.01 and peak.frequency[0] <= 68.0 and peak.data_height > 0.0:
				for w2w3 in w2w3_peaks:
					if (abs(peak.frequency[1] - w2w3.frequency[w2idx]) < s.tolerance[w2nuc]) and (abs(peak.frequency[2] - w2w3.frequency[w3idx]) < s.tolerance[w3nuc]) and peak not in Keep_list:
						Keep_list.append(peak)
						peak.color = original_color ## rest peak color to original user defined color
						peak.selected= 0
			## Pass any peak with frequencies less than 42ppm and a negative intensity 
			if peak.frequency[0] >= 60.01 and peak.frequency[0] <= 78.0 and peak.data_height < 0.0: 
				for w2w3 in w2w3_peaks:
					if (abs(peak.frequency[1] - w2w3.frequency[w2idx]) < s.tolerance[w2nuc]) and (abs(peak.frequency[2] - w2w3.frequency[w3idx]) < s.tolerance[w3nuc]) and peak not in Keep_list:
						Keep_list.append(peak)
						peak.color = original_color ## rest peak color to original user defined color
						peak.selected= 0
				message = (' Checked %d peaks of %d peaks' % (self.checked , self.numpeaks))
				self.progress_report(message)
		#self.session.command_characters("")
		tkMessageBox.showinfo("Filter Peaks", "Found %s bad peaks in original %s peaks" % (len(peaks) -len(Keep_list), len(peaks)))
		for i in range(len(peaks)):
			peak = peaks[i]
			if peak.color == 'red':
				peak.note  = 'bad frequency'

	def Filter_BackBone_sp(self):
		s = self.get_settings()
		spectrum = s.spectrum_3D
		if spectrum == None:
			return
		## Get identity nuclei of each dimension in 3D noesy
		w1nuc = s.spectrum_3D.nuclei[0]
		w2nuc = s.spectrum_3D.nuclei[1]
		w3nuc = s.spectrum_3D.nuclei[2]
		## Get dimension index in w2w3 2D spectrum corresponding to w2 and w3 nuclei in 3D NOESY
		w2idx = s.w2w3_spectrum.nuclei.index(w2nuc)
		w3idx = s.w2w3_spectrum.nuclei.index(w3nuc)
		## Make a list of all possible values of w1 in 3D NOESY
		w1_freqs = []
		peaks = s.spectrum_3D.peak_list()
		self.numpeaks = len(peaks)
		Keep_list = []
		w2w3_peaks = s.w2w3_spectrum.peak_list()
		for i in range(len(peaks)):
			self.checked = i + 1
			peak = peaks[i] ## this allows for count to be shown in progress label 
			original_color = peak.color ## in case user has colored peaks
			peak.color = 'red'
			peak.selected = 1
			for w2w3 in w2w3_peaks:
				if (abs(peak.frequency[1] - w2w3.frequency[w2idx]) < s.tolerance[w2nuc]) and (abs(peak.frequency[2] - w2w3.frequency[w3idx]) < s.tolerance[w3nuc]) and peak.data_height > 0.0 and peak not in Keep_list:
					## Pass any peak with frequencies less than 42ppm and a negative intensity 
							Keep_list.append(peak)
							peak.color = original_color ## rest peak color to original user defined color
							peak.selected= 0
			message = (' Checked %d peaks of %d peaks' % (self.checked , self.numpeaks))
			# self.progress_report(message)
		# self.session.command_characters("")
		tkMessageBox.showinfo("Filter Peaks", "Found %s bad peaks in original %s peaks" % (len(peaks) -len(Keep_list), len(peaks)))
		for i in range(len(peaks)):
			peak = peaks[i]
			if peak.color == 'red':
				peak.note  = 'bad frequency'
	# ------------------------------------------------------------------------------
	# return atoms_list entry containing assignment and freq_dict keys for a given 
	# heavy atom in atoms_list_ref or atoms_list_noe
	# ------------------------------------------------------------------------------



def show_dialog(session):
	sputil.the_dialog(filter_peaks_dialog,session).show_window(1)
