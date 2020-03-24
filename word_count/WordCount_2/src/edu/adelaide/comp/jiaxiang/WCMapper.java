package edu.adelaide.comp.jiaxiang;

import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class WCMapper extends Mapper<Object, Text, Text, IntWritable> {

	// each word only count 1 in Mapper
	private final static IntWritable one = new IntWritable(1);
	
	// key_out object
	private Text word = new Text();
	
	
	/// mapping method ()
	public void map(Object key, Text value, Context context) throws IOException, InterruptedException{
		StringTokenizer st = new StringTokenizer(value.toString());
		
		while(st.hasMoreTokens()){
			// key-word, value-one
			word.set(st.nextToken());
			context.write(word, one);
		}
	}
		
}
