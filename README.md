##CSTMC Helper

These are the files that I use to help me parse the CSMTC datasets

#Usage

	git clone git@github.com:guinslym/cstmc_helper_to_parse_the_dataset.git
	cd cstmc_helper_to_parse_the_dataset
	python2 artefact.py

####artefact.py
Artefact.py will download all the xml file, than it will parse it to create a .json file.
	Dependency:
	pip install wget
	pip install bs4
	pip install pprint

####ex-fire.xslt
This stylesheet will transform any XML file into a simplier version.
	import artefact.py as art
	art.simplify_this_dataset(any_dataset.xml_file)

####Seed.rb
A ruby file this was a prototype to cut and paste into the seeds.rb (Rails app)


###voilà!
HackSafe!!!