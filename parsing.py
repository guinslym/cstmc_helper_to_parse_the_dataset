import urllib2
import json
from pprint import pprint
from threading import Thread
import os
import time#benchmark
import datetime

#contains all the noun found url
not_found_url = []
temporary_holder = []
data_list_json= []

def create_a_list_of_list(data):
    final_list=[]
    b =[]
    # You don't need `a` to be a list here, just iterate the `range` object
    for num in data:
        if len(b) < 5:
            b.append(num)
        else:
            # Add `b` to `final_list` here itself, so that you don't have
            # to check if `b` has 3 elements in it, later in the loop.
            final_list.append(b)

            # Since `b` already has 3 elements, create a new list with one element
            b = [num]

    # `b` might have few elements but not exactly 3. So, add it if it is not empty
    if len(b) != 0:
        final_list.append(b)

    return final_list


def download_image(url):
    url = url['image']['image_link']
    print(url)
    file_name = url.split('/')[-1]
    try:
        u = urllib2.urlopen(url)
        f = open("images/"+file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()
    except urllib2.HTTPError, URLError:
        print("error not a valid url")
        not_found_url.append(url)
        temporary_holder.append(url)



def parse_this_json_file(file):
    json_data=open('json/'+ file)
    data = json.load(json_data)
    data_list_json = create_a_list_of_list(data)
    #print(data_list_json)
    json_data.close()
    send_this_data_to_the_thread_function(data_list_json)


def send_this_data_to_the_thread_function(data_list_json):
    for list_of_list in data_list_json:
        threadlist = []
        #for u in list_of_list:
        #download_image(u)
        for u in list_of_list:
            t = Thread(target=download_image, args=(u,))
            t.start()
            threadlist.append(t)
        for b in threadlist:
            b.join()
        

def cleaning_this_directory():
    """After downloading all the XML dataset
    and after parsing the xml file to be able to create a
    json file. This FUNCTION will move all the .xml and .json
    to the directory ./json or ./xml
    """
    import os, shutil
    files = os.listdir(".")
    for f in files:
        if os.path.isfile(f):
            extension = f.split(".")[-1]
            if extension == 'jpg':
                #move the file
                os.rename(f, "images/"+f)
            elif extension == 'JPG':
                #move to xml file
                os.rename(f, 'xml/'+f)
            else:
                pass

def rewrite_this_dataset(file_name):
	  """
    I need to 
	  """
	  for data in data_list_json:
	      uid = data['unique_identifier']
	      for a in temporary_holder:
	      	  if a['unique_identifier'] == uid:
	      	  	  data_list_json.remove(data)
	  write_a_json_file_for_the_database(data_list_json, file_name)

def write_a_json_file_for_the_database(artefact, dataset_name):
    with io.open(dataset_name, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(artefact, ensure_ascii=True, indent=4 )))

def main():
    files = os.listdir('json')
    for f in files[::]:
        print(f)
        temporary_holder =[]
        if os.path.isfile("json/"+f):
            parse_this_json_file(f)
        if len(temporary_holder)>0:
            rewrite_this_dataset(f)
    write_a_json_file_for_the_database(not_found_url, 'not_found_url.json')
    cleaning_this_directory()

#----------------------------------------------------------------------
if __name__ == "__main__":
    start_time = time.time()
    main()
    seconds = (time.time() - start_time)
    time_in_total = str(datetime.timedelta(seconds=seconds))
    print("Time took to download\nall the dataset => {0}".format(time_in_total))