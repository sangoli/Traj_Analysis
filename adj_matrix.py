import pandas as pd

def create_adj_matrix(n):
    adj_mat = [[False] * n for y in range(n)]
    print("Creating new matrix of size", n, "x", len(adj_mat[0]))
    return adj_mat


def load_mat(filename, n):
    df = pd.read_csv(filename)
    df['date_from_key'] = df['Tile_key '].apply(
        lambda x: x.split('_')[2])  # please note Tile_key has a space at the end.
    df['date_from_key'] = pd.to_datetime(df['date_from_key'], unit='s').dt.date

    grouped_df = df.groupby(['date_from_key'])
    print(len(grouped_df))
    d = {}
    for date, list_rows in grouped_df:
        mat = create_adj_matrix(n)
        print(date)
        # print(list_rows['UserA'])
        # print(type(list_rows))
        for row in list_rows.values:
            if mat[row[0]][row[5]] is False:
                mat[row[0]][row[5]] = row[10]
                mat[row[5]][row[0]]=row[10]

            else:
                prev = mat[row[0]][row[5]]
                if row[10] < prev:
                    print("Updating distance between User " + str(row[0]) + " and User " + str(row[5]))
                    print("From distance " + str(prev) + " to " + str(row[10]))
                    mat[row[0]][row[5]] = row[10]
                    mat[row[5]][row[0]] = row[10]

        for i in range(len(mat)):
            if mat[i][i] is False:
                 mat[i][i]=1
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j]!= mat[j][i]:
                    print(" I and J values not same")
                    return {}


        d[str(date)] = mat
    print("Tensor created of length",len(d))
    return d


def update_dist_from_date_user_id(T, key, UserA, UserB, dist_value):
    target_mat=T.get(key)
    try:
        print("Updating")
        target_mat[UserA][UserB] = dist_value
        target_mat[UserB][UserA] = dist_value

    except:
        print("Can't update value. Check indices")

    return  target_mat[UserA][UserB] == target_mat[UserB][UserA]


Tensor_dict = load_mat('consolidated_csv/fragments_ds100_dt300.csv', 182)

print(update_dist_from_date_user_id(Tensor_dict, '2012-06-17',153,163,10))

# 0.9638707755094332
