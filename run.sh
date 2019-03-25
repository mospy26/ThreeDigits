command="python3 ThreeDigits.py B "

for file in ./tests/*.txt;
do
case "$file" in
	*BFS*.txt)	echo -e $file; cat $file; echo -e "\n"; python3 ThreeDigits.py B $file;;
	*DFS*.txt) echo -e $file; cat $file; echo -e "\n"; python3 ThreeDigits.py D $file;;
	*IDS*.txt) echo -e $file; cat $file; echo -e "\n"; python3 ThreeDigits.py I $file;;
	*GDY*.txt) echo -e $file; cat $file; echo -e "\n"; python3 ThreeDigits.py G $file;;
	*)	break;
esac
echo -e "\n"
echo "-----------";
echo -e "\n"
done
