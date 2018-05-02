To Parse Script File:

1. Obtaining Script in JSON Format
	- Go to script parser
	- Run movie script parser
	- Follow instructions in console
	- Will return script in json file

2. Aligning times
	- take JSON file obtained from step one and put it in FinalYearProject/files
	- place subtitle track file in FinalYearProject/files directory
	(there are already files in the directory that this can be tested with)
	- go back to FinalYearProject directory
	- run format.py with the names of the ouput files you want for the timings and formatted subtitles, and the name of the subtitle track file
	- run jsonreader.py with the names of the input formatted subtitle track file and the parsed script fie
	- this will return two json files; one containing only the dialogue with the aligned times and the other with all the stage direction and location information still included

3.Obtaining csv file of movie data
	- run csvParser.py in FinalYearProject directory with the name of the json file from the previous step that still contains all the stage direction and location information

4.Videoplayer
	- This video player is coded for the purposes of demoing the project using a Star Wars Episode IV MP4 file and the formatted and temporally aligned script data