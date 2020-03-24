package edu.adelaide.comp.jiaxiang;

import java.io.IOException;
import java.util.Collection;
import java.util.Set;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import com.google.common.collect.HashMultimap;
import com.google.common.collect.Multimap;

public class FRReducer extends Reducer<Text, ValuePair, Text, Text> {
	
	// value key output object
	private Text outKey = new Text();
	private Text outValue = new Text();
	
	@Override
	public void reduce(Text key, Iterable<ValuePair> values, Context context) 
			throws IOException, InterruptedException {
		
		this.outKey = key;
		Multimap<String, String> map = HashMultimap.create();
		
		for (ValuePair v:values){
			// getFriend, friend with key,  getUnion-> 'yes' or null
			map.put(v.getFriend(), v.getUnion());
		}
		
		
		// using to save output result
		StringBuilder outString = new StringBuilder();
		// get every one who are related with key (v.getFriend())
		Set<String> keys = map.keySet();
		
		for(String s:keys){
			// saving output value
			StringBuilder outStr = new StringBuilder();
			boolean isok = true; // if it is friend with key
			
			Collection<String> v = map.get(s);// v represent 'yes' or 'no' with key
			outStr.append(s+",");
			// if isok, means key(outkey) annd target(s) is already friend
			// they dont need recommondation
			for(String u: v){
				if(u.equals("yes")){
					isok = false;
					break;
				}
			}
			// add in final
			if(isok){
				outString.append(outStr);
			}
		}
		
		// outString -> string type
		outValue.set(outString.toString());
		// out
		context.write(outKey,  outValue);
	}
}
