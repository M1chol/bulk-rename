# Bulk Patern Rename tool
### Python tool used to bulk rename files based on patterns!

---
This tool supports renaming and deleting files, you specify files and folders using 
custom language. Before you execute program you need to set up special file with automation
code written in _Rename Script_   
   
The first line of code must contain version of interpreter code is written for. And file extension must be .rs     
```
v1
rename evidence{*}.png dog_{@counter}.png
del {*}.txt
```
![GIF](https://github.com/M1chol/bulk-rename/blob/master/misc/bulk4.gif)   
You can always check interpreter version on the .exe


## Documentation

### for loop
```
for [type] [name]   

aviable wildcards:
@dirs; all folders

naming:
@number; any number
*; anything

usecase:

for @dirs {@number}
printloop
end

explanation:
printloop command prints all folders selected by for loop
for @dirs {@number} => 2, 89
for @dirs temp_{@number} => temp_22, temp_0 
```   
### rename
```
rename [old name] [new name]

avaiable wildcards:
@original; holding original name of file
@parent; holding name of parent folder
@counter; counts renamed files!
@l_counter; (local counter) same as @counter but resets on new dirictory 

usecase:

rename {@number}.png camera_{@original}.png
- 1225.png => camera_1225.png
rename data_{@number}.ods exel{@counter}
- data_12.ods => exel_1.ods
- data_24.ods => exel_2.ods
```   
### del
```
del evidence{@number}.png => removes all evidence! handy!
```

---

### More of the tool in action
![GIF](https://github.com/M1chol/bulk-rename/blob/master/misc/bulk.gif)

![GIF](https://github.com/M1chol/bulk-rename/blob/master/misc/bulk2.gif)

![GIF](https://github.com/M1chol/bulk-rename/blob/master/misc/bulk3.gif)
     
