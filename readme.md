Name: pyworklistserver      
Description: Lightweight DICOM worklist server command line utility     
Intended use: Act as worklist server for HAST       
Dependencies: see requirements.txt      

Functionality:
* Reproduce with seed
* Configfile to manage functionality 
* Too long string
* Easy manageble data
* Variable character set(This feature is sanitised by pydicom (issue #18))
* NULL and Empty strings
* Delay

Install from source:
    py -3 -m pip install --no-index --find-links=%LOCALPYTHONPACKAGECACHE% .

Install from wheel:
    py -3 -m pip install pyworklistserver-1.0-py3-none-any.whl --no-index --find-links=%LOCALPYTHONPACKAGECACHE% .

Run:
    py -3 -m pyworklistserver
    
For more info about optional arguments:
    use --help as argument when running the program.
