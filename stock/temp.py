import pandas as pd




def main():
    pass


    data = {'name': ['apple', 'egg', 'watermelon'], 'color': ['red', 'yellow', 'green'], 'num': [30, 40, 50]}
    df1 = pd.DataFrame(data)
    print (df1)
    print(type(df1))
    items = df1.itertuples()
    for item in items:
        # print (item)
        print(item.name)
        # print (type(item))





if __name__ == '__main__':
    main()