## word count
#### files
`WordCount.jar`  jar package for run hadoop <br>
`WordCount_2` mean files implemented the word count<br>
`output` running result<br>
`100-0.txt` input txt file<br>

#### environment
use `uname -a` check version of Linux<br>
my env is Linux quickstart.cloudera 2.6.32-w358.el6.x86_64 #1 SMP Fri Feb 22 00:31:26 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux<br>

#### how to run
1. copy the `WordCount_2` in eclipes directory, and right click this projecrt , find `export`, and export it to a jar file such like `WordCount.jar`<br>
2. open terminal change to dirctory saved jar file<br>
`hadoop fs -mkdir /user/cloudera/word_count`<br>
`hadoop fs -put 100-0.txt /user/cloudera/word_count`<br>
`hadoop jar WordCount.jar edu.adelaide.comp.jiaxiang.WordCount`<br>
until that complete, download the result to local<br>
`hadoop fs -get /user/clouder/output .`<br> then you have result