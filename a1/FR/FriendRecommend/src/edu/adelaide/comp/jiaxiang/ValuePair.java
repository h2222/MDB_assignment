package edu.adelaide.comp.jiaxiang;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

import org.apache.hadoop.io.WritableComparable;

public class ValuePair implements WritableComparable<ValuePair> {
/*
 * value pair class: map value output
 * OP class
 */
	
	private String friend;
	private String union;
	
	public String getFriend(){
		return friend;
	}
	
	public void setFriend(String friend){
		this.friend = friend;
	}
	
	public String getUnion(){
		return union;
	}
	
	
	public void setUnion(String union){
		this.union = union;
	}
	
	// constructor
	public ValuePair(){
		
	}
	
	public ValuePair(String f, String u){
		this.friend = f;
		this.union = u;
	}
	
	@Override
	public void readFields(DataInput in) throws IOException{
		this.friend = in.readUTF();
		this.union = in.readUTF();
	}

	@Override
	public void write(DataOutput out) throws IOException {
		// TODO Auto-generated method stub
		out.writeUTF(this.friend);
		out.writeUTF(this.friend);		
	}

	// recursive find the 
	@Override
	public int compareTo(ValuePair o) {
		
		// input parameter Friednship ValuePair
		// o means other 
		// if current person has a friend who also is 
		// other's friend
		if (this.friend.equals(o.getFriend())){
			return this.union.compareTo(o.getFriend());
		}else{
			return this.friend.compareTo(o.getFriend());
		}
	}
}
