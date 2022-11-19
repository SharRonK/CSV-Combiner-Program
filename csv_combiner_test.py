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

Unit Test File
"""

import sys 
import os 
import pandas as pd
import unittest
from csv_combiner import file_validate, csv_combiner

class CSVCombinerTest(unittest.TestCase):

	# Paths of the files used in unittest
	py = "./csv_combiner.py"
	file1 = "./fixtures_test/accessories.csv"
	file2 = "./fixtures_test/clothing.csv"
	file3 = "./fixtures_test/household_cleaners.csv"
	file_diff_cols = "./fixtures_test/different_cols.csv"
	file_wrong_type = "./fixtures_test/wrong_type.xlsx"
	file_empty = "./fixtures_test/empty.csv"
	file_wrong_name = "./fixtures_test/cloth.csv"


	def test_no_input_file(self):
		argv = [self.py]
		with self.assertRaises(SystemExit) as cm:
			csv_combiner(argv)

		self.assertEqual(cm.exception.code, "\033[1m" + "No file read from the command line.\n" 
			+ "To successfully run the program, please enter your input in the format of e.g.\n"
			+ "$ ./csv-combiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv > combined.csv" + "\033[0m")

	def test_wrong_file_type(self):
		argv = [self.py, self.file_wrong_type]
		with self.assertRaises(SystemExit) as cm:
			csv_combiner(argv)

		self.assertEqual(cm.exception.code, "\033[1m" + ".xlsx" + " files not supported. Please only use .csv files" + "\033[0m")


	def test_empty_file(self):
		argv = [self.py, self.file_empty, self.file1]
		with self.assertRaises(SystemExit) as cm:
			csv_combiner(argv)

		self.assertEqual(cm.exception.code, "\033[1m" + "The file empty.csv is empty." + "\033[0m")
		
	def test_wrong_file_name(self):
		argv = [self.py, self.file_wrong_name, self.file1]
		with self.assertRaises(SystemExit) as cm:
			csv_combiner(argv)

		self.assertEqual(cm.exception.code, "\033[1m" + "The file cloth.csv does not exist. Please check your input file name or path." + "\033[0m")

	def test_diff_cols(self):
		argv = [self.py, self.file1, self.file_diff_cols]
		with self.assertRaises(SystemExit) as cm:
			csv_combiner(argv)

		self.assertEqual(cm.exception.code, "\033[1m" + "Inputs have different columns" + "\033[0m")


	def test_two_inputs(self):
		argv = [self.py, self.file2, self.file1]
		result = csv_combiner(argv)
		num_of_rows = 0
		num_of_cols = 0
		for file in argv[1:]:
			temp = pd.read_csv(file)
			num_of_rows += temp.shape[0]
			num_of_cols = temp.shape[1] + 1
		self.assertEqual(result.shape[0], num_of_rows)
		self.assertEqual(result.shape[1], num_of_cols)
		self.assertIn("filename", set(result.columns))

	def test_multiple_inputs(self):
		argv = [self.py, self.file2, self.file1, self.file3]
		result = csv_combiner(argv)
		num_of_rows = 0
		num_of_cols = 0
		for file in argv[1:]:
			temp = pd.read_csv(file)
			num_of_rows += temp.shape[0]
			num_of_cols = temp.shape[1] + 1
		self.assertEqual(result.shape[0], num_of_rows)
		self.assertEqual(result.shape[1], num_of_cols)
		self.assertIn("filename", set(result.columns))



if __name__ == '__main__':
	unittest.main()