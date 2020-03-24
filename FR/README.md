## friend recommend system
#### files
`FR.jar`  jar package for run hadoop <br>
`FriendRecommend` mean files implemented the friend recommand system<br>
`description.md` the description about how the friend recommend system work<br>
`output_FR` running result<br>
`soc-LiveJournal1Adj.txt` input txt file<br>

### environment
use `uname -a` check version of Linux<br>
my env is Linux quickstart.cloudera 2.6.32-w358.el6.x86_64 #1 SMP Fri Feb 22 00:31:26 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux<br>

#### how to run
1. copy the `FriendRecommend` in eclipes directory, and right click this projecrt , find `export`, and export it to a jar file such like `FR.jar`<br>
2. open terminal change to dirctory saved jar file<br>
`hadoop fs -mkdir /user/cloudera/FR`<br>
`hadoop fs -put soc-LiveJournal1Adj.txt /user/cloudera/FR/`<br>
`hadoop jar FR.jar edu.adelaide.comp.jiaxiang.FriendRecommend`<br>
until that complete, download the result to local<br>
`hadoop fs -get /user/clouder/output_FR .`<br> then you have result