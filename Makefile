SEDIR=~/games/space_engine/SpaceEngine/

asp:
	python spaceengine.py data/kalgash.lp -o $(SEDIR) --overwrite
json:
	python spaceengine.py data/kalgash.json -o $(SEDIR) --overwrite
