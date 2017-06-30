# FileLoadTK

Implemented:
Simple GUI for selecting 1. File of log names, 2. File of user input (equations, specs, etc), 3. Folder of log location.
Used List comprehensions with string based attribute setters, and inspecting the grid to set the button for sumbit. (can't press submit if there are no files). 





Desires:
1. Make the first button able to select file or folder, that way if we need to iterate through all files in a folder we don't need a list.
1a. This would auto fill out the text to the right of the third button, since we already have the file location.
2. Either remove second button, or implement some usage for it. 
3. Change grid for submit so that the button is much bigger. 
4. When you re-click a button, but you don't select a file I want to not delete the current information. 
5. If on exit but the submit button isn't available, don't want to process the entered data. 
6. Remove as many string entries as possible (text='Submit', title('LogAnalysis'), etc.

