import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_finance as mpf
# import pandas_datareader
import tkinter
import tkinter.messagebox


str = 'code(600001)'
pattern = re.compile(r'[(](.*?)[])]')
print(re.findall(pattern,str))

def main():
    padf = pd.read_csv('601318.csv')
    print(padf)
    # drawKLine(padf)
    # drawComplexKline(padf)
    # maBuyPointer(padf)
    # print(padf.info())
    # print(len(padf))
    # term = 12
    # calEMA(padf, term)
    padf_macd = calMACD(padf)
    # print(padf_macd)
    # drawMACD(padf_macd)
    # draw_K_Volume_MACD(padf_macd)
    # print(padf)
    # buyPointByMACD(padf)
    # draw_K_MACDByGS(padf)
    # tk_practice()
    # tk_combox()
    # tk_radio_button()
    tk_check_button()


def tk_check_button():
    import tkinter as tk
    win = tk.Tk()
    win.title('复选框')
    win.geometry('300x150')
    tk.Label(win, text='我已经掌握的编程语言:').pack(anchor=tkinter.W)

    def handle():
        msg = ''
        if pythonselected.get() == True:
            msg = msg + pythoncheckbutton.cget('text')
            msg = msg + '\n'
        if javaselected.get() == True:
            msg = msg + javacheckbutton.cget('text')
            msg = msg + '\n'
        if goselected.get() == True:
            msg = msg + gocheckbutton.cget('text') + '\n'
            msg = msg + '\n'
        text.delete(0, tkinter.END)
        text.insert('insert', msg)

    pythonselected = tk.BooleanVar()
    pythoncheckbutton = tkinter.Checkbutton(win, text='Python', variable=pythonselected, command=handle)
    pythoncheckbutton.pack(anchor=tkinter.W)
    javaselected = tk.BooleanVar()
    javacheckbutton = tkinter.Checkbutton(win, text='Java', variable=javaselected, command=handle)
    javacheckbutton.pack(anchor=tkinter.W)
    goselected = tk.BooleanVar()
    gocheckbutton = tkinter.Checkbutton(win, text='Go', variable=goselected, command=handle)
    gocheckbutton.pack(anchor=tkinter.W)

    text = tkinter.Entry(win)
    text.place(x=3, y=100, width=150, height=30)

    win.mainloop()






def tk_radio_button():
    import tkinter as tk
    win = tk.Tk()
    win.title('单选框')
    win.geometry('300x150')
    tk.Label(win, text='您目前学的是:').pack()

    def handle():
        text.delete(0, tk.END)
        text.insert('insert', selectval.get())

    selectval = tk.StringVar()
    selectval.set('Python')

    tk.Radiobutton(win, text='python', value='Python', variable=selectval, command=handle).pack()
    tk.Radiobutton(win, text='java', value='java', variable=selectval, command=handle).pack()

    text = tk.Entry(win,  width=20)
    text.pack()

    win.mainloop()



def tk_combox():
    import tkinter as tk
    from tkinter import ttk

    win = tk.Tk()
    win.title('下拉框')
    tk.Label(win, text='选择编程语言').grid(column=0, row=0)
    comboxval = tk.StringVar
    combobox = ttk.Combobox(win, width=12, textvariable=comboxval)
    combobox['values'] = ('python', 'java', '.net', 'go')
    combobox.grid(column=1, row=0)
    combobox.current(0)

    def handle():
        text.delete(0, tk.END)
        text.insert(0, combobox.get())

    button = tk.Button(win, text='选择', width=12, command=handle)
    button.grid(column=1, row=1)
    val = tk.StringVar()
    text = tk.Entry(win, width=12, textvariable=val)
    text.grid(column=0, row=1)

    text.focus()
    win.mainloop()


def tk_practice():
    loginWin = tkinter.Tk()
    loginWin.geometry('220x120')
    loginWin.title('登录窗口')
    # 放置2个标签
    tkinter.Label(loginWin, text='用户名: ').place(x=10, y=20)
    tkinter.Label(loginWin, text='密  码: ').place(x=10, y=50)
    userval = tkinter.StringVar()
    pasval = tkinter.StringVar()

    tkinter.Entry(loginWin, textvariable=userval).place(x=65, y=20)
    tkinter.Entry(loginWin, textvariable=pasval, show='*').place(x=65, y=50)

    def check():
        username = userval.get()
        pwd = pasval.get()
        print('用户名:'+username)
        print('密码:'+pwd)
        if username == 'python' and pwd == 'kdj':
            tkinter.messagebox.showinfo('提示', '登录成功')
        else:
            tkinter.messagebox.showinfo('提示', '登录失败')
    tkinter.Button(loginWin, text='登录', width=12, command=check).place(x=10, y=85)
    tkinter.Button(loginWin, text='退出', width=12, command=loginWin.quit).place(x=120, y=85)
    tkinter.mainloop()


def buyPointByMACD(df):
    print(df)
    cnt =0
    while cnt< len(df):
        if (cnt>=30):
            try:
                if df.iloc[cnt]['DIF']>df.iloc[cnt]['DEA'] and df.iloc[cnt-1]['DIF']<df.iloc[cnt-1]['DEA']:
                    if df.iloc[cnt]['MACD']>0:
                        print('buy point by MACD is {}'.format(df.iloc[cnt]['date']))
            except:
                pass
        cnt = cnt +1


def draw_K_MACDByGS(df):
    # import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    fig = plt.figure(dpi=100,
                     constrained_layout=True,  # 类似于tight_layout，使得各子图之间的距离自动调整【类似excel中行宽根据内容自适应】
                     )

    gs = GridSpec(6, 1, figure=fig)  # GridSpec将fiure分为3行3列，每行三个axes，gs为一个matplotlib.gridspec.GridSpec对象，可灵活的切片figure
    axPrice = fig.add_subplot(gs[0:4, 0])
    # plt.plot([1, 2, 3])
    axVol = fig.add_subplot(gs[4, 0])  # gs[0, 0:3]中0选取figure的第一行，0:3选取figure第二列和第三列

    axMACD = fig.add_subplot(gs[5, 0])
    # plt.subplot(gs[1, 0:2])  # 同样可以使用基于pyplot api的方式
    # plt.scatter([1, 2, 3], [4, 5, 6], marker='*')

    # ax4 = fig.add_subplot(gs[1:3, 2:3])
    # plt.bar([1, 2, 3], [4, 5, 6])

    # ax5 = fig.add_subplot(gs[2, 0:1])
    # ax6 = fig.add_subplot(gs[2, 1:2])
    axPrice.sharex(axMACD)
    axVol.sharex(axMACD)

    mpf.candlestick2_ochl(ax=axPrice, opens=df['open'].values, closes=df['close'].values, highs=df['high'].values,
                          lows=df['low'].values, colordown='green', colorup='red', width=0.5)
    df['close'].rolling(window=5).mean().plot(ax=axPrice, color='blue', linewidth=1)
    df['close'].rolling(window=10).mean().plot(ax=axPrice, color='green', linewidth=1)
    df['close'].rolling(window=20).mean().plot(ax=axPrice, color='red', linewidth=1)

    df['DEA'].plot(ax=axMACD, color='red', label='DEA', linewidth=1)
    df['DIF'].plot(ax=axMACD, color='blue', label='DIF', linewidth=1)

    date = []
    for i in range(0, len(df.index.values), 5):
        date.append(df['date'].values[i])
    # print(date)
    for index, row in df.iterrows():
        if row['close'] > row['open']:
            axVol.bar(row['date'], row['volume']/100000, width=0.5, color='red')
        if row['close'] <= row['open']:
            axVol.bar(row['date'], row['volume']/100000, width=0.5, color='green')

        if row['MACD'] > 0:
            axMACD.bar(row['date'], row['MACD'], width=0.3, color='red')
        else:
            axMACD.bar(row['date'], row['MACD'], width=0.3, color='green')

    date = []
    list = []
    for i in range(0, len(df.index.values), 5):
        date.append(df['date'].values[i])
        list.append(' ')
    axMACD.set_xticks(range(0, len(df.index.values), 5), date, rotation=90)

    fig.suptitle(df.iloc[0]['code'], color='r')
    plt.show()


def draw_K_Volume_MACD(df):
    print (df)
    axPrice = plt.subplot2grid((6, 1), (0, 0), rowspan=4)
    axVol = plt.subplot2grid((6, 1), (4, 0), rowspan=1)
    axMACD = plt.subplot2grid((6, 1), (5, 0), rowspan=1)
    # plt.tight_layout()

    mpf.candlestick2_ochl(ax=axPrice, opens=df['open'].values, closes=df['close'].values, highs=df['high'].values,
                          lows=df['low'].values, colordown='green', colorup='red', width=0.5)
    df['close'].rolling(window=5).mean().plot(ax = axPrice,color='blue', linewidth=1)
    df['close'].rolling(window=10).mean().plot(ax = axPrice,color='green', linewidth=1)
    df['close'].rolling(window=20).mean().plot(ax = axPrice,color='red', linewidth=1)

    df['DEA'].plot(ax=axMACD ,color = 'red',label = 'DEA',linewidth=1)
    df['DIF'].plot(ax = axMACD,color = 'blue',label = 'DIF',linewidth=1)

    date = []
    for i in range(0, len(df.index.values), 5):
        date.append(df['date'].values[i])
    # print(date)
    for index,row in df.iterrows():
        if row['close']>row['open']:
            axVol.bar(row['date'],row['volume'],width=0.5,color = 'red')
        if row['close']<= row['open']:
            axVol.bar(row['date'], row['volume'], width=0.5, color='green')

        if row['MACD']>0:
            axMACD.bar(row['date'],row['MACD'],width=0.3,color = 'red')
        else:
            axMACD.bar(row['date'], row['MACD'], width=0.3, color='green')

    date = []
    list= []
    for i in range(0, len(df.index.values), 5):
        date.append(df['date'].values[i])
        list.append(' ')

    axVol.set_xticks(range(0,len(df),5),list)
    axPrice.set_xticks(range(0, len(df), 5), list)
    axMACD.set_xticks(range(0, len(df.index.values), 5), date, rotation=90)
    # axPrice.sharex(axMACD)
    # axVol.sharex(axMACD)

    # plt.xticks(range(0, len(df.index.values), 5), date, rotation=90)

    plt.show()


def drawMACD(padf_macd):
    plt.figure()
    padf_macd['DEA'].plot(color = 'red',label = 'DEA',linewidth=1)
    padf_macd['DIF'].plot(color = 'blue',label = 'DIF',linewidth=1)
    for index,row in padf_macd.iterrows():
        if row['MACD']>0:
            plt.bar(row['date'],row['MACD'],width=0.3,color = 'red')
        else:
            plt.bar(row['date'], row['MACD'], width=0.3, color='green')

    date = []
    for i in range(0, len(padf_macd.index.values), 5):
        date.append(padf_macd['date'].values[i])
    plt.xticks(range(0, len(padf_macd.index.values), 5), date, rotation=90)

    plt.show()


def calEMA(padf,term):
    ema = []
    for i in range(len(padf)):
        if i==0:
            a = padf.iloc[i]['close']
        if i>0:
            a = (term-1)/(term+1)*ema[i-1]+2/(term+1)*padf.iloc[i]['close']
        ema.append(a)
    # print(ema)
    return ema

def calMACD(padf,short_term=12,long_term = 26,difterm = 9):
    '''
    计算MACD的值
    '''
    shortEMA = calEMA(padf,short_term)
    longEMA = calEMA(padf,long_term)
    padf['DIF']=pd.Series(shortEMA)-pd.Series(longEMA)
    # print(padf.head())
    list_dea = []
    for i in range(len(padf)):
        if i==0:
            dea = padf.iloc[i]['DIF']
        if i>0:
            dea = (difterm-1)/(difterm+1)*list_dea[i-1]+2/(difterm+1)*padf.iloc[i]['DIF']
        list_dea.append(dea)
    # print(list_dea)
    padf['DEA'] = pd.Series(list_dea)
    padf['MACD'] = 2*(padf['DIF']-padf['DEA'])
    # print(padf.head())
    return padf


def testPlt():
    x = np.arange(20)
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(x,2*x)
    plt.subplot(2, 2, 3)
    plt.plot(x, 3 * x)
    plt.subplot(2, 2, 4)
    plt.plot(x, 4 * x)
    plt.show()


def drawKLine(padf):

    figure,(axPrice,axVol) = plt.subplots(2,sharex=True)
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    mpf.candlestick2_ochl(ax=axPrice, opens=padf['open'].values, closes=padf['close'].values, highs=padf['high'].values,
                          lows=padf['low'].values, colordown='green', colorup='red', width=0.5)
    padf['close'].rolling(window=5).mean().plot(ax = axPrice,color='blue', linewidth=1)
    padf['close'].rolling(window=10).mean().plot(ax = axPrice,color='green', linewidth=1)
    padf['close'].rolling(window=20).mean().plot(ax = axPrice,color='red', linewidth=1)
    date = []
    for i in range(0, len(padf.index.values), 5):
        date.append(padf['date'].values[i])
    # print(date)
    for index,row in padf.iterrows():
        if row['close']>row['open']:
            axVol.bar(row['date'],row['volume'],width=0.5,color = 'red')
        else:
            axVol.bar(row['date'], row['volume'], width=0.5, color='green')

    plt.xticks(range(0, len(padf.index.values), 5), date, rotation=90)

    # padf['open'].plot(color='red')
    # padf['close'].plot(color = 'blue')
    # plt.plot(padf['open'].values,color='r')
    # plt.plot(padf['close'], color='g')
    plt.show()


def drawComplexKline(padf):
    # padf = pd.read_csv('601318.csv')
    axPrice = plt.subplot2grid((5, 1), (0, 0), rowspan=4)
    axVol = plt.subplot2grid((5, 1), (4, 0), rowspan=1)
    mpf.candlestick2_ochl(ax=axPrice, opens=padf['open'].values, closes=padf['close'].values, highs=padf['high'].values,
                          lows=padf['low'].values, colordown='green', colorup='red', width=0.5)
    padf['close'].rolling(window=5).mean().plot(ax=axPrice, color='blue', linewidth=1)
    padf['close'].rolling(window=10).mean().plot(ax=axPrice, color='green', linewidth=1)
    padf['close'].rolling(window=20).mean().plot(ax=axPrice, color='red', linewidth=1)
    date = []
    for i in range(0, len(padf.index.values), 5):
        date.append(padf['date'].values[i])
    # print(date)
    for index, row in padf.iterrows():
        if row['close'] > row['open']:
            axVol.bar(row['date'], row['volume'], width=0.5, color='red')
        else:
            axVol.bar(row['date'], row['volume'], width=0.5, color='green')

    plt.xticks(range(0, len(padf.index.values), 5), date, rotation=90)
    # axVol.xticks(range(0, len(padf.index.values), 5), date, rotation=90)
    # axVol.set

    # padf['open'].plot(color='red')
    # padf['close'].plot(color = 'blue')
    # plt.plot(padf['open'].values,color='r')
    # plt.plot(padf['close'], color='g')
    plt.show()

def maBuyPointer(padf):
    print('show buy point')
    maIntervalList = ['3','5','10']
    for maInterval in maIntervalList:
        padf['MA_'+maInterval]=padf['close'].rolling(window=int(maInterval)).mean()
    print(padf)
    cnt = 0
    while cnt<len(padf)-1:
        try:
            if padf.iloc[cnt-2]['close']<padf.iloc[cnt-1]['close'] and padf.iloc[cnt-1]['close']<padf.iloc[cnt]['close']:
                if padf.iloc[cnt-2]['MA_5'] < padf.iloc[cnt-1]['MA_5'] and  padf.iloc[cnt-1]['MA_5']< padf.iloc[cnt]['MA_5']:
                    if padf.iloc[cnt-1]['MA_5']>padf.iloc[cnt-2]['close'] and padf.iloc[cnt]['MA_5']<padf.iloc[cnt-1]['close']:
                        print('Buy point on'+padf.iloc[cnt]['date'])
            # if  padf.iloc[cnt-1]['close']<padf.iloc[cnt]['close']:
            #     print('a')
            #     if   padf.iloc[cnt-1]['MA_5']< padf.iloc[cnt]['MA_5']:
            #         print('b')
            #         if padf.iloc[cnt-1]['MA_5']>padf.iloc[cnt-1]['close'] and padf.iloc[cnt]['MA_5']<padf.iloc[cnt]['close']:
            #             print('Buy point on'+padf.iloc[cnt]['date'])
        except:
            pass
        cnt = cnt+1
        # print(cnt)

# def buyPointLiangZengJiaPing(padf):
#     print('量增价平的买点')
#     cnt = 0
#     while cnt<len(padf)-1:
#         try:
#             if isLessThanPer


if __name__ == '__main__':
    main()