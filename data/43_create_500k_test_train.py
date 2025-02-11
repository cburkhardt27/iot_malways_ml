import numpy as np

# create two arrays of random unique indices for row numbers
# splitting the data based on row label in order to read in file line by line (file too big for Shuffle())
def createRandomArr(num=1000000,start = 8, end = 67321818):
    arr = np.random.choice(np.arange(start,end+1),size = num,replace=False)
    return set(arr[0:500000]), set(arr[500000:1000000])

def main():
    set_test_ind, set_train_ind = createRandomArr()
    lnr = 0
    test_f = open('test_data_500k.csv','w')
    train_f = open('train_data_500k.csv','w')
    mal_ben_bulk_f = open('mal_ben_bulk.csv','w')
    hor_port_ben_bulk_f = open('hor_port_ben_bulk.csv','w')

    with open('conn.log.labeled','r') as f:
        for line in f:
            if lnr < 6:
                pass
            elif lnr == 6 or lnr == 7:
                test_f.write(line)
                train_f.write(line)
                hor_port_ben_bulk_f.write(line)
                mal_ben_bulk_f.write(line)

            elif lnr in set_test_ind:
                test_f.write(line)
            else:
                if lnr in set_train_ind:
                    train_f.write(line)
                if 'Benign' in line:
                    mal_ben_bulk_f.write(line)
                    hor_port_ben_bulk_f.write(line)
                elif 'Horizontal' in line:
                    hor_port_ben_bulk_f.write(line)
                else:         
                    mal_ben_bulk_f.write(line)
            if (lnr % 100000 ==0):
                print("Row number: ", lnr)  
            lnr += 1
    f.close()


if __name__ == "__main__":
    main()