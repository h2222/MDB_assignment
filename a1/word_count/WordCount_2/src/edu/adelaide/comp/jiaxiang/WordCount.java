package edu.adelaide.comp.jiaxiang;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class WordCount {

	public static void main(String[] args) throws Exception {
		
		// configuration step
		Configuration conf = new Configuration(true);
		Job job = Job.getInstance(conf);
		// set job name
		job.setJobName("WordCount");
		
		//  run by jar file	
		job.setJarByClass(WordCount.class);
			
		
		// ----- conf -------
		
		// slice block
		
		// set map class,  map-key class, map-value class
		job.setMapperClass(WCMapper.class);
		job.setMapOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
		
		
		// partition and Comparate
		// job.setPartitionerClass(WCParitioner.class);
		
		
		// set reduce class,  reduce-key class,  reduce-value class
		job.setReducerClass(WCReducer.class);
		
		
		// file path (hdfs)
		//  input
		Path input = new Path("/user/cloudera/word_count");
		FileInputFormat.addInputPath(job, input);

		
		// output
		Path output = new Path("/user/clouder/output");
		
		// if output exist, recursive delete it
		if (output.getFileSystem(conf).exists(output)){
			output.getFileSystem(conf).delete(output, true);
		}
		
		FileOutputFormat.setOutputPath(job, output);
		
		
		// 1 mapper
		job.setNumReduceTasks(2);
		
		
		job.waitForCompletion(true);

	}

}
