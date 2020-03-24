## the description of friend recommandation system

### 1. contents
the mean files of Friend Recommendation system (FR) inlcude:<br>
`FriendRecommend.java` the configuartion of whole system<br>
`FRMapper.java` the the mapping file that transfer one line firend relationship to ValuePair object, the ValuePair will talk below<br>

`ValuePair.java` the new data structure that we want to return from map (map output value)<br>

`FRReducer.java` the reduce file that do compute and return the final results.<br>


### 2. How it work ?



Fristly, the configure some information such as the input and output file directories, map class name, reduce class name, the type of map key object and the type of map value object, etc.<br>


Then, we introduce the ValuePiar class, which is customized map output value object. this class inlcude 2 attributes, Friend and Union. Friend can see as the relationship between someone A and someone B, and the Union means a evidence of firend relationship between somone A and someone B. Furthermore, the ValuePiar must overwrite the compareTO method, which use to arrange the key value pair of output of map. <br>


Then, we extend the Mapper class and overwrite the map method. In map method, we use String.split method sperate the current people and his friend list, and we ues context.write to write  key value pair for tasks, we first loop the firend list of current person, for every one who is in current people friend list, we return the key value pair <current person number, ValuePair<current friend, if they has relationship>>. For example, if the input line is like `1<tab>2, 3, 4, 5`, so the current person is 1 and the friend is[2, 3, 4, 5], we then loop the friend list, assume we come to 2 and the key value pair will be like <1, <2, "yes">>.<br>


Then, we extend the Reducer class and overwrite the reduce method. In recudce method, the privous key value pair provided by Mapper has been sorted, those key value pairs that have some key will be send to a reduce method. the input key of reduce method is the Mapper's output key, the input value of reduce method is a Iterator that include lot of ValuePair object that has same input key. For example, I draw a data structrue below:<br>

1, Iterator [< 2,"yes">, <3, "yes">, <4, "yes">, <5, "yes">]<br>
2, Iterator [<4, "yes">, <5, "yes">,......]<br>
......<br>

Thus, we can loop the Iterator and get the ValuePair Friend and ValuePair Union, we create a multiMap object, then we set Friend as map key and Union as map value, then we use map.keySet method to get map key set and loop to get key. Once we get keys, then we can judge if the fried is input reduce key's friend or not.













