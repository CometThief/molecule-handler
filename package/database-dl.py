import requests
import time
import os
import zlib
import json
import sys

#fetches all tranches
def fetch_zinc(rep="3D", since="", db_r="", format="mol2.gz",using="uri"):
    all_3d_url = "https://zinc.docking.org/tranches/all3D.json"
    download_url = "https://zinc.docking.org/tranches/download"
    r = requests.get(all_3d_url)
    tranches = r.json()

    data = {
        'representation': rep,
        'tranches': ' '.join(x['name'] for x in tranches),
        'format': format,
        'using': using
    }

    r = requests.post(download_url, data=data, stream=True)

    with open('alltranches', 'wb+') as a:
        a.write(r.content)

    open_mol2(r)

#takes list of tranches and treats them individually
def open_mol2(r, WORKING_DIR='tranches'):

    os.makedirs(WORKING_DIR, exist_ok=True)
    counter = 0

    try:
        with open('finished_tranches', 'r') as all_file:
            done_list = set(all_file.read().split())
    except FileNotFoundError:
        done_list = set()

    print('Downloading tranches')

    for x in r.iter_lines():

        if (str(x)) not in done_list:

            #this bit is only to visually confirm current tranche in the terminal
            sys.stdout.write("\033[K")
            print('Current tranche: ', x[36:42],
            'Status: downloading', end='\r')

            #getting each tranche and writing the gz file
            resp = requests.get(x)

            #apparently zinc15 has tons of empty tranches, so this conditional is necessary
            #if server is down then this will assume all tranches are empty
            if(resp.ok):
                current_file_name = os.path.join(WORKING_DIR, x[36:].decode('utf-8'))
                with open (current_file_name, 'wb+') as f:
                    f.write(resp.content)

                #gz_files()
                #zlib test, doesn't work, use gz
                '''with open(current_file_name, 'rb') as f:
                    current_tranche = zlib.decompress(f.read(), zlib.MAX_WBITS|16)
                current_tranche = current_tranche.decode('utf-8').split('\n')
                
                with open ('tmpfile', 'w+') as e:
                    json.dump(current_tranche, e, indent = 4)'''

            #writes to a file with a list of correctly downloaded tranches
            with open('finished_tranches', 'a') as f:
                f.write(str(x) + '\n')

        else:
            print('Current tranche: ', x[36:42],
            'Status: already downloaded', end="\r")

    done_list.close()

#future function for gz file handling
#def gz_files(current_file):

fetch_zinc()
