# -----------------------------------------------------------------------------
# Get amino acid or nucleic acid sequence for molecules
#
import string
import Tkinter
import re
import atomnames
import pyutil
import sputil
import tkutil
import tkMessageBox
import os
import myseq

# -----------------------------------------------------------------------------
# Updated by Woonghee Lee
# e-mail: whlee@nmrfam.wisc.edu
# National Magnetic Resonance Facilities at Madison
# Department of Bichemistry, University of Wisconsin at Madison
#
# Last updated: Oct 7, 2019
#
# Updated by : Mary Clay PhD
# e-mail: mary.clay@stjude.org
# St Jude Children's Research Hospital 
# Department of Structural Biology Memphis, TN 
#
# Last updates: May 25, 2022
#
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Query user for sequence.
#
class sequence_dialog(tkutil.Dialog):

  def __init__(self, session):

    self.molecule = None
    self.session = session  ## updated
    
    tkutil.Dialog.__init__(self, session.tk, 'Sequence Entry')

    se = self.sequence_entry(self.top)
    se.pack(side = 'top', anchor = 'w', fill = 'both', expand = 1)

    br = tkutil.button_row(self.top,
         ('Ok', self.ok_cb),
                           ('Cancel', self.close_cb),
                           ('Help', sputil.help_cb(session, 'Sequence')),
         )
    br.frame.pack(side = 'top', anchor = 'w')
      
  # ---------------------------------------------------------------------------
  #
  def sequence_entry(self, parent):

    f = Tkinter.Frame(parent)

    h = Tkinter.Label(f, text = 'Sequence')
    h.pack(side = 'top', anchor = 'w')
    self.header = h
    
    t = tkutil.scrolling_text(f)
    t.text['wrap'] = 'char'
    t.frame.pack(side = 'top', fill = 'both', expand = 1)
    self.sequence_text = t

    ff = tkutil.file_field2(self.top, 'Sequence file', 'sequence', file_type=[('1-letter-code sequence file', '.fasta'), ('3-letter-code sequence file with indices', '.seq'), ('3-letter-code sequence file without indices', '.txt')], default_ext='.fasta')
    ff.frame.pack(side = 'top', anchor = 'w')
    self.file_field = ff

    fr = tkutil.entry_field(f, 'First residue number', '')
    fr.frame.pack(side = 'top', anchor = 'w')
    self.first_residue = fr

    return f

  # ---------------------------------------------------------------------------
  # Read in sequence file, with + indicating break in numbering 
  # Returns a space separated number sequence as a string A1 F3 ... G200
  def read_sequence(self):
    import os
    seq = ''
    path = self.file_field.get()
    first_residue = self.first_residue.variable.get()

    if os.path.exists(self.session.project.save_path + '.seq'):
      readseq = myseq.ReadSequence(self.session)
    elif path:
      readseq = myseq.ReadSequenceFromFile2(path, first_residue)

    for (iSeqIdx, szA) in readseq:
      seq = seq + szA + str(iSeqIdx) + ','
    seq = seq[:-1]
    # print seq
    self.sequence_text.text.delete('0.0', 'end')
    self.sequence_text.text.insert('0.0', seq)
    s = sequence(seq)
    return s

  # ---------------------------------------------------------------------------
  # Save the sequence to a file with name session.project.save_path + '.seq'
  # with single line entry for each aa in sequence with 
  # three letter abbreviation space sequence index 
  #
  def ok_cb(self):
    session = self.session
    seq = self.read_sequence()    # s = return sequence(seq)
    if self.molecule:
      set_molecule_sequence(self.molecule, seq)

    try:
      seq_path = session.project.save_path + '.seq'
    except:
      seq_path = ''

    try:
      result = True
      if os.path.exists(seq_path):
        result = tkMessageBox.askokcancel('Stored sequence file found.', 'Do you want to overwrite to stored sequence file?')
      
      if result is True:  
        import myseq
        # build sequence
        seq_list = []
        for res in seq.numseq.split(','):
          seq_list.append((int(res[1:]),res[0]))
        myseq.WriteSequenceToFile(seq_path, seq_list)
    except:
      pass    
      
    self.close_cb()

  # ---------------------------------------------------------------------------
  # 
  def set_molecule(self, molecule):

    self.molecule = molecule

    if molecule and molecule.name:
      self.header['text'] = 'Sequence for %s molecule' % molecule.name
    else:
      self.header['text'] = 'Sequence'

    self.sequence_text.text.delete('0.0', 'end')

    if molecule:
      seq = has_molecule_sequence(molecule)
      if seq:
        self.sequence_text.text.insert('0.0', seq.numseq)

  # ---------------------------------------------------------------------------
  # not really sure   
  def get_sequence(self, molecule):

    self.set_molecule(molecule)
    self.return_when_closed()

# -----------------------------------------------------------------------------
#
def has_molecule_sequence(molecule):

  if not hasattr(molecule, 'sequence'):
    s = molecule.saved_value('sequence')
    if s == None:
      molecule.sequence = None
    else:
      molecule.sequence = sequence(s)

  return molecule.sequence


# -----------------------------------------------------------------------------
# seq = s returned at end of read _sequence
def set_molecule_sequence(molecule, seq):

  if seq:
    s = seq.numseq
    molecule.save_value('sequence', s)
  molecule.sequence = seq

# -----------------------------------------------------------------------------
# Return the molecule sequence.  Query user if it is not known.
#
def molecule_sequence(molecule):

  seq = has_molecule_sequence(molecule)
  if seq == None:
    print 'cant find seq for molecule '
    d = sputil.the_dialog(sequence_dialog, molecule.session)
    d.get_sequence(molecule)

  return has_molecule_sequence(molecule)
# -----------------------------------------------------------------------------
#
# Return the sequence.  Query user if it is not known.
#
# def molecule_sequence(session):

#   seq = has_molecule_sequence(molecule)
#   if seq == None:
#     print 'cant find seq for molecule '
#     d = sputil.the_dialog(sequence_dialog, molecule.session)
#     d.get_sequence(molecule)

#   return has_molecule_sequence(molecule)
# -----------------------------------------------------------------------------
#
class sequence:

  def __init__(self, seq):

    olc = olc2 =''
    for res in seq.split(','):
      olc = olc + string.capitalize(res[0])
      olc2 = olc2 + res[0]

    self.bt = myseq.GetBiomoleculeTypeByFasta(olc)
    if self.bt == 'p':
      self.one_letter_codes = olc
    else:
      self.one_letter_codes = olc2 # keep cases for nucleic acids
    self.numseq = seq
    n2s = self.number_to_symbol_table(seq)

    self.number_to_symbol = n2s
                                                        
    self.first_residue_number = int(seq.split(',')[0][1:])
    self.last_residue_number = int(seq.split(',')[-1][1:])
    self.resonances = self.create_resonances()

    nsa_to_res = {}
    for r in self.resonances:
      print str(r.number) +' '+ r.symbol +' '+  r.atom_name
      nsa_to_res[(r.number, r.symbol, r.atom_name)] = r
    self.nsa_to_resonance = nsa_to_res
    ga_to_res = {}
    for r in self.resonances:
      ga_to_res[r.group_atom] = r
    self.group_atom_to_resonance = ga_to_res
    
  # ---------------------------------------------------------------------------
  # Dictionary for converting sequence index to residue type
  def number_to_symbol_table(self, seq):

    ns_table = {}
    for res in seq.split(','):
      ns_table[int(res[1:])] = res[0]
    return ns_table

  # ---------------------------------------------------------------------------
  #
  def create_resonances(self):
    rlist = []
    for number, symbol in self.number_to_symbol.items():
      if self.bt == 'p':
        for atom_name in atomnames.protein_atoms_by_group[symbol]:
          r = resonance(number, symbol, atom_name)
          rlist.append(r)
      else:    
        for atom_name in atomnames.dna_rna_atoms_by_group[symbol.upper()]:
          r = resonance(number, symbol, atom_name)
          rlist.append(r)
    return rlist
  # ---------------------------------------------------------------------------
  #
  def resonance(self, number, symbol, atom_name):

    nsa = (number, symbol, atom_name)
    if nsa in self.nsa_to_resonance:
      return self.nsa_to_resonance[nsa]
    return None
    
  # ---------------------------------------------------------------------------
  #
  def peak_resonances(self, peak):

    res = []
    for r in peak.resonances():
      seq_r = self.resonance(r.group.number, r.group.symbol, r.atom.name)
      res.append(seq_r)
    return tuple(res)
  
# -----------------------------------------------------------------------------
#
class resonance:

  def __init__(self, number, symbol, atom_name):
    
    self.number = number
    self.symbol = symbol
    self.atom_name = atom_name
    self.group_name = symbol + repr(number)
    self.group_atom = (self.group_name, atom_name)

# -----------------------------------------------------------------------------
# Show molecule sequence dialog
#
def show_sequence_dialog(session):

  d = sputil.the_dialog(sequence_dialog, session)
  s = session.selected_spectrum()
  if s:
    if len(s.molecule.group_list()) != 0:
      d.set_molecule(s.molecule)
      d.show_window(1)
      return
  if session.project != None:
    seq_path = session.project.save_path + '.seq'
    if os.path.exists(seq_path):
      d.file_field.set(seq_path)
  seq = d.read_sequence()
  d.show_window(1)
  