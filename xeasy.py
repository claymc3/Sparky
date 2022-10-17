# -----------------------------------------------------------------------------
# Produce chemical shift and peak list output from Sparky in XEASY format.
# This is the the format read by structure calculation program Dyana.
#
import string
import Tkinter
import myseq
import pyutil
import sparky
import sputil
import cyana
import tkutil

# -----------------------------------------------------------------------------
#
# Updated by : Mary Clay PhD
# e-mail: mary.clay@stjude.org
# St Jude Children's Research Hospital 
# Department of Structural Biology Memphis, TN 
#
# Last updates: September 13, 2022
#
# Update added the ability of filter the resonances list to detect entries that are
#   Not in sequence 
#   Incorrect atoms name
#   High standard deviation indicating miss assignment 
#
# -----------------------------------------------------------------------------
#

Allowed_atoms = {'A': ['?', 'H', 'HA', 'HB', 'C', 'CA', 'CB', 'N','QB'],
 'C': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HG', 'C', 'CA', 'CB', 'N'],
 'D': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HD2', 'C', 'CA', 'CB', 'CG', 'N'],
 'E': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HE2', 'HG2', 'HG3', 'QG', 'C', 'CA', 'CB', 'CD', 'CG', 'N'],
 'F': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HD1', 'HD2', 'QD', 'HE1', 'HE2', 'QE', 'HZ', 'C', 'CA', 'CB', 'CD1', 'CD2', 'CE1', 'CE2', 'CG', 'CZ', 'N'],
 'G': ['?', 'H', 'HA2', 'HA3', 'C', 'CA', 'N'],
 'H': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'QB', 'HD1', 'HD2', 'QD', 'HE1', 'HE2', 'QE', 'C', 'CA', 'CB', 'CD2', 'CE1', 'CG', 'N', 'ND1', 'NE2'],
 'I': ['?', 'H', 'HA', 'HB', 'HG12', 'HG13', 'QG1', 'HD1', 'QD1', 'HG2', 'QG2', 'C', 'CA', 'CB', 'CD1', 'CG1', 'CG2', 'N'],
 'K': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HD2', 'HD3', 'QD', 'HE2', 'HE3', 'QE', 'HG2', 'HG3', 'QG', 'C', 'CA', 'CB', 'CD', 'CE', 'CG', 'N', 'NZ', 'QZ', 'HZ'],
 'L': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HG', 'HD1', 'QD1', 'HD2', 'QD2', 'C', 'CA', 'CB', 'CD1', 'CD2', 'CG', 'N'],
 'M': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HG2', 'HG3', 'QG', 'HE', 'QE', 'C', 'CA', 'CB', 'CE', 'CG', 'N'],
 'N': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HD21', 'HD22', 'QD', 'C', 'CA', 'CB', 'CG', 'N', 'ND2'],
 'P': ['?', 'HA', 'HB2', 'HB3', 'QB', 'HD2', 'HD3', 'QD', 'HG2', 'HG3', 'QG', 'C', 'CA', 'CB', 'CD', 'CG', 'N'],
 'Q': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HE21', 'HE22', 'QE2', 'HG2', 'HG3', 'QG', 'C', 'CA', 'CB', 'CD', 'CG', 'N', 'NE2'],
 'R': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HD2', 'HD3', 'QD', 'HG2', 'HG3', 'QG', 'HH11', 'HH12','QH1', 'HH21', 'HH22', 'QH2', 'C', 'CA', 'CB', 'CD', 'CG', 'CZ', 'N', 'NE', 'NH1', 'NH2', 'HE'],
 'S': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HG', 'C', 'CA', 'CB', 'N'],
 'T': ['?', 'H', 'HA', 'HB', 'HG1', 'HG2', 'QG2', 'C', 'CA', 'CB', 'CG2', 'N'],
 'V': ['?', 'H', 'HA', 'HB', 'HG1', 'QG1', 'HG2', 'QG2', 'C', 'CA', 'CB', 'CG1', 'CG2', 'N'],
 'W': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HD1', 'HE1', 'HE3', 'HH2', 'HZ2', 'HZ3', 'C', 'CA', 'CB', 'CD1', 'CD2', 'CE2', 'CE3', 'CG', 'CH2', 'CZ2', 'CZ3', 'N', 'NE1'],
 'Y': ['?', 'H', 'HA', 'HB2', 'HB3', 'QB', 'HD1', 'HD2', 'QD', 'HE1', 'HE2', 'QE',  'HH', 'C', 'CA', 'CB', 'CD1', 'CD2', 'CE1', 'CE2', 'CG', 'CZ', 'N']}


# -----------------------------------------------------------------------------
#
class xeasy_format_dialog(tkutil.Dialog, tkutil.Stoppable):

  def __init__(self, session):

    self.session = session
    self.sequence = myseq.ReadSequence(self.session)
    tkutil.Dialog.__init__(self, session.tk, 'DYANA / XEASY Format')

    sc = sputil.spectrum_menu(session, self.top, 'Spectrum: ')
    sc.frame.pack(side = 'top', anchor = 'w')
    self.spectrum_choice = sc

    NOESYtypes = ('2D NOESY [H,H]','3D N15NOESY [H,N,HN]','3D N15NOESY [HN,N,H]','3D C13NOESY [H,C,HC]','3D C13NOESY [HC,C,H]','3D CCNOESY [C1,C2,H2]','3D CCNOESY [H2,C2,H1]','3D NCNOESY [C,N,HN]','3D NCNOESY [HN,N,C]','3D NCNOESY [N,C,HC]','3D NCNOESY [HC,C,N]','4D CCNOESY [H1,C1,C2,H2]','4D NNNOESY [H1,N1,N2,H2]','4D NCNOESY [HC,C,N,HN]','2D DARR [C1,C2]','2D PSDS [C1,C2]','2D PAIN [N,C]','2D PAIN [C,N]','3D PAIN [C,N,HN]','3D PAIN [HN,N,C]')
    initial=NOESYtypes[3]
    self.NOESYtype = tkutil.option_menu(self.top, "Select NOESY Type", NOESYtypes, initial)
    self.NOESYtype.frame.pack(side = 'top', anchor = 'w')

    sl = tkutil.scrolling_list(self.top, 'Chemical shift list', 5)
    sl.frame.pack(fill = 'both', expand = 1)
    sl.listbox.bind('<ButtonRelease-1>', self.resonance_cb)
    self.shift_list = sl

    pl = sputil.peak_listbox(self.top)
    pl.frame.pack(fill = 'both', expand = 1)
    pl.heading['text'] = 'Peak list'
    pl.listbox.bind('<ButtonRelease-1>', pl.select_peak_cb)
    pl.listbox.bind('<ButtonRelease-2>', pl.goto_peak_cb)
    pl.listbox.bind('<Double-ButtonRelease-1>', pl.goto_peak_cb)
    self.peak_list = pl

    cy = tkutil.checkbutton(self.top, 'Cyana Formatting ?', 1)
    cy.button.pack(side = 'top', anchor = 'w')
    self.cyana = cy

    hb = tkutil.checkbutton(self.top,
                            'Show peak heights instead of volumes?', 1)
    hb.button.pack(side = 'top', anchor = 'w')
    self.heights = hb

    ib = tkutil.checkbutton(self.top, 'Include unintegrated peaks?', 1)
    ib.button.pack(side = 'top', anchor = 'w')
    self.unintegrated = ib

    ab = tkutil.checkbutton(self.top, 'Include unassigned peaks?', 1)
    ab.button.pack(side = 'top', anchor = 'w')
    self.unassigned = ab

    mb = tkutil.checkbutton(self.top,
                            'Include assignments without a residue number?', 1)
    mb.button.pack(side = 'top', anchor = 'w')
    self.unnumbered = mb

    nb = tkutil.checkbutton(self.top, 'Show peak notes?', 0)
    nb.button.pack(side = 'top', anchor = 'w')
    self.note = nb

    ri = tkutil.checkbutton(self.top, 'Add 10000 to assigned peak index', 0)
    ri.button.pack(side = 'top', anchor = 'w')
    self.reindex = ri

    eh = Tkinter.Label(self.top, text = 'Omit peak if note has a word from:')
    eh.pack(side = 'top', anchor = 'w')
    ef = tkutil.entry_field(self.top, '  ', width = 30)
    ef.frame.pack(side = 'top', anchor = 'w')
    self.note_words = ef
    et = Tkinter.Label(self.top, text = '(comma separated list of words)')
    et.pack(side = 'top', anchor = 'w')

    bl = tkutil.scrolling_list(self.top, 'Bad Chemical shift list', 5)
    bl.frame.pack(fill = 'both', expand = 1)
    bl.listbox.bind('<ButtonRelease-1>', self.bad_resonance_cb)
    self.bad_shift_list = bl

    er = tkutil.entry_row(self.top, 'PPM tolerance: ',
                                    ('1H', '0.02', 5),
                                    ('13C', '0.20', 5),
                                    ('15N', '0.20', 5))
    er.frame.pack(side = 'top', anchor = 'w')
    self.ppm_range = er


    # self.ppm_range = er
    progress_label = Tkinter.Label(self.top, anchor = 'nw')
    progress_label.pack(side = 'top', anchor = 'w')

    br = tkutil.button_row(self.top,
                           ('Update', self.update_cb),
                           ('Write Shifts', self.save_shifts_cb),
                           ('Write Peaks', self.save_peaks_cb),
                           ('Stop', self.stop_cb),
                           ('Close', self.close_cb),
                           ('Help', sputil.help_cb(session, 'XEASYFormat')),
         )
    br.frame.pack(side = 'top', anchor = 'w')

    tkutil.Stoppable.__init__(self, progress_label, br.buttons[3])

  # ---------------------------------------------------------------------------
  #
  def update_cb(self):

    spectrum = self.spectrum_choice.spectrum()
    if spectrum == None:
      return
    NOESYtype = self.NOESYtype.get()
    cyana_header = self.cyana.state()
    show_heights = self.heights.state()
    show_unintegrated = self.unintegrated.state()
    show_unassigned = self.unassigned.state()
    show_unnumbered = self.unnumbered.state()
    reindex_peaks = self.reindex.state()
    show_note = self.note.state()
    note_words = self.note_words.variable.get().split(',')
    self.tolerance={'H':float(self.ppm_range.variables[0].get()),'C':float(self.ppm_range.variables[1].get()),'N':float(self.ppm_range.variables[2].get())}
    print self.tolerance
    self.stoppable_call(self.show_chemical_shifts, spectrum.condition,
                        show_unnumbered)
    self.stoppable_call(self.show_peaks, spectrum, cyana_header,
                        show_heights, show_unintegrated, show_unassigned,
                        show_unnumbered, show_note, note_words, reindex_peaks)
    self.stoppable_call(self.show_bad_chemical_shifts, spectrum.condition,
                        self.sequence, self.tolerance)

  # ---------------------------------------------------------------------------
  #
  def save_shifts_cb(self):
    
    path = tkutil.save_file(self.top, 'Save XEASY Chemical Shifts', 'peaklist')
    if path:
      self.shift_list.write_file(path, 'w', write_heading = 0)

  # ---------------------------------------------------------------------------
  #
  def save_peaks_cb(self):
    
    path = tkutil.save_file(self.top, 'Save XEASY Peak List', 'peaklist')
    if path:
      self.peak_list.write_file(path, 'w', write_heading = 0)

  # ---------------------------------------------------------------------------
  #
  def resonance_cb(self, event):
    
    r = self.shift_list.event_line_data(event)
    if r:
      self.session.show_resonance_peak_list(r)
      
  # ---------------------------------------------------------------------------
  # Update the bad chemcials shifts check box with resoancnes peaks for bad entries 
  def bad_resonance_cb(self, event):
    
    r2 = self.bad_shift_list.event_line_data(event)
    if r2:
      self.session.show_resonance_peak_list(r2)

  # ---------------------------------------------------------------------------
  #
  def show_chemical_shifts(self, condition, show_unnumbered):

    reslist = condition.resonance_list()
    reslist.sort(sputil.compare_resonances)
    self.assign_atom_ids(reslist)
      
    self.shift_list.clear()
    self.stoppable_loop('shifts', 100)
    cyana_dict = None;
    if self.cyana.state():
        cyana_dict = cyana.CyanaDictionary();
    for r in reslist:
      self.check_for_stop()
      if show_unnumbered or r.group.number != None:
        line = self.shift_line(r,cyana_dict);
        self.shift_list.append(line, r)

  # ---------------------------------------------------------------------------
  #
  def shift_line(self,r,cyana_dict):

    format = '%4d %8.3f %6.3f %6s %d'

    group_num = r.group.number
    if group_num == None:
      group_num = 0
      
    atom_name = r.atom.name;
    if cyana_dict:
      aa = r.group.name[0];
      atom_name = cyana_dict.toCyana(aa,atom_name);

    values = (r.atom.xeasy_id, r.frequency, r.deviation,
              atom_name, group_num)
    return format % values

  # ---------------------------------------------------------------------------
  #
  def show_bad_chemical_shifts(self, condition, sequence, tolerance):
    reslist = condition.resonance_list()
    reslist.sort(key = lambda x: x.group.name)

    groups_list = [szA+str(szID) for (szID,szA) in sequence]
    self.assign_atom_ids(reslist)
      
    self.bad_shift_list.clear()
    self.stoppable_loop('shifts', 100)
    for r in reslist:
      self.check_for_stop()
      if r.group.name[0] in Allowed_atoms.keys():
         if r.atom.name not in Allowed_atoms[r.group.name[0]]:
            line = self.bad_shift_line(r);
            self.bad_shift_list.append(line, r)
      if r.deviation >= tolerance[r.atom.nucleus[-1]]:
        line = self.bad_shift_line(r);
        self.bad_shift_list.append(line, r)
      if r.group.name not in groups_list:
        line = self.bad_shift_line(r);
        self.bad_shift_list.append(line, r)

  # ---------------------------------------------------------------------------
  #
  def bad_shift_line(self,r):

    format = '%4d %8.3f %6.3f %6s %s'
    group = r.group.name
    group_num = r.group.number
    if group_num == None:
      group_num = 0
    atom_name = r.atom.name
    values = (r.atom.xeasy_id, r.frequency, r.deviation,
              atom_name, group)
    return format % values

  # ---------------------------------------------------------------------------
  #
  def assign_atom_ids(self, reslist):

    max_id = 0
    for r in reslist:
      if hasattr(r.atom, 'xeasy_id'):
        max_id = max(max_id, r.atom.xeasy_id)
      
    next_id = max_id + 1
    for r in reslist:
      if not hasattr(r.atom, 'xeasy_id'):
        r.atom.xeasy_id = next_id
        next_id = next_id + 1
        
  # ---------------------------------------------------------------------------
  #
  def show_peaks(self, spectrum, cyana_header,
                 show_heights, show_unintegrated, show_unassigned,
                 show_unnumbered, show_note, note_words, reindex_peaks):

    headerdict = {'2D NOESY [H,H]':['#Number of dimensions 3','#FORMAT xeasy2D','#INAME 1 H1','#INAME 2 H2','#SPECTRUM NOESY H1 H2','#TOLERANCE 0.0300 0.0200'],
                  '3D N15NOESY [H,N,HN]':['#Number of dimensions 3','#FORMAT xeasy3D','#INAME 1 H','#INAME 2 N','#INAME 3 HN','#SPECTRUM N15NOESY H N HN','#TOLERANCE 0.0300 0.3000 0.0200'],
                  '3D N15NOESY [HN,N,H]':['#Number of dimensions 3','#FORMAT xeasy3D','#INAME 1 HN','#INAME 2 N','#INAME 3 H','#SPECTRUM N15NOESY HN N H','#TOLERANCE 0.0200 0.3000 0.0300'],
                  '3D C13NOESY [H,C,HC]':['#Number of dimensions 3','#FORMAT xeasy3D','#INAME 1 H','#INAME 2 C','#INAME 3 HC','#SPECTRUM C13NOESY H C HC','#TOLERANCE 0.0300 0.2000 0.0200'],
                  '3D C13NOESY [HC,C,H]':['#Number of dimensions 3','#FORMAT xeasy3D','#INAME 1 HC','#INAME 2 C','#INAME 3 H','#SPECTRUM C13NOESY HC C H','#TOLERANCE 0.0200 0.2000 0.0300'],
                  '3D CCNOESY [C1,C2,H2]':['#Number of dimensions 4','#FORMAT xeasy4D','#INAME 1 C1','#INAME 2 C2','#INAME 3 H2','#INAME 4 H1','#SPECTRUM CCNOESY C1 C2 H2 H1','#TOLERANCE 0.2000 0.2000 0.0200 999.999'],
                  '3D CCNOESY [H2,C2,C1]':['#Number of dimensions 4','#FORMAT xeasy4D','#INAME 1 H2','#INAME 2 C2','#INAME 3 C1','#INAME 4 H1','#SPECTRUM CCNOESY H2 C2 C1 H1','#TOLERANCE 0.0200 0.2000 0.2000 999.999'],
                  '3D NCNOESY [C,N,HN]':['#Number of dimensions 4','#FORMAT xeasy4D','#INAME 1 C','#INAME 2 N','#INAME 3 HN','#INAME 4 HC','#SPECTRUM NCNOESY C N HN HC','#TOLERANCE 0.2000 0.3000 0.0200 999.999'],
                  '3D NCNOESY [HN,N,C]':['#Number of dimensions 4','#FORMAT xeasy4D','#INAME 1 HN','#INAME 2 N','#INAME 3 C','#INAME 4 HC','#SPECTRUM NCNOESY HN N C HC','#TOLERANCE 0.0200 0.3000 0.2000 999.999'],
                  '3D NCNOESY [N,C,HC]':['#Number of dimensions 4','#FORMAT xeasy4D','#INAME 1 N','#INAME 2 C','#INAME 3 HC','#INAME 4 HN','#SPECTRUM NCNOESY N C HC HN','#TOLERANCE 0.3000 0.2000 0.0200 999.999'],
                  '3D NCNOESY [HC,C,N]':['#Number of dimensions 4','#FORMAT xeasy4D','#INAME 1 HC','#INAME 2 C','#INAME 3 N','#INAME 4 HN','#SPECTRUM NCNOESY HC C N HN','#TOLERANCE 0.0200 0.2000 0.3000 999.999'],
                  '4D CCNOESY [H1,C1,C2,H2]':['#Number of dimensions 4','#FORMAT xeasy4D','#INAME 1 H1','#INAME 2 C1','#INAME 3 C2','#INAME 4 H2','#SPECTRUM CCNOESY H1 C1 C2 H2','#TOLERANCE 0.0300 0.3000 0.3000 0.03000'],
                  '4D NNNOESY [H1,N1,N2,H2]':['#Number of dimensions 4','#FORMAT xeasy4D','#INAME 1 H1','#INAME 2 N1','#INAME 3 N2','#INAME 4 H2','#SPECTRUM NNNOESY H1 N1 N2 H2','#TOLERANCE 0.0300 0.4000 0.4000 0.03000'],
                  '4D NCNOESY [HC,C,N,HN]':['#Number of dimensions 4','#FORMAT xeasy4D','#INAME 1 HC','#INAME 2 C','#INAME 3 N','#INAME 4 HN','#SPECTRUM NCNOESY HC C N HN','#TOLERANCE 0.0300 0.3000 0.3000 0.03000'],
                  '4D NCNOESY [HN,N,C,HC]':['#Number of dimensions 4','#FORMAT xeasy4D','#INAME 1 HN','#INAME 2 N','#INAME 3 C','#INAME 4 HC','#SPECTRUM NCNOESY HN N C HC','#TOLERANCE 0.0300 0.3000 0.3000 0.03000'],
                  '2D DARR [C1,C2]':['#Number of dimensions 2','#FORMAT xeasy2D','#INAME 1 C1','#INAME 2 C2','#SPECTRUM DARR C1 C2','#TOLERANCE 0.3000 0.3000'],
                  '2D PSDS [C1,C2]':['#Number of dimensions 2','#FORMAT xeasy2D','#INAME 1 C1','#INAME 2 C2','#SPECTRUM PSDS C1 C2','#TOLERANCE 0.3000 0.3000'],
                  '2D PAIN [N,C]':['#Number of dimensions 2','#FORMAT xeasy2D','#INAME 1 N','#INAME 2 C','#SPECTRUM PAIN N C','#TOLERANCE 0.3000 0.3000'],
                  '2D PAIN [C,N]':['#Number of dimensions 2','#FORMAT xeasy2D','#INAME 1 N','#INAME 2 C','#SPECTRUM PAIN N C','#TOLERANCE 0.3000 0.3000'],
                  '3D PAIN [C,N,HN]':['#Number of dimensions 3','#FORMAT xeasy3D','#INAME 1 C','#INAME 2 N','#INAME 3 HN','#SPECTRUM PAIN3D C N HN','#TOLERANCE 0.3000 0.3000 0.0300'],
                  '3D PAIN [HN,N,C]':['#Number of dimensions 3','#FORMAT xeasy3D','#INAME 1 HN','#INAME 2 N','#INAME 3 C','#SPECTRUM PAIN3D HN N C','#TOLERANCE 0.0300 0.3000 0.3000']}
    pseudo4D = False
    self.peak_list.clear()
    spectrum_peak_list = spectrum.peak_list();
    if not cyana_header:
      header = '# Number of dimensions %s' % spectrum.dimension
      self.peak_list.append(header, None)
      heading = '#Number of peaks %s' % len(spectrum_peak_list) 
      self.peak_list.append(heading, None)
    if cyana_header:
      header = headerdict[self.NOESYtype.get()][0]
      for line in headerdict[self.NOESYtype.get()]:
        self.peak_list.append(line, None)
      heading = '#Number of peaks %s' % len(spectrum_peak_list) 
      self.peak_list.append(heading, None)

    if header[-1] != str(spectrum.dimension):
      pseudo4D = True

    peak_id = 0
    self.stoppable_loop('peaks', 100)
    for peak in spectrum_peak_list:
      self.check_for_stop()
      peak_id = peak_id + 1
      line = self.peak_line(peak, peak_id, show_heights, pseudo4D)
      if reindex_peaks:
        if peak.is_assigned:
          peak_id2 = peak_id + 10000
          line = self.peak_line(peak, peak_id2, show_heights, pseudo4D)
      if show_note and len(peak.note) > 0:
        line = line + '   # ' + peak.note
      import re
      if len(note_words[0]) > 0 and len(peak.note) > 0:
        for words in note_words:
          if re.search(words.lower().strip(),peak.note.lower()):
            line = '# ' + peak.note + ' ' + line.lstrip()

      self.peak_list.append(line, peak)

  # ---------------------------------------------------------------------------
  #
  def peak_line(self, peak, peak_id, show_heights, pseudo4D):

    if '?' not in peak.assignment:
      color_code = 1
    if '?' in peak.assignment:
      color_code = 4
    spectrum_type = 'U'
    intensity_error = 0.0

    if show_heights:
      intensity_method = 'e'
      intensity = sputil.peak_height(peak)
    elif peak.volume == None:
      intensity_method = '-'
      intensity = 0.0
    else:
      intensity_method = 'e'
      intensity = peak.volume

    atom_ids = []
    for r in peak.resonances():
      if r:
        atom_ids.append(r.atom.xeasy_id)
      else:
        atom_ids.append(0)

    freq_text = pyutil.sequence_string(peak.frequency, '%8.3f')
    if pseudo4D == True:
      freq_text = freq_text + '%8.3f' %(-2.000)
      atom_ids.append(0)
    id_text = pyutil.sequence_string(atom_ids, ' %5d')
    
    format = '%7d%s %1d %1s % 13.5E % 13.2E %1s 0%s'
    values = (peak_id, freq_text, color_code, spectrum_type,
              intensity, intensity_error, intensity_method, id_text)
    line = format % values
    
    return line

  # ---------------------------------------------------------------------------
  #
  def assignment_numbered(self, assignment):

    for r in assignment:
      if r and r.group.number == None:
        return 0
    return 1

# -----------------------------------------------------------------------------
#
def show_dialog(session):
  d = sputil.the_dialog(xeasy_format_dialog, session)
  d.show_window(1)
