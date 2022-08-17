import Tkinter
import pyutil
import sparky
import sputil
import tkutil
import pars_ucsf as ng
import os
from datetime import datetime
import tkFileDialog
import numpy as np
import tkMessageBox
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import cm
import warnings
warnings.filterwarnings("ignore", message="No contour levels were found")
# ------------------------------------------------------------------------------
#
# Updated by : Mary Clay PhD
# e-mail: mary.clay@stjude.org
# St Jude Children's Research Hospital 
# Department of Structural Biology Memphis, TN 
#
# Last updates: June 2, 2021
#
#
# ------------------------------------------------------------------------------
#
lpd = {(0, 1):1, (1, 0):2, (0, 1, 2):1, (0, 2, 1):2, (1, 0, 2):3, (1, 2, 0):4, (2, 0, 1):5, (2, 1, 0):6}
Nuc_format = {'1H':r"$^{1}$H (ppm)", '13C':r"$^{13}$C (ppm)", '15N':r"$^{15}$N (ppm)", '31P':r"$^{31}$P (ppm)", '2H':r"$^{2}$H (ppm)", '19F':r"$^{19}$F (ppm)"}
xscal_dic = {'1H':1.0, '13C':0.25, '15N':0.1, '19F': 0.98 , '31P':0.42 , '2H':0.15 }
strip_dic = {(0, 1, 2):'data[min_x:max_x+1, min_y:max_y+1, z_idx]', 
			 (1, 0, 2):'data[min_y:max_y+1, min_x:max_x+1, z_idx]', 
			 (0, 2, 1):'data[min_x:max_x+1, z_idx, min_y:max_y+1]', 
			 (2, 0, 1):'data[min_y:max_y+1, z_idx, min_x:max_x+1]', 
			 (1, 2, 0):'data[z_idx, min_x:max_x+1, min_y:max_y+1]', 
			 (2, 1, 0):'data[z_idx, min_y:max_y+1, min_x:max_x+1]',
			 (0, 1, 2, 3):'data[min_x:may_x+1, min_y:may_x+1, z_idx, w_idx]',
			 (1, 0, 2, 3):'data[min_y:max_y+1, min_x:max_x+1, z_idx, w_idx]',
			 (3, 2, 1, 0):'data[z_idx, w_idx, min_x:max_x+1, min_y:max_y+1]',
			 (2, 3, 1, 0):'data[w_idx, z_idx, min_x:max_x+1, min_y:max_y+1]',
			 (0, 1):'data[min_x:max_x+1, min_y:max_y+1]', 
			 (1, 0):'data[min_y:max_y+1, min_x:max_x+1]'}

COLORS = {"alice blue": "#f0f8ff","AliceBlue": "#f0f8ff","antique white": "#faebd7","AntiqueWhite": "#faebd7","AntiqueWhite1": "#ffefdb","AntiqueWhite2": "#eedfcc","AntiqueWhite3": "#cdc0b0","AntiqueWhite4": "#8b8378","agua": "#00ffff","aquamarine": "#7fffd4","aquamarine1": "#7fffd4","aquamarine2": "#76eec6","aquamarine3": "#66cdaa","aquamarine4": "#458b74","azure": "#f0ffff","azure1": "#f0ffff","azure2": "#e0eeee","azure3": "#c1cdcd","azure4": "#838b8b","beige": "#f5f5dc","bisque": "#ffe4c4","bisque1": "#ffe4c4","bisque2": "#eed5b7","bisque3": "#cdb79e","bisque4": "#8b7d6b","black": "#000000","blanched almond": "#ffebcd","BlanchedAlmond": "#ffebcd","blue": "#0000ff","blue violet": "#8a2be2","blue1": "#0000ff","blue2": "#0000ee","blue3": "#0000cd","blue4": "#00008b","BlueViolet": "#8a2be2","brown": "#a52a2a","brown1": "#ff4040","brown2": "#ee3b3b","brown3": "#cd3333","brown4": "#8b2323","burlywood": "#deb887","burlywood1": "#ffd39b","burlywood2": "#eec591","burlywood3": "#cdaa7d","burlywood4": "#8b7355","cadet blue": "#5f9ea0","CadetBlue": "#5f9ea0","CadetBlue1": "#98f5ff","CadetBlue2": "#8ee5ee","CadetBlue3": "#7ac5cd","CadetBlue4": "#53868b",
"chartreuse": "#7fff00","chartreuse1": "#7fff00","chartreuse2": "#76ee00","chartreuse3": "#66cd00","chartreuse4": "#458b00","chocolate": "#d2691e","chocolate1": "#ff7f24","chocolate2": "#ee7621","chocolate3": "#cd661d","chocolate4": "#8b4513","coral": "#ff7f50","coral1": "#ff7256","coral2": "#ee6a50","coral3": "#cd5b45","coral4": "#8b3e2f","cornflower blue": "#6495ed","CornflowerBlue": "#6495ed","cornsilk": "#fff8dc","cornsilk1": "#fff8dc","cornsilk2": "#eee8cd","cornsilk3": "#cdc8b1","cornsilk4": "#8b8878","crymson": "#dc143c","cyan": "#00ffff","cyan1": "#00ffff","cyan2": "#00eeee","cyan3": "#00cdcd","cyan4": "#008b8b","dark blue": "#00008b","dark cyan": "#008b8b","dark goldenrod": "#b8860b","dark gray": "#a9a9a9","dark green": "#006400","dark grey": "#a9a9a9","dark khaki": "#bdb76b","dark magenta": "#8b008b","dark olive green": "#556b2f","dark orange": "#ff8c00","dark orchid": "#9932cc","dark red": "#8b0000","dark salmon": "#e9967a","dark sea green": "#8fbc8f","dark slate blue": "#483d8b","dark slate gray": "#2f4f4f","dark slate grey": "#2f4f4f","dark turquoise": "#00ced1","dark violet": "#9400d3","DarkBlue": "#00008b","DarkCyan": "#008b8b","DarkGoldenrod": "#b8860b",
"DarkGoldenrod1": "#ffb90f","DarkGoldenrod2": "#eead0e","DarkGoldenrod3": "#cd950c","DarkGoldenrod4": "#8b6508","DarkGray": "#a9a9a9","DarkGreen": "#006400","DarkGrey": "#a9a9a9","DarkKhaki": "#bdb76b","DarkMagenta": "#8b008b","DarkOliveGreen": "#556b2f","DarkOliveGreen1": "#caff70","DarkOliveGreen2": "#bcee68","DarkOliveGreen3": "#a2cd5a","DarkOliveGreen4": "#6e8b3d","DarkOrange": "#ff8c00","DarkOrange1": "#ff7f00","DarkOrange2": "#ee7600","DarkOrange3": "#cd6600","DarkOrange4": "#8b4500","DarkOrchid": "#9932cc","DarkOrchid1": "#bf3eff","DarkOrchid2": "#b23aee","DarkOrchid3": "#9a32cd","DarkOrchid4": "#68228b","DarkRed": "#8b0000","DarkSalmon": "#e9967a","DarkSeaGreen": "#8fbc8f","DarkSeaGreen1": "#c1ffc1","DarkSeaGreen2": "#b4eeb4","DarkSeaGreen3": "#9bcd9b","DarkSeaGreen4": "#698b69","DarkSlateBlue": "#483d8b","DarkSlateGray": "#2f4f4f","DarkSlateGray1": "#97ffff","DarkSlateGray2": "#8deeee","DarkSlateGray3": "#79cdcd","DarkSlateGray4": "#528b8b","DarkSlateGrey": "#2f4f4f","DarkTurquoise": "#00ced1","DarkViolet": "#9400d3","deep pink": "#ff1493","deep sky blue": "#00bfff","DeepPink": "#ff1493","DeepPink1": "#ff1493","DeepPink2": "#ee1289","DeepPink3": "#cd1076","DeepPink4": "#8b0a50","DeepSkyBlue": "#00bfff","DeepSkyBlue1": "#00bfff","DeepSkyBlue2": "#00b2ee",
"DeepSkyBlue3": "#009acd","DeepSkyBlue4": "#00688b","dim gray": "#696969","dim grey": "#696969","DimGray": "#696969","DimGrey": "#696969","dodger blue": "#1e90ff","DodgerBlue": "#1e90ff","DodgerBlue1": "#1e90ff","DodgerBlue2": "#1c86ee","DodgerBlue3": "#1874cd","DodgerBlue4": "#104e8b","firebrick": "#b22222","firebrick1": "#ff3030","firebrick2": "#ee2c2c","firebrick3": "#cd2626","firebrick4": "#8b1a1a","floral white": "#fffaf0","FloralWhite": "#fffaf0","forest green": "#228b22","ForestGreen": "#228b22","fuchsia": "#ff00ff","gainsboro": "#dcdcdc","ghost white": "#f8f8ff","GhostWhite": "#f8f8ff","gold": "#ffd700","gold1": "#ffd700","gold2": "#eec900","gold3": "#cdad00","gold4": "#8b7500","goldenrod": "#daa520","goldenrod1": "#ffc125","goldenrod2": "#eeb422","goldenrod3": "#cd9b1d","goldenrod4": "#8b6914","gray": "#bebebe","gray0": "#000000","gray1": "#030303","gray2": "#050505","gray3": "#080808","gray4": "#0a0a0a","gray5": "#0d0d0d","gray6": "#0f0f0f","gray7": "#121212","gray8": "#141414","gray9": "#171717","gray10": "#1a1a1a","gray11": "#1c1c1c","gray12": "#1f1f1f","gray13": "#212121",
"gray14": "#242424","gray15": "#262626","gray16": "#292929","gray17": "#2b2b2b","gray18": "#2e2e2e","gray19": "#303030","gray20": "#333333","gray21": "#363636","gray22": "#383838","gray23": "#3b3b3b","gray24": "#3d3d3d","gray25": "#404040","gray26": "#424242","gray27": "#454545","gray28": "#474747","gray29": "#4a4a4a","gray30": "#4d4d4d","gray31": "#4f4f4f","gray32": "#525252","gray33": "#545454","gray34": "#575757","gray35": "#595959","gray36": "#5c5c5c","gray37": "#5e5e5e","gray38": "#616161","gray39": "#636363","gray40": "#666666","gray41": "#696969","gray42": "#6b6b6b","gray43": "#6e6e6e","gray44": "#707070","gray45": "#737373","gray46": "#757575","gray47": "#787878","gray48": "#7a7a7a","gray49": "#7d7d7d","gray50": "#7f7f7f","gray51": "#828282","gray52": "#858585","gray53": "#878787","gray54": "#8a8a8a","gray55": "#8c8c8c","gray56": "#8f8f8f","gray57": "#919191","gray58": "#949494","gray59": "#969696","gray60": "#999999","gray61": "#9c9c9c","gray62": "#9e9e9e","gray63": "#a1a1a1",
"gray64": "#a3a3a3","gray65": "#a6a6a6","gray66": "#a8a8a8","gray67": "#ababab","gray68": "#adadad","gray69": "#b0b0b0","gray70": "#b3b3b3","gray71": "#b5b5b5","gray72": "#b8b8b8","gray73": "#bababa","gray74": "#bdbdbd","gray75": "#bfbfbf","gray76": "#c2c2c2","gray77": "#c4c4c4","gray78": "#c7c7c7","gray79": "#c9c9c9","gray80": "#cccccc","gray81": "#cfcfcf","gray82": "#d1d1d1","gray83": "#d4d4d4","gray84": "#d6d6d6","gray85": "#d9d9d9","gray86": "#dbdbdb","gray87": "#dedede","gray88": "#e0e0e0","gray89": "#e3e3e3","gray90": "#e5e5e5","gray91": "#e8e8e8","gray92": "#ebebeb","gray93": "#ededed","gray94": "#f0f0f0","gray95": "#f2f2f2","gray96": "#f5f5f5","gray97": "#f7f7f7","gray98": "#fafafa","gray99": "#fcfcfc","gray100": "#ffffff","green": "#00ff00","green yellow": "#adff2f","green1": "#00ff00","green2": "#00ee00","green3": "#00cd00","green4": "#008b00","GreenYellow": "#adff2f","grey": "#bebebe","grey0": "#000000","grey1": "#030303","grey2": "#050505","grey3": "#080808","grey4": "#0a0a0a",
"grey5": "#0d0d0d","grey6": "#0f0f0f","grey7": "#121212","grey8": "#141414","grey9": "#171717","grey10": "#1a1a1a","grey11": "#1c1c1c","grey12": "#1f1f1f","grey13": "#212121","grey14": "#242424","grey15": "#262626","grey16": "#292929","grey17": "#2b2b2b","grey18": "#2e2e2e","grey19": "#303030","grey20": "#333333","grey21": "#363636","grey22": "#383838","grey23": "#3b3b3b","grey24": "#3d3d3d","grey25": "#404040","grey26": "#424242","grey27": "#454545","grey28": "#474747","grey29": "#4a4a4a","grey30": "#4d4d4d","grey31": "#4f4f4f","grey32": "#525252","grey33": "#545454","grey34": "#575757","grey35": "#595959","grey36": "#5c5c5c","grey37": "#5e5e5e","grey38": "#616161","grey39": "#636363","grey40": "#666666","grey41": "#696969","grey42": "#6b6b6b","grey43": "#6e6e6e","grey44": "#707070","grey45": "#737373","grey46": "#757575","grey47": "#787878","grey48": "#7a7a7a","grey49": "#7d7d7d","grey50": "#7f7f7f","grey51": "#828282","grey52": "#858585","grey53": "#878787","grey54": "#8a8a8a",
"grey55": "#8c8c8c","grey56": "#8f8f8f","grey57": "#919191","grey58": "#949494","grey59": "#969696","grey60": "#999999","grey61": "#9c9c9c","grey62": "#9e9e9e","grey63": "#a1a1a1","grey64": "#a3a3a3","grey65": "#a6a6a6","grey66": "#a8a8a8","grey67": "#ababab","grey68": "#adadad","grey69": "#b0b0b0","grey70": "#b3b3b3","grey71": "#b5b5b5","grey72": "#b8b8b8","grey73": "#bababa","grey74": "#bdbdbd","grey75": "#bfbfbf","grey76": "#c2c2c2","grey77": "#c4c4c4","grey78": "#c7c7c7","grey79": "#c9c9c9","grey80": "#cccccc","grey81": "#cfcfcf","grey82": "#d1d1d1","grey83": "#d4d4d4","grey84": "#d6d6d6","grey85": "#d9d9d9","grey86": "#dbdbdb","grey87": "#dedede","grey88": "#e0e0e0","grey89": "#e3e3e3","grey90": "#e5e5e5","grey91": "#e8e8e8","grey92": "#ebebeb","grey93": "#ededed","grey94": "#f0f0f0","grey95": "#f2f2f2","grey96": "#f5f5f5","grey97": "#f7f7f7","grey98": "#fafafa","grey99": "#fcfcfc","grey100": "#ffffff","honeydew": "#f0fff0","honeydew1": "#f0fff0","honeydew2": "#e0eee0","honeydew3": "#c1cdc1",
"honeydew4": "#838b83","hot pink": "#ff69b4","HotPink": "#ff69b4","HotPink1": "#ff6eb4","HotPink2": "#ee6aa7","HotPink3": "#cd6090","HotPink4": "#8b3a62","indian red": "#cd5c5c","IndianRed": "#cd5c5c","IndianRed1": "#ff6a6a","IndianRed2": "#ee6363","IndianRed3": "#cd5555","IndianRed4": "#8b3a3a","indigo": "#4b0082","ivory": "#fffff0","ivory1": "#fffff0","ivory2": "#eeeee0","ivory3": "#cdcdc1","ivory4": "#8b8b83","khaki": "#f0e68c","khaki1": "#fff68f","khaki2": "#eee685","khaki3": "#cdc673","khaki4": "#8b864e","lavender": "#e6e6fa","lavender blush": "#fff0f5","LavenderBlush": "#fff0f5","LavenderBlush1": "#fff0f5","LavenderBlush2": "#eee0e5","LavenderBlush3": "#cdc1c5","LavenderBlush4": "#8b8386","lawn green": "#7cfc00","LawnGreen": "#7cfc00","lemon chiffon": "#fffacd","LemonChiffon": "#fffacd","LemonChiffon1": "#fffacd","LemonChiffon2": "#eee9bf","LemonChiffon3": "#cdc9a5","LemonChiffon4": "#8b8970","light blue": "#add8e6","light coral": "#f08080","light cyan": "#e0ffff","light goldenrod": "#eedd82","light goldenrod yellow": "#fafad2","light gray": "#d3d3d3","light green": "#90ee90","light grey": "#d3d3d3","light pink": "#ffb6c1","light salmon": "#ffa07a","light sea green": "#20b2aa",
"light sky blue": "#87cefa","light slate blue": "#8470ff","light slate gray": "#778899","light slate grey": "#778899","light steel blue": "#b0c4de","light yellow": "#ffffe0","LightBlue": "#add8e6","LightBlue1": "#bfefff","LightBlue2": "#b2dfee","LightBlue3": "#9ac0cd","LightBlue4": "#68838b","LightCoral": "#f08080","LightCyan": "#e0ffff","LightCyan1": "#e0ffff","LightCyan2": "#d1eeee","LightCyan3": "#b4cdcd","LightCyan4": "#7a8b8b","LightGoldenrod": "#eedd82","LightGoldenrod1": "#ffec8b","LightGoldenrod2": "#eedc82","LightGoldenrod3": "#cdbe70","LightGoldenrod4": "#8b814c","LightGoldenrodYellow": "#fafad2","LightGray": "#d3d3d3","LightGreen": "#90ee90","LightGrey": "#d3d3d3","LightPink": "#ffb6c1","LightPink1": "#ffaeb9","LightPink2": "#eea2ad","LightPink3": "#cd8c95","LightPink4": "#8b5f65","LightSalmon": "#ffa07a","LightSalmon1": "#ffa07a","LightSalmon2": "#ee9572","LightSalmon3": "#cd8162","LightSalmon4": "#8b5742","LightSeaGreen": "#20b2aa","LightSkyBlue": "#87cefa","LightSkyBlue1": "#b0e2ff","LightSkyBlue2": "#a4d3ee","LightSkyBlue3": "#8db6cd","LightSkyBlue4": "#607b8b","LightSlateBlue": "#8470ff","LightSlateGray": "#778899","LightSlateGrey": "#778899","LightSteelBlue": "#b0c4de","LightSteelBlue1": "#cae1ff","LightSteelBlue2": "#bcd2ee","LightSteelBlue3": "#a2b5cd","LightSteelBlue4": "#6e7b8b",
"LightYellow": "#ffffe0","LightYellow1": "#ffffe0","LightYellow2": "#eeeed1","LightYellow3": "#cdcdb4","LightYellow4": "#8b8b7a","lime": "#00ff00", "limegreen": "#32cd32","lime green": "#32cd32","LimeGreen": "#32cd32","linen": "#faf0e6","magenta": "#ff00ff","magenta1": "#ff00ff","magenta2": "#ee00ee","magenta3": "#cd00cd","magenta4": "#8b008b","maroon": "#b03060","maroon1": "#ff34b3","maroon2": "#ee30a7","maroon3": "#cd2990","maroon4": "#8b1c62","medium aquamarine": "#66cdaa","medium blue": "#0000cd","medium orchid": "#ba55d3","medium purple": "#9370db","medium sea green": "#3cb371","medium slate blue": "#7b68ee","medium spring green": "#00fa9a","medium turquoise": "#48d1cc","medium violet red": "#c71585","MediumAquamarine": "#66cdaa","MediumBlue": "#0000cd","MediumOrchid": "#ba55d3","MediumOrchid1": "#e066ff","MediumOrchid2": "#d15fee","MediumOrchid3": "#b452cd","MediumOrchid4": "#7a378b","MediumPurple": "#9370db","MediumPurple1": "#ab82ff","MediumPurple2": "#9f79ee","MediumPurple3": "#8968cd","MediumPurple4": "#5d478b","MediumSeaGreen": "#3cb371","MediumSlateBlue": "#7b68ee","MediumSpringGreen": "#00fa9a","MediumTurquoise": "#48d1cc","MediumVioletRed": "#c71585","midnight blue": "#191970","MidnightBlue": "#191970","mint cream": "#f5fffa","MintCream": "#f5fffa","misty rose": "#ffe4e1",
"MistyRose": "#ffe4e1","MistyRose1": "#ffe4e1","MistyRose2": "#eed5d2","MistyRose3": "#cdb7b5","MistyRose4": "#8b7d7b","moccasin": "#ffe4b5","navajo white": "#ffdead","NavajoWhite": "#ffdead","NavajoWhite1": "#ffdead","NavajoWhite2": "#eecfa1","NavajoWhite3": "#cdb38b","NavajoWhite4": "#8b795e","navy": "#000080","navy blue": "#000080","NavyBlue": "#000080","old lace": "#fdf5e6","OldLace": "#fdf5e6","olive": "#808000","olive drab": "#6b8e23","OliveDrab": "#6b8e23","OliveDrab1": "#c0ff3e","OliveDrab2": "#b3ee3a","OliveDrab3": "#9acd32","OliveDrab4": "#698b22","orange": "#ffa500","orange red": "#ff4500","orange1": "#ffa500","orange2": "#ee9a00","orange3": "#cd8500","orange4": "#8b5a00","OrangeRed": "#ff4500","OrangeRed1": "#ff4500","OrangeRed2": "#ee4000","OrangeRed3": "#cd3700","OrangeRed4": "#8b2500","orchid": "#da70d6","orchid1": "#ff83fa","orchid2": "#ee7ae9","orchid3": "#cd69c9","orchid4": "#8b4789","pale goldenrod": "#eee8aa","pale green": "#98fb98","pale turquoise": "#afeeee","pale violet red": "#db7093","PaleGoldenrod": "#eee8aa","PaleGreen": "#98fb98","PaleGreen1": "#9aff9a","PaleGreen2": "#90ee90","PaleGreen3": "#7ccd7c","PaleGreen4": "#548b54",
"PaleTurquoise": "#afeeee","PaleTurquoise1": "#bbffff","PaleTurquoise2": "#aeeeee","PaleTurquoise3": "#96cdcd","PaleTurquoise4": "#668b8b","PaleVioletRed": "#db7093","PaleVioletRed1": "#ff82ab","PaleVioletRed2": "#ee799f","PaleVioletRed3": "#cd687f","PaleVioletRed4": "#8b475d","papaya whip": "#ffefd5","PapayaWhip": "#ffefd5","peach puff": "#ffdab9","PeachPuff": "#ffdab9","PeachPuff1": "#ffdab9","PeachPuff2": "#eecbad","PeachPuff3": "#cdaf95","PeachPuff4": "#8b7765","peru": "#cd853f","pink": "#ffc0cb","pink1": "#ffb5c5","pink2": "#eea9b8","pink3": "#cd919e","pink4": "#8b636c","plum": "#dda0dd","plum1": "#ffbbff","plum2": "#eeaeee","plum3": "#cd96cd","plum4": "#8b668b","powder blue": "#b0e0e6","PowderBlue": "#b0e0e6","purple": "#a020f0","purple1": "#9b30ff","purple2": "#912cee","purple3": "#7d26cd","purple4": "#551a8b","red": "#ff0000","red1": "#ff0000","red2": "#ee0000","red3": "#cd0000","red4": "#8b0000","rosy brown": "#bc8f8f","RosyBrown": "#bc8f8f","RosyBrown1": "#ffc1c1","RosyBrown2": "#eeb4b4","RosyBrown3": "#cd9b9b","RosyBrown4": "#8b6969","royal blue": "#4169e1","RoyalBlue": "#4169e1","RoyalBlue1": "#4876ff",
"RoyalBlue2": "#436eee","RoyalBlue3": "#3a5fcd","RoyalBlue4": "#27408b","saddle brown": "#8b4513","SaddleBrown": "#8b4513","salmon": "#fa8072","salmon1": "#ff8c69","salmon2": "#ee8262","salmon3": "#cd7054","salmon4": "#8b4c39","sandy brown": "#f4a460","SandyBrown": "#f4a460","sea green": "#2e8b57","SeaGreen": "#2e8b57","SeaGreen1": "#54ff9f","SeaGreen2": "#4eee94","SeaGreen3": "#43cd80","SeaGreen4": "#2e8b57","seashell": "#fff5ee","seashell1": "#fff5ee","seashell2": "#eee5de","seashell3": "#cdc5bf","seashell4": "#8b8682","sienna": "#a0522d","sienna1": "#ff8247","sienna2": "#ee7942","sienna3": "#cd6839","sienna4": "#8b4726","silver": "#c0c0c0","sky blue": "#87ceeb","SkyBlue": "#87ceeb","SkyBlue1": "#87ceff","SkyBlue2": "#7ec0ee","SkyBlue3": "#6ca6cd","SkyBlue4": "#4a708b","slate blue": "#6a5acd","slate gray": "#708090","slate grey": "#708090","SlateBlue": "#6a5acd","SlateBlue1": "#836fff","SlateBlue2": "#7a67ee","SlateBlue3": "#6959cd","SlateBlue4": "#473c8b","SlateGray": "#708090","SlateGray1": "#c6e2ff","SlateGray2": "#b9d3ee","SlateGray3": "#9fb6cd","SlateGray4": "#6c7b8b","SlateGrey": "#708090","snow": "#fffafa",
"snow1": "#fffafa","snow2": "#eee9e9","snow3": "#cdc9c9","snow4": "#8b8989","spring green": "#00ff7f","SpringGreen": "#00ff7f","SpringGreen1": "#00ff7f","SpringGreen2": "#00ee76","SpringGreen3": "#00cd66","SpringGreen4": "#008b45","steel blue": "#4682b4","SteelBlue": "#4682b4","SteelBlue1": "#63b8ff","SteelBlue2": "#5cacee","SteelBlue3": "#4f94cd","SteelBlue4": "#36648b","tan": "#d2b48c","tan1": "#ffa54f","tan2": "#ee9a49","tan3": "#cd853f","tan4": "#8b5a2b","teal": "#008080","thistle": "#d8bfd8","thistle1": "#ffe1ff","thistle2": "#eed2ee","thistle3": "#cdb5cd","thistle4": "#8b7b8b","tomato": "#ff6347","tomato1": "#ff6347","tomato2": "#ee5c42","tomato3": "#cd4f39","tomato4": "#8b3626","turquoise": "#40e0d0","turquoise1": "#00f5ff","turquoise2": "#00e5ee","turquoise3": "#00c5cd","turquoise4": "#00868b","violet": "#ee82ee","violet red": "#d02090","VioletRed": "#d02090","VioletRed1": "#ff3e96","VioletRed2": "#ee3a8c","VioletRed3": "#cd3278","VioletRed4": "#8b2252","wheat": "#f5deb3","wheat1": "#ffe7ba","wheat2": "#eed8ae","wheat3": "#cdba96","wheat4": "#8b7e66","white": "#ffffff",
"white smoke": "#f5f5f5","WhiteSmoke": "#f5f5f5","yellow": "#ffff00","yellow green": "#9acd32","yellow1": "#ffff00","yellow2": "#eeee00","yellow3": "#cdcd00","yellow4": "#8b8b00","YellowGreen": "#9acd32"}

linewidths = 1.0
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.sans-serif'] = 'arial'
mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.linewidth'] = linewidths
mpl.rcParams['xtick.direction'] = mpl.rcParams['ytick.direction']='out'
mpl.rcParams['xtick.labelsize'] = mpl.rcParams['ytick.labelsize']=10
mpl.rcParams['xtick.major.size'] = mpl.rcParams['ytick.major.size'] = 4
mpl.rcParams['xtick.major.width'] = mpl.rcParams['ytick.major.width']=linewidths
mpl.rcParams['xtick.minor.size'] = mpl.rcParams['ytick.minor.size'] = 2.5
mpl.rcParams['xtick.minor.width']= mpl.rcParams['ytick.minor.width'] = linewidths *0.5
mpl.rcParams['xtick.major.pad']=mpl.rcParams['ytick.major.pad']= 2
mpl.rcParams['axes.labelpad'] = 4
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.sf'] = 'sans\\-serif'
plt.rcParams['mathtext.default'] = 'regular'
mpl.mathtext.FontConstantsBase.sup1 = 0.25

class obj:
  pass
class view_menu(tkutil.option_menu):

  def __init__(self, session, parent, label, allow_no_choice = 0):

	self.session = session
	self.allow_no_choice = allow_no_choice
	self.names = self.view_names()
	tkutil.option_menu.__init__(self, parent, label, 
								self.names, self.default_view_name())
	self.menu['postcommand'] = self.update_menu_cb

  # --------------------------------------------------------------------------
  #
  def view_names(self):

	views = self.session.project.view_list()
	return pyutil.attribute_values(views, 'name')

  # --------------------------------------------------------------------------
  def default_view_name(self):
	return pyutil.attribute(self.session.selected_view(), 'name', '')
  # --------------------------------------------------------------------------
  def update_menu_cb(self):

	current_names = self.view_names()
	if current_names != self.names:
	  self.names = current_names
	  self.remove_all_entries()
	  for name in self.names:
		self.add_entry(name)
	  if not self.get() in self.names:
		self.set(self.default_spectrum_name())
  # --------------------------------------------------------------------------
  def spectrum(self):
	view_spectrum = sputil.name_to_view(self.get(), self.session)

	return sputil.name_to_spectrum(view_spectrum.spectrum.name, self.session)

  def view(self):

	return sputil.name_to_view(self.get(), self.session)

class pdf_printing_dialog(tkutil.Dialog):

  # ------------------------------------------------------------------------------
  #
  def __init__(self, session):

	tkutil.Dialog.__init__(self, session.tk, 'Save to PDF')
	self.session = session

	self.overlays = {}
	if session.project.save_path: 
	  overlay =[line.rstrip() for line in open(session.project.save_path, 'r').readlines() if line.rstrip() and line.split()[0] == 'overlay' ]
	  for line in overlay:
		  if line.split()[2] in self.overlays.keys():
			  self.overlays[line.split()[2]].append(line.split()[1])
		  else:
			  self.overlays[line.split()[2]] = [line.split()[1]]
	print self.overlays 
	print ''

	
	## select view to plot 
	vc = view_menu(self.session, self.top, 'View: ')
	vc.frame.pack(side = 'top', anchor = 'w')
	self.view_choice = vc
	print vc
	self.pf = self.Get_View_settings(Tkinter.Frame(self.top), self.view_choice.view())
	self.pf.pack(side='top')

	w = Tkinter.Label(self.top, text = 'Additional Options', justify = 'left')
	w.pack(side = 'top', anchor = 'w')

	### Check boxes to show or hide spectrum elements ###
	## Show Banner with spectrum information 
	bancb = tkutil.checkbutton(self.top, 'Show Banner', 0)
	bancb.button.pack(side = 'top', anchor = 'w')
	self.baner = bancb
	### Show Labels check box 
	lscb = tkutil.checkbutton(self.top, 'Hide Labels', 0)
	lscb.button.pack(side = 'top', anchor = 'w')
	self.ls = lscb
	### Show Peaks check box 
	pscb = tkutil.checkbutton(self.top, 'Hide Peaks', 1)
	pscb.button.pack(side = 'top', anchor = 'w')
	self.ps = pscb
	### Show Labels and color them all black check box 
	blcb = tkutil.checkbutton(self.top, 'Black Labels', 0)
	blcb.button.pack(side = 'top', anchor = 'w')
	self.bl = blcb
	### Show minor tick marks  check box 
	mtcb = tkutil.checkbutton(self.top, 'Hide minor ticks', 0)
	mtcb.button.pack(side = 'top', anchor = 'w')
	self.mt = mtcb
	### Do Strip plots check box 
	spcb = tkutil.checkbutton(self.top, 'Stip Plots', 0)
	spcb.button.pack(side = 'top', anchor = 'w')
	self.sp = spcb
	w = Tkinter.Label(self.top, text = "Strip Plot Options", justify = 'left')
	w.pack(side = 'top', anchor = 'w')
	spxtickcb = tkutil.checkbutton(self.top, 'Hide X-ticks', 0)
	spxtickcb.button.pack(side = 'top', anchor = 'w')
	self.spxtick = spxtickcb
	spvlinecb = tkutil.checkbutton(self.top, 'Add Vertical Line', 0)
	spvlinecb.button.pack(side = 'top', anchor = 'w') 
	self.spvline = spvlinecb
	w = Tkinter.Label(self.top, text = "\nTick Label Precision or Tick Spacing do not have to specified\nFor multi-panel images use same aspect ratio (vt)\nSave project before saving overlays (js)\nTick label precision is number of decimal places to be displayed\n", justify = 'left')
	w.pack(side = 'top', anchor = 'w')
	br = tkutil.button_row(self.top, 
						   ('Save', self.save_pdf_cb),
						   ('Close', self.close_cb))
	br.frame.pack(side = 'top', anchor = 'w')

# -----------------------------------------------------------------------------
#
  def Get_View_settings(self, parent, view):
	# view =sputil.name_to_view(view, self.session)
	# spectrum =sputil.name_to_spectrum(view.spectrum.name, self.session)
	print 'inside of Get_View_settings'
	print view.name
	
	xdim = view.axis_order[0]
	ydim = view.axis_order[1]
	pl = tkutil.grid_labels(parent, ('w'+str(1+xdim)+' %3s' % view.spectrum.nuclei[xdim], 1, 0), 
								('w'+str(1+ydim)+' %3s' % view.spectrum.nuclei[ydim], 2, 0), 
								('Downfield', 0, 1), 
								('Upfield', 0, 2), 
								('Tick Label\nprecision', 0, 3), 
								('Tick Spacing\n (ppm)', 0, 4))
	(self.xmax, 
	self.xmin, 
	self.xfloatp, 
	self.xmajor, 
	self.ymax, 
	self.ymin, 
	self.yfloatp, 
	self.ymajor) = tkutil.grid_entries(parent, 13, ('%10.3f' %view.region[1][xdim], 1, 1), 
										('%10.3f' %view.region[0][xdim], 1, 2), 
										('', 1, 3), 
										('', 1, 4), 
										('%10.3f' %view.region[1][ydim], 2, 1), 
										('%10.3f' %view.region[0][ydim], 2, 2), 
										('', 2, 3), 
										('', 2, 4))
	return parent

# -----------------------------------------------------------------------------
#
  def save_pdf_cb(self):
	file_opt = options = {}
	options['defaultextension'] = '.pdf'
	options['filetypes'] = [('portable document format', '.pdf')]
	options['title'] = 'Save PDF'
	options['initialfile'] = self.view_choice.view().name.replace('/','_') + '.pdf'

	path = tkFileDialog.asksaveasfilename(**file_opt)
	#path = tkutil.save_file(self.top, 'Save PDF', self.view_choice.spectrum().name + '.pdf')
	#path = tkutil.save_file2(self.top, 'Save PDF', 'pdf', self.view_choice.spectrum().name + '.pdf', 'pdf')
	if path:
		if self.view_choice.spectrum().dimension == 2:
			self.plot_2D(path)
		if self.view_choice.spectrum().dimension == 4:
			self.plot_4D(path)
		if self.view_choice.spectrum().dimension == 3:
			if self.sp.state() == False:
				self.plot_3D(path)
			if self.sp.state() == True:
				self.strips = sorted(self.session.selected_peaks(), key = lambda x: (x.resonances()[0].group.number, x.frequency[0]))
				self.strip_plots(path, self.strips)
# -----------------------------------------------------------------------------
#
  def close_cb(self):
	self.top.destroy()

# -----------------------------------------------------------------------------
#
  def get_selections(self):
	selections = pyutil.generic_class()
	selections.view = self.view_choice.view()
	selections.xmax =   float(self.xmax.get())
	selections.xmin =   float(self.xmin.get())
	selections.xfloatp = self.xfloatp.get()
	selections.xmajor = self.xmajor.get()
	selections.ymax =   float(self.ymax.get())
	selections.ymin =   float(self.ymin.get())
	selections.yfloatp = self.yfloatp.get()
	selections.ymajor = self.ymajor.get()
	selections.banner = self.baner.state()
	selections.ls = self.ls.state()
	selections.ps = self.ps.state()
	selections.bl = self.bl.state()
	selections.mt = self.mt.state()
	selections.sp = self.sp.state()
	selections.strip_x = self.spxtick.state()
	selections.add_vline = self.spvline.state()
	selections.overlays = self.overlays
	return selections
# -----------------------------------------------------------------------------
#
  def generate_banner(self):
	s = self.get_selections()
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	banner = 'Spectrum: %s\nUser: %s    Date: %s\nPositive contours: low %1.2E levels %d factor %f\nNegative contours: low %1.2E levels %d factor %f' %(s.view.name, os.environ.get('USER'), dt_string, s.view.positive_levels.lowest, s.view.positive_levels.levels, s.view.positive_levels.factor, s.view.negative_levels.lowest, s.view.negative_levels.levels, s.view.negative_levels.factor)
	if len(s.xfloatp) != 0:
		banner = banner + "\nX scale: %fppm/cm  Y scale: %fppm/cm" %(s.xfloatp, s.yfloatp)
	return banner

# -----------------------------------------------------------------------------
#
  def plot_2D(self, path):

	## Get the selections from the input window 
	s = self.get_selections()

	mspec = sputil.name_to_spectrum(s.view.spectrum.name, self.session)
	axis_order = s.view.axis_order
	xdim = s.view.axis_order[0]
	ydim = s.view.axis_order[1]
	Savedata = open(mspec.save_path).readlines()
	for line in open(mspec.save_path).readlines():
		line = line.rstrip()
		if 'ornament.label.size' in line:
			labelsize = float(line.split()[-1])
		if 'ornament.peak.size' in line:
			peaksize = float(line.split()[-1])

	## Get aspect ratio from the view options
	aspect = s.view.pixel_size[ydim]/s.view.pixel_size[xdim]
	minwidth = 2.5
	pdf = PdfPages(path)

	if len(s.xmajor) != 0:
		xpres = float(s.xmajor)
	if len(s.xmajor) == 0:
		xpres = self.get_tick_pres(s.xmax, s.xmin)
	if len(s.xmajor) != 0:
		ypres = float(s.ymajor)
	if len(s.xmajor) == 0:
		ypres = self.get_tick_pres(s.ymax, s.ymin)
	fig_w, fig_h, xppmin, yppmin = self.Calc_Figure_size( minwidth, xpres, ypres)

	scale = (mspec.spectrum_width[xdim]/xppmin)/(mspec.data_size[0]/72)
	label_size = labelsize * scale
	peak_size = peaksize *scale
	if label_size > 10:
		scale = (mspec.spectrum_width[ydim]/yppmin)/(mspec.data_size[1]/72)
		label_size = labelsize * scale
	print 'Figure size = %f, %f' %(fig_w, fig_h)
	fig=plt.figure(figsize=(fig_w, fig_h))
	ax = fig.add_subplot(111)

	## Create a list of spectra to be plotted 
	plot_list = [s.view.name]
	if s.view.name in self.overlays.keys():
		plot_list.extend(self.overlays[s.view.name])

	for view_name in plot_list:
		## Get spectrum  and view object using name 
		view = sputil.name_to_view(view_name, self.session)
		spec = sputil.name_to_spectrum(view.spectrum.name, self.session)
		if s.view.spectrum.nuclei[ydim] != view.spectrum.nuclei[ydim] or s.view.spectrum.nuclei[xdim] != view.spectrum.nuclei[xdim]:
			tkMessageBox.showinfo('Input Error', "Attempting to overlay %s spectrum on to %s spectrum " %(view.spectrum.nuclei, s.view.spectrum.nuclei))
			return
		## Set the contour levels 
		poscon = view.positive_levels
		negcon = view.negative_levels
		pcl = [poscon.lowest * poscon.factor ** l for l in range(poscon.levels)]
		ncl = [negcon.lowest * (negcon.factor ** l) for l in range(negcon.levels)]
		## Reverse the order of negative contour levels because values must be in increasing order for contour plots 
		ncl = ncl[::-1]

		## Retrieve ucsf data using and apply the offset used in sparky 
		dic, data = ng.read(view.spectrum.data_path)
		offset = spec.scale_offset
		for i in range(len(offset)):
			dic['w'+str(1+i)]['xmtr_freq']= dic['w'+str(1+i)]['xmtr_freq']+ offset[i]

		## Get index specifying x and y dimensions
		xdim = view.axis_order[0]
		ydim = view.axis_order[1]

		## Retrieve X axis data and shift values 
		uc_x = ng.make_uc(dic, data, dim=xdim)
		uc_y = ng.make_uc(dic, data, dim=ydim)

		min_x, max_x, min_y, max_y = self.get_xyppm( s.xmin, s.xmax, s.ymin, s.ymax, uc_x, uc_y)

		ppm_x = uc_x.ppm_scale()[min_x:max_x+1]
		ppm_y = uc_y.ppm_scale()[min_y:max_y+1]
		## Extract region to be plotted from data 
		region = eval(strip_dic[view.axis_order])
		region_x, region_y = np.meshgrid(ppm_x, ppm_y)
		if poscon.levels != 0:
			if poscon.color not in COLORS.keys():
				ax.contour(region_x, region_y, region, pcl, colors = self.gen_cm(poscon.levels, poscon.color), norm=mpl.colors.Normalize(vmin=np.min(data), vmax=poscon.lowest*poscon.levels), linewidths=0.1)
			else:
				ax.contour(region_x, region_y, region, pcl, colors=COLORS[poscon.color], linewidths=0.1)
		if negcon.levels != 0:
			if negcon.color not in COLORS.keys():
				 ax.contour(region_x, region_y, region, ncl, colors =self.gen_cm(negcon.levels, negcon.color), norm=mpl.colors.Normalize(vmin=negcon.lowest*negcon.levels, vmax=np.max(data)), linewidths=0.1, linestyles='solid')
			else:
				ax.contour(region_x, region_y, region, ncl, colors=COLORS[negcon.color], linewidths=0.1, linestyles='solid')
	if s.ls == False:
		for i in range(len(Savedata)):
			line = Savedata[i].rstrip()
			if 'type label' in line:
				label = Savedata[i+5].rstrip().split()[-1]
				if s.bl == True:
					lcolor = 'black'
				if s.bl == False:
					lcolor = COLORS[Savedata[i+1].rstrip()[12:].replace('white', 'black')]
				lxy = [float(val) for val in Savedata[i+6].split()[lpd[axis_order]].split(',')]
				lpos = [float(Savedata[i+4].rstrip().split()[1:][xdim]), float(Savedata[i+4].rstrip().split()[1:][ydim])]
				if s.xmin < lxy[0]  and lxy[0] < s.xmax and s.ymin < lxy[1]  and lxy[1] < s.ymax:
					ax.annotate(label, xy=lpos, xycoords='data', xytext=lxy, textcoords='data', fontsize=label_size, ha='center', va='center', arrowprops=dict(arrowstyle= 'wedge', fc=lcolor, ec="none", shrinkA = 0.1, shrinkB = 0.01), bbox=dict(boxstyle="square, pad=0.01", fc='none', ec='none') , color= lcolor)
	if s.ps == False:
		for peak in mspec.peak_list():
			pcolor = peak.color.replace('white', 'black')
			if s.bl == True:
				pcolor = 'black'
			posx, posy = peak.frequency[xdim], peak.frequency[ydim]
			if s.xmin < posx  and posx < s.xmax and s.ymin < posy  and posy < s.ymax:
				ax.plot(posx,posy, marker='x',color = COLORS[pcolor], markersize = peaksize)

	ax.invert_xaxis()
	ax.invert_yaxis()
	ax.set_aspect(1.0/aspect)
	ax.set_ylim([s.ymax, s.ymin])
	ax.set_xlim([s.xmax, s.xmin])
	ax.set_ylabel(s.view.spectrum.nuclei[ydim]+' (ppm)')
	ax.set_xlabel(s.view.spectrum.nuclei[xdim]+' (ppm)')
	if len(s.xfloatp) != 0:
		xpres = '%.'+ s.xfloatp +'f'
		ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(xpres))
	if len(s.yfloatp) !=0:
		ypres = '%.'+ s.yfloatp +'f'
		ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(ypres))
	if s.mt == False:
		ax.minorticks_on()
	if len(s.xmajor) != 0:
		ax.xaxis.set_major_locator(ticker.MultipleLocator(float(s.xmajor)))
	if len(s.ymajor) != 0:
		ax.yaxis.set_major_locator(ticker.MultipleLocator(float(s.ymajor)))
	ax.yaxis.set_ticks_position('left')
	ax.xaxis.set_ticks_position('bottom')
	ax.set_clip_on(False)
	plt.tight_layout()
	pdf.savefig(facecolor = 'none', edgcolor = 'none', transparent=True)
	plt.close()

	if s.banner == True:
		fig = plt.figure(figsize=(7.0, 1.5))
		ay = fig.add_subplot(111)
		ay.text(0.05, 0.95, self.generate_banner(), va='top', ha='left', fontsize = 12)
		plt.axis('off')
		pdf.savefig(facecolor = 'none', edgcolor = 'none', transparent=True)
		plt.close()
	pdf.close()
# -----------------------------------------------------------------------------
#
  def plot_3D(self, path):

	## Get the selections from the input window 
	s = self.get_selections()

	mspec = sputil.name_to_spectrum(s.view.spectrum.name, self.session)
	axis_order = s.view.axis_order
	## Get index specifying x and y dimensions
	xdim = axis_order[0]
	ydim = axis_order[1]
	zdim = axis_order[2]
	z_plane = float(s.view.center[zdim])
	Savedata = open(s.view.spectrum.save_path).readlines()
	for i in range(len(Savedata)):
		line = Savedata[i].rstrip()
		if 'ornament.label.size' in line:
			labelsize = float(line.split()[-1])
		if 'ornament.peak.size' in line:
			peaksize = float(line.split()[-1])

	## Get aspect ratio from the view options
	aspect = s.view.pixel_size[ydim]/s.view.pixel_size[xdim]
	print 'aspect = %f' %aspect
	pdf = PdfPages(path)
	minwidth = 0.6

	if len(s.xmajor) != 0:
		xpres = float(s.xmajor)
	if len(s.xmajor) == 0:
		xpres = self.get_tick_pres(s.xmax, s.xmin)
	if len(s.xmajor) != 0:
		ypres = float(s.ymajor)
	if len(s.xmajor) == 0:
		ypres = self.get_tick_pres(s.ymax, s.ymin)

	fig_w, fig_h, xppmin, yppmin  = self.Calc_Figure_size(minwidth, xpres, ypres)
	scale = (s.view.spectrum.spectrum_width[xdim]/xppmin)/(s.view.spectrum.data_size[0]/72.0)
	label_size = labelsize * scale
	if label_size > 10:
		scale = (mspec.spectrum_width[ydim]/yppmin)/(mspec.data_size[1]/72)
		label_size = labelsize * scale
	print 'fig_H orig = %f ' %fig_h
	fig_h = float(fig_h) + 0.33
	print 'Figure size = %f, %f' %(fig_w, fig_h)
	fig=plt.figure(figsize=(fig_w, fig_h))
	ax = fig.add_subplot(111)

	## Create a list of spectra to be plotted 
	plot_list = [s.view.name]
	if s.view.name in self.overlays.keys():
		plot_list.extend(self.overlays[s.view.name])

	for view_name in plot_list:
		## Get spectrum  and view object using name 
		view = sputil.name_to_view(view_name, self.session)
		spec = sputil.name_to_spectrum(view.spectrum.name, self.session)
		if s.view.spectrum.nuclei[ydim] != view.spectrum.nuclei[ydim] or s.view.spectrum.nuclei[xdim] != view.spectrum.nuclei[xdim]:
			tkMessageBox.showinfo('Input Error', "Attempting to overlay %s spectrum on to %s spectrum " %(view.spectrum.nuclei, s.view.spectrum.nuclei))
			return
		## Get and Set the contour levels 
		poscon = view.positive_levels
		negcon = view.negative_levels
		# negcon_first = negcon.lowest /(negcon.factor ** negcon.levels)
		pcl = [poscon.lowest * poscon.factor ** l for l in range(poscon.levels)]
		ncl = [negcon.lowest * (negcon.factor ** l) for l in range(negcon.levels)]
		ncl = ncl[::-1]
		## Retrieve data using nmrglue 
		dic, data = ng.read(view.spectrum.data_path)
		## Shift each dimension by the scale_offset value 
		offset = spec.scale_offset
		for i in range(len(offset)):
			dic['w'+str(1+i)]['xmtr_freq']= dic['w'+str(1+i)]['xmtr_freq']+ offset[i]
		## Get index specifying x and y dimensions
		xdim = view.axis_order[0]
		ydim = view.axis_order[1]
		zdim = view.axis_order[2]
		# make unit conversion objects for each axis of each spectrum
		uc_x = ng.make_uc(dic, data, xdim)
		uc_y = ng.make_uc(dic, data, ydim)
		uc_z = ng.make_uc(dic, data, zdim)
		# find limits in units of points
		z_idx = uc_z(z_plane, "ppm")

		min_x, max_x, min_y, max_y = self.get_xyppm( s.xmin, s.xmax, s.ymin, s.ymax, uc_x, uc_y)

		# extract strip, remember axis limits must be in original axis order of 0, 1, 2
		strip_s1 = eval(strip_dic[view.axis_order])
		# determine ppm limits of contour plot
		strip_ppm_x = uc_x.ppm_scale()[min_x:max_x+1]
		strip_ppm_y = uc_y.ppm_scale()[min_y:max_y+1]
		strip_x, strip_y = np.meshgrid(strip_ppm_x, strip_ppm_y)
		if poscon.levels != 0:
			if poscon.color not in COLORS.keys():
				ax.contour(strip_x, strip_y, strip_s1, pcl, colors= self.gen_cm(poscon.levels, poscon.color), norm=mpl.colors.Normalize(vmin=np.min(strip_s1), vmax=poscon.lowest*poscon.levels) , linewidths=0.1)
			else:
				ax.contour(strip_x, strip_y, strip_s1, pcl, colors= COLORS[poscon.color], linewidths=0.1)
		if negcon.levels != 0:
			if negcon.color not in COLORS.keys():
				ax.contour(strip_x, strip_y, strip_s1, ncl, colors= self.gen_cm(negcon.levels, negcon.color), norm=mpl.colors.Normalize(vmin=negcon.lowest*negcon.levels, vmax=np.max(strip_s1)), linewidths=0.1, linestyles='solid')
			else:
				ax.contour(strip_x, strip_y, strip_s1, ncl, colors=COLORS[negcon.color], linewidths=0.1, linestyles='solid')
	if s.ls == False:
		for i in range(len(Savedata)):
			line = Savedata[i].rstrip()
			if 'type label' in line:
				label = Savedata[i+5].rstrip().split()[-1]
				if s.bl == True:
					lcolor = 'black'
				if s.bl == False:
					lcolor = COLORS[Savedata[i+1].rstrip()[12:].replace('white', 'black')]
				lxy = [float(val) for val in Savedata[i+6].split()[lpd[axis_order]].split(',')]
				lpos = [float(Savedata[i+4].split()[1:][xdim]), float(Savedata[i+4].split()[1:][ydim])]
				if abs(z_plane - float(Savedata[i+4].split()[1:][zdim])) <= s.view.visible_depth[zdim]:
					if s.xmin < lxy[0]  and lxy[0] < s.xmax and s.ymin < lxy[1]  and lxy[1] < s.ymax:
						ax.annotate(label, xy=lpos, xycoords='data', xytext=lxy, textcoords='data', fontsize=label_size, ha='center', va='center', arrowprops=dict(arrowstyle= 'wedge', fc=lcolor, ec="none", shrinkA = 0.1, shrinkB = 0.01), bbox=dict(boxstyle="square, pad=0.01", fc='none', ec='none') , color= lcolor)
	# mytext = "%s: %.3f" %( Nuc_format[s.view.spectrum.nuclei[zdim]], round(z_plane, 3))
	# # ax.text(0.05, 0.975, mytext, verticalalignment='center', fontsize=8, transform=ax.transAxes)
	# ax.set_title(mytext, fontsize = 8)
	if s.ps == False:
		for peak in mspec.peak_list():
			pcolor = peak.color.replace('white', 'black')
			if s.bl == True:
				pcolor = 'black'
			posx, posy,posz = peak.frequency[xdim], peak.frequency[ydim], peak.frequency[zdim]
			if abs(z_plane - posz) <= s.view.visible_depth[zdim]:
				if s.xmin < posx  and posx < s.xmax and s.ymin < posy  and posy < s.ymax:
					ax.plot(posx,posy, marker='x',color = COLORS[pcolor], markersize = peaksize)

	ax.invert_xaxis()
	ax.invert_yaxis()
	# ax.set_aspect(aspect)
	ax.set_ylim([s.ymax, s.ymin])
	ax.set_xlim([s.xmax, s.xmin])
	ax.set_ylabel(s.view.spectrum.nuclei[ydim]+' (ppm)')
	ax.set_xlabel(s.view.spectrum.nuclei[xdim]+' (ppm)')
	if len(s.xfloatp) != 0:
		xpres = '%.'+ s.xfloatp +'f'
		ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(xpres))
	if len(s.yfloatp) !=0:
		ypres = '%.'+ s.yfloatp +'f'
		ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(ypres))
	if s.mt == False:
		ax.minorticks_on()
	if len(s.xmajor) != 0:
		ax.xaxis.set_major_locator(ticker.MultipleLocator(float(s.xmajor)))
	if len(s.ymajor) != 0:
		ax.yaxis.set_major_locator(ticker.MultipleLocator(float(s.ymajor)))
	ax.yaxis.set_ticks_position('left')
	ax.xaxis.set_ticks_position('bottom')
	ax.set_clip_on(False)
	plt.tight_layout()
	pdf.savefig(facecolor = 'none', edgcolor = 'none', transparent=True)
	plt.close()

	if s.banner == True:
		fig = plt.figure(figsize=(7.0, 1.5))
		ay = fig.add_subplot(111)
		ay.text(0.05, 0.95, self.generate_banner(), va='top', ha='left', fontsize = 12)
		plt.axis('off')
		pdf.savefig(facecolor = 'none', edgcolor = 'none', transparent=True)
		plt.close()
	pdf.close()
# -----------------------------------------------------------------------------
#
  def strip_plots(self, path, strips):

	print strips
	## Get the selections from the input window 
	s = self.get_selections()
	axis_order = s.view.axis_order
	xdim = axis_order[0]
	ydim = axis_order[1]
	zdim = axis_order[2]
	# print 'xdim %d ydim %d zdim %d' %(xdim, ydim, zdim)
	# print 'xdim nuc %s ydim nuc %s zdim nuc %s' %(s.view.spectrum.nuclei[xdim], s.view.spectrum.nuclei[ydim], s.view.spectrum.nuclei[zdim])
	refspec = strips[0].spectrum
	spXdim = refspec.nuclei.index(s.view.spectrum.nuclei[xdim])
	spZdim = refspec.nuclei.index(s.view.spectrum.nuclei[zdim])
	# print 'ref spectrums xdim nuc = %s zdim nuc = %s' %(refspec.nuclei[spXdim],refspec.nuclei[spZdim])
	### Get contour level setting
	poscon = s.view.positive_levels
	negcon = s.view.negative_levels
	# negcon_first = negcon.lowest /(negcon.factor ** negcon.levels)
	pcl = [poscon.lowest * poscon.factor ** l for l in range(poscon.levels)]
	ncl = [negcon.lowest * (negcon.factor ** l) for l in range(negcon.levels)]
	ncl = ncl[::-1]
	mspec = sputil.name_to_spectrum(s.view.spectrum.name, self.session)
	## Retrieve data using nmrglue 
	dic, data = ng.read(s.view.spectrum.data_path)
	## Shift each dimension by the scale_offset value 
	offset = s.view.spectrum.scale_offset
	for i in range(len(offset)):
		dic['w'+str(1+i)]['xmtr_freq']= dic['w'+str(1+i)]['xmtr_freq']+ offset[i]
	# make unit conversion objects for each axis of each spectrum
	uc_x = ng.make_uc(dic, data, xdim)
	uc_y = ng.make_uc(dic, data, ydim)
	uc_z = ng.make_uc(dic, data, zdim)

	Savedata = open(s.view.spectrum.save_path).readlines()
	# print s.view.spectrum.data_path
	for i in range(len(Savedata)):
		line = Savedata[i].rstrip()
		if 'ornament.label.size' in line:
			labelsize = float(line.split()[-1])
		if 'ornament.peak.size' in line:
			peaksize = float(line.split()[-1])

	## Get aspect ratio from the view options
	aspect = s.view.pixel_size[ydim]/s.view.pixel_size[xdim]
	pdf = PdfPages(path)
	if len(s.xmajor) != 0:
		xpres = float(s.xmajor)
	if len(s.xmajor) == 0:
		xpres = self.get_tick_pres(s.xmax, s.xmin)
	if len(s.xmajor) != 0:
		ypres = float(s.ymajor)
	if len(s.xmajor) == 0:
		ypres = self.get_tick_pres(s.ymax, s.ymin)
	minwidth = 0.6
	fig_w, fig_h, xppmin, yppmin = self.Calc_Strip_size(s.xmin, s.xmax, s.ymin, s.ymax, aspect, minwidth, xpres, ypres, s.view.spectrum.nuclei[xdim], len(strips))
	scale = (s.view.spectrum.spectrum_width[xdim]/xppmin)/(s.view.spectrum.data_size[0]/72.0)
	label_size = labelsize * scale
	if label_size > 10:
		scale = (s.view.spectrum.spectrum_width[ydim]/yppmin)/(s.view.spectrum.data_size[1]/72)
		label_size = labelsize * scale
	print "figure size = %f, %f " %(fig_w, fig_h)
	fig = plt.figure(figsize=(fig_w,fig_h))
	# fig, axes = plt.subplots(1, len(strips), figsize=(fxsz, ysz), sharex=False, sharey=True)
	# for x, ax  in zip(range(len(strips)), axes.flatten()):
	for x in range(len(strips)):
		ax = plt.subplot(1,len(strips), x+1)
		plt.subplots_adjust(wspace = 0.001)
		strip = strips[x]
		z_plane = strip.frequency[spZdim]

		xwidth = (s.xmax - s.xmin) / 2.0 
		# find limits in units of points
		z_idx = uc_z(strip.frequency[spZdim], "ppm")
		### Get the desired x region, and make adjustments if the view area is outside of the spectrum limits 
		spxmin = strip.frequency[spXdim] - xwidth
		spxmax = strip.frequency[spXdim] + xwidth

		min_x, max_x, min_y, max_y = self.get_xyppm( spxmin, spxmax, s.ymin, s.ymax, uc_x, uc_y)

		# extract strip, remember axis limits must be in original axis order of 0, 1, 2
		strip_s1 = eval(strip_dic[s.view.axis_order])
		# determine ppm limits of contour plot
		strip_ppm_x = uc_x.ppm_scale()[min_x:max_x+1]
		strip_ppm_y = uc_y.ppm_scale()[min_y:max_y+1]
		strip_x, strip_y = np.meshgrid(strip_ppm_x, strip_ppm_y)
		if poscon.levels != 0:
			if poscon.color not in COLORS.keys():
				ax.contour(strip_x, strip_y, strip_s1, pcl, colors= self.gen_cm(poscon.levels, poscon.color), norm=mpl.colors.Normalize(vmin=np.min(strip_s1), vmax=poscon.lowest*poscon.levels) , linewidths=0.1)
			else:
				ax.contour(strip_x, strip_y, strip_s1, pcl, colors= COLORS[poscon.color], linewidths=0.1)
		if negcon.levels != 0:
			if negcon.color not in COLORS.keys():
				ax.contour(strip_x, strip_y, strip_s1, ncl, colors= self.gen_cm(negcon.levels, negcon.color), norm=mpl.colors.Normalize(vmin=negcon.lowest*negcon.levels, vmax=np.max(strip_s1)), linewidths=0.1, linestyles='solid')
			else:
				ax.contour(strip_x, strip_y, strip_s1, ncl, colors=COLORS[negcon.color], linewidths=0.1, linestyles='solid')
		if s.ls == False:
			for i in range(len(Savedata)):
				line = Savedata[i].rstrip()
				if 'type label' in line:
					label = Savedata[i+5].rstrip().split()[-1]
					if s.bl == True:
						lcolor = 'black'
					if s.bl == False:
						lcolor = COLORS[Savedata[i+1].rstrip()[12:].replace('white', 'black')]
					lxy = [float(val) for val in Savedata[i+6].split()[lpd[axis_order]].split(',')]
					lpos = [float(Savedata[i+4].split()[1:][xdim]), float(Savedata[i+4].split()[1:][ydim])]
					if abs(z_plane - float(Savedata[i+4].split()[1:][zdim])) <= s.view.visible_depth[zdim]:
						if spxmin < lpos[0]  and lpos[0] < spxmax and s.ymin < lpos[1]  and lpos[1] < s.ymax:
							ax.annotate(label, xy=lpos, xycoords='data', xytext=lxy, textcoords='data', fontsize=label_size, ha='center', va='center', arrowprops=dict(arrowstyle= 'wedge', fc=lcolor, ec="none", shrinkA = 0.1, shrinkB = 0.01), bbox=dict(boxstyle="square, pad=0.01", fc='none', ec='none') , color= lcolor)
		if s.ps == False:
			for peak in mspec.peak_list():
				pcolor = peak.color.replace('white', 'black')
				if s.bl == True:
					pcolor = 'black'
				posx, posy,posz = peak.frequency[xdim], peak.frequency[ydim], peak.frequency[zdim]
				if abs(z_plane - posz) <= s.view.visible_depth[zdim]:
					if spxmin < posx  and posx < spxmax and s.ymin < posy  and posy < s.ymax:
						ax.plot(posx,posy, marker='x',color = COLORS[pcolor], markersize = peaksize)
		if strip.is_assigned == 1:
			ax.set_title(strip.resonances()[spZdim].name,fontsize=8)
		if strip.is_assigned == 0:
			mytext = "%4.3f \n %4.3f" %(strip.frequency[0], strip.frequency[1])
			ax.set_title(mytext,fontsize=8)
		# mytext = "%s: %.3f" %( Nuc_format[s.view.spectrum.nuclei[zdim]], round(z_plane, 3))
		# ax.text(0.05, 0.975, mytext, verticalalignment='center', fontsize=8, transform=ax.transAxes)
		ax.invert_xaxis()
		ax.invert_yaxis()
		ax.set_ylim([s.ymax, s.ymin])
		ax.set_xlim([spxmax, spxmin])
		# ax.xaxis.set_ticks_position('bottom')
		ax.set_clip_on(False)
		if s.strip_x == True:
			ax.tick_params(axis ='x', bottom=False, labelbottom=False)
			ax.tick_params(axis='x', which='minor', bottom=False)
			ax.set_xlabel(strip.frequency[spXdim],fontsize = 8)
		if s.add_vline == True:
			ax.axvline(x=strip.frequency[spXdim], color = [0.5,0.5,0.5], alpha = 0.5)
		# if len(s.xmajor) == 0:
		#     xmajor = -(-xwidth)/2.0
		#     print 'xmajor %f' %xmajor
		#     ax.xaxis.set_major_locator(ticker.MultipleLocator(xmajor))

		if xwidth <= 0.5:
			ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
		if xwidth > 0.5 and xwidth <= 5.0:
			ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
		if xwidth > 5.0:
			ax.xaxis.set_major_locator(ticker.MultipleLocator(2.5))
		if len(s.xmajor) != 0:
			ax.xaxis.set_major_locator(ticker.MultipleLocator(float(s.xmajor)))
		if len(s.xfloatp) != 0:
			xpres = '%.'+ s.xfloatp +'f'
			ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(xpres))
		if s.mt == False:
			ax.minorticks_on()
		if x == 0 :
			ax.yaxis.set_ticks_position('left')
			ax.set_ylabel(s.view.spectrum.nuclei[ydim]+' (ppm)')
			ax.tick_params(axis ='y', labelleft=True)

			if len(s.ymajor) != 0:
				ax.yaxis.set_major_locator(ticker.MultipleLocator(float(s.ymajor)))
			if len(s.yfloatp) !=0:
				ypres = '%.'+ s.yfloatp +'f'
				ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(ypres))
		if x !=0 :
			ax.tick_params(axis='y', which='minor', left=False, bottom=False)
			ax.tick_params(axis='y', top=False, labelleft=False, left=False, right=False)
	fig.add_subplot(111, frame_on=False)
	plt.tick_params(labelcolor="none", bottom=False, left=False)
	plt.xlabel(s.view.spectrum.nuclei[xdim]+' (ppm)', ha='center')
	plt.tight_layout(pad = 0.01, w_pad = 0.01, h_pad = 0.01)
	fig.tight_layout(pad = 0.01)
	pdf.savefig(facecolor = 'none', edgcolor = 'none', transparent=True)
	plt.close()

	if s.banner == True:
		fig = plt.figure(figsize=(7.0, 1.5))
		ay = fig.add_subplot(111)
		ay.text(0.05, 0.95, self.generate_banner(), va='top', ha='left', fontsize = 12)
		plt.axis('off')
		pdf.savefig(facecolor = 'none', edgcolor = 'none', transparent=True)
		plt.close()

	pdf.close()
# -----------------------------------------------------------------------------
#
  # def plot_4D(self, path):

  #   ## Get the selections from the input window 
  #   s = self.get_selections()

  #   mspec = sputil.name_to_spectrum(s.view.spectrum.name, self.session)
  #   axis_order = s.view.axis_order
  #   xdim = axis_order[0]
  #   ydim = axis_order[1]
  #   zdim = axis_order[2]
  #   wdim = axis_order[3]
  #   print 'xdim %d ydim %d zdim %d wdim %d' %(xdim, ydim, zdim, wdim)
  #   z_plane = float(s.view.center[zdim])
  #   w_plane = float(s.view.center[wdim])
  #   Savedata = open(mspec.save_path).readlines()
  #   for i in range(len(Savedata)):
  #       line = Savedata[i].rstrip()
  #       if 'ornament.label.size' in line:
  #           labelsize = float(line.split()[-1])
  #   ## Get aspect ratio from the view options
  #   aspect = s.view.pixel_size[ydim]/s.view.pixel_size[xdim]

  #   pdf = PdfPages(path)
  #   xppmin = xscal_dic[s.view.spectrum.nuclei[xdim]]
  #   print xppmin
  #   xsz = ((s.xmax - s.xmin) / xppmin)
  #   if xsz < 0.5: xsz = 0.5
  #   xppmin = (s.xmax-s.xmin)/(xsz-1)
  #   yppmin = xppmin * aspect
  #   ysz = 1+ ((s.ymax - s.ymin)/ yppmin)
  #   scale = (mspec.spectrum_width[xdim]/xppmin)/(mspec.data_size[0]/72.0)
  #   label_size = labelsize * scale
  #   if label_size > 10:
  #       scale = (mspec.spectrum_width[ydim]/yppmin)/(mspec.data_size[1]/72)
  #       label_size = labelsize * scale
  #   fig=plt.figure(figsize=(xsz+1, ysz))
  #   ax = fig.add_subplot(111)

  #   ## Create a list of spectra to be plotted 
  #   plot_list = [s.view.name]
  #   if s.view.name in self.overlays.keys():
  #       plot_list.extend(self.overlays[s.view.name])

  #   for view_name in plot_list:
  #       ## Get spectrum  and view object using name 
  #       view = sputil.name_to_view(view_name, self.session)
  #       spec = sputil.name_to_spectrum(view.spectrum.name, self.session)
  #       if s.view.spectrum.nuclei[ydim] != view.spectrum.nuclei[ydim] or s.view.spectrum.nuclei[xdim] != view.spectrum.nuclei[xdim]:
  #           tkMessageBox.showinfo('Input Error', "Attempting to overlay %s spectrum on to %s spectrum " %(view.spectrum.nuclei, s.view.spectrum.nuclei))
  #           return
  #       ## Get and Set the contour levels 
  #       poscon = view.positive_levels
  #       negcon = view.negative_levels
  #       # negcon_first = negcon.lowest /(negcon.factor ** negcon.levels)
  #       pcl = [poscon.lowest * poscon.factor ** l for l in range(poscon.levels)]
  #       ncl = [negcon.lowest * (negcon.factor ** l) for l in range(negcon.levels)]
  #       ncl = ncl[::-1]
  #       ## Retreave data using nmrglue 
  #       dic, data = ng.read(view.spectrum.data_path)

  #       ## Shift each dimension by the scale_offset value 
  #       offset = spec.scale_offset
  #       for i in range(len(offset)):
  #           dic['w'+str(1+i)]['xmtr_freq']= dic['w'+str(1+i)]['xmtr_freq']+ offset[i]

  #       ## Get index specifiying x and y dimensions
  #       xdim = view.axis_order[0]
  #       ydim = view.axis_order[1]
  #       zdim = view.axis_order[2]
  #       wdim = view.axis_order[3]

  #       # make unit conversion objects for each axis of each spectrum
  #       uc_x = ng.make_uc(dic, data, xdim)
  #       uc_y = ng.make_uc(dic, data, ydim)
  #       uc_z = ng.make_uc(dic, data, zdim)
  #       uc_w = ng.make_uc(dic, data, wdim)

  #       # find limits in units of points
  #       z_idx = uc_z(z_plane, "ppm")
  #       w_idx = uc_w(w_plane, "ppm")

  #       min_x, max_x, min_y, max_y = self.get_xyppm( s.xmin, s.xmax, s.ymin, s.ymax, uc_x, uc_y)


  #       # extract strip, remember axis lismits must be in orignal axis order of 0, 1, 2
  #       strip_s1 = eval(strip_dic[view.axis_order])

  #       # determine ppm limits of contour plot
  #       strip_ppm_x = uc_x.ppm_scale()[min_x:max_x+1]
  #       strip_ppm_y = uc_y.ppm_scale()[min_y:max_y+1]
  #       strip_x, strip_y = np.meshgrid(strip_ppm_x, strip_ppm_y)

  #       if poscon.levels != 0:
  #           if poscon.color not in COLORS.keys():
  #               ax.contour(strip_x, strip_y, strip_s1, pcl, colors=self.gen_cm(poscon.levels, poscon.color), norm=mpl.colors.Normalize(vmin=np.min(strip_s1), vmax=poscon.lowest*poscon.levels), extent=(ppm_x_0, ppm_x_1, ppm_y_0, ppm_y_1), linewidths=0.1)
  #           else:
  #               ax.contour(strip_x, strip_y, strip_s1, pcl, colors= COLORS[poscon.color], extent=(ppm_x_0, ppm_x_1, ppm_y_0, ppm_y_1), linewidths=0.1)
  #       if negcon.levels != 0:
  #           if negcon.color not in COLORS.keys():
  #               ax.contour(strip_x, strip_y, strip_s1, ncl, colors=self.gen_cm(negcon.levels, negcon.color), norm=mpl.colors.Normalize(vmin=negcon.lowest*negcon.levels, vmax=np.max(strip_s1)), extent=(ppm_x_0, ppm_x_1, ppm_y_0, ppm_y_1), linewidths=0.1, linestyles='solid')
  #           else:
  #               ax.contour(strip_x, strip_y, strip_s1, ncl, colors=COLORS[negcon.color], extent=(ppm_x_0, ppm_x_1, ppm_y_0, ppm_y_1), linewidths=0.1, linestyles='solid')
  #   if s.ls == False:
  #       for i in range(len(Savedata)):
  #           line = Savedata[i].rstrip()
  #           if 'type label' in line:
  #               label = Savedata[i+5].rstrip().split()[-1]
  #               if s.bl == True:
  #                   lcolor = 'black'
  #               if s.bl == False:
  #                   lcolor = COLORS[Savedata[i+1].rstrip()[12:].replace('white', 'black')]
  #               lxy = [float(val) for val in Savedata[i+6].split()[lpd[axis_order]].split(',')]
  #               lpos = [float(Savedata[i+4].split()[1:][xdim]), float(Savedata[i+4].split()[1:][ydim])]
  #               if abs(z_plane - float(Savedata[i+4].split()[1:][zdim])) < s.view.visible_depth[zdim]:
  #                   if s.xmin < lxy[0]  and lxy[0] < s.xmax and s.ymin < lxy[1]  and lxy[1] < s.ymax:
  #                       ax.annotate(label, xy=lpos, xycoords='data', xytext=lxy, textcoords='data', fontsize=label_size, ha='center', va='center', arrowprops=dict(arrowstyle= 'wedge', fc=lcolor, ec="none", shrinkA = 0.1, shrinkB = 0.01), bbox=dict(boxstyle="square, pad=0.01", fc='none', ec='none') , color= lcolor)
  #   mytext = "%s: %.3f" %( Nuc_format[s.view.spectrum.nuclei[zdim]], round(z_plane, 3))
  #   ax.text(0.05, 0.975, mytext, verticalalignment='center', fontsize=8, transform=ax.transAxes)
  #   ax.invert_xaxis()
  #   ax.invert_yaxis()
  #   ax.set_ylim([s.ymax, s.ymin])
  #   ax.set_xlim([s.xmax, s.xmin])
  #   ax.set_ylabel(s.view.spectrum.nuclei[ydim]+' (ppm)')
  #   ax.set_xlabel(s.view.spectrum.nuclei[xdim]+' (ppm)')
  #   if len(s.xfloatp) != 0:
  #       xpres = '%.'+ s.xfloatp +'f'
  #       ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(xpres))
  #   if len(s.yfloatp) !=0:
  #       ypres = '%.'+ s.yfloatp +'f'
  #       ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(ypres))
  #   if s.mt == False:
  #       ax.minorticks_on()
  #   if len(s.xmajor) != 0:
  #       ax.xaxis.set_major_locator(ticker.MultipleLocator(float(s.xmajor)))
  #   if len(s.ymajor) != 0:
  #       ax.yaxis.set_major_locator(ticker.MultipleLocator(float(s.ymajor)))
  #   ax.yaxis.set_ticks_position('left')
  #   ax.xaxis.set_ticks_position('bottom')
  #   ax.set_clip_on(False)
  #   plt.tight_layout(pad = 0.01)
  #   pdf.savefig(facecolor = 'none', edgcolor = 'none', transparent=True)
  #   plt.close()

  #   if s.banner == True:
  #       fig = plt.figure(figsize=(7.0, 1.5))
  #       ay = fig.add_subplot(111)
  #       ay.text(0.05, 0.95, self.generate_banner(), va='top', ha='left', fontsize = 12)
  #       plt.axis('off')
  #       pdf.savefig(facecolor = 'none', edgcolor = 'none', transparent=True)
  #       plt.close()
  #   pdf.close()

# -----------------------------------------------------------------------------
#
  def gen_cm(self, nlev, color):
	cmap_dict = {'red-blue': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'blue-red':[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], 'green-blue':[6, 7, 8, 9, 10], 'blue-green':[10, 9, 8, 7, 6], 'red-yellow':[0, 1, 2, 3, 4], 'yellow-red':[4, 3, 2, 1 ,0],
				0:'#ff0000', 1:'#ff8c00', 2:'#ffa500', 3:'#ffd700', 4:'#ffff00', 5:'#7fff00', 6:'#00ff00', 7:'#00ff00', 8:'#00ff7f', 9:'#00bfff', 10:'#0000ff'}
	icmap = cmap_dict[color]
	nc = -(-nlev/ len(icmap))
	cmap1 = []
	for x in range(nc):
	  cmap1.extend(icmap)
	cmap2 = []
	for i in sorted(cmap1[:nlev]):
	  cmap2.append(cmap_dict[i])
	if color in ['blue-red', 'blue-green', 'yellow-red']:
	  cmap2 = cmap2[::-1]
	return cmap2
# -----------------------------------------------------------------------------
#
  def get_tick_pres(self, amax, amin):
	sw = amax-amin
	if sw <= 0.25: amajor = 0.1
	if sw > 0.25 and sw <= 1.0: amajor = 0.2 
	if sw > 1.0 and sw <= 3: amajor = 0.5
	if sw > 3.0 and sw <= 6: amajor = 1
	if sw > 6.0 and sw <= 15: amajor = 2
	if sw >= 15: amajor = 5
	return amajor
# -----------------------------------------------------------------------------
#
  def Calc_Figure_size(self, minwidth, xpres, ypres):
	
	s = self.get_selections()
	xdim = s.view.axis_order[0]
	ydim = s.view.axis_order[1]
	aspect = s.view.pixel_size[ydim]/s.view.pixel_size[xdim]
	xnuc = s.view.spectrum.nuclei[xdim]

	if len(s.view.spectrum.nuclei) == 2 and s.view.spectrum.nuclei[ydim] == '13C':
	  xppmin = xscal_dic[xnuc]*1.25
	else: 
	  xppmin = xscal_dic[xnuc]

	xsz = (s.xmax-s.xmin) * xppmin
	if xsz < minwidth: xsz = minwidth
	xppmin = (s.xmax-s.xmin)/(xsz)
	yppmin = xppmin * aspect
	ysz =(s.ymax - s.ymin)/ yppmin

	xtxt = 0.07725 * len(str(np.arange(s.xmin,s.xmax,xpres)[-1]))
	if "." in str(xpres):
	  xtxt = xtxt - 0.03865

	ytxt = 0.07725 * len(str(np.arange(s.ymin,s.ymax,ypres)[-1]))
	if "." in str(ypres):
	  ytxt = ytxt - 0.03865

	fig_w = xsz + 0.23 + ytxt 
	if np.arange(s.xmin,s.xmax,xpres)[-1] == s.xmax:
	  fig_w = fig_w + xtxt / 2.0

	fig_h = ysz + 0.47
	if np.arange(s.ymin,s.ymax,ypres)[-1] == s.ymax:
	  fig_h = fig_h + 0.1643
	return fig_w, fig_h, xppmin, yppmin


  def Calc_Strip_size(self, xmin, xmax, ymin, ymax, aspect, minwidth, xpres, ypres, xnuc, nstrips):
	xppmin = xscal_dic[xnuc]
	xsz = (xmax-xmin) * xppmin
	if xsz < minwidth: xsz = minwidth
	xppmin = (xmax-xmin)/(xsz)
	yppmin = xppmin * aspect
	ysz =(ymax - ymin)/ yppmin

	xtxt = 0.07725 * len(str(np.arange(xmin,xmax,xpres)[-1]))
	if "." in str(xpres):
	  xtxt = xtxt - 0.03865

	ytxt = 0.07725 * len(str(np.arange(ymin,ymax,ypres)[-1]))
	if "." in str(ypres):
	  ytxt = ytxt - 0.03865

	fig_w = (xsz + 0.08) * nstrips + 0.23 + ytxt 
	if np.arange(xmin,xmax,xpres)[-1] == xmax:
	  fig_w = fig_w + xtxt / 2.0

	fig_h = ysz + 0.80
	if np.arange(ymin,ymax,ypres)[-1] == ymax:
	  fig_h = fig_h + 0.1643
	return fig_w, fig_h, xppmin, yppmin
# -----------------------------------------------------------------------------
#
  def get_xyppm(self, x_min, x_max, y_min, y_max, uc_x, uc_y):
	### Get the x axis limits, and adjust if out of spectrum range 
	if x_min < min(uc_x.ppm_limits()):
	  xmin = min(uc_x.ppm_limits())
	else:xmin = x_min
	if x_max > max(uc_x.ppm_limits()):
	  xmax = max(uc_x.ppm_limits())
	else:xmax = x_max
	min_x = uc_x(xmin, 'ppm')
	max_x = uc_x(xmax, 'ppm')
	if min_x > max_x:
		min_x, max_x = max_x, min_x
	
	### Get the y axis limits, and adjust if out of spectrum range 
	if y_min < min(uc_y.ppm_limits()):
	  ymin = min(uc_y.ppm_limits())
	else:ymin = y_min
	if y_max > max(uc_y.ppm_limits()):
	  ymax = max(uc_y.ppm_limits())
	else:ymax = y_max
	min_y = uc_y(ymin, 'ppm')
	max_y = uc_y(ymax, 'ppm')
	if min_y > max_y:
	  min_y, max_y = max_y, min_y

	return min_x, max_x, min_y, max_y
# -----------------------------------------------------------------------------
#
def show_dialog(session):
  sputil.the_dialog(pdf_printing_dialog, session).show_window(1)
