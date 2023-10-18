# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:36:26 2023
@author: kmutnb
"""

class Moneyset:
    def __init__(self, mID="", name="", value=0, qty=0):
        """Constructor Method to create Moneyset instance"""
        self.ID = mID
        self.name = name
        self.value = value
        self.qty = qty

    def __str__(self):
        return f'{self.ID:3} {self.name:20} {self.value:4d} {self.qty:4d}'

    def showTotalValue(self):
        """Show value*qty Method"""
        print(self.value * self.qty)

class Goodset:
    def __init__(self, code="", name="", unitp=0, qty=0):
        """Constructor Method to create Goodset instance"""
        self.code = code
        self.name = name
        self.unitp = unitp
        self.qty = qty

    def __str__(self):
        return f'{self.code:3} {self.name:20} {self.unitp:4d} {self.qty:4d}'

    def showGoodsDetail(self):
        """Show Detail of Goodset Method"""
        print(self.code, self.name, self.unitp, self.qty)

def goodsToMem():
    """Read goods.txt file to goodsMem"""
    fin = open('Goods.txt', 'r')
    gMem = []
    with fin:
        for gRecord in fin:
            gNo, gName, gPrice, gQty = gRecord.split()
            gMem.append(Goodset(gNo, gName, int(gPrice), int(gQty)))
    return gMem

def showAllGoogsMem(gMem):
    """Show All GoogsMem"""
    sumA = 0
    for oneGMem in gMem:
        totAmt = oneGMem.unitp * oneGMem.qty
        sumA += totAmt
        print(f'{oneGMem.code:2} {oneGMem.name:20} {oneGMem.unitp:4} {oneGMem.qty:4}')
    return sumA

def walletToMem():
    """Read wallet.txt file to walletMem"""
    fin = open('Wallet.txt', 'r')
    wlMem = []
    with fin:
        for wlRecord in fin:
            wID, wName, wValue, wQty = wlRecord.split()
            wlMem.append(Moneyset(wID, wName, int(wValue), int(wQty)))
    return wlMem

def walletToInitCashMem():
    """Read wallet.txt file to Cash Mem"""
    fin = open('Wallet.txt', 'r')
    cashMem = []
    with fin:
        for chRec in fin:
            chID, chName, chValue, chQty = chRec.split()
            chQty = '0'
            cashMem.append(Moneyset(chID, chName, int(chValue), int(chQty)))
    return cashMem

def showAllWalletMem(wlMem):
    """Show All walletMem"""
    sumA = 0
    for oneWLMem in wlMem:
        totAmt = oneWLMem.value * oneWLMem.qty
        sumA += totAmt
        print(f'{oneWLMem.ID:2} {oneWLMem.name:20} {oneWLMem.value:4} {oneWLMem.qty:4}')
    return sumA

def inputAllWalletMemQty(wlMem):
    """Enter All walletMem Qty"""
    i = 0
    for oldOneMem in wlMem:
        newQty = input(f'{oldOneMem.ID},{oldOneMem.name},{oldOneMem.value},\nQty = {oldOneMem.qty} <none> = ')
        if newQty == '':
            newQty = oldOneMem.qty
        else:
            newQty = int(newQty)
        wlMem[i].qty = newQty
        i += 1
    return wlMem

def inputAllGoodsMemQty(gMem):
    """Enter All Goods Qty"""
    i = 0
    for oldOneMem in gMem:
        newQty = input(f'{oldOneMem.code},{oldOneMem.name},{oldOneMem.unitp},\nQty = {oldOneMem.qty} <none> = ')
        if newQty == '':
            newQty = oldOneMem.qty
        else:
            newQty = int(newQty)
        gMem[i].qty = newQty
        i += 1
    return gMem

def buyGoodsItem(gId, gMem):
    """ """
    cashMem = walletToInitCashMem()
    # for i in range (1,10):
    # print (cashMem[i])
    return gMem[gId].name, gMem[gId].unitp, gMem[gId].qty

# Start work
def find_value_in_list(fvalue):
    cashMem = walletToMem()
    i_return = 0
    for i in cashMem:
        if fvalue == i.value:
            return_value = i_return
            break
        else:
            i_return += 1
    return i_return

def good_Mem_to_file(gMem):
    file_out = open('Goods.txt', 'w')
    for oneGMem in gMem:
        file_out.writelines(f'{oneGMem.code:2} {oneGMem.name:20} {oneGMem.unitp:4} {oneGMem.qty:4}\n')

def wallet_Mem_to_file(cashMem):
    file_out = open('Wallet.txt', 'w')
    for oneWLMem in cashMem:
        file_out.writelines(f'{oneWLMem.ID:2} {oneWLMem.name:20} {oneWLMem.value:4} {oneWLMem.qty:4}\n')

def cal_return_cash(cashMem, total, gvalue):
    return_code = 0
    return_cash = walletToInitCashMem()
    value_temp = [1000, 500, 100, 50, 20, 10, 5, 2, 1]
    wallet = walletToMem()
    cash = total - gvalue
    for i in range(0, 9):
        i_temp = find_value_in_list(value_temp[i])
        return_cash[i_temp].qty = int(cash / value_temp[i])
        cash %= value_temp[i]
        if return_cash[i_temp].qty > wallet[i_temp].qty:
            return_code = 1
            return_cash = cashMem
            break
    if return_code != 1:
        for i in range(0, 9):
            i_temp = find_value_in_list(value_temp[i])
            wallet[i_temp].qty += cashMem[i_temp].qty
            wallet[i_temp].qty -= return_cash[i_temp].qty

    wallet_Mem_to_file(wallet)
    return return_code, return_cash

def decrees_by_gid(gid, gmem):
    gmem[gid].qty -= 1
    good_Mem_to_file(gmem)

if __name__ == '__main__':
    # print('GoodsMem')
    # print('========')
    goodsMem = goodsToMem()
    gName, gUnitp, gQty = buyGoodsItem(9, goodsMem)
    print(f'{gName} {gUnitp} , {gQty}')

    totalGoodValue = showAllGoogsMem(goodsMem)
    print(f'Total Goods = {totalGoodValue:,d}')
    # goodsMem = inputAllGoodsMemQty(goodsMem)
    # totalGoodValue = showAllGoogsMem(goodsMem)
    # print(f'Total after input = {totalGoodValue:,d}')
