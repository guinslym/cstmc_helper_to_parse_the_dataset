#!/usr/bin/env python3
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
# -*- coding: utf-8 -*-

"""
Goal:
    This module helps the programmer to ease his workflow
    while working with the Canadian Science and Technology Museum datasets

Require:
    Beautiful soup
    wget
    xmlutils

Workflow:
    #download a dataset:
    dataset_name="fire-fighting-lutte-contre-les-incendies.xml"
    wget_this_dataset(dataset_name)
        Optional:
        #simplify this dataset. Will remove all the attributes within the elements (nodes)
        new_dataset_name = simplify_this_dataset(dataset_name)
    #Parse the xml file
    artefacts = xml_clean_the_dataset_for_rails(dataset_name)
       #Optional
       artefacts = xml_clean_the_dataset_for_rails(new_dataset_name)
    #Write a json file for this dataset
       write_a_json_file_for_the_database(artefacts)

Notes: 
    To download the 29 datasets and parse them takes about 26 min.
"""
import wget
import urllib
import os
from lxml import etree
from bs4 import BeautifulSoup
import io
import json
from xmlutils.xml2json import xml2json
from pprint import pprint
import time#benchmark
import datetime
import uuid

#   VARIABLE: DATASET NAME TO BE DOWNLOAD:W

artefacts_dataset =  ['vacuum-tubes-tubes-electronique.xml', 'space-technology-technologie-de-lespace.xml', 
                     'railway-transportation-transports-ferroviaires.xml', 'printing-imprimerie.xml',
                     'physics-physique.xml', 'photography-photographie.xml',
                     'non-motorized-ground-transportation-transports-terrestres-non-motorises.xml',
                     'motorized-ground-transportation-transports-terrestres-motorises.xml',
                     'mining-and-metallurgy-mines-et-metallurgie.xml',
                     'metrology-metrologie.xml', 'medical-technology-technologie-medicale.xml',
                     'meteorology-meteorologie.xml', 'mathematics-mathematiques.xml',
                     'marine-transportation-transports-maritimes.xml',
                     'lighting-technology-technologie-declairage.xml',
                     'industrial-technology-technologie-industrielle.xml',
                     'horology-horlogorie.xml',
                     'forestry-exploitation-forestiere.xml',
                     'fire-fighting-lutte-contre-les-incendies.xml',
                     'fisheries-service-des-peches.xml',
                     'exploration-and-survey-exploration-et-leve.xml',
                     'energy-electric-energie-electrique.xml',
                     'domestic-technology-technologie-domestique.xml',
                     'computing-technology-technologie-informatique.xml',
                     'communications-communications.xml',
                     'chemistry-chimie.xml',
                     'bookbinding-reliure.xml',
                     'aviation-aviation.xml',
                     'astronomy-astronomie.xml',
                     'agriculture-agriculture.xml'
                     ]
#test_db =['bookbinding-reliure.xml','horology-horlogorie.xml']

def wget_this_dataset(dataset_name="fire-fighting-lutte-contre-les-incendies.xml"):
    """Will download with WGET a dataset in your directory."""
    import wget
    print("Downloading : {0}".format(dataset_name))
    if 'artefacts-tout' in dataset_name:
        BASE_URL = 'http://source.techno-science.ca/datasets-donn%C3%A9es/artifacts-artefacts/'
        print('This dataset have a size of 400 MB.. \nThis may take a while to download\n')
    else:
        BASE_URL = 'http://source.techno-science.ca/datasets-donn%C3%A9es/artifacts-artefacts/groups-groupes/'
    file_url = BASE_URL + dataset_name
    try:
        file_name = wget.download(file_url)
        os.rename(file_name, file_name)
    except urllib.error.HTTPError:
        print("Errors can't download this dataset => {0}".format(dataset_name))

def simplify_this_dataset(dataset):
    """Create A simplify version of an xml file
    it will remove all the attributes and assign them as Elements instead
    """
    module_path = os.path.dirname(os.path.abspath(__file__))
    data = open(module_path+'/ex-fire.xslt')
    xslt_content = data.read()
    try:
        xslt_root = etree.XML(xslt_content)
        dom = etree.parse(module_path+'/'+dataset)
        transform = etree.XSLT(xslt_root)
        result = transform(dom)
        new_file_name = dataset.split(".")[0] + "_simplify.xml"
        f = open(module_path+ '/'+new_file_name, 'w')
        f.write((str(result)))
        f.close() 
    except ValueError:
        print("use python2 instead for this function")
    return new_file_name

def xml_to_json(dataset_name):
    """Convert the xml file into a JSON document"""
    module_path = os.path.dirname(os.path.abspath(__file__))
    dataset_name_json = dataset_name+ ".json"
    converter = xml2json(module_path+"/"+dataset_name, module_path+ "/" + dataset_name_json, encoding='utf-8')
    #print(dataset_name_json)
    converter.convert()
    return dataset_name_json

def i18n_this_string(string_value):
    """ This function will return a json object that has
    two attributes. {'fr':'name in french', 'en':'name in english'}

    keywords arguments:
    string_value: a string object within this form:
        "NamOrganisation": "Unknown;:;Inconnu"
        or
        "ObjObjectName": "Press, embossing;:;Presse \u00e0 gaufrer"
    return: a dict
    {'fr':'name in french', 'en':'name in english'}
    """
    string_value = string_value.split(";:;")
    en = string_value[0]
    fr = string_value[1]
    if "," in en:
        en = string_value[0].split(',')
        en = en[1].strip().capitalize() + " " + en[0]
    return {'fr':fr, 'en':en}

def parse_image_links(img, thumb):
    if 'thumb' in img:
        tempo = img
        img = thumb
        thumb = tempo
    return {'image_link':img, 'image_thumbnail':thumb}

def retrieve_image_links(json_object):
    """

    """
    image =  json_object['tuple']['DocIdentifier_tab']['tuple']
    #I know that (len image have 2 links [img, thumbnail]
    img = image[0]['DocIdentifier']
    thumb = image[1]['DocIdentifier']
    #checking if 'img' includes 'thumb' it will means that the link are reversed
    value = parse_image_links(img, thumb)
    return value

def open_the_json_version_of_this(dataset = 'fisheries-service-des-peches.json'):
    json_data = open('fisheries-service-des-peches.json')
    data = json.load(json_data)
    return data

def retrieve_refs(artefact):
    """this function will return all the References (paper, book)
    that are associated with this Artefact

    keywords: 
    artefact = will be the artefact object

    return:
    a list of value or an empty list []
    """
    art_refs = []
    if artefact.get('ArtRefReferences_tab', None):
        art = artefact['ArtRefReferences_tab']['tuple']
        for i in art:
            art_refs.append(art['ArtRefReferences'])
    return art_refs

def retrieve_thesaurus_info(artefact, art_tab, art_field):
    """this function will return all the Info
    that are associated with this Artefact

    keywords: 
    artefact = will be the artefact object

    return:
    a list of value : [{'fr': u'Outils et \xe9quipement', 'en': u'Tools & equipment'}]
    or 
    an empty list []
    """
    art_refs = []
    if artefact.get(art_tab, None):
        art = artefact[art_tab]['tuple']
        if len(art)<2:
            for i in art:
                arte = art[art_field]
                if len(arte) >=2:
                    if ";:;" in arte:
                        arte = i18n_this_string(art[art_field])
                art_refs.append(arte)
        #nested field
        else:
            for i in art:
                for a in i:
                    if ";:;" in i[art_field]:
                        arte = i18n_this_string(i[art_field])
                    art_refs.append(arte)
    return art_refs

def find_the_date_for_this_artefact(d):
    """Return a date

    """
    #By default the date for the Artifact will be the one on the link
    image = retrieve_image_links(d['MulMultiMediaRef_tab'])
    image = image['image_link'].split('/')
    date = image[4].split(".")[0]

    #find if the AssesmentDate is 
    return  date

def find_single_element_value_in_xml(artefact_xml, attribut, not_raw_xml_file=True):
    try:
        if not_raw_xml_file:
            value = artefact_xml.find(attribut).string
        else:
            value = artefact_xml.find(attrs={'name':attribut}).string
    except (NameError, AttributeError):
        value = 'non identifie'
    if ';:;' in value:
        value = i18n_this_string(value)
    return value

def find_images_link_in_xml(artefact_xml, attribut, not_raw_xml_file=True):
    value = []
    if not_raw_xml_file:
        element_value = artefact_xml.find_all(attribut)
    else:
        element_value = artefact_xml.find_all(attrs={'name':attribut})
    for i in element_value:
        value.append(i.string)
    value = parse_image_links(value[0], value[1])
    return value

def find_many_element_value(artefact_xml, attribut, not_raw_xml_file=True):
    value = []
    if not_raw_xml_file:
        element_value = artefact_xml.find_all(attribut)
    else:
        element_value = artefact_xml.find_all(attrs={'name':attribut})
    for i in element_value:
        if ';:;' in i.string:
            value.append(i18n_this_string(i.string))
        else:
            value.append(i.string)
    return value

def this_artefact_contains_at_least_two_images(artefact_xml, attribut, not_raw_xml_file=True ):
    """This function will check if the Node Element has
    at least 2 images links (1:Thumbnail, 1:original_image)

    keywords:
        artefact_xml = a node (element of a dataset)
        attribut = The element that want to make sure that 
            this Node have.
        not_raw_xml_file = If this Node has attributes or not 
            (view:find_if_this_xml_file_has_attributes())
    Return:
        True or False
    """
    value = 0
    try:
        if not_raw_xml_file:
            value = artefact_xml.find_all(attribut)
        else:
            value = artefact_xml.find_all(attrs={'name':attribut})
        value = len(value) 
    except (NameError, AttributeError):
        value = 1
    if value>=2:
        return True
    return False

def find_if_this_xml_file_has_attributes(soup):
    """Return True or False
    if the root element is 'ecatalogue' it will returns True
    That means that I'm dealing with the simplify version of the dataset
    (so there is no attribute)
    keywords: soup
        the root element of the dataset
    Returns:
        True or False
    """
    try:
        a = soup.find('ecatalogue')
        if a:
            the_root_element_has_no_attribute = True
        else:
            the_root_element_has_no_attribute = False
    except (NameError, AttributeError):
        print("error on this table")
    return the_root_element_has_no_attribute

def xml_clean_the_dataset_for_rails(dataset_name):
    artefact_for_db= []
    compte = 0
     #how many object (i.e: 100artifacts/260 total artifacs)
    inner_compte = 0
    soup = BeautifulSoup(open(dataset_name), "xml")
    not_raw_xml_file = find_if_this_xml_file_has_attributes(soup)
    #print(not_raw_xml_file)
    if not_raw_xml_file:
        links = soup.find_all('ObjObjectDiscipline')
    else:
        links = soup.find_all(attrs={'name':'ObjObjectDiscipline'})
    for node in links:
        artefact_xml = node.parent
        if this_artefact_contains_at_least_two_images(artefact_xml, 'DocIdentifier', not_raw_xml_file):
            discipline = find_single_element_value_in_xml(artefact_xml, 'ObjObjectDiscipline', not_raw_xml_file)
            catalogue_number = find_single_element_value_in_xml(artefact_xml, 'ObjCatalogueNumber', not_raw_xml_file)
            objname = find_single_element_value_in_xml(artefact_xml,'ObjObjectName', not_raw_xml_file)
            image_url_links = find_images_link_in_xml(artefact_xml, 'DocIdentifier', not_raw_xml_file)
            group_value = find_many_element_value(artefact_xml, 'ArtLexGroup', not_raw_xml_file)
            categories = find_many_element_value(artefact_xml, 'ArtLexCategory', not_raw_xml_file)
            subcategories = find_many_element_value(artefact_xml, 'ArtLexSubCategory',not_raw_xml_file)
            references_monographie = find_many_element_value(artefact_xml, 'ArtRefReferences', not_raw_xml_file)
            composition_general = find_many_element_value(artefact_xml, 'ArtCompMaterialCHINGeneral', not_raw_xml_file)
            composition_specific = find_many_element_value(artefact_xml, 'ArtCompMaterialCHINSpecific', not_raw_xml_file)
            xml_file_name_index = dataset_name
            #16*8 choice of uuid
            unique_identifier = str(uuid.uuid4())[0:8]
            #date_from = find_many_element_value(artefact_xml, 'ObjManufactureDateFrom', not_raw_xml_file)
            #assesment_date = find_many_element_value(artefact_xml, 'AssAssessmentDate', not_raw_xml_file)
            image_date = ((image_url_links['image_link']).split('/')[4]).split('.')[0]
            a = {'discipline':discipline, 'catalogue_number':catalogue_number, 'objname':objname, 'image':image_url_links}
            a.update({'artefact_references':references_monographie, 'artefacts_group':group_value, 'artefacts_categorie':categories})
            a.update({'artefacts_sub_categorie':subcategories, 'artefacts_composition_general':composition_general})
            a.update({'artefacts_composition_specific':composition_specific, 'assigned_date':image_date})
            a.update({'dataset_name': xml_file_name_index})
            artefact_for_db.append(a)
            compte= compte+1
            inner_compte = inner_compte + 1
            #print(a)
        compte=compte+1
    print("{0}/{1}".format(inner_compte, compte))
    return artefact_for_db

def write_a_json_file_for_the_database(artefact, dataset_name):
    with io.open("rails_"+dataset_name+'.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(artefact, ensure_ascii=True, indent=4 )))

def main():
    number_of_dataset_to_download = len(artefacts_dataset)
    for dataset_name in artefacts_dataset:
        print("\t---Dataset {0}/{1}--".format((artefacts_dataset.index(dataset_name)+1), number_of_dataset_to_download))
        #wget_this_dataset(dataset_name)
        print("\t---Parsing this dataset...")
        artefacts = xml_clean_the_dataset_for_rails(dataset_name)
        write_a_json_file_for_the_database(artefacts, dataset_name)
#----------------------------------------------------------------------
if __name__ == "__main__":
    start_time = time.time()
    main()
    seconds = (time.time() - start_time)
    time_in_total = str(datetime.timedelta(seconds))
    print("Time took to download\nall the dataset => {0}".format(time_in_total))

