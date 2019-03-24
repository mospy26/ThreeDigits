command="python3 ThreeDigits.py B "

for file in ./tests/*.txt;
do
case "$file" in
	*BFS*.txt)	python3 ThreeDigits.py B $file; echo -e "\n";;
	*DFS*.txt) python3 ThreeDigits.py D $file; echo -e "\n";;
	*IDS*.txt) python3 ThreeDigits.py I $file; echo -e "\n";;
	*GDY*.txt) python3 ThreeDigits.py G $file; echo -e "\n";;
	*)	break;
esac
echo -e "\n"
echo "-----------";
echo -e "\n"
done
