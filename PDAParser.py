import argparse
import os
import re
import zipfile
import sys



# Class used to parse Command Line Arguments from the user.
class Arguments:
    # Constructor
    def __init__(self):
        # Forbidden extensions from the command line
        self.extensions = (".txt", ".csv", ".json")
        
        parser = argparse.ArgumentParser(description="A script for parsing zip files of data into a single CSV file.")
        parser.add_argument("-f","--filename",type=str,help="The name of the ZIP file that is trying to be parsed. For example, \"TSPR.zip\"")
        parser.add_argument("-p","--prefix",type=str,help="The optional prefix for column headers in the result.")
        parser.add_argument("-r","--result",type=str,help="The name of the output file (without the file extension). The default result filename is results.csv")
        self.args = parser.parse_args()
        
        # Check if ZIP file exists
        if not os.path.exists(self.args.filename):
            raise FileNotFoundError(f"ZIP file '{self.args.filename}' not found.")
        # Validation steps for zip files, and prefix
        if not self.args.filename.endswith(".zip"):
            raise ValueError(f"Invalid file type. Expected .zip but got .{self.args.filename.split('.')[-1]}")
        if isinstance(self.args.prefix,type(None)):
            # Default prefix is nothing
            self.args.prefix = ""
            # Default output filename
        if isinstance(self.args.result,type(None)):
            self.args.result = "results.csv"
        elif self.args.result.endswith(self.extensions):
            # Removing some invalid file extensions
            for ext in self.extensions:
                if self.args.result.endswith(ext):
                    self.args.result = self.args.result.removesuffix(ext)
                    break
            self.args.result += ".csv"
        elif not self.args.result.endswith(self.extensions):
            self.args.result += ".csv"
        else:
            raise ValueError("Please do not enter a file extension for the result file.")
        
        # If running as an executable, get the real dir
        if getattr(sys, 'frozen', False):
            # Executable dir
            scriptDir = os.path.dirname(sys.executable)
        else:
            # Script dir
            scriptDir = os.path.dirname(os.path.abspath(__file__))  

        # Correct ZIP file path
        self.args.filename = os.path.join(scriptDir, self.args.filename)  
        zipDir = os.path.dirname(self.args.filename)
        # Ensure output is in the same dir as ZIP file
        self.args.result = os.path.join(zipDir, self.args.result)  


            
    # Getter for args  
    def getArgs(self):
        return self.args
    

# Class for operating on ZIP files
class ZipFunctions:
    # Constructors
    def __init__(self,args):
        self.data = {}
        self.zipLocation = args
    # Parses ZIP file
    def parseZip(self,prefix):
        
        # Opens ZIP file
        with zipfile.ZipFile(self.zipLocation, 'r') as zipObj:
            # Names of all files in ZIP file
            filenames = zipObj.namelist()
            
            # Regex for finding specific files, just in case
            fileRegex = r'[^\d]*(\d+).*\.csv'
            
            files = []
            
            # Getting correct files from ZIP file (using the regex)
            for file in filenames:
                match = re.match(fileRegex, file)
                if match:
                    number = int(match.group(1))
                    files.append((file, number))
            print(files)
            
            # Main data processing loop for individual files
            for file, number in files:
                print(f"Processing {file} (number: {number})")
                
                # Open specific file
                with zipObj.open(file) as f:
                    # Decode file and remove carriage returns
                    content = f.read().decode("utf-8", errors="replace")
                    content = content.replace("\r","")
                    
                    # Split by line
                    splitContentNL = content.split("\n")
                    
                    # Split by commas
                    for i in range(len(splitContentNL)):
                        splitContentNL[i] = splitContentNL[i].split(",")
                    
                    
                    dataPoints = []
                    for i in range(len(splitContentNL)):
                        if len(splitContentNL[i]) < 2:
                            break
                        category = -1
                        for j in range(len(splitContentNL[i])):
                            if i == 0:
                                if j == 0:
                                    continue
                                else:
                                    # Adding Headers to top of results csv
                                    if splitContentNL[i][j-1] == "":
                                        if prefix != "":
                                            dataPoints.append([prefix + "_" + splitContentNL[i][j].removesuffix("_AV")])
                                        else:
                                            dataPoints.append([splitContentNL[i][j].removesuffix("_AV")])
                                        # Index 0 in sublist is PDAa and PDAb is index 1
                                        dataPoints[len(dataPoints)-1].append([0.0,0.0])
                            else:
                                # Skip first index
                                if j == 0:
                                    continue
                                # Parse Data
                                elif splitContentNL[i][j] != "":
                                    if splitContentNL[i][j-1] == "":
                                        dataPoints[category][1][0] = max(float(splitContentNL[i][j]),dataPoints[category][1][0])
                                    else:
                                        dataPoints[category][1][1] = max(float(splitContentNL[i][j]),dataPoints[category][1][1])
                                # Shift over to next column in results csv (category)
                                else:
                                    category += 1
                        # Add to self.data dictionary
                        self.newDataKey(dataPoints,number)  
            
    
    # Adds to data dictionary for data storage
    def newDataKey(self,newlst,key):
        self.data[key] = newlst
        
    # Getter for data    
    def getData(self):
        return self.data
    
    
    
class CSVWrite:
    
    def __init__(self):
        pass
    
    def writeToCSV(self,filename,data):
        try:
            # Open results file
            with open(filename,mode="w",newline="") as file:
                i = 1
                # Loop through 1 through n indexes
                while i < len(data.keys()) + 1:
                    dataStr = ""
                    if i == 1: 
                        # CSV header row
                        dataStr += "ID,"
                        for column in data[i]:
                            dataStr += column[0]+"_PDAa,"+column[0]+"_PDAb,"
                        dataStr = dataStr.removesuffix(",")
                        file.write(dataStr+"\n")
                        
                        # First data row in result CSV
                        dataStr = "1,"
                        for column in data[i]:
                            dataStr += str(column[1][0])+"," +str(column[1][1])+","
                        dataStr = dataStr.removesuffix(",")
                        file.write(dataStr+"\n")
                        
                    # All other data rows in CSV
                    else:
                        dataStr = str(i) + ","
                        for column in data[i]:
                            dataStr += str(column[1][0])+"," +str(column[1][1])+","
                        dataStr = dataStr.removesuffix(",")
                        file.write(dataStr+"\n")
                    # Move to next dataset
                    i += 1
            return True
        except Exception as e:
            return False
            
                          
                        
                
    
    
    
    
# Main
if __name__ == "__main__":
    try:
        # Get arguments
        argObj = Arguments().getArgs()
        # Create a new zipObj
        zipObj = ZipFunctions(argObj.filename)
        # Parse ZIP file
        zipObj.parseZip(argObj.prefix)
        
        csvObj = CSVWrite()
        
        print(f"Writing to {argObj.result}")
        # Write parsed and processed data to CSV
        successBool = csvObj.writeToCSV(argObj.result, zipObj.getData())
        
        if successBool:
            print(f"Results correctly written to {argObj.result}")
        else:
            print(f"Error: Results were unable to be written.")
            
    except Exception as e:
        print(f"Error: {e}")
    