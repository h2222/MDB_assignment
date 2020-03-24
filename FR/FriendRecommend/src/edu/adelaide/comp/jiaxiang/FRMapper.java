package edu.adelaide.comp.jiaxiang;

import java.io.IOException;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class FRMapper extends Mapper<LongWritable, Text, Text, ValuePair> {

	// ......
	private Text outkey = new Text();
	private ValuePair outvalue = new ValuePair();
		
	/// mapping method ()
	public void map(LongWritable key, Text value, Context context) 
			throws IOException, InterruptedException{
		
		String input = value.toString();
		
		// [persion,  person's friends string sperated by common]
		String[] sz = input.split("\t");
		
		System.out.println("length::::::"+sz.length);
		
		
		// set current person
		this.outkey.set(sz[0]);
		
		// use sz1 to save the friends
		String[] sz1 = sz[sz.length-1].split(",");
		
		
		// 
		for (int i=0; i < sz1.length; i++){
			// get every friend of current person
			// outvalue is a friendPair object
			// set friend 
			
			// context <1, "yes">  means: <friend number, if it is friend>
			this.outvalue.setFriend(sz1[i]);
			this.outvalue.setUnion("yes"); // yes represent that key has been friend with outvalue
			context.write(this.outkey, this.outvalue);
		}
		
		// in friend list, find if there are some people who know each other
		// and count it
		
		// for 1, get every one(target) in friend list
		for (int i=0;i<sz1.length;i++){
			// for 2, get others except target
			for(int j=i+1;j<sz1.length;j++){
				
				// set target as key
				this.outkey.set(sz1[i]);
				
				// 
				this.outvalue.setFriend(sz1[j]);
				
				// this sz[0] is people who are both target and target's friend. friend.
				this.outvalue.setUnion(sz[0]);
				
				// <2, <3, 1>> 2 is target, 3 is target's firend, 1 is both target and target's friends firends
				context.write(this.outkey, this.outvalue);
				
				
				// beacuse they are mutual friend, so if target is others friends and
				// also others also will be target friend.
				// <target'friend, target>
				this.outkey.set(sz1[j]);
				this.outvalue.setFriend(sz1[i]);
				context.write(this.outkey, this.outvalue);
				
			}
		}	
	}
	
}
