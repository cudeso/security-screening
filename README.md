# security-screening

A batch file to be used for
- Security screening
- Compliancy check
- Quick forensic information gathering

Ideally the script needs to run with administrator privileges.

Completing the script can take a couple of minutes. 
A number of errors (fe. "This user name could not be found." or "The syntax of this command is") will occur during runtime. This is normal behaviour and due to lazy parsing of the output of the different commands.

The output of the script results in a large (>50) set of text files and CSV files. All these files are put into one ZIP file, after which the output directory is deleted.
