SEDIR=~/games/space_engine/SpaceEngine/
INFILE=

asp:
	$(MAKE) _run INFILE=kalgash.lp
json:
	$(MAKE) _run INFILE=kalgash.json
customs:
	$(MAKE) _run INFILE=customs.lp


_run:
	python spaceengine.py data/$(INFILE) -o $(SEDIR) --overwrite
