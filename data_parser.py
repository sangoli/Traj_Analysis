import os


def parse(n):
    for i in range(n):
        user = '%03d' % i
        print("------------USER----------"+user)
        userdata = 'data/' + user + '/Trajectory/'
        filelist = os.listdir(userdata)
        for f in filelist:
            print(f)
            # fp = open('data/' + user + '/Trajectory/' + filelist[f])
            with open('data/' + user + '/Trajectory/' + f, 'r') as file1, open('parsed_data/output_'+user+'.txt', 'a+') as file2:
                for i, line in enumerate(file1):
                    if (i > 5):
                        file2.write(",".join(line.split(',')[0:2]) + "," + ",".join(line.split(',')[5:7]))

parse(182)# change for number of users