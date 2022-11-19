"""
PMG Graduate Leadership Program Coding Challenge 
Author: Yuru "Sharron" Kang
November 2022

Write a command line program that takes several CSV files as arguments. 
Each CSV file (found in the fixtures directory of this repo) will have the same columns. 
Your script should output a new CSV file to stdout that contains the rows from each of 
the inputs along with an additional column that has the filename from which the row came 
(only the file's basename, not the entire path). 
Use filename as the header for the additional column.
"""

import sys 
import os 
import pandas as pd


def file_validate(file):
	filename = os.path.basename(file) 
	if os.path.exists(file):
		# Not .csv file
		if filename[-3:] != "csv":
			sys.exit("\033[1m" + filename[filename.index("."):] + " files not supported. Please only use .csv files" + "\033[0m")				
		# Empty file
		elif pd.read_csv(file).empty:
			sys.exit("\033[1m" + "The file " + filename + " is empty." + "\033[0m")				
		else:
			return True
	else:
		# Wrong file name
		sys.exit("\033[1m" + "The file " + filename + " does not exist. Please check your input file name or path." + "\033[0m")

def csv_combiner(argv):
	# validate the input files in the command line
	files = argv[1:]
	df = pd.DataFrame()
	flag = False
	# no file input
	if len(files) == 0:
		sys.exit("\033[1m" + "No file read from the command line.\n" 
			+ "To successfully run the program, please enter your input in the format of e.g.\n"
			+ "$ ./csv-combiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv > combined.csv" + "\033[0m")

	for file in files:
		file_validate(file)

		#different columns
		df1 = pd.read_csv(file)
		t = set(df1.columns)
		t.add("filename")
		if flag and set(df.columns) != t:
			sys.exit("\033[1m" + "Inputs have different columns" + "\033[0m")

		df1 = pd.read_csv(file, chunksize = 100000)
		# to deal with very large files
		for i in df1:
			i["filename"] = os.path.basename(file) 
			df = pd.concat([df, i])
		flag = True
	
	return df

def main():
	df = csv_combiner(sys.argv)
	res = df.to_csv()
	print(res)


if __name__ == '__main__':
	main()
