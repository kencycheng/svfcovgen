# svfcovgen
Fucntional coverage model play an import role in constraint random simulation. It is a key metric to understand what kind of stimulus and insteresting scenario have been tested. However, the coverage model itself is not easy to be verified. This generator will transfer the coverage groups/points from an excel to systemverilog model. If the coverage points are reviewed in an excel file, the generator will do the routine jobs for you to convert the fileds to systemverilog syntax to avoid the human mistakes.

# The Field definitions

##  The column 0 is fixed
preserved for special symbols to help the svfcovgen parsing the excel file
~~~
#: skip this row
^: The first row which constants the column name
$: The end the row
~~~

## The other column definition are changable
The column position is changable. The parser will recognite the column position according keywords of the first row. The first row is the row which has a '^' in the column 0.

Table1 is identical to Table2 

Table1

|^| Label  | TARGET |PRIORITY|
| ------------- |------------- | ------------- | ------------- |
| |cp_pkt_len| pkt_len  |1|
| |cp_speed  | speed  |2|

Table2

|^|Label  |PRIORITY| TARGET |
|------------- |------------- | ------------- | ------------- |
| |cp_pkt_len|1| pkt_len  |
| |cp_speed  |2| speed  |
