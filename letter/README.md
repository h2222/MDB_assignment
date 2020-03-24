## Letter
#### files for exercise 4.1.1
`./exercise_4_1_1/Letter_sl.jar`  jar package for run hadoop <br>
`Letter_length` mean files implemented the letter statistic<br>
`output_le` running result<br>
`pg100.txt` input txt file<br>


#### files for exercise 4.1.2
`./exercise_4_1_2/Letter_2.jar`  jar package for run hadoop <br>
`Letter_length` mean files implemented the letter statistic<br>
`output_le_2` running result<br>
`3399.txt` input txt file<br>


#### environment
use `uname -a` check version of Linux<br>
my env is Linux quickstart.cloudera 2.6.32-w358.el6.x86_64 #1 SMP Fri Feb 22 00:31:26 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux<br>

#### how to run for exercise 4.1.1 (4.1.2 same operation)
1. copy the `Letter_length` in eclipes directory, and right click this projecrt , find `export`, and export it to a jar file such like `Letter_sl.jar`<br>
2. open terminal change to dirctory saved jar file<br>
`hadoop fs -mkdir /user/cloudera/letter`(change `letter` to `letter/exercise_4_2` in 4.1.2)<br>
`hadoop fs -put pg100.txt /user/cloudera/letter`(change `letter` to `letter/exercise_4_2` and `pg100.txt` to `3399.txt` in 4.1.2)<br>
`hadoop jar Letter_sl.jar edu.adelaide.comp.jiaxiang.Letter`(change `Letter_sl.jar` to `Letter_2.jar` in 4.1.2)<br>
until that complete, download the result to local<br>
`hadoop fs -get /user/clouder/output_le .`(change `output_le` to `output_le_2` in 4.1.2)<br> then you have result