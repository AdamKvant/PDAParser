# PDAParser

### Key Terms
* **EMG:** Electromyography
* **PDA:** Peak Dynamic Activity (of a muscle)

### Description
PDAParser is a quaint CLI program that I created to aid a life-long friend, **<a href="https://www.linkedin.com/in/jacksonwatsonmed/">Jackson Watson D.O.'28</a>**, in processing data from his medical research lab. This program normalizes values from raw EMG data on muscles in the foot and lower leg, and puts them in an easily readable output file. This program was straightforward to create, and saved significant time in processing data from the lab. Information about the study can be found under **<a href=""> Study Information</a>**.

The program takes in a ZIP file containing `n` CSV files that are named according to a standardized naming scheme in sequential order. These CSV files are also rigorously structured, and this program is specifically tailored to read them.

The regex used for the filenames of files in the input ZIP was: `'[^\d]*(\d+).*\.csv'` and an example filename is: `ShS02TSPr(Pooled_Trials).csv`. The only data that needed to be extracted from the filename was the first occurrence of a number in the filename. This number is used to assign the ID of each set of trials in the output file. 

PDAParser reads the maximum average PDA of a muscle across five trials (PDAa), and the maximum PDA across five trials (PDAb).
These maximums are all reported to an `output.csv` file or the specified output filename.


## Directions

The user is able to run the program by having the executable *and* the zip file in the same directory.

*Note: The executable `PDAParser` file can be taken out of the `dist` directory and be used elsewhere.* 

### Flags

There are various flags that can be enabled in the CLI for some required and optional functionality.

* `-f` or `-filename` (required) is the flag used to enter the name of the input Zip file.
* `-p` or `--prefix` (optional) is the flag used to specify a prefix for column headers in the output file.
* `-r` or `--result` (optional) is the name of the output file **without** the file extension. The default name for the output file is results.csv

### Running the program (Linux)

1. Put the ZIP file in the directory containing the `PDAParser` executable.
2. Open the CLI and navigate to the directory containing the `PDAParser` executable.
3. Enter `./PDAParser -f <input ZIP filename>.zip` into the terminal and press `enter`.
4. Outputs can be found in the `results.csv` file.

### Demo Files

Demo files can be found in the root directory for test data and results.
Demo results can be found in `results.csv`, and demo data can be found in `demo.zip`.

# Study Information

### **<a href="https://docs.google.com/document/d/1fA5ljCOL5eLoWoGuXdGdGCyOjCLV--RFDZeleVdnGOw/edit?pli=1&tab=t.0">Abstract Link</a>**

![Study Poster](/images/Final_Study_Poster.png)