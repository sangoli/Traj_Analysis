import os


def create_struct(ls):
    for dir in ls:
        if not os.path.exists(dir):
             os.mkdir(dir)

ls=['consolidated_csv','parsed_data','structure','exclusions','figures','heatmapsbydate','data']
create_struct(ls)
