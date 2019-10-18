# svfcovgen
Fucntional coverage model play an import role in constraint random simulation. It is a key metric to understand what kind of stimulus and insteresting scenario have been tested. However, the coverage model itself is not easy to be verified. This generator will transfer the coverage groups/points from an excel to systemverilog model. If the coverage points are reviewed in an excel file, the generator will do the routine jobs for you to convert the fileds to systemverilog syntax to avoid the human mistakes.

#The excel file field definitions
## col 0:
preserved for special symbols to help the svfcovgen parsing the excel file
### #: skip this row
### ^: The first row which constants the column name
### $: The end the row
