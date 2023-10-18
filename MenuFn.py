# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:36:26 2023
@author: kmutnb
"""
import FileAndMEM_class as FMC
import os
import msvcrt

def clearScreen():
    """Clear window screen."""
    os.system('cls')
    return

def raw_input(imax=1, prompt='\npress any key '):
    """Raw input."""
    print(f'{prompt}', end='')
    sp = bytes(' ', 'utf-8')
    mvl = bytes(chr(8), 'utf-8')
    p = bytes('*', 'utf-8')
    sstr = ''
    iloop = True
    i = 0
    while iloop:
        c = msvcrt.getch()
        if ord(c) == 8:
            i -= 2
            msvcrt.putch(mvl)
            msvcrt.putch(sp)
            msvcrt.putch(mvl)
            sstr = sstr[0:-1]
        elif ord(c) == 13:
            iloop = False
        else:
            msvcrt.putch(c)
            sstr += chr(ord(c))
        i += 1
        if i >= imax:
            iloop = False
    return sstr

def getPWD(imax=20, csh='*'):
    """Get password."""
    cpwd = bytes(csh, 'utf-8')
    sp = bytes(' ', 'utf-8')
    mvl = bytes(chr(8), 'utf-8')
    p = bytes('*', 'utf-8')
    sstr = ''
    iloop = True
    i = 0
    while iloop:
        c = msvcrt.getch()
        if ord(c) == 8:
            i -= 2
            msvcrt.putch(mvl)
            msvcrt.putch(sp)
            msvcrt.putch(mvl)
            sstr = sstr[0:-1]
        elif ord(c) == 13:
            iloop = False
        else:
            msvcrt.putch(cpwd)
            sstr += chr(ord(c))
        i += 1
        if i >= imax:
            iloop = False
    return sstr

def getBuyGoodsMenu(gMem):
    """Get Buy Goods Menu."""
    clearScreen()
    print(f'----------------------------------------')
    print(f" Goods Name Price Q'ty ")
    print(f'----------------------------------------')
    chList = ['e']
    for i in range(1, 10):
        if gMem[i].qty > 0:
            print (f'{gMem[i].code:3} {gMem[i].name:20} {gMem[i].unitp:4} {gMem[i].qty:4} <{i}>')
            chList.append(f'{i}')
        else:
            print (f'{gMem[i].code:3} {gMem[i].name:20} {gMem[i].unitp:4} {" ":4}')
    
    print(f'----------------------------------------') 
    print(f' End select <e>')
    ch = raw_input(1, '\nSelect = ')
    while (ch not in chList):
        ch = raw_input(1, '\nPlease Select = ')
    
    return ch

def getMainMenu():
    """Get Main Menu."""
    clearScreen()
    print(f'=====================')
    print(f' Main MENU ')
    print(f'=====================')
    print(f' 1. Buy Menu <b>')
    print(f' 2. Maintenance <m>')
    print(f' 3. Shutdown <s>')
    print(f'=====================')
    
    chList = ['b', 'm', 's']
    ch = raw_input(1, '\nSelect <b, m, s> = ')
    while (ch not in chList):
        ch = raw_input(1, '\nPlease Select <b, m, s> = ')
    
    return ch

# Student work

def Maintenance_menu():
    clearScreen()
    print(f'======================')
    print(f' Maintenance menu ')
    print(f'======================')
    print(f' 1. Edit goods <g>')
    print(f' 2. Edit wallet <w>')
    print(f' 3. Exit <e>')
    print(f'======================')
    
    chList = ['g', 'w', 'e']
    ch = raw_input(1, '\nSelect <g,w,e> = ')
    while (ch not in chList):
        ch = raw_input(1, '\nPlease Select <g, w, e> = ')
    
    return ch

def maintenance_function():
    clearScreen()
    print("Enter password\n :")
    input_password = getPWD(6)
    iloop = True
    
    if input_password == "123456":
        while iloop:
            ch = Maintenance_menu()
            print('')
            if ch == 'g':
                maintenance_goods()
            elif ch == 'w':
                maintenance_wallet()
            elif ch == 'e':
                iloop = False
            else:
                print("\nWrong password")
                x = input("")

def maintenance_goods():
    goodMem = FMC.goodsToMem()
    goodMem = FMC.inputAllGoodsMemQty(goodMem)
    FMC.good_Mem_to_file(goodMem)

def maintenance_wallet():
    walletMem = FMC.walletToMem()
    walletMem = FMC.inputAllWalletMemQty(walletMem)
    FMC.wallet_Mem_to_file(walletMem)

def payment_function(gName, gqty, gValue, gid, goodMem):
    cashMem = FMC.walletToInitCashMem()
    total_balance = 0
    
    iloop = True
    while iloop:
        clearScreen()
        print(f'----------------------------------------')
        print(f" Goods Name Price Q'ty ")
        print(f'----------------------------------------')
        print(f' {gName:20} {gValue:4} {gqty:4} ')
        print(f' Your balance : {total_balance:6}')
        chList = ['1000', '500', '100', '50', '20', '10', '5', '2', '1', 'c']
        ch = raw_input(4, '\n<c> = cancel\nSelect < 1, 2, 5, 10, 20, 50, 100, 500, 1000, c> = ')
        while ch not in chList:
            ch = raw_input(4, '\nPlease Select < 1, 2, 5, 10, 20, 50, 100, 500, 1000, c> = ')
        
        if ch == 'c':
            iloop = False
            return_cash(cashMem)
        elif ch in chList:
            index_cash = FMC.find_value_in_list(int(ch))
            total_balance += cashMem[index_cash].value
            cashMem[index_cash].qty += 1
        else:
            print(f'\nError')
            return_cash(cashMem)
            iloop = False
    
    if total_balance >= gValue:
        iloop = False
        return_cd, cashMem = FMC.cal_return_cash(cashMem, total_balance, gValue)
        if return_cd == 1:
            print(f'Error: Cash not enough\n')
            return_cash(cashMem)
        else:
            return_cash(cashMem)
            FMC.decrees_by_gid(gid, goodMem)

def return_cash(cashMem):
    print(f'\nReturning your cash')
    for i in cashMem:
        if i.qty != 0:
            print(f'<{i.value:5}> {i.qty}')

def shut_down_function():
    clearScreen()
    print("Enter password\n :")
    input_password = getPWD(6)
    iloop = False
    
    if input_password == "123456":
        iloop = True
        clearScreen()
        print(f'\n<system shutting down>')
        x = input("Press Any key")
    else:
        print("\nWrong password")
        x = input("")

    return iloop

if __name__ == '__main':
    wMem = FMC.walletToMem()
    
    print('WalletMem')
    for i in range(1, 10):
        # print(wMem[i].ID, wMem[i].name, wMem[i].value, wMem[i].qty)
        print(wMem[i])
    
    cashMem = wMem
    
    print('\n\nCashMem')
    for i in range(1, 10):
        cashMem[i].qty = 0 
        # print(cashMem[i].ID, cashMem[i].name, cashMem[i].value, cashMem[i].qty)
        print(cashMem[i])
