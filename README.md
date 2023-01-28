# Bulk Patern Rename tool
### Python tool used to bulk rename files based on code!

---

I wrote custom language to speed up renaming files.

simple usecase presented below   

### for loop
```
for [type] [name]   
for @dirs temp_{@number} => temp_2, temp_89

aviable wildcards:
@dirs; all folders
@file; all files
@number; any number
*; anything (similar to windows console)

usecase:

for @dirs {@number}
printloop
end

```   
### rename
```
rename [old name] [new name]

usecase:

rename {@number}.png camera_{@original} (14.png => camera_14.png)

avaiable wildcards:
@original; holding original name of file
@parent; holding name of parent folder
```   
---
## More complicated usecases:
![GIF](https://github.com/M1chol/bulk-rename/blob/master/misc/bulk.gif)

### More of the tool in action
![GIF](https://github.com/M1chol/bulk-rename/blob/master/misc/bulk2.gif)
     
