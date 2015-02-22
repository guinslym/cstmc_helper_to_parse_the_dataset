from bs4 import BeautifulSoup
import urllib2
import requests
import re
import json
import os
import shutil
import time
import io
from PIL import Image, ImageStat
import operator
import string
import random
import urllib, cStringIO

def link_to_download(link):
    data_url = link
    data_page = urllib2.urlopen(data_url)
    soup = BeautifulSoup(data_page, "xml")
    return soup

#find the discipline
def find_single_element_value(artefact_xml, attribut):
    try:
        value = artefact_xml.find(attrs={'name':attribut}).string 
    except (NameError, AttributeError):
        value = 'non identifie'
    return value

def find_many_element_value(artefact_xml, attribut):
    value = []
    element_value = artefact_xml.find_all(attrs={'name':attribut})
    for i in element_value:
        value.append(i.string)
    return value

def create_artefact_dict(links, dataset_name):
    artefacts =[]
    for node in links:
        elem_attribute = []
        artefact_xml = node.parent
        discipline = find_single_element_value(artefact_xml, 'ObjObjectDiscipline')
        #print("{0} ==> {1}".format(dataset_name, discipline))
        discipline = find_language(discipline)
        catalogue_number = find_single_element_value(artefact_xml, 'ObjCatalogueNumber')
        #print("{0} ==> {1} ==> {2}".format(dataset_name, discipline, catalogue_number))
        objname = find_single_element_value(artefact_xml,'ObjObjectName')
        #print("objname =>")
        #print(objname)
        objname = find_language(objname)
        #print("{0} ==> {1} ==> {2}".format(dataset_name, objname, catalogue_number))
        #elements has many children
        group_value = find_many_element_value(artefact_xml, 'ArtLexGroup')
        group_value = find_languages(group_value)
        categories = find_many_element_value(artefact_xml, 'ArtLexCategory')
        categories = find_languages(categories)
        subcategories = find_many_element_value(artefact_xml, 'ArtLexSubCategory')
        subcategories = find_languages(subcategories)
        #image_links = find_many_element_value(artefact_xml, 'DocIdentifier')
        #'''#removing size info
        image_links = []
        image_url_links = find_many_element_value(artefact_xml, 'DocIdentifier')
        image_links.append(image_url_links)
        if (len(image_url_links) > 1):
            img_info = image_information(image_url_links[0])
            image_links.append(img_info)
        #'''
        couleurs = find_many_element_value(artefact_xml, 'ArtRefImage')
        couleurs = find_languages(couleurs)
        references_monographie = find_many_element_value(artefact_xml, 'ArtRefReferences')
        composition_general = find_many_element_value(artefact_xml, 'ArtCompMaterialCHINGeneral')
        composition_general = find_languages(composition_general)
        composition_specific = find_many_element_value(artefact_xml, 'ArtCompMaterialCHINSpecific')
        composition_specific = find_languages(composition_specific)
        date_from = find_many_element_value(artefact_xml, 'ObjManufactureDateFrom')
        assesment_date = find_many_element_value(artefact_xml, 'AssAssessmentDate')
        date_from = find_many_element_value(artefact_xml, 'ObjManufactureDateFrom')
        #print(assesment_date)
        #print('-'*7)
        a = {'discipline':discipline, 'catalogue_number':catalogue_number, 'objname':objname, 
             'group_value': group_value, 'categories':categories, 'subcategories':subcategories,
             'image_links': image_links, 'references_monographie': references_monographie,
             'composition_general': composition_general, 'composition_specific': composition_specific,
             'assesment_date': assesment_date, 'dataset_name': dataset_name, 'date_from':date_from,
             'color': couleurs}
        if not (len(image_url_links) == 0):
            artefacts.append(a)
            print(dataset_name + " : index => " + str(artefacts_dataset.index(dataset_name)))
    return artefacts


def find_image_information(image_link):
    file = cStringIO.StringIO(urllib.urlopen(image_link).read())
    img = Image.open(file)
    width, height = img.size
    #color = detect_color_image(image_link)
    size = [{'width':width, 'height':height, 'landscape': width > height}]
    return size
    
#find_image_information('http://source.techno-science.ca/images/1991.0593.001.aa.cs.thumb.jpg')

def image_information(url):
    if not 'http' in url:
        return False
    try:
        4+5
        #file = cStringIO.StringIO(urllib.urlopen(url).read())
    except IOError:
        return False
    try:
        3+4
        #im=Image.open(file)
    except IOError:
        return False
    width = 340
    height = 345
    size = [{'width':width, 'height':height, 'landscape': width > height}]
    return size

def find_language(valeur):
    #print(valeur)
    if not ':' in valeur:
        return valeur
    en, fr = valeur.split(':')
    en = en.replace(';' ,' ').strip()
    fr = fr.replace(';' ,' ').strip()
    if (len(en.split(',')) > 1):
        en = en.split(',')
        en = en[1] + ' ' + en[0]
        en = en.strip().capitalize()
    language = {}
    language.update({'en':en, 'fr':fr})
    #print(language)
    return(language)

def find_languages(group_value):
    result =[]
    for i in group_value:
        result.append(find_language(i))
    return result


#detecting image color
#http://stackoverflow.com/questions/20068945/detect-if-image-is-color-grayscale-or-black-and-white-with-python-pil
def detect_color_image(file, thumb_size=40, MSE_cutoff=22, adjust_color_bias=True):
    file = cStringIO.StringIO(urllib.urlopen(file).read())
    pil_img = Image.open(file)
    bands = pil_img.getbands()
    if bands == ('R','G','B') or bands== ('R','G','B','A'):
        thumb = pil_img#.resize((thumb_size,thumb_size))
        SSE, bias = 0, [0,0,0]
        if adjust_color_bias:
            bias = ImageStat.Stat(thumb).mean[:3]
            bias = [b - sum(bias)/3 for b in bias ]
        for pixel in thumb.getdata():
            mu = sum(pixel)/3
            SSE += sum((pixel[i] - mu - bias[i])*(pixel[i] - mu - bias[i]) for i in [0,1,2])
        MSE = float(SSE)/(thumb_size*thumb_size)
        if MSE <= MSE_cutoff:
            return 'gs'##print "grayscale\t",
        else:
            return 'cl'##print "Color\t\t\t",
        #print "( MSE=",MSE,")"
        pass
    elif len(bands)==1:
        return 'bw'#pass##print "Black and white", bands
    else:
        return 'unknow'#pass#print "Don't know...", bands
    
#detect_color_image('http://source.techno-science.ca/images/1991.0593.001.aa.cs.thumb.jpg')

def bytestomegabytes(bytes):
    return (bytes / 1024) / 1024

def kilobytestomegabytes(kilobytes):
    return kilobytes / 1024


url  = 'http://source.techno-science.ca/datasets-donn%C3%A9es/artifacts-artefacts/groups-groupes/'
artefacts_dataset =  [
'non-motorized-ground-transportation-transports-terrestres-non-motorises.xml',
'forestry-exploitation-forestiere.xml'

                     ]
"""
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
                     'fire-fighting-lutte-contre-les-incendies.xml'
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
"""
#non-motorized-ground-transportation-transports-terrestres-non-motorises.xml
# 'forestry-exploitation-forestiere.xml',

artefact_node = []
artefact_short_version = []
for dataset in artefacts_dataset:
    root = link_to_download(url+dataset)
    links = root.find_all(attrs={'name':'ObjObjectDiscipline'})
    art_node = create_artefact_dict(links, dataset)
    artefact_node.append(art_node)
    artefact_short_version.append(art_node)
    with io.open('json/' + dataset + '.json', 'w', encoding='utf-8') as f:
    	  f.write(unicode(json.dumps(artefact_short_version, ensure_ascii=True )))
    
#print(artefact_node)
with io.open('artefact_generate.json', 'w', encoding='utf-8') as f:
  f.write(unicode(json.dumps(artefact_node, ensure_ascii=True, indent=4 )))
    
print('done')
