#!/usr/bin/env python3
from pprint import pprint
from subprocess import check_output as bash
import unicodedata

import sys
import re


def remove_capital__accents(string):
    # Normalizar y eliminar acentos
    normalized_string = ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))

    # Convertir a minúsculas
    final_string = normalized_string.lower()

    return final_string

def find_boxes(f_data, i_LINES_start):
    for i_line_start in i_LINES_start:
        i_line_end           = i_line_start 
        i_line_start_p       = 0
        i_line_end_p         = 0
        i_line_start_details = 0
        i_line_end_details   = 0
        
        found = False
        while not found:

            if "<details><summary>" in f_data[i_line_end]:
                i_line_start_details = i_line_end
            elif "</details>"       in f_data[i_line_end]:
                i_line_end_details   = i_line_end
            elif "<p"               in f_data[i_line_end]:
                i_line_start_p       = i_line_end
            elif "</p></div>"       in f_data[i_line_end]:
                i_line_end_p         = i_line_end
                found = True
            elif "</p>"             in f_data[i_line_end]:
                i_line_end_p         = i_line_end
            elif "</div>"           in f_data[i_line_end]:
                found = True
            
            i_line_end += 1
        i_line_end -= 1       

        ########################
        ######## TITLE 

        i_line_title = i_line_start + 1
        line_title   = f_data[i_line_title]
        
        # Esta expresión es para borrar los espacios       
        # title_no_clean_aux = e.sub(r'"(.*?)"', 
        #                     lambda x: x.group(0).replace(' ', ''), line_title)
    
        title_no_clean = re.search(r'"([^"]*)"', line_title).group(1)
        title = re.sub(r'<.*?>', '', title_no_clean.split(':')[0])   #  +'\\n",\n'
        title_lowercase = remove_capital__accents(title)
        
        
        ########################
        ######## Prints y asserts

        assert i_line_start_p       <= i_line_end_p, f"Problems findins <p>, {i_line_start_p} and </p> {i_line_end_p}"
        assert i_line_start_details <= i_line_end_details, f"Problems findins <details>, {i_line_start_p} and </details> {i_line_end_p}"
        
        print(i_line_start,             {f_data[i_line_start]})

        if i_line_start_p > 0:
            assert i_line_start <= i_line_start_p < i_line_end_p <= i_line_end
            if i_line_start < i_line_start_p:
                print(i_line_start_p,   {f_data[i_line_start_p]})
        
        print(i_line_title,             {title}, title_lowercase)
        
        if i_line_start_details > 0:
            assert i_line_start < i_line_start_details < i_line_end_details < i_line_end
            print(i_line_start_details, {f_data[i_line_start_details]})
            print(i_line_end_details,   {f_data[i_line_end_details]})
        
        if i_line_end_p > 0:
            if i_line_end > i_line_end_p:
                print(i_line_end_p,   {f_data[i_line_end_p]})

        print(i_line_end,               {f_data[i_line_end]})
        print("===============================================================")

        with open("pruebas_write.txt", 'a') as f_out:
            f_out.write(f_data[i_line_start])
            f_out.write(title)
            f_out.write(f_data[i_line_end])

file_name = sys.argv[1:][0]
print("===========================")
print("File = ", file_name)
print("===========================")

#command_line_start_alert_info   = '($(grep -n "<div class=" '+file_name+'| grep "alert alert-block alert-info" |  cut -d":" -f1))'
command_i_LINES_start_alert_info   = 'grep -n "<div class=" '+file_name+'| grep "alert alert-block alert-info" |  cut -d":" -f1'
command_i_LINES_start_alert_danger = 'grep -n "<div class=" '+file_name+'| grep "alert alert-block alert-danger" |  cut -d":" -f1'

command_i_LINES_start_alert_details = 'grep -n "<details><summary>" '+file_name+'| grep "alert alert-block alert-danger" |  cut -d":" -f1'

#print(command_line_start_alert_info)
#print(command_line_start_alert_danger)

out_i_LINES_start_alert_info   = bash(command_i_LINES_start_alert_info  , shell=True).decode("utf-8")
out_i_LINES_start_alert_danger = bash(command_i_LINES_start_alert_danger, shell=True).decode("utf-8")


i_LINES_start_alert_info = []
for line in out_i_LINES_start_alert_info.splitlines():
    i_LINES_start_alert_info.append(int(line)-1)


i_LINES_start_alert_danger = []
for line in out_i_LINES_start_alert_danger.splitlines():
    i_LINES_start_alert_danger.append(int(line)-1)




with open(file_name, 'r') as f:
    #f_data = f.read()
    #print(f_data[20])

    f_data=[]
    for line in f:
        #print(line)
        f_data.append(line)
    
    with open("pruebas_write.txt", 'w') as f_out:
        f_out.write("Pruebas:\n")
    
    find_boxes(f_data, i_LINES_start_alert_info)
    find_boxes(f_data, i_LINES_start_alert_danger)


    