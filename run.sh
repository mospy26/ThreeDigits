command="python3 ThreeDigits.py B "

for file in ./tests/*.txt;
do
case "$file" in
	*BFS*.txt)	python3 ThreeDigits.py B $file;;
	*)	break;
esac
echo -e "\n"
echo "-----------";
echo -e "\n"
done
