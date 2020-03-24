package edu.adelaide.comp.jiaxiang;

import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class LMapper extends Mapper<Object, Text, Text, IntWritable> {

	// each word only count 1 in Mapper
	private final static IntWritable one = new IntWritable(1);
	
	
	// key_out object
	private Text word = new Text();
	
	
	/// mapping method ()
	public void map(Object key, Text value, Context context) throws IOException, InterruptedException{
		
		// value is 1 line data
		
		StringTokenizer st = new StringTokenizer(value.toString().toLowerCase());
		
		while(st.hasMoreTokens()){
			
			String t = st.nextToken();
			
			if (t.length() == 10){
				word.set("lenght=10");
				context.write(word, one);
				
			}else if (t.length() == 4){
				word.set("length=4");
				context.write(word, one);
			}
		}	
	}
}
