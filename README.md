##CSTMC Helper

Theses are the files that I use to help me parse the CSMTC datasets

#Usage

	git clone git@github.com:guinslym/cstmc_helper_to_parse_the_dataset.git
	cd cstmc_helper_to_parse_the_dataset
	python2 artefact.py

####artefact.py
Artefact.py will download all the xml file, than it will parse it to create a .json file. Please refer to the **docstring**

	Dependency:
	pip install wget
	pip install bs4
	pip install pprint

####ex-fire.xslt
This stylesheet will transform any XML file into a simplier version.

	import artefact.py as art
	art.simplify_this_dataset(any_dataset.xml_file)

####parsing.py
A loosing time script.... :) I wanted to download all the images from the CSMTC server that are related with the open dataset. Because on my DB I have a column Height and width so In order to know the dimension of the photo I needed to download the images. This file will create 5 thread to download all the pictures... (66000 pics) it took me 15 hours.... And I didn't use the picture... don'T have time for that. So on my db the size field are empty.

	python2 parsing.py


####Seed.rb
A ruby file this was a prototype to cut and paste into the seeds.rb (Rails app)


###voilà!
HackSafe!!!