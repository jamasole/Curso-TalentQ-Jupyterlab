line_start_def_the_lem=($(grep -n "<div class=" 111_Cubits.ipynb | grep "alert alert-block alert-info" |  cut -d':' -f1))

line_start_note=($(grep -n "<div class=" 111_Cubits.ipynb | grep "alert alert-block alert-danger" |  cut -d':' -f1))

