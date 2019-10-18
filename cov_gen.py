import sys
from sv_cov import *
import xlrd

try:
    table = xlrd.open_workbook(sys.argv[1])
except:
    print('File %s does not exist' % sys.argv[1])
    exit()

sheets = table.sheets()

class FCOV:
    def __init__(self, sheets):
        self.sheets = sheets
        self.cp_line_state = 0
        self.cg_cp_info = []
    def print_sheet(self):
	for sheet in self.sheets:
            print('covergroup '+ sheet.name +';\n\n')
            print('//  put options here if required')
            cp_info = [sheet.name, 0];
	    for row in range(sheet.nrows):
                if(sheet.cell(row,0).value == '#'):
                    continue
                elif(sheet.cell(row,0).value == '^'):
                    self.parse_col_num(sheet, row)
                    self.cp_line_state = 1
                elif(self.cp_line_state >0):
                    label = sheet.cell(row,self.label_col_num).value
                    if (('cp_' in label)or('cc_' in label)):
                        if(self.cp_line_state == 2 or self.cp_line_state == 3):
			    self.cp.gen_coverpoint()
			    print(self.cp)
			self.cp_line_state = 2
                        cp_info[1] +=1
		        # finished consecutive structure
			# process old structure
			this_target = sheet.cell(row,self.target_col_num).value
			this_iff = sheet.cell(row,self.iff_col_num).value
			this_prefixs = sheet.cell(row,self.prefixs_col_num).value
			# new a coverage structure
			# print("new cov struct -"+label)
			self.cp = COVERPOINT(label, this_target, this_iff, this_prefixs)
	       	    elif('$' in sheet.cell(row,0).value):
			self.cp_line_state = 0
			self.cp.gen_coverpoint()
			print(self.cp)
		    else:
                        if(self.cp_line_state == 2):
			    self.cp_line_state = 3
                 
						
		    bin_type = sheet.cell(row,self.bin_type_col_num).value
		    bin_name = sheet.cell(row,self.bin_name_col_num).value
                    bin_val = self.de_float(sheet.cell(row,self.bin_val_col_num).value)

		    # Handle the decoding of ' character. To deal with strings like 2'b10, 32'hffff
		    bin_val = bin_val.replace(u'\u2019', u'\'').encode('ascii', 'ignore')

		    if('M_' in bin_name):	
			this_bin = PREDEF_BIN(bin_name, this_target, int(bin_val))
			self.cp.add_predef_bins(this_bin)
		    elif(bin_name !=''):						    
			if(bin_type == ''):
			    this_bin = COV_BIN(bin_name, bin_val)
			else:
			    this_bin = COV_BIN(bin_name, bin_val, bin_type)

		        self.cp.add_bins(this_bin)
                        
                    # add options to cp
                    # Options is independently to bins 
                    if(self.cp_line_state ==2 or self.cp_line_state ==3):
                        option_exp = self.de_float(sheet.cell(row,self.cp_option_exp_col_num).value)
                        if(sheet.cell(row,self.cp_option_col_num).value !=''):
                            self.cp.add_options(sheet.cell(row,self.cp_option_col_num).value,option_exp)
            self.cg_cp_info.append(cp_info)
            print('endgroup\n\n')

    def de_float(self,in_val):
        if(isinstance(in_val, float)):
            out = str(int(in_val))
        else:
            out = in_val 
        return out
  
    def parse_col_num(self, sheet, row):
        for col in range(1,sheet.ncols):
            if(sheet.cell(row,col).value=="LABEL"):
                self.label_col_num = col
            elif(sheet.cell(row,col).value=="TARGET"):
                self.target_col_num = col
            elif(sheet.cell(row,col).value=="IFF"):
                self.iff_col_num = col
            elif(sheet.cell(row,col).value=="BIN_TYPE"):
                self.bin_type_col_num = col
            elif(sheet.cell(row,col).value=="BIN_NAME"):
                self.bin_name_col_num = col
            elif(sheet.cell(row,col).value=="BIN_VAL"):
                self.bin_val_col_num = col
            elif(sheet.cell(row,col).value=="PREFIXS"):
                self.prefixs_col_num = col
            elif(sheet.cell(row,col).value=="OPTION"):
                self.cp_option_col_num = col
            elif(sheet.cell(row,col).value=="OPTION_EXP"):
                self.cp_option_exp_col_num = col
          

    def __str__(self):
        s = 'Total summary => \n'
        for cg in self.cg_cp_info:
            s = s + "covergroup %12s, %4d coverpoints" %(cg[0], cg[1]) + '\n'  
        return s

fcov = FCOV(sheets)
fcov.print_sheet()
print(fcov)
