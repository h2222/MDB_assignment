package edu.adelaide.comp.jiaxiang;

import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class WCReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
	
	// valueOut object
	private IntWritable result = new IntWritable();
	
	public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
		// initialize counting
		int sum = 0;
		
		// key is same, adding one together
		for (IntWritable val:values){
			sum += val.get();
		}
		
		result.set(sum);
		
		// return final result
		context.write(key, result);
	}
}
