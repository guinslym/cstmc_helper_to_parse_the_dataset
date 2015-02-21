require 'json'
require 'yaml'



=begin 
a = {'discipline':discipline, 'catalogue_number':catalogue_number, 'objname':objname, 'image':image_url_links}
a.update({'artefact_references':references_monographie, 'artefacts_group':group_value, 'artefacts_categorie':categories})
a.update({'artefacts_sub_categorie':subcategories, 'artefacts_composition_general':composition_general})
a.update({'artefacts_composition_specific':composition_specific, 'assigned_date':image_date})
=end

Artifact.delete_all

files =  Dir.entries("db/artefact_seed/")
files.each do |n|
  if n.size < 5
    files.delete(n)
  end
end


def populate_array(data, language)
  cummulator  = []
  data.each {|n| cummulator.push(n[language])}
  return cummulator
end

def parse_the_json_file_to_db(json_file_name)
  file = File.read("db/artefact_seed/"+json_file_name)
  data_hash = JSON.parse(file)

  data_hash.each do |data|
    #artifact = Artifact.create(
    artifact = Artifact.create(
discipline_en: data['discipline']['en'],
discipline_fr: data['discipline']['fr'],
catalogue_number: data['catalogue_number'],
image_original: data['image']['image_link'],
image_thumbnail: data['image']['image_thumbnail'],
artifact_group_en: populate_array(data['artefacts_group'], 'en'),
artifact_group_fr: populate_array(data['artefacts_group'], 'fr'),
artifact_category_en:  populate_array(data['artefacts_categorie'], 'en'),
artifact_category_fr:  populate_array(data['artefacts_categorie'], 'fr'),
artifact_sub_category_en: populate_array(data['artefacts_sub_categorie'], 'en'),
artifact_sub_category_fr: populate_array(data['artefacts_sub_categorie'], 'fr'),
artifact_composition_general_en: populate_array(data['artefacts_composition_general'], 'en'),
artifact_composition_general_fr: populate_array(data['artefacts_composition_general'], 'fr'),
artifact_composition_specific_en: populate_array(data['artefacts_composition_specific'], 'en'),
artifact_composition_specific_fr: populate_array(data['artefacts_composition_specific'], 'fr'),
artifact_date: data['assigned_date'],
objname_en: data['objname']['en'],
objname_fr: data['objname']['fr'],
artifact_references: data['artefact_references'],
art_dataset_name: data['dataset_name']
     )
    puts artifact
    #Create it in the db
  end#data_hash.each
end#def

files.first(2).each {|f| parse_the_json_file_to_db(f) }


=begin 
#field to create in rails
rails g scaffold artifact art_dataset_name discipline_en discipline_fr catalogue_number image_original image_thumbnail artifact_group_en artifact_group_fr artifact_category_en artifact_category_fr artifact_sub_category_en artifact_sub_category_fr artifact_composition_general_en artifact_composition_general_fr artifact_composition_specific_en artifact_composition_specific_fr artifact_date objname_en objname_fr artifact_references
=end

#I need to create a mongodb rails app
	