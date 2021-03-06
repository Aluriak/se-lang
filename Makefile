SEDIR=~/games/space_engine/SpaceEngine/
INFILE=

asp:
	$(MAKE) _run INFILE=kalgash.lp
json:
	$(MAKE) _run INFILE=kalgash.json
customs:
	$(MAKE) _run INFILE=customs.lp
ss:
	$(MAKE) _run INFILE=simple-system.lp


_run:
	python -m selang data/$(INFILE) -o $(SEDIR) --overwrite

release:
	fullrelease
