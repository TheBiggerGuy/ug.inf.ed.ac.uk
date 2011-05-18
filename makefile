
LATEX      = pdflatex
LATEXFLAGS = -file-line-error -halt-on-error -output-format pdf

VERSION = HEAD
VERSION_REP = __GIT_HASH__

all: ug2 ug3
	echo "Making all"

ug2: mi4b
	echo "	Making all UG2"

ug3: car ct cs st dbs
	echo "	Making all UG3"

mi4b:
	echo "		Making mi4b"
	cd ug2/mi4b; \
	cat main.tex | sed -e "s/"$(VERSION_REP)"/"$(VERSION)"/g" | $(LATEX) $(LATEXFLAGS);\
	mv texput.pdf mi4b.pdf

car:
	echo "		Making car"
	cd ug3/car; \
	cat main.tex | sed -e "s/"$(VERSION_REP)"/"$(VERSION)"/g" | $(LATEX) $(LATEXFLAGS);\
	mv texput.pdf car.pdf

ct:
	echo "		Making ct"
	cd ug3/ct; \
	cat main.tex | sed -e "s/"$(VERSION_REP)"/"$(VERSION)"/g" | $(LATEX) $(LATEXFLAGS);\
	mv texput.pdf ct.pdf

cs:
	echo "		Making cs"
	cd ug3/cs; \
	cat main.tex | sed -e "s/"$(VERSION_REP)"/"$(VERSION)"/g" | $(LATEX) $(LATEXFLAGS);\
	mv texput.pdf cs.pdf

st:
	echo "		Making st"
	cd ug3/st; \
	cat main.tex | sed -e "s/"$(VERSION_REP)"/"$(VERSION)"/g" | $(LATEX) $(LATEXFLAGS);\
	mv texput.pdf st.pdf

dbs:
	echo "		Making dbs"
	cd ug3/dbs; \
	cat main.tex | sed -e "s/"$(VERSION_REP)"/"$(VERSION)"/g" | $(LATEX) $(LATEXFLAGS);\
	mv texput.pdf dbs.pdf
