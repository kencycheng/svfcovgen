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
        self.line_state = 0

    def print_sheet(self):
	for sheet in self.sheets:
	    for row in range(sheet.nrows):
		if(row == 0):
                    for col in range(sheet.ncols):
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
                            self.option_col_num = col
                        elif(sheet.cell(row,col).value=="OPTION_EXP"):
                            self.option_exp_col_num = col
                    self.all_cp_cc = [];
                else:
                    label = sheet.cell(row,self.label_col_num).value
                    if (('cp_' in label)or('cc_' in label)):
                        if(self.line_state == 1 or self.line_state == 2):
			    self.cp.gen_coverpoint()
			    print(self.cp)
			self.line_state = 1
		        # finished consecutive structure
			# process old structure
			this_target = sheet.cell(row,self.target_col_num).value
			this_iff = sheet.cell(row,self.iff_col_num).value
			this_prefixs = sheet.cell(row,self.prefixs_col_num).value
			# new a coverage structure
			# print("new cov struct -"+label)
			self.cp = COVERPOINT(label, this_target, this_iff, this_prefixs)
	       	    elif('FIN' in label):
			self.line_state = 0
			self.cp.gen_coverpoint()
			print(self.cp)
		    else:
                        if(self.line_state == 1):
			    self.line_state = 2
						
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
                    if(self.line_state ==1 or self.line_state ==2):
                        option_exp = self.de_float(sheet.cell(row,self.option_exp_col_num).value)
                        if(sheet.cell(row,self.option_col_num).value !=''):
                            self.cp.add_options(sheet.cell(row,self.option_col_num).value,option_exp)

    def de_float(self,in_val):
        if(isinstance(in_val, float)):
            out = str(int(in_val))
        else:
            out = in_val 
        return out
          

    def __str__(self):
	return ("LABEL=%d, TARGET=%d, IFF=%d, BIN_NAME=%d, BIN_VAL+%d, PREFIXS=%d" % (self.label_col_num,
		        self.target_col_num,
			self.iff_col_num,
			self.bin_name_col_num,
			self.bin_val_col_num,
			self.prefixs_col_num))

fcov = FCOV(sheets)
fcov.print_sheet()
#print(fcov)
