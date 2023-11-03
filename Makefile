test:
	./main.py Heisig.txt N5N4.csv
	diff ref.txt Heisig_reordered.txt
