#!/usr/bin/env python3
#from pprint import pprint
from subprocess import check_output as bash
import unicodedata

import sys
import re

def grep_file_index(grep_command):
    
    out_grep_command = bash(grep_command, shell=True).decode("utf-8")

    index_Lines = []
    for line in out_grep_command.splitlines():
        index_Lines.append(int(line)-1)
    
    return index_Lines

def remove_capital__accents(string):
    # Normalizar y eliminar acentos
    normalized_string = ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))

    # Convertir a minúsculas
    final_string = normalized_string.lower()

    return final_string

def find_boxes(f_data, i_LINES_start):
    i_line_end_list           = [] 
    i_line_start_list         = []
    i_line_start_p_list       = []
    i_line_end_p_list         = []
    i_line_start_details_list = []
    i_line_end_details_list   = []
    i_line_title_list         = []
    title_details_list        = []
    title_list                = []
    title_lowercase_list      = []
    subtitle_list             = []


    i_line_end_last_iteration = 0
    for i_line_start in i_LINES_start:

        assert i_line_end_last_iteration < i_line_start, f"{i_line_end_last_iteration} < {i_line_start} The previous box ends after the begining of the next one"

        i_line_end           = i_line_start 
        i_line_start_p       = 0
        i_line_end_p         = 0
        i_line_start_details = 0
        i_line_end_details   = 0
        i_line_title         = 0
        
        title_details   = "NONE"
        subtitle        = "NONE"
        title           = "NONE"
        title_lowercase = "NONE"
        subtitle        = "NONE"
                
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
            elif "<b>"              in f_data[i_line_end] and i_line_title == 0:
                i_line_title         = i_line_end
            elif "</div>"           in f_data[i_line_end]:
                found = True
            
            i_line_end += 1
        i_line_end -= 1       

        i_line_end_last_iteration = i_line_end
        ########################
        ######## TITLE 

        line_title   = f_data[i_line_title]
        
        # Esta expresión es para borrar los espacios       
        # title_no_clean_aux = e.sub(r'"(.*?)"', 
        #                     lambda x: x.group(0).replace(' ', ''), line_title)

        title_no_clean = re.search(r'"([^"]*)"', line_title).group(1)
        title = re.sub(r'<.*?>', '', title_no_clean.split(':')[0]).strip()   #  +'\\n",\n'
        title_lowercase = remove_capital__accents(title).strip()
        
        ########################
        ######## SUB-TITLE 

        if "<i>" in f_data[i_line_title]:
            subtitle_no_clean = re.search(r'<i>(.*?)</i>', f_data[i_line_title])
            subtitle = subtitle_no_clean.group(1)             

        
        ########################
        ######## #prints y asserts

        #assert i_line_start_p       <= i_line_end_p, f"Problems findins <p>, {i_line_start_p} and </p> {i_line_end_p}"
        #assert i_line_start_details <= i_line_end_details, f"Problems findins <details>, {i_line_start_p} and </details> {i_line_end_p}"
        
        print(i_line_start,             {f_data[i_line_start]})

        if i_line_start_p > 0:
            assert i_line_start <= i_line_start_p < i_line_end, f"{i_line_start} <= {i_line_start_p} < {i_line_end}"
            if i_line_start < i_line_start_p:
                print(i_line_start_p,   {f_data[i_line_start_p]})
        
        print(i_line_title,  title, title_lowercase, subtitle)
        
        if i_line_start_details > 0:
            assert i_line_start < i_line_start_details <= i_line_end, f"{i_line_start} < {i_line_start_details} <= {i_line_end}"

            ###### Title details:
            title_details = re.search(r'<i>(.*?)</i>', f_data[i_line_start_details]).group(1)

            #print(i_line_start_details, {f_data[i_line_start_details]})
            print("")
            print(i_line_start_details, {f_data[i_line_start_details]} , title_details)

        if i_line_end_details > 0:
            
            assert i_line_start < i_line_start_details < i_line_end_details <= i_line_end, f"{i_line_start} < {i_line_start_details} < {i_line_end_details} <= {i_line_end}"
            
            print(i_line_end_details,   {f_data[i_line_end_details]})
        
        if i_line_end_p > 0:
            
            assert i_line_start <= i_line_start_p < i_line_end_p <= i_line_end, f"{i_line_start} <= {i_line_start_p} < {i_line_end_p} <= {i_line_end}"
            
            if i_line_end > i_line_end_p:
                print(i_line_end_p,   {f_data[i_line_end_p]})

        print("")
        print(i_line_end,               {f_data[i_line_end]})
        print("===============================================================")
        
        if not title == "NONE":

            i_line_end_list.append(i_line_end) 
            i_line_start_list.append(i_line_start) 
            i_line_start_p_list.append(i_line_start_p) 
            i_line_end_p_list.append(i_line_end_p) 
            i_line_start_details_list.append(i_line_start_details) 
            i_line_end_details_list.append(i_line_end_details) 
            i_line_title_list.append(i_line_title) 
            title_details_list.append(title_details) 
            title_list.append(title) 
            title_lowercase_list.append(title_lowercase) 
            subtitle_list.append(subtitle)
    
    index_list_list = [i_line_start_list, 
                       i_line_end_list,
                       i_line_start_p_list, 
                       i_line_end_p_list, 
                       i_line_start_details_list, 
                       i_line_end_details_list, 
                       i_line_title_list]

    titles_list_list = [title_details_list, title_list, title_lowercase_list, subtitle_list]
        
    return index_list_list, titles_list_list


def my_replace(f_data, i_line, new_text):

    #print("------> ", new_text)

    # Encontrar la posición de la primera comilla doble
    index_firts_quote = f_data[i_line].find('"')

    # Realizar la sustitución
    f_data[i_line]= f_data[i_line][:index_firts_quote + 1] +new_text 
        #f_data[i_line_start_p][f_data[i_line_start_p].find('\n', indice_primera_comilla + 1):] 



def build_admonition_box(i, f_data, Class):

    i_line_start         = index_list_list[0][i]  # 1
    i_line_end           = index_list_list[1][i]  # 7
    i_line_start_p       = index_list_list[2][i]  # 1,2
    i_line_end_p         = index_list_list[3][i]
    i_line_start_details = index_list_list[4][i]
    i_line_end_details   = index_list_list[5][i]
    i_line_title         = index_list_list[6][i]
       
    title_details   = titles_list_list[0][i]
    title           = titles_list_list[1][i]
    #title_lowercase = titles_list_list[2][i]
    subtitle        = titles_list_list[3][i]
    

    #print("===================================================================")

    #print(f"{i_line_start},{i_line_start_p},{i_line_title},{i_line_start_details},{i_line_end_details},{i_line_end_p},{i_line_end}")
    
    #print("")
    for i in range(i_line_end-i_line_start+1):
        print({f_data[i_line_start+i]})
    print("")

    ############################################################################
    ######## </div> o </p></div>

    ##print(i_line_end, {f_data[i_line_end]})    
    my_replace(f_data, i_line_end, '::::'+'\\n"\n' )
    #print(i_line_end, {f_data[i_line_end]})  

    if i_line_end_p > 0:
        ##############################
        ######## </p>
        if i_line_end > i_line_end_p:
            #print(i_line_end_p,   {f_data[i_line_end_p]})
            my_replace(f_data, i_line_end_p, ''+'\\n",\n' )
            #print(i_line_end_p,   {f_data[i_line_end_p]})


    if i_line_end_details > 0:
        ##############################
        ######## </details>
        if i_line_end > i_line_end_details:
            #print(i_line_end_details,   {f_data[i_line_end_details]})
            my_replace(f_data, i_line_end_details, ':::'+'\\n",\n')
            #print(i_line_end_details,   {f_data[i_line_end_details]})

    if i_line_start_details > 0:
        ##############################
        ######## <detail>
        #print("")
        #print(i_line_start_details, {f_data[i_line_start_details]} , title_details)
        my_replace(f_data, i_line_start_details, ':::{dropdown} '+ title_details+'\\n",\n')
        #print(i_line_start_details, {f_data[i_line_start_details]})


    #print(i_line_title,  {f_data[i_line_title]})
    my_replace(f_data, i_line_title, ':class:'+Class+'\\n",\n')
    #print(i_line_title,  {f_data[i_line_title]})
    
    if i_line_start_p > 0:
        ##############################
        ######## <p style=...>

        if i_line_start < i_line_start_p:
            #print(i_line_start_p,   {f_data[i_line_start_p]})
            my_replace(f_data, i_line_start_p, ''+'\\n",\n')
            #print(i_line_start_p,   {f_data[i_line_start_p]})

    ##############################
    ######## TITLE and <div class...> o <div class...><p style...>
    
    if subtitle == "NONE":
        #print(i_line_start,             {f_data[i_line_start]})
        my_replace(f_data, i_line_start, '::::{admonition} '+ title+'\\n",\n')
        #print(i_line_start,             {f_data[i_line_start]})
    else:
        #print(i_line_start,             {f_data[i_line_start]})
        my_replace(f_data, i_line_start, '::::{admonition} '+ title + '(' + subtitle + ')'+'\\n",\n')
        #print(i_line_start,             {f_data[i_line_start]})

    print("")
    for i in range(i_line_end-i_line_start+1):
        print({f_data[i_line_start+i]})
    #print("")


file_name = sys.argv[1:][0]
print("===========================")
print("File = ", file_name)
print("===========================")


#command_i_LINES_start_alert_info   = 'grep -n "<div class=" '+file_name+'| grep "alert alert-block alert-info" |  cut -d":" -f1'
#command_i_LINES_start_alert_danger = 'grep -n "<div class=" '+file_name+'| grep "alert alert-block alert-danger" |  cut -d":" -f1'
#command_i_LINES_start_alert_success = 'grep -n "<div class=" '+file_name+'| grep "alert-block alert-success" |  cut -d":" -f1'


command_i_Lines_start_alert   = 'grep -n "<div class=" '+file_name+'| grep "alert alert-block alert" |  cut -d":" -f1'
i_Lines_start_alert = grep_file_index(command_i_Lines_start_alert)

with open(file_name, 'r') as f:
    #f_data = f.read()
    ##print(f_data[20])

    f_data=[]
    for line in f:
        ##print(line)
        f_data.append(line)
    

    
    index_list_list, titles_list_list = find_boxes(f_data, i_Lines_start_alert)

    #print(index_list_list)
    #print(titles_list_list)

    for i in reversed(range(len(index_list_list[0]))):


        title_lowercase = titles_list_list[2][i]        

        #if 'definicion' in title_lowercase:
        #    build_card_box(i)
        #elif 'teorema' in title_lowercase:
        #    build_card_box(i)
        #elif 'lema' in title_lowercase:
        #    build_card_box(i)
            
        if 'nota' in title_lowercase:
            build_admonition_box(i, f_data, Class = "note")
        elif 'ejercicio' in title_lowercase:
            build_admonition_box(i, f_data, Class = "tip")
        elif 'ejemplo' in title_lowercase:
            build_admonition_box(i, f_data, Class = "tip")



################################################################################
###### Guardamos los cambios en un nuevo fichero

out_file = file_name[:-5]+'_lab.ipynb'

with open(out_file, 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])


################################################################################
###### Eliminamos los </br>

clean_br_command = "sed -i 's/<br>//g' " + out_file
bash(clean_br_command, shell=True).decode("utf-8")

################################################################################
##### Eliminamos la primera celda y añadimos las dos celdas de título

number_line_head = str(int(bash('grep -n "^  }," Firts_cells.ipynb |  cut -d":" -f1 | head -n 2 | tail -n 1' , shell=True).decode("utf-8")))

bash('head -n ' +number_line_head+' Firts_cells.ipynb ' +' > ' + out_file + '_clean' , shell=True).decode("utf-8")

number = str(int(bash('grep -n "^  }," ' + out_file + ' |  cut -d":" -f1 | head -n 1', shell= True).decode("utf-8")) +1)

bash('tail -n +' + number + ' ' + out_file  +' >> ' + out_file + '_clean', shell=True).decode("utf-8")
bash('mv ' +  out_file + '_clean ' + out_file, shell=True).decode("utf-8")




'''
def build_card_box():
'''



        
    
        

    

    
