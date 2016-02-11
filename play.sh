#!/bin/bash

#printf "\n\tWhich File you wanna play?: "


# Figure out some way to pass the arguement from python.
# $1 is the file name to be searched. It is passed as a parameter to the script.
#
#file_name=$1

#file_name=$1

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

#i=0;

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


#Takes each file name and removes everything from name until the last '/' from left is found

#count=1
#color=30
#cat /home/$USER/search.txt | while read line
#do
#	let color++
#	printf "\e[1;${color}m"
#	printf "%-2d | " $count
#	echo $line | sed 's/.*\///g'
#	printf "\e[0m"
#	let count++
#	if [ $color -eq 38 ]; then
#		let color=30
#	fi
#done


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

choice=$1

echo -e "\n\nThe file is located at path:\n"

cat /home/$USER/gtk-search.txt | sed ''$choice'q;d' | sed 's/ /\\ /g' | sed 's/(/\\(/g' | sed 's/)/\\)/g' | sed "s/'/\\\'/g" | sed 's/&/\\&/g'

# The application to be used for opening the file totally depends on the extension of the file chosen
# for opening. the output of the previous command is plain file name w/o extensions.
# strip of everythiing and obtain the extension. Depending on it, decide whether to use okular or vlc
# in the gtk app, display a menu => about, application bindings, manage password
# in application bindings, take input as to what command to use for opening vlc or okular.
# give the application command at run time.

str=$(cat /home/$USER/gtk-search.txt | sed ''$choice'q;d' | sed 's/ /\\ /g' | sed 's/(/\\(/g' | sed 's/)/\\)/g' | sed "s/'/\\\'/g" | sed 's/&/\\&/g')
# slashes removed
#name=$(echo $str | sed 's/.*\///g')
#echo $name
# stripping the extension from the file name
ext=${str##*.}
#echo extension is $ext

vlc=$2
okular=$3

#echo the vlc command is $2 and okular command is $3

#<<"C"
	if [ $ext = "pdf" ]; then
		echo launching with OKULAR
		cat /home/$USER/gtk-search.txt | sed ''$choice'q;d' | sed 's/ /\\ /g' | sed 's/(/\\(/g' | sed 's/)/\\)/g' | sed "s/'/\\\'/g" | sed 's/&/\\&/g' | xargs $okular 2>/dev/null & disown
	else
		echo launching with VLC
		cat /home/$USER/gtk-search.txt | sed ''$choice'q;d' | sed 's/ /\\ /g' | sed 's/(/\\(/g' | sed 's/)/\\)/g' | sed "s/'/\\\'/g" | sed 's/&/\\&/g' | xargs $vlc 2>/dev/null & disown
	fi

#C




exit 0




echo -e "\nLaunching with okular..."

cat /home/$USER/gtk-search.txt | sed ''$choice'q;d' | sed 's/ /\\ /g' | sed 's/(/\\(/g' | sed 's/)/\\)/g' | sed "s/'/\\\'/g" | sed 's/&/\\&/g' | xargs okular 2>/dev/null & disown

#echo -e "\nUsage: vlc 'copied_string'\n"


#echo the nameis $str


#echo -e "\n"

#COMMENT

exit 0

