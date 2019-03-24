command="python3 ThreeDigits.py B "

for file in ./tests/*.txt;
do
case "$file" in
	*BFS*.txt)	python3 ThreeDigits.py B $file; echo -e "BFS \n";;
	*DFS*.txt) python3 ThreeDigits.py D $file; echo -e "DFS \n";;
	*IDS*.txt) python3 ThreeDigits.py I $file; echo -e "IDS \n";;
	*GDY*.txt) python3 ThreeDigits.py G $file; echo -e " GDY \n";;
	*)	break;
esac
echo -e "\n"
echo "-----------";
echo -e "\n"
done
