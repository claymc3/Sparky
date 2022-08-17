# -----------------------------------------------------------------------------
# My sequence module
# -----------------------------------------------------------------------------
#
# Developed by Woonghee Lee
# e-mail: whlee@nmrfam.wisc.edu
# National Magnetic Resonance Facilities at Madison
# Department of Bichemistry, University of Wisconsin at Madison
#
# Last updated: Oct 7, 2019
# 
# -----------------------------------------------------------------------------
# 
# Updated by : Mary Clay PhD
# e-mail: mary.clay@stjude.org
# St Jude Children's Research Hospital 
# Department of Structural Biology Memphis, TN 
#
# Last updated: Feb 25, 2020
#
#
# 
# -----------------------------------------------------------------------------
import tkutil
import sputil
import tkFileDialog
import pinelayout
import re
import Tkinter
import tkMessageBox
import os

# -----------------------------------------------------------------------------
AAA_dict = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
A_dict = {'C': 'CYS', 'D': 'ASP', 'S': 'SER', 'Q': 'GLN', 'K': 'LYS',
     'I': 'ILE', 'P': 'PRO', 'T': 'THR', 'F': 'PHE', 'N': 'ASN', 
     'G': 'GLY', 'H': 'HIS', 'L': 'LEU', 'R': 'ARG', 'W': 'TRP', 
     'A': 'ALA', 'V':'VAL', 'E': 'GLU', 'Y': 'TYR', 'M': 'MET'}     
NA_AAA_dict = {'ADE': 'A', 'GUA': 'G', 'CYT': 'C', 'URA': 'U', 'THY': 'T'}
NA_A_dict = {'A': 'ADE', 'G': 'GUA', 'C': 'CYT', 'U': 'URA', 'T': 'THY'}  

Ponly = 'RNDQEHILKMFPSWYV'

# ----------------------------------------------------------------------------
def aaa2a(szAAA):
  if len(szAAA) == 1:
    if A_dict.has_key(szAAA.upper()):
      return szAAA.upper()
  if len(szAAA) != 3:
    return 'X'
  if not AAA_dict.has_key(szAAA.upper()):
    return "X"
  return AAA_dict[szAAA.upper()]
# ----------------------------------------------------------------------------
def a2aaa(szA):
  if len(szA) == 3:
    if AAA_dict.has_key(szA.upper()):
      return szA.upper()
  if len(szA) <> 1:
    return 'XXX'
  if not A_dict.has_key(szA.upper()):
    return "XXX"
  return A_dict[szA.upper()]
# ----------------------------------------------------------------------------
def na_aaa2a(szAAA):
  if len(szAAA) <> 3:
    return 'X'
  if not NA_AAA_dict.has_key(szAAA.upper()):
    return "X"
  return NA_AAA_dict[szAAA.upper()]
# ----------------------------------------------------------------------------
def na_a2aaa(szA):
  if len(szA) <> 1:
    return 'XXX'
  if not NA_A_dict.has_key(szA.upper()):
    return "XXX"
  return NA_A_dict[szA.upper()]

# ----------------------------------------------------------------------------  
# sequence format is list of ....
# (1, 'A')
# (2, 'R') ......  
def CheckSequence(sequence):
  # sort sequence
  iMin = 9999
  iMax = -9999
  iFirstIndex = -9999  
  result_sequence = []

  for seq in sequence:
    print seq
    try:
      temp = int(seq[0])
    except:
      continue
    if iMin > seq[0]: 
      iMin = seq[0]
    if iMax < seq[0]: 
      iMax = seq[0]
    
  iFirstIndex = iMin
  if iMin == 9999:
    return []
         
  for i in range(iMin, iMax+1):
    iFound = 0
    for seq in sequence:
      if seq[0] == i:
        result_sequence.append(seq)
        iFound = 1
        break
    if iFound == 0:
      result_sequence.append( (i, 'X') )        

  return result_sequence

# ----------------------------------------------------------------------------  
def GapInSequence(sequence):
  for seq in sequence:
    if seq[1] == 'X': return 1
  return 0
    
# ----------------------------------------------------------------------------
def LoadSeq(session, sequence):

  # set sequences
  readsequence = ReadSequence(session)
  
  # try to fill the gap
  retSeq = FillSequenceGap(readsequence, sequence)

  return retSeq  
# -----------------------------------------------------------------------------
# iMode:
#    0: template: shiftx or bmrb
#    1: template: your assignment
def ReadSequence2(template_cs_list):
  iTemMin = 9999
  iTemMax = -9999
  for group in template_cs_list:
    if group[0] < iTemMin: iTemMin = group[0]
    if group[1] > iTemMax: iTemMax = group[0]
  szTemSeq = ''

  # make fasta of temp
  retSeq = []
  for i in range(iTemMin, iTemMax+1):
    iFound = 0
    for group in template_cs_list:
      if group[0] == i:
        retSeq.append( (i, group[1]) )
        iFound = 1
        break
    if iFound == 0:
        retSeq.append( (i, 'X') )

  return retSeq
# -----------------------------------------------------------------------------  
def SaveSparkyResonance(session, external_cs_list):   
  import tkutil
  path = tkutil.save_file(session.tk, "Save to Sparky resonance format (.list)", "Save to Sparky resonance file format (.list)")
  if not path: return
  
  line_queue = []
  for rec in external_cs_list:
    (iSeqIdx,  szA, szAtom, dCS) = rec
    if (szAtom[0] == 'C'): 
      szNuc = '13C'
    elif (szAtom[0] == 'N'): 
      szNuc = '15N'
    elif (szAtom[0] == 'H') or (szAtom[0] == 'Q') or (szAtom[0] == 'M'): 
      szNuc = '1H'
    else:
      continue
    szLine = '%s%d   %s   %s %7.3f   0.0     0\n' % (szA, iSeqIdx, szAtom, szNuc, dCS)
    line_queue.append(szLine)
    
  f = open(path, 'w')
  for line in line_queue:
    f.write(line)
  f.close()   
# -----------------------------------------------------------------------------  
def GetExternalFreq(session, iSeqID, szA, szAtom, external_cs_list):   
  for rec in external_cs_list:
    if rec[0] == iSeqID and rec[1] == szA and rec[2] == szAtom:
      return rec[3] 
  
  # we need to look at pseudo-atoms    
  # this only works for protons  
  if not szAtom[:1] in ['H', 'Q', 'M']:
    return 9999
  # HN
  if szAtom == 'H' or szAtom == 'HN':
    for rec in external_cs_list:
      if rec[0] == iSeqID and rec[1] == szA and (rec[2] == 'HN' or rec[2] == 'H'):
        return rec[3] 
    return 9999      
    
  # processing pseudo atoms
  prefixes = ['H','Q','M']
  if pinelayout.pseudo_layout.has_key(szA) and len(szAtom) > 1:
    for prefix in prefixes:
      szPseudoAtom = prefix + szAtom[1:len(szAtom)]
      for rec in external_cs_list:
        if rec[0] == iSeqID and rec[1] == szA and rec[2] == szPseudoAtom:
          return rec[3] 
  # processing sub-level
  postfixes = ['1','2','3']
  if pinelayout.pseudo_layout.has_key(szA) and len(szAtom) > 1:
    for postfix in postfixes:
      szPseudoAtom = szAtom + postfix
      for rec in external_cs_list:
        if rec[0] == iSeqID and rec[1] == szA and rec[2] == szPseudoAtom:
          return rec[3] 
  return 9999
# -----------------------------------------------------------------------------
def RenumberSeqIndices(session):
  renumber_dialog = sputil.the_dialog(renum_seq, session)
  renumber_dialog.show_window(1)

class renum_seq(tkutil.Dialog, tkutil.Not_Stoppable):
  def __init__(self, session):
    self.session = session

    tkutil.Dialog.__init__(self, session.tk, 'Renumber sequence indices')
    explain = ('Sequence does not require fasta format')
    w = Tkinter.Label(self.top, text = explain, justify = 'left')
    w.pack(side = 'top', anchor = 'w')        
    ep = tkutil.file_field(self.top, 'Sequence file full pathway: ', 'Browse...', 35)
    self.seq_path = ep.variable
    ep.frame.pack(side = 'top', anchor = 'w')
    w.pack(side = 'top', anchor = 'w')
    e = tkutil.entry_field(self.top, 'Incorrect starting index(s): ', '', 8)
    self.orig_start_number = e.variable
    e.frame.pack(side = 'top', anchor = 'w')
    w.pack(side = 'top', anchor = 'w')
    e = tkutil.entry_field(self.top, 'Correct starting index(s): ', '', 8)
    self.new_start_number = e.variable
    e.frame.pack(side = 'top', anchor = 'w')

    br = tkutil.button_row(self.top,
                          ('Okay', self.okay_cb),
                          ('Cancel', self.close_cb),
               )
    br.frame.pack(side = 'top', anchor = 'w')

  def okay_cb(self):
    session = self.session
    seqf = self.seq_path.get()
    bad_indexs = [int(x) for x in self.orig_start_number.get().split(',')]
    good_indexs = [int(x) for x in self.new_start_number.get().split(',')]

    # -----------------------------------------------------------------------------
    # make a dictionary to rename old resonance list to new resonance list 

    Renumber = {}
    Sequence = ''
    New_seq = []
    sflines = [line.rstrip().upper() for line in open(seqf).readlines() if line.rstrip() and ">" not in line and "#" not in line]
    ### For three letter code fully indexed, partially indexed, and no index style input sequences 
    if re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', sflines[0]) or len(sflines[0]) == 3:
      if re.search('[A-Z][A-Z][A-Z]', sflines[0]) in NA_AAA_dict.keys():
        tlc2olc = NA_AAA_dict
      else:
        tlc2olc = AAA_dict

      for line in sflines:
        if re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', line):
          if re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', line).group().split()[0].upper() in tlc2olc.keys():
            Sequence = Sequence + tlc2olc[re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', line).group().split()[0].upper()]
        if re.search('[A-Z][A-Z][A-Z]', line) and not re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', line):
          if re.search('[A-Z][A-Z][A-Z]', line).group().upper() in tlc2olc.keys():
            Sequence = Sequence + tlc2olc[re.search('[A-Z][A-Z][A-Z]', line).group().upper()]
        if '+' in line:
          Sequence = Sequence + '+'
    ### For single letter code fasta style sequences 
    if len(sflines[0]) != 3 and not re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', sflines[0]):
      for line in sflines:
        Sequence = Sequence + line
    Sequence = Sequence.replace('++','+')


    ### Build dictionary to translate old numbered sequence to new numbered sequence ["D20":"D259"]
    ### Only correctly assigned resonances will be renumbered, and rn can be run in projects containing 
    ### spectra both correctly indexed and incorrectly indexed resonances

    if GetBiomoleculeTypeByFasta(Sequence) == 'n':
      olc2tlc = NA_A_dict
    else:
      olc2tlc = A_dict
    for x in range(len(Sequence.split('+'))):
      for i in range(len(Sequence.split('+')[x])):
        Renumber[Sequence.split('+')[x][i] + str(i + bad_indexs[x])] = Sequence.split('+')[x][i] + str(i + good_indexs[x])
        New_seq.append((olc2tlc[Sequence.split('+')[x][i]],i + good_indexs[x]))

    print Renumber
    for spectrum in session.project.spectrum_list():
      for peak in spectrum.peak_list():
        pAssign = sputil.parse_assignment(peak.assignment)
        if pAssign:
          for i in range(len(pAssign)):
            if pAssign[i][0] in Renumber.keys():
              peak.assign(i, Renumber[pAssign[i][0]], pAssign[i][1])

    ### Check to see if session.project.save_path + '.seq' exist and update or create it
    seq_path = session.project.save_path + '.seq'
    if os.path.exists(seq_path):
      result = tkMessageBox.askokcancel('Stored sequence file found.', 'Do you want to overwrite to stored sequence file?')
      if result is True:
        f = open(seq_path,'w')
        for (szAAA, iIdx) in New_seq:
          f.write('%s %5d\n' % (szAAA, iIdx))
        f.close()

    tkMessageBox.showinfo('Finished', 'Renumbered. Type dr to remove unused resonances.')
    self.close_cb()  
  
# -----------------------------------------------------------------------------
def PineSeqFormatting(session):
  readSeq = ReadSequence(session)
  if len(readSeq) == 0: return
  file_opt = options = {}  
  options['defaultextension'] = '.seq'
  options['filetypes'] = [('3-letter-code sequence file without indices', '.txt'), ('1-letter-code sequence file without indices', '.TXT')]
  options['title'] = 'Name your new sequence file in PINE format'  
  szFileName = tkFileDialog.asksaveasfilename(**file_opt)
  
  if szFileName == '':
    return
  f = open(szFileName, 'w')
  if f == None:
    return
  
  userseq = ''  
  for seq in readSeq:
    userseq = userseq + seq[1]
    if szFileName.endswith(".txt"):
      szAAA = a2aaa(seq[1].upper())
      f.write(szAAA+'\n')
    else:
      f.write(seq[1])
  f.close()
  import tkMessageBox
  tkMessageBox.showinfo('Finished', 'PINE sequence formatting finished: ' + userseq)
      
# -----------------------------------------------------------------------------
def GetBiomoleculeTypeByFasta(fasta):
  for i in range(len(Ponly)):
    if fasta.find(Ponly[i]) != -1:
      return 'p'
  return 'n'
  
# -----------------------------------------------------------------------------
def ReadSequence(session):

  # check if sequence file exists
  import os
  try:
    persist_path = session.project.save_path + '.seq'
  except:
    persist_path = ''
  readsequence = []
  import tkMessageBox
  szFileName = ''      
  ## If the session.project.save_path + '.seq' file exist then produce readsequence = [(idx, szA)]
  if os.path.exists(persist_path):
    # result = tkMessageBox.askokcancel('Stored sequence file found.', 'Do you want to use stored sequence file?')
    # if result is True:
    szFileName = persist_path
    pszLines =[line.rstrip() for line in open(szFileName).readlines() if line.rstrip() and ">" not in line and "#" not in line]
    for line in pszLines:
      if line.split()[0] in AAA_dict.keys():
        readsequence.append((int(line.split()[1]), AAA_dict[line.split()[0]]))

  if not os.path.exists(persist_path):
    file_opt = options = {}
    options['defaultextension'] = '.seq'
    options['filetypes'] = [('3-letter-code sequence file with indices', '.seq'), ('1-letter-code sequence file', '.fasta'), ('3-letter-code sequence file without indices', '.txt')]
    options['title'] = 'Select a sequence file to read'
    szFileName = tkFileDialog.askopenfilename(**file_opt)
       
    if szFileName == '':
      return []
    f = open(szFileName, 'r')
    if f == None:
      return [] 

    sflines =[line.rstrip() for line in f.readlines() if line.rstrip() and ">" not in line and "#" not in line]
    f.close()

    if re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', sflines[0]):
      if re.search('[A-Z][A-Z][A-Z]', sflines[0]) in NA_AAA_dict.keys():
        tlc2olc = NA_AAA_dict
      else:
        tlc2olc = AAA_dict
    if re.search('([0-9]*) * [A-Z][A-Z][A-Z]', sflines[0]): 
      if re.search('[A-Z][A-Z][A-Z]', sflines[0]) in NA_AAA_dict.keys():
        tlc2olc = NA_AAA_dict
      else:
        tlc2olc = AAA_dict

    # set sequences (###, szA)
    if re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', line):
      for line in sflines:
        szSplit = line.split()
        if szSplit[0].upper() in tlc2olc.keys():
          readsequence.append((int(szSplit[1]), tlc2olc[szSplit[0].upper()]))
    if re.search('([0-9]*) * [A-Z][A-Z][A-Z]', line):
      for line in sflines:
        szSplit = line.split()
        if szSplit[1].upper() in tlc2olc.keys():
          readsequence.append((int(szSplit[0]), tlc2olc[szSplit[1].upper()]))
    ### For single letter code fasta style sequences 
    firstIdx = 1

    if len(sflines[0]) != 3 and not re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', sflines[0]):
      Sequence = ''
      iCurIdx = 1
      for line in sflines:
        Sequence = Sequence + line
      for szA in Sequence:
        readsequence.append( (iCurIdx, szA) )
        iCurIdx = iCurIdx + 1

    WriteSequenceToFile(persist_path, readsequence)
  print readsequence
  return readsequence
# -----------------------------------------------------------------------------

def WriteSequenceToFile(szFileName, readsequence):
  fasta = ''
  for i in range(len(readsequence)):
    fasta = fasta + readsequence[i][1]
  bt =  GetBiomoleculeTypeByFasta(fasta)
  if bt == 'p':
    olc2tlc = A_dict
  if bt == 'n':
    olc2tlc = NA_A_dict
  try:
    f = open(szFileName, 'w')
    for (iCurIdx, szA) in readsequence:
      if szA in olc2tlc.keys():
        f.write('%s %5d\n' % (olc2tlc[szA], iCurIdx))
    f.close()
  except:
    pass

# -----------------------------------------------------------------------------

def ReadSequenceFromFile2(szFileName, first_residue):
  if szFileName == '':
    return []
  f = open(szFileName, 'r')
  if f == None:
    return []
  readsequence = [] #[(iCurIdx, szA)]
  Sequence = ''
  NumSeq = ''
  Indexes = []
  sflines = [line.rstrip() for line in open(szFileName).readlines() if line.rstrip() and ">" not in line and "#" not in line]
  
  ### Set the dictionary to use, NA or protein 
  
  ### For 3 letter code sequences numbered or not
  if re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', sflines[0]) or len(sflines[0]) == 3:
    if re.search('[A-Z][A-Z][A-Z]', sflines[0]) in NA_AAA_dict.keys():
      tlc2olc = NA_AAA_dict
    else:
      tlc2olc = AAA_dict
    for line in sflines:
      if re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', line):
        if re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', line).group().split()[0].upper() in tlc2olc.keys():
          Sequence = Sequence + tlc2olc[re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', line).group().split()[0].upper()]
      if re.search('[A-Z][A-Z][A-Z]', line) and not re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', line):
        if re.search('[A-Z][A-Z][A-Z]', line).group().upper() in tlc2olc.keys():
          Sequence = Sequence + tlc2olc[re.search('[A-Z][A-Z][A-Z]', line).group().upper()]
      if '+' in line:
        Sequence = Sequence + '+'
  ### For single letter code fasta style sequences 
  if len(sflines[0]) != 3 and not re.search('[A-Z][A-Z][A-Z] * ([0-9]*)', sflines[0]):
    for line in sflines:
      Sequence = Sequence + line
  Sequence = Sequence.replace('++','+')
  
  for x in first_residue.split(','):
    Indexes.append(int(x)) 

  for x in range(len(Sequence.split('+'))):
    for i in range(len(Sequence.split('+')[x])):
      index = i + int(Indexes[x])
      readsequence.append((index, Sequence.split('+')[x][i])) 
      NumSeq = NumSeq + Sequence.split('+')[x][i] + str(index) + ', '

  NumSeq = NumSeq[:-2]
  print 'Sequence from myseq.ReadSequenceFromFile'
  print NumSeq
  return readsequence

# -----------------------------------------------------------------------------
def getFirstKey(item):
  return item[0]
# -----------------------------------------------------------------------------

def ReadSequenceFromFile(szFileName):
  if szFileName == '':
    return []
  f = open(szFileName, 'r')
  if f == None:
    return []

  if szFileName.endswith(".seq") or szFileName.endswith(".SEQ") or szFileName.endswith(".Seq"):
    isThree = 1
  elif szFileName.endswith(".txt") or szFileName.endswith(".TXT") or szFileName.endswith(".Txt"):
    isThree = 2
  else:
    isThree = 0

  pszLines = f.readlines()
  f.close()

  # set sequences
  readsequence = []

  # three letter code
  if isThree > 0:
    iFirstIdx = -9999
    iCurIdx = -9999
    iType = 0
    for szLine in pszLines:
      if szLine == '': continue
      if szLine.strip()[:1] == '#': continue

      szSplited = szLine.split()
      if len(szSplited) == 2 and iFirstIdx == -9999:
        try:
          iFirstIdx = int(szSplited[0])
          iType = 0
        except:
          try:
            iFirstIdx = int(szSplited[1])
            iType = 1
          except:
            iFirstIdx = 1
            iType = 2
        iCurIdx = iFirstIdx
      elif iFirstIdx == -9999:
        iFirstIdx = 1
        iCurIdx = iFirstIdx
        iType = 1

      if iType == 0:
        szA = aaa2a(szSplited[1].upper())
      else:
        szA = aaa2a(szSplited[0].upper())
      readsequence.append( (iCurIdx, szA) )
      iCurIdx = iCurIdx + 1
  # one letter code
  else:
    iFirstIdx = 1
    iCurIdx = 1
    for szLine in pszLines:
      if szLine == '': continue
      if szLine.strip()[:1] == '#': continue
      if szLine.strip()[:1] == '>': continue
      for szA in szLine:
        szAAA = a2aaa(szA)
        if szAAA == 'XXX': continue
        readsequence.append( (iCurIdx, szA) )

        iCurIdx = iCurIdx + 1
  sort_list = sorted(readsequence, key=getFirstKey)
  return sort_list

# -----------------------------------------------------------------------------

# accepts ( (1,'A' ) and returns same
def FillSequenceGap(cur_sequence, template_sequence):
  # try to fill the gap
  iDiff = -9999
  szReadSeq = ''
  print cur_sequence
  for i in range(len(cur_sequence)):  
    szReadSeq = szReadSeq + cur_sequence[i][1]
    
  iUserSeqFirst = template_sequence[0][0]
  szUserSeq = ''
  for i in range(len(template_sequence)):  
    szUserSeq = szUserSeq + template_sequence[i][1]
    
  for i in range(len(template_sequence)-5):
    szUserPartSeq = szUserSeq[i: i+5]
    iDiff = szReadSeq.find(szUserPartSeq)
    if iDiff != -1: break
  if iDiff == -1:
    return None
  
  retSeq = []
  for i in range(len(template_sequence)):
    seq = template_sequence[i]
    if seq[1] != 'X':
      retSeq.append(seq)
      continue
    if (i+iDiff) > (len(cur_sequence)-1):
      return retSeq # end here
    retSeq.append( (seq[0], szReadSeq[i+iDiff]) )
  return retSeq  

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Build Sequence from resonance stored in NMRFAM-SPARKY
# iMode:
#   0: 'AXSAGADSCBSD' -> regular 1-letter-code
#   1: ('A', 'S', 'X'...) -> 1-letter-code in list
#   2: ('ALA', 'SER', 'XXX'....) -> 3-letter-code in list
#   3: ( (1,'A')) -> my group list
#   4: ( ('A',1)) -> my group list, used in tan.py
def BuildSequence(session, iMode):
  sequence_from_session = []

  iMin = 9999
  iMax = -9999
  for molecule in session.project.molecule_list():
    for group in molecule.group_list():
      sequence_from_session.append( (group.number, group.name[0]) )
      if group.number < iMin:
        try:
          iMin = int(group.number)
        except:
          pass
      if group.number > iMax:
        try:
          iMax = int(group.number)
        except:
          pass

  szSequence = ''
  sequence_list = []

  for i in range(iMin, iMax+1):
    iFound = 0
    for seq_group in sequence_from_session:
      if seq_group[0] != i: continue
      if iMode == 0:
        szSequence = szSequence + seq_group[1]
      elif iMode == 1:
        sequence_list.append(seq_group[1])
      elif iMode == 2:
        szSequence = szSequence + seq_group[1]
        aaa = seq_group[1]
        sequence_list.append(aaa)
      elif iMode == 3:
        sequence_list.append( (seq_group[0], seq_group[1]) )
      elif iMode == 4:
        sequence_list.append( (seq_group[1], seq_group[0]) )
      iFound = 1
    if iFound != 1:
      if iMode == 0:
        szSequence = szSequence + 'X'
      elif iMode == 1:
        sequence_list.append('X')
      elif iMode == 2:
        sequence_list.append('XXX')
      elif iMode == 3:
        sequence_list.append( (seq_group[0], 'X') )
      elif iMode == 4:
        sequence_list.append( ('X', seq_group[0]) )
      iFound = 1
  if iMode == 2: # treat N.A.
    bt = GetBiomoleculeTypeByFasta(szSequence)    
    for i in range(len(sequence_list)):
      aaa = sequence_list[i]
      if bt == 'p':
        sequence_list[i] = a2aaa(aaa)
      if bt == 'n':
        sequence_list[i] = na_a2aaa(aaa)
  return sequence_list
  
# -----------------------------------------------------------------------------
# Build chemical shift list in NMRFAM-SPARKY
# Seq ID, Seq ID, Seq, Atom, Atom type, Isotop, CS, CS_Dev, 2
def BuildResonance(session):
  groups = []
  fasta = ''
  for condition in session.project.condition_list():
    for resonance in condition.resonance_list():
      if resonance == None: continue
      if resonance.group == None: continue
      if resonance.group.number == None: continue
      aaa = resonance.group.symbol
      if aaa == '': continue
      if resonance.atom.name.find('_s') != -1: continue # this is simulated assignment
      fasta = fasta + resonance.group.symbol
      atom_type = resonance.atom.name[0:1]
      if (atom_type == 'Q') or (atom_type == 'M'): atom_type = 'H'
      isotope = 1
      if atom_type == 'C': isotope = 13
      elif atom_type == 'N': isotope = 15
      elif atom_type == 'P': isotope = 31

      group = [resonance.group.number, aaa, resonance.atom.name,
              atom_type, isotope, resonance.frequency, resonance.deviation]
      groups.append(group)
  bt = GetBiomoleculeTypeByFasta(fasta)
  for i in range(len(groups)):
    if bt == 'p':
      groups[i][1] = a2aaa(groups[i][1])
    if bt == 'n':
      groups[i][1] = na_a2aaa(groups[i][1])
  groups.sort()
  
# -----------------------------------------------------------------------------
# Get attached heavy atom from protons.
#
def GetAttachedHeavyAtom(szA, szAtom):
  if (szAtom == "HN") or (szAtom == "H") or ("HT" in szAtom):
    return "N"
    
  if len(szA) == 3:
    szA =  AAA_dict[szA.upper()]
  
  if len(szAtom) < 2:
    return ""  
    
  if szAtom[1] == "A": return "CA"
  if szAtom[1] == "B": return "CB"  
  
  if szA == "R":
    if szAtom[1] == "G": return "CG"
    if szAtom[1] == "D": return "CD"    
    if szAtom[1] == "Z": return "CZ"
    if szAtom[1] == "E": return "NE"
    if szAtom[1] == "H": 
      if len(szAtom) == 2: return "NH"
      if szAtom[2] == "1": return "NH1"
      if szAtom[2] == "2": return "NH2"
  elif szA == "N":
    if szAtom[1] == "G": return "CG"
    if szAtom[1] == "D": return "ND2"
  elif szA == "D":
    if szAtom[1] == "G": return "CG"  
  elif szA == "Q":
    if szAtom[1] == "G": return "CG"  
    if szAtom[1] == "E": return "NE2"    
  elif szA == "E":
    if szAtom[1] == "G": return "CG"
  elif szA == "H":
    if szAtom[1] == "G": return "CG"
    if len(szAtom) < 3: return ""
    if szAtom[1] == "D" and szAtom[2] == "2": return "CD2"
    if szAtom[1] == "D" and szAtom[2] == "1": return "NE1"
    if szAtom[1] == "E" and szAtom[2] == "1": return "CE1"
    if szAtom[1] == "E" and szAtom[2] == "2": return "NE2"
  elif szA == "I":  
    if szAtom[1] == "G" and len(szAtom) == 2: return "CG"
    if szAtom[1] == "D" and len(szAtom) == 2: return "CD"    
    if len(szAtom) < 3: return ""
    if szAtom[1] == "G" and szAtom[2] == "1": return "CG1"
    if szAtom[1] == "G" and szAtom[2] == "2": return "CG2"    
    if szAtom[1] == "D" and szAtom[2] == "1": return "CD1"
  elif szA == "L":
    if szAtom[1] == "G": return "CG"     
    if szAtom[1] == "D" and len(szAtom) == 2: return "CD"    
    if len(szAtom) < 3: return ""        
    if szAtom[1] == "D" and szAtom[2] == "1": return "CD1"    
    if szAtom[1] == "D" and szAtom[2] == "2": return "CD2"        
  elif szA == "K":
    if szAtom[1] == "G": return "CG"   
    if szAtom[1] == "D": return "CD"    
    if szAtom[1] == "E": return "CE"
    if szAtom[1] == "Z": return "NZ"
  elif szA == "M":  
    if szAtom[1] == "G": return "CG"  
    if szAtom[1] == "E": return "CE"  
  elif szA == "F":  
    if szAtom[1] == "G": return "CG"
    if szAtom[1] == "D" and len(szAtom) == 2: return "CD"    
    if szAtom[1] == "E" and len(szAtom) == 2: return "CE"     
    if len(szAtom) < 3: return ""        
    if szAtom[1] == "D" and szAtom[2] == "1": return "CD1"
    if szAtom[1] == "D" and szAtom[2] == "2": return "CD2"
    if szAtom[1] == "E" and szAtom[2] == "1": return "CE1"
    if szAtom[1] == "E" and szAtom[2] == "2": return "CE2"    
    if szAtom[1] == "Z": return "CZ"
  elif szA == "P":
    if szAtom[1] == "G" and len(szAtom) == 2: return "CG"
    if szAtom[1] == "D" and len(szAtom) == 2: return "CD" 
  elif szA == "T":  
    if len(szAtom) < 3: return ""
    if szAtom[1] == "G" and szAtom[2] == "2": return "CG2"  
  elif szA == "W":
    if szAtom[1] == "G": return "CG"
    if szAtom[1] == "D" and len(szAtom) == 2: return "CD"    
    if szAtom[1] == "E" and len(szAtom) == 2: return "CE"     
    if szAtom[1] == "Z" and len(szAtom) == 2: return "CZ"
    if szAtom[1] == "H" and len(szAtom) == 2: return "CH"    
    if len(szAtom) < 3: return ""        
    if szAtom[1] == "D" and szAtom[2] == "1": return "CD1"
    if szAtom[1] == "D" and szAtom[2] == "2": return "CD2"
    if szAtom[1] == "E" and szAtom[2] == "1": return "NE1"
    if szAtom[1] == "E" and szAtom[2] == "2": return "CE2"
    if szAtom[1] == "E" and szAtom[2] == "3": return "CE3"    
    if szAtom[1] == "Z" and szAtom[2] == "1": return "CZ1"
    if szAtom[1] == "Z" and szAtom[2] == "2": return "CZ2"
    if szAtom[1] == "Z" and szAtom[2] == "3": return "CZ3"    
    if szAtom[1] == "H" and szAtom[2] == "1": return "CH1"
    if szAtom[1] == "H" and szAtom[2] == "2": return "CH2"
  elif szA == "Y":  
    if szAtom[1] == "G": return "CG"
    if szAtom[1] == "D" and len(szAtom) == 2: return "CD"
    if szAtom[1] == "E" and len(szAtom) == 2: return "CE"
    if len(szAtom) < 3: return ""
    if szAtom[1] == "D" and szAtom[2] == "1": return "CD1"
    if szAtom[1] == "D" and szAtom[2] == "2": return "CD2"
    if szAtom[1] == "E" and szAtom[2] == "1": return "CE1"
    if szAtom[1] == "E" and szAtom[2] == "2": return "CE2"
  elif szA == "V":  
    if szAtom[1] == "G" and len(szAtom) == 2: return "CG"
    if len(szAtom) < 3: return ""
    if szAtom[1] == "G" and szAtom[2] == "1": return "CG1"
    if szAtom[1] == "G" and szAtom[2] == "2": return "CG2"
  return ""      
