# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:36:26 2023
@author: kmutnb
"""
import MenuFn as MFn
import FileAndMEM_class as FMC
import os
import msvcrt

if __name__ == '__main__':
    iloop = True
    iMain = MFn.getMainMenu()

    while iloop:
        if iMain == 'b':
            goodsMem = FMC.goodsToMem()
            iBuy = MFn.getBuyGoodsMenu(goodsMem)

            while iBuy != 'e':
                if iBuy != 'e':
                    gName, gUnitp, gQty = FMC.buyGoodsItem(int(iBuy), goodsMem)
                    MFn.payment_function(gName, gQty, gUnitp, int(iBuy), goodsMem)

                MFn.raw_input(1, f'\nBuy Goods Menu Select {iBuy}\nPress Any key ')
                iBuy = MFn.getBuyGoodsMenu(goodsMem)
        
        elif iMain == 'm':
            MFn.maintenance_function()
        
        elif iMain == 's':
            if MFn.shut_down_function():
                iloop = False
                break
        
        iMain = MFn.getMainMenu()
