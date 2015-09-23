# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 09:38:36 2015

@author: skh469
"""

import string

def caesar_encrypt(inputstring, shift):
    shift=shift % 26
    original_chars_lower = list(string.lowercase[:])
    shifted_chars_lower = original_chars_lower[shift:]+original_chars_lower[:shift]
    cipher_dict_lower=dict(zip(original_chars_lower, shifted_chars_lower))
    
    original_chars_upper = list(string.uppercase[:])
    shifted_chars_upper = original_chars_upper[shift:]+original_chars_upper[:shift]
    cipher_dict_upper=dict(zip(original_chars_upper, shifted_chars_upper))
    cipher_dict=cipher_dict_lower    
    
    cipher_dict.update(cipher_dict_upper)
    
    
    output=''    
    
    for char in inputstring:
        if str.isalpha(char):
            output+=cipher_dict[char]
        else:
            output+=char
    return output
    
print caesar_encrypt('Caesar Cipher',2)
print caesar_encrypt('HELLO',4)
print caesar_encrypt("A shift of zero is nothing.", 0)
print caesar_encrypt("Backwards will also work. Like this!", -2)
print caesar_encrypt("---====HeY====---", 55)
print caesar_encrypt("Uvrivjk Ifdre wizveu, nyrk'j lg? Pfl jyflcu tyvtb flk dp "
                     "evn kfxr,zk cffbj kfkrccp jlgvi tffc, reu Z xfk zk fww r "
                     "tirqp jrcv rk Tztvif'j,wfi aljk 2 uverizz. Z'd xfeer yzk "
                     "jfdv srij crkvi nzky zk, reu Z'dkyzebzex zk nzcc sv gfglcri "
                     "nzky kyv cruzvj. Nyrk riv pfl ufzex crkvi?Nreer yzk kyv xpd?",-17)