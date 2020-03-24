package edu.adelaide.comp.jiaxiang;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Partitioner;




public class WCParitioner extends Partitioner<Text, IntWritable>{

	// partition -- grouping key, prevent data skew
	// for exmaple, the word 'the' has very high frequence in documents.
	// so the server used to count 'the' may load much higher pressure than
	// other, so can we just send the key value pair of word 'the' in a radnom
	// server , which can highly reduce the pressure of one server machine.
	
	// the numPartition represent the Mapper number 
	
	@Override
	public int getPartition(Text text, IntWritable value, int numPartitions){
		return text.hashCode() % numPartitions;
	}
}
