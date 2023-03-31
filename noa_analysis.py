import tkinter
import types
import re
import math as m
import pyutil
import sparky 
import sputil
import tkutil
import tkinter.messagebox

# ------------------------------------------------------------------------------
#
# Updated by : Mary Clay PhD
# e-mail: mary.clay@stjude.org
# St Jude Children's Research Hospital 
# Department of Structural Biology Memphis, TN 
#
# Last updates: March 31, 2023
#
#
# ------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------

class obj:
  pass

class check_peaks_dialog(tkutil.Dialog):

  # ------------------------------------------------------------------------------
  #
  def __init__(self, session):

    self.session = session
    self.selection_notice = None
    tkutil.Dialog.__init__(self, session.tk, 'Examine {:} Peaks'.format(self.session.selected_spectrum().name))

    self.spectrum_choice_3DNOESY = self.session.selected_spectrum()

    ep = tkutil.file_field2(self.top, 'Peak List File', 'Browse...', file_type=[('post cyana list', '.list')], default_ext='.list')
    self.peaks_path = ep.variable
    ep.frame.pack(side = tkinter.TOP, anchor = 'w', fill=tkinter.X)

    pl = sputil.peak_listbox(self.top)
    pl.frame.pack(fill = 'both', expand = 1)
    pl.heading['text'] = 'Peak list\n{:}  {:^26}  {:^24}  {:^9}  {:^6}  {:^24}   {:^24}'.format('peakid','frequencies','Connection','Dist' ,'Pshift','Comment','Note')
    pl.listbox.bind('<ButtonRelease-1>', pl.select_peak_cb)
    pl.listbox.bind('<Double-ButtonRelease-1>', pl.goto_peak_cb)
    pl.listbox.bind('<ButtonRelease-3>', pl.goto_peak_cb)
    pl.listbox['selectmode'] = 'extended' #'multiple'
    self.peak_list = pl

    e = tkutil.entry_field(self.top, 'Note: ', '', 50)
    self.note_words = e.variable
    e.frame.pack(side = 'top', anchor = 'w', fill= tkinter.X)

    colors = ["white", "blue", "coral", "cyan", "gold", "green", "light blue", "light green", "light yellow","magenta", "maroon", "orange", "pink", "purple", "red","tomato", "turquoise", "yellow", "dark blue","dark green", "dark orange", "lime green", "medium purple", "indian red", "sandy brown", "dark khaki","royal blue"]
    initial=colors[0]
    self.color_choice = tkutil.option_menu(self.top, "color", colors, initial)
    self.color_choice.frame.pack(side = 'top', anchor = 'w')

    sortopts = ['peak number','w1','w2','w3','connection','dist','pshift','comment']
    initial2=sortopts[0]
    self.sort_by = tkutil.option_menu(self.top, "Sort By:", sortopts, initial2)
    self.sort_by.frame.pack(side = 'top', anchor = 'w')

    searchframe = tkinter.Frame(self.top)
    sflabel = tkinter.Label(searchframe, text = 'Search For:')
    sflabel.grid(column = 0, row = 0)
    self.keyword = tkinter.StringVar(searchframe)
    self.keyword.set('')
    keyword_ef = tkinter.Entry(searchframe, textvariable = self.keyword, width = 10)
    keyword_ef.grid(column = 1, row = 0)
    searchframe.pack(side = 'top', anchor = 'w')
    keyword_ef.bind('<Return>', self.cb_search)

    br = tkutil.button_row(self.top,
                          ('Update List', self.update_list_cb),
                          ('Update Peaks', self.update_peaks_cb),
                          ('Close', self.close_cb))
    br.frame.pack(side = 'top', anchor = 'w')

  # ---------------------------------------------------------------------------
  #
  def cb_search(self, event):
    sstr = self.keyword.get()
    inlist = self.peaks_path.get()
    if sstr != '':
      noalistlines = [line.rstrip() for line in open(inlist).readlines() if line.strip() and '#' not in line.split()[0]]
      matches = []
      for line in noalistlines:
        try:
          int(sstr)
          if line.split()[0] == sstr:
            matches.append(line)
        except ValueError:
          if re.search(sstr, line):
            matches.append(line)
    if sstr == '':
      matches = [line.rstrip() for line in open(inlist).readlines() if line.strip() and '#' not in line.split()[0]]
    self.show_peaks(self.spectrum_choice_3DNOESY, matches, self.sort_by.get())


  # ---------------------------------------------------------------------------
  #
  def update_peaks_cb(self):

    spectrum = self.spectrum_choice_3DNOESY
    note_words = self.note_words.get()
    color = self.color_choice.get()
    for peak in self.peak_list.selected_line_data():
      peak.note = note_words
      peak.color = color
    for idx in self.peak_list.listbox.curselection():
      self.peak_list.listbox.itemconfig(idx,{'fg':color.replace('white','black')})

  # ---------------------------------------------------------------------------
  #
  def update_list_cb(self):

    self.session.unselect_all_ornaments()
    spectrum = self.spectrum_choice_3DNOESY
    inlist = [line.rstrip() for line in open(self.peaks_path.get()).readlines() if line.strip() and '#' not in line.split()[0]]
    sort_by = self.sort_by.get()
    self.show_peaks(spectrum, inlist, sort_by)

  # ---------------------------------------------------------------------------
  #
  def show_peaks(self, spectrum, inlist, sort_by):

    self.peak_list.clear()
    spectrum_peak_list = spectrum.peak_list()

    peakdict = {}
    for peak in spectrum_peak_list:
      peakdict["{:8.3f}, {:8.3f}, {:8.3f}".format(peak.frequency[0],peak.frequency[1],peak.frequency[2])] = peak

    sort_dict = {'peak number':'lambda x: float(x.strip().split()[0])','w1':'lambda x: float(x.strip().split()[1])','w2':'lambda x: float(x.strip().split()[2])',
      'w3':'lambda x: float(x.strip().split()[3])','connection':'lambda x: x.strip().split()[4]','dist':'lambda x: x.strip().split()[5]',
      'pshift':'lambda x: float(x.strip().split()[6])', 'comment':'lambda x: x[79:]'}
    noalist = sorted(inlist, key = eval(sort_dict[sort_by]))

    idx = -1
    for line in noalist:
      freq = "{:8.3f}, {:8.3f}, {:8.3f}".format(float(line.split()[1]),float(line.split()[2]),float(line.split()[3]))
      if freq in peakdict.keys():
        idx+=1
        peak = peakdict[freq]
        outline = '{:<105} {:}'.format(line.rstrip(),peak.note)
        self.peak_list.append(outline, peak)
        self.peak_list.listbox.itemconfig(idx,{'fg':peak.color.replace('white','black')})


def show_dialog(session):

  spectrum = session.selected_spectrum()
  if spectrum == None:
    return

  try:
    dialogs = session.spectrum_dialogs
  except:
    session.spectrum_dialogs = {}
    dialogs = session.spectrum_dialogs
  if (spectrum in dialogs and not dialogs[spectrum].is_window_destroyed()):
    dialogs[spectrum].show_window(1)
  else:
    d = check_peaks_dialog(session)
    d.show_window(1)
    dialogs[spectrum] = d
