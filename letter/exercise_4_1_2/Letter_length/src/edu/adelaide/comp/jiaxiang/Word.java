package edu.adelaide.comp.jiaxiang;


import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

import org.apache.hadoop.io.WritableComparable;


public class Word implements WritableComparable<Word>{
	private int length;
	private String  str;
	
	public void setLength(int length){
		this.length = length;
	}
	public int getLength(){
		return this.length;
	}
	public void setStr(String str){
		this.str = str;
	}
	public String getStr(){
		return this.str;
	}
	
	// constructor
	public Word(){
		
	}
	
	public Word(String str, int length){
		this.length = length;
		this.str = str;
	}
	
		
	@Override
	public void readFields(DataInput in) throws IOException {
		// TODO Auto-generated method stub
		this.length = in.readInt();
		
	}

	@Override
	public void write(DataOutput out) throws IOException {
		// TODO Auto-generated method stub
		out.write(this.length);
		
	}

	@Override
	public int compareTo(Word o) {
		return Integer.compare(this.getLength(), o.getLength());
	}

}
