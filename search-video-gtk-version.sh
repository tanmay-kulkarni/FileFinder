#!/bin/bash

#printf "\n\tWhich File you wanna play?: "


# Figure out some way to pass the arguement from python.
# $1 is the file name to be searched. It is passed as a parameter to the script.
#
#file_name=$1

file_name=$1
check_case=$2	# whether to ignore case or not

root_dir=$3	# root dir for searching 


# values are truth values against each format.
all_formats=$4
mp4=$5
pdf=$6
avi=$7
mkv=$8


pwd=$9

#<<COMMENT 

#whether to ignore cases or not.
if [ $check_case = "true" ];
then
	case_or_not="-iname"
else
	case_or_not="-name"
fi
	
declare -A formats_arr

formats_arr[mp4]=$mp4
formats_arr[pdf]=$pdf
formats_arr[avi]=$avi
formats_arr[mkv]=$mkv


#echo im here


# if the all_formats options is enabled, make the entire array true.

if [ $all_formats = "true" ];
then
	for format_index in "${!formats_arr[@]}"
	do
		formats_arr[$format_index]="true"
	done

#for format in ${!formats_arr[@]}
#do
#	echo "$format: ${formats_arr[$format]}" 
#done

fi

# print the status of checkboxes.
<<"f"
for format in ${!formats_arr[@]}
do
	echo -e "$format: \t ${formats_arr[$format]}" 
done

f

echo -e "\n..............................................................................\n"
#sleep 1


#COMMENT


#	if [ $file_name -z ]; then
#		echo -e "\n\n\tNo input. Process terminated. \n\n"
#		exit 0 
#	fi

# No need to print this in the gtk version. 
#echo -e "\tYou entered file : $file_name \n\nMy search shows following possibilities:\n\nNo.| \t Name"

#echo -e "------------------------------------------------"

# This is where the fun begins.
# the search path is currently hardcoded, but should be picked up from the "search root" provided by the user
# same goes for file formats.
# pass the file formats as arguements too. 
# $1= filename
# $2= mp3, $3= avi, $4= mp4, 
# If the checkboxes aren't checked, pass some default..."None".
# So every parameter will be passed. 
# An if else ladder here to decide what formats should be searched using the find command.

#take an array here for storing formats. pass this array to search function. Loop through the array values to build the find command. Or search them 1by1 and club the results. This way, all files with the same format will be together.

# 

i=0;

# This is ugly. Better do it later by looping through the parameters. #@ or something may be used.
#<< 'COMMENT'
#if [ $2 -ne "None" ];		# mp3 is None.
#	format_array[i]=".mp3"
#	let i++
#fi
#if [ $3 -ne "None" ];
#	format_array[i]=".avi"
#	let i++
#fi
#if [ $4 -ne "None" ];
#	format_array[i]=".mp4"
#	let i++
#fi	 

#'
#COMMENT

#find /home/$USER/ \( -iname "*$file_name*.mp4" -o -iname "*$file_name*.avi" -o -iname "*$file_name*.mkv" \)  > /home/tanmay/search.txt

# searching for pdf for now.
#find /home/$USER/  \( -iname "*$file_name*.pdf" -o -iname "*$file_name*.avi" -o -iname "*$file_name*.mkv" \)  > /home/$USER/search.txt

# latest comment here============================>
#find $root_dir  \( -iname "*$file_name*.pdf" -o -iname "*$file_name*.avi" -o -iname "*$file_name*.mkv" -o -iname "*$file_name*.mp4" \)  > /home/$USER/search.txt


# mp3,mp4,avi,pdf,mkv

#<<"COMMENT"



# function that receives an extension and serches files having it.
search_this_extension(){
	# sent extension is $1
	extension=$1
	# append the result of the find command to the text file.
	echo $pwd | sudo -S find $root_dir -type f $case_or_not "*$file_name*.$extension" >> /home/$USER/gtk-search.txt
}


# get the search file ready. create using touch if not present. nullify if not empty.
touch /home/$USER/gtk-search.txt
cp /dev/null /home/$USER/gtk-search.txt

#echo "after touch"

# iterate through the array indices.
# '!' creates array indices in bash
for extension in ${!formats_arr[@]}
do
# for each extension found true, call the search function with extension as parameter.
	if [ ${formats_arr[$extension]} = "true" ];
	then
			search_this_extension $extension		
	fi

done



#COMMENT









#Takes each file name and removes everything from name until the last '/' from left is found
#<<C
count=1
#color=30
cat /home/$USER/gtk-search.txt | while read line
do
#	let color++
#	printf "\e[1;${color}m"	
	printf "%-2d | " $count
 	echo $line | sed 's/.*\///g'  
#	printf "\e[0m"
	let count++
#	if [ $color -eq 38 ]; then
#		let color=30
#	fi
done

#C

#echo "\n\n\n\n\n"

#<<  'COMMENT'
#
#printf "\nSelect Option: "
#read -t 5 choice
#
#if [ $choice -z  ]; then
#	echo -e "\n\n\t No input detected. Process terminated.\n\n"
#	exit 0
#fi


#echo -e "\n\nThe file is located at path:\n"

#cat /home/tanmay/search.txt | sed ''$choice'q;d' | sed 's/ /\\ /g' | sed 's/(/\\(/g' | sed 's/)/\\)/g' | sed "s/'/\\\'/g" | sed 's/&/\\&/g'

#echo -e "\nLaunching with VLC..."

#cat /home/tanmay/search.txt | sed ''$choice'q;d' | sed 's/ /\\ /g' | sed 's/(/\\(/g' | sed 's/)/\\)/g' | sed "s/'/\\\'/g" | sed 's/&/\\&/g' | xargs vlc --fullscreen 2>/dev/null & disown

#echo -e "\nUsage: vlc 'copied_string'\n"


#echo -e "\n"

#COMMENT

exit 0

