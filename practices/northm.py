import pandas as pd

def main():
    print('this is main function')
    excel_filename = 'northmoney.xlsx'
    sheet = pd.read_excel(excel_filename, sheet_name=2)
    print(sheet)


if __name__ == '__main__':
    main()


