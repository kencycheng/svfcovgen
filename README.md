# svfcovgen
Fucntional coverage model play an import role in constraint random simulation. It is a key metric to understand what kind of stimulus and insteresting scenario have been tested. However, the coverage model itself is not easy to be verified. This generator will transfer the coverage groups/points from an excel to systemverilog model. If the coverage points are reviewed in an excel file, the generator will do the routine jobs for you to convert the fileds to systemverilog syntax to avoid the human mistakes.
# Require package 
xlrd
# How
~~~
python cov_gen.py AHB_M_COV.xlsx
python cov_gen.py FCOV_TEMPLATE.xlsx
~~~  
# Excel examples
* FCOV_TEMPLATE.xlsx - Template for vairous coverage styles
* AHB_M_COV.xlsx - AHB master coverage group
