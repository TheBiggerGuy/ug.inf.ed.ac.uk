
LATEX      = pdflatex
LATEXFLAGS = -file-line-error -halt-on-error -output-format pdf

all: ug2 ug3
	echo "Making all"

ug2: mi4b
	echo "	Making all UG2"

ug3: car ct cs dbs
	echo "	Making all UG3"

mi4b:
	echo "		Making mi4b"
	cd ug2/mi4b; \
	$(LATEX) $(LATEXFLAGS) main.tex;\
	mv main.pdf mi4b.pdf

car:
	echo "		Making car"
	cd ug3/car; \
	$(LATEX) $(LATEXFLAGS) main.tex;\
	mv main.pdf car.pdf

ct:
	echo "		Making ct"
	cd ug3/ct; \
	$(LATEX) $(LATEXFLAGS) main.tex;\
	mv main.pdf ct.pdf

cs:
	echo "		Making cs"
	cd ug3/cs; \
	$(LATEX) $(LATEXFLAGS) main.tex;\
	mv main.pdf cs.pdf

dbs:
	echo "		Making dbs"
	cd ug3/dbs; \
	$(LATEX) $(LATEXFLAGS) main.tex;\
	mv main.pdf dbs.pdf
