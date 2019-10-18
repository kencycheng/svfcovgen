#
# The base classes for generating systemverilog coverage model
#
class COV_STRUCT:
    def __init__(self):
        self.cov_struct_s = []
        self.cov_bins = []
        self.options = []

    def __str__(self):
        s=""
        for lines in self.cov_struct_s:
            s = s + lines + "\n"
        return s
class COV_BIN:
    def __init__(self, bin_name, bin_val, bin_type = 'bins '):
        self.bin_name = bin_name
        self.bin_type = bin_type
        self.bin_val = bin_val.replace('0x','\'h')
        self.bin_val = self.bin_val.replace('0b','\'b')
    def __str__(self):
        with_keyword = 0
        bins_keyword = ['binsof', 'interset', 'with']
        for keyword in bins_keyword:
            if(keyword in self.bin_val):
                with_keyword = 1
                break
        if(with_keyword == 0):
            self.bin_val = '{ ' + self.bin_val + ' }'

        s =self.bin_type + ' %12s'% self.bin_name + ' = ' + self.bin_val + ';' 
        return s

class PREDEF_BIN:
    def __init__(self, bin_type, *args, **keargs):
        self.bin_type = bin_type
        self.cov_bins = []
        self.vector = []
        if(bin_type == 'M_BITWISE'):
            self.gen_bitwise(args[0], args[1])

    def gen_bitwise(self, name_prefix, bit_num):
        for i in range(bit_num):
            self.vector.append('?') 
        vector_prefix = str(bit_num)+'\'b'
        for i in range(bit_num):
            vector1 = list(self.vector)
            vector1[bit_num -1-i] = '1'
            one_bin = COV_BIN(name_prefix + str(i) + '_1', 
                              vector_prefix + ''.join(vector1) ) 
            vector1[bit_num -1-i] = '0'
            zero_bin = COV_BIN(name_prefix + str(i) + '_0', 
                              vector_prefix + ''.join(vector1) ) 
            self.cov_bins.append(one_bin)
            self.cov_bins.append(zero_bin)

class COVERPOINT(COV_STRUCT):
    def __init__(self, cp_name, target, iff='', prefix ='' ):
        self.cp_name = cp_name
        self.target = target 
        self.iff = iff
        self.prefix = prefix
        self.predef_bins= []
        COV_STRUCT.__init__(self) 

    def add_bins(self, cov_bin): 
        self.cov_bins.append(cov_bin)

    def add_options(self, option, option_exp):
        this_option = [option, option_exp]
        self.options.append(this_option)

    def add_predef_bins(self, predef_bin):
        for i in predef_bin.cov_bins:
            self.cov_bins.append(i)
    def gen_coverpoint(self): 
        line1 = self.cp_name + ':' + ' coverpoint ' + self.prefix + self.target;

        if(self.iff != ''):
            line1 = line1 + ' iff('+ self.iff + ')'
        if(len(self.cov_bins) == 0):
            line1 = line1 + ';'
        else:
            line1 = line1 + ' {'

        self.cov_struct_s.append(line1)
        # options
       

        # bins
        for option in self.options: 
            self.cov_struct_s.append('  %s = %s;'% (option[0], option[1]))

        if(len(self.cov_bins)>0):
            for ii in self.cov_bins:
                self.cov_struct_s.append('  ' + str(ii))
            self.cov_struct_s.append('} ')



class CROSS(COV_STRUCT):
    def __init__(self, cc_name, target):
        self.cp_name = cc_name
        self.target  = target
        COV_STRUCT.__init__(self) 

    def add_bins(self, cov_bin): 
        self.cov_bins.append(cov_bin)

    def gen_cross(self): 
        line1 = self.cp_name + ':' + ' cross ' + self.target;
        if(len(self.cov_bins) == 0):
            line1 = line1 + ';'
        else:
            line1 = line1 + ' {'

        self.cov_struct_s.append(line1)

        if(len(self.cov_bins)>0):
            for ii in self.cov_bins:
                self.cov_struct_s.append('  ' + str(ii))
            self.cov_struct_s.append('} ')
