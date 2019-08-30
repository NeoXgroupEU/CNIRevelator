# -*- coding: utf8 -*-
"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       MRZ data dictionnary for CNIRevelator analyzer and              *
*                   functions to analyze these data                            *
*                                                                              *
*  Copyright © 2018-2019 Adrien Bourmault (neox95)                             *
*                                                                              *
*  This file is part of CNIRevelator.                                          *
*                                                                              *
*  CNIRevelator is free software: you can redistribute it and/or modify        *
*  it under the terms of the GNU General Public License as published by        *
*  the Free Software Foundation, either version 3 of the License, or           *
*  any later version.                                                          *
*                                                                              *
*  CNIRevelator is distributed in the hope that it will be useful,             *
*  but WITHOUT ANY WARRANTY*without even the implied warranty of               *
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               *
*  GNU General Public License for more details.                                *
*                                                                              *
*  You should have received a copy of the GNU General Public License           *
* along with CNIRevelator. If not, see <https:*www.gnu.org/licenses/>.         *
********************************************************************************
"""

import re
import datetime

import logger       # logger.py
import globs        # globs.py
import lang         # lang.py
import critical     # critical.py

## SEX CODES
sexcode = {'M':'Homme', 'F':'Femme',  'X':'Non spécifié'}

## COUNTRY CODES

landcode2 = lang.all[globs.CNIRlang]["LANDCODE2"]

landcode3 = lang.all[globs.CNIRlang]["LANDCODE3"]

## DOCUMENTS TYPES

P = [
  ["11222333333333333333333333333333333333333333", "444444444566677777789AAAAAABCCCCCCCCCCCCCCDE"],
  {
    "1":  ["2", "CODE", "P."],
    "2":  ["3", "PAYS", "[A-Z]+"],
    "3": ["39", "NOM", "([A-Z]|<)+"],
    "4":  ["9", "NO", ".+"],
    "5":  ["1", "CTRL", "[0-9]", "4"],
    "6":  ["3", "NAT", "[A-Z]+"],
    "7":  ["6", "BDATE", "[0-9]+"],
    "8":  ["1", "CTRL", "[0-9]", "7"],
    "9":  ["1", "SEX", "[A-Z]"],
    "A":  ["6", "EDATE", "[0-9]+"],
    "B":  ["1", "CTRL", "[0-9]", "A"],
    "C": ["14", "FACULT", ".+"],
    "D":  ["1", "CTRLF", "[0-9]", "C"],
    "E":  ["1", "CTRL", "[0-9]", "4578ABCD"]
  },
  lang.all[globs.CNIRlang]["Passeport lisible à la machine"]
]

IP = [
  ["112223333333334555555555555555", "66666678999999ABBBCCCCCCCCCCCD"],
  {
    "1": ["2", "CODE", "IP"],
    "2": ["3", "PAYS", "[A-Z]+"],
    "3": ["9", "NO", ".+"],
    "4": ["1", "CTRL", "[0-9]", "3"],
    "5": ["15", "FACULT", ".+"],
    "6": ["6", "BDATE", "[0-9]+"],
    "7": ["1", "CTRL", "[0-9]", "6"],
    "8": ["1", "SEX", "[A-Z]"],
    "9": ["6", "EDATE", "[0-9]+"],
    "A": ["1", "CTRL", "[0-9]", "9"],
    "B": ["3", "NAT", "[A-Z]+"],
    "C": ["11", "FACULT", ".+"],
    "D": ["1", "CTRL", "[0-9]", "345679AC"]
  },
  lang.all[globs.CNIRlang]["Carte-passeport"]
]

IDEUR = [
  ["112223333333334555555555555555", "66666678999999ABBBCCCCCCCCCCCD"],
  {
    "1": ["2", "CODE", "I."],
    "2": ["3", "PAYS", "[A-Z]+"],
    "3": ["9", "NO", ".+"],
    "4": ["1", "CTRL", "[0-9]", "3"],
    "5": ["15", "FACULT", ".+"],
    "6": ["6", "BDATE", "[0-9]+"],
    "7": ["1", "CTRL", "[0-9]", "6"],
    "8": ["1", "SEX", "[A-Z]"],
    "9": ["6", "EDATE", "[0-9]+"],
    "A": ["1", "CTRL", "[0-9]", "9"],
    "B": ["3", "NAT", "[A-Z]+"],
    "C": ["11", "FACULT", ".+"],
    "D": ["1", "CTRL", "[0-9]", "345679AC"]
  },
  lang.all[globs.CNIRlang]["Carte d’identité européenne"]
]

TSEUR = [
  ["112223333333334555555555555555", "66666678999999ABBBCCCCCCCCCCCD"],
  {
    "1": ["2", "CODE", "IR"],
    "2": ["3", "PAYS", "[A-Z]+"],
    "3": ["9", "NO", ".+"],
    "4": ["1", "CTRL", "[0-9]", "3"],
    "5": ["15", "FACULT", ".+"],
    "6": ["6", "BDATE", "[0-9]+"],
    "7": ["1", "CTRL", "[0-9]", "6"],
    "8": ["1", "SEX", "[A-Z]"],
    "9": ["6", "EDATE", "[0-9]+"],
    "A": ["1", "CTRL", "[0-9]", "9"],
    "B": ["3", "NAT", "[A-Z]+"],
    "C": ["11", "FACULT", ".+"],
    "D": ["1", "CTRL", "[0-9]", "345679AC"]
  },
  lang.all[globs.CNIRlang]["Carte de séjour européenne"]
]

AC = [
  ["112223333333334EEE555555555555", "66666678999999ABBBCCCCCCCCCCCD"],
  {
    "1": ["2", "CODE", "AC"],
    "2": ["3", "PAYS", "[A-Z]+"],
    "3": ["9", "NO", ".+"],
    "4": ["1", "CTRL", "[0-9]", "3"],
    "E": ["3", "INDIC", "[A-Z]{1,2}."],
    "5": ["12", "FACULT", ".+"],
    "6": ["6", "BDATE", "[0-9]+ "],
    "7": ["1", "CTRL", "[0-9]", "6"],
    "8": ["1", "SEX", "[A-Z]"],
    "9": ["6", "EDATE", "[0-9]+"],
    "A": ["1", "CTRL", "[0-9]", "9"],
    "B": ["3", "NAT", "[A-Z]+"],
    "C": ["11", "FACULT", ".+"],
    "D": ["1", "CTRL", "[0-9]","345679AC"]
  },
  lang.all[globs.CNIRlang]["Certificat de membre d'équipage"]
]

VA = [
  ["11222333333333333333333333333333333333333333", "444444444566677777789AAAAAABCCCCCCCCCCCCCCCC"],
  {
    "1": ["2", "CODE", "V."],
    "2": ["3", "PAYS", "[A-Z]+"],
    "3": ["39", "NOM", "([A-Z]|<)+"],
    "4": ["9", "NO", ".+"],
    "5": ["1", "CTRL", "[0-9]","4"],
    "6": ["3", "NAT", "[A-Z]+"],
    "7": ["6", "BDATE", "[0-9]+"],
    "8": ["1", "CTRL", "[0-9]", "7"],
    "9": ["1", "SEX", "[A-Z]"],
    "A": ["6", "EDATE", "[0-9]+"],
    "B": ["1", "CTRL", "[0-9]", "A"],
    "C": ["16", "FACULT", ".+"]
  },
  lang.all[globs.CNIRlang]["Visa de type A"]
]

VB = [
  ["112223333333333333333333333333333333", "444444444566677777789AAAAAABCCCCCCCC"],
  {
    "1": ["2", "CODE", "V."],
    "2": ["3", "PAYS", "[A-Z]+"],
    "3": ["31", "NOM", "([A-Z]|<)+"],
    "4": ["9", "NO", ".+"],
    "5": ["1", "CTRL", "[0-9]","4"],
    "6": ["3", "NAT", "[A-Z]+"],
    "7": ["6", "BDATE", "[0-9]+"],
    "8": ["1", "CTRL", "[0-9]", "7"],
    "9": ["1", "SEX", "[A-Z]"],
    "A": ["6", "EDATE", "[0-9]+"],
    "B": ["1", "CTRL", "[0-9]", "A"],
    "C": ["8", "FACULT", ".+"]
  },
  lang.all[globs.CNIRlang]["Visa de type B"]
]

TSF = [
  ["112223333333333333333333333333333333", "444444444566677777789AAAAAABCCCCCC"],
  {
    "1": ["2", "CODE", "TS"],
    "2": ["3", "PAYS", "FRA"],
    "3": ["31", "NOM", "([A-Z]|<)+"],
    "4": ["9", "NO", ".+"],
    "5": ["1", "CTRL", "[0-9]","4"],
    "6": ["3", "NAT", "[A-Z]+"],
    "7": ["6", "BDATE", "[0-9]+"],
    "8": ["1", "CTRL", "[0-9]", "7"],
    "9": ["1", "SEX", "[A-Z]"],
    "A": ["6", "EDATE", "[0-9]+"],
    "B": ["1", "CTRL", "[0-9]", "A"],
    "C": ["8", "FACULT", ".+"]
  },
  lang.all[globs.CNIRlang]["Carte de séjour FR"]
]

TDV = [
  ["112223333333333333333333333333333333", "444444444566677777789AAAAAABCCCCCCCD"],
  {
    "1": ["2", "CODE", "I."],
    "2": ["3", "PAYS", "[A-Z]+"],
    "3": ["31", "NOM", "([A-Z]|<)+"],
    "4": ["9", "NO", ".+"],
    "5": ["1", "CTRL", "[0-9]", "4"],
    "6": ["3", "NAT", "[A-Z]+"],
    "7": ["6", "BDATE", "[0-9]+"],
    "8": ["1", "CTRL", "[0-9]", "7"],
    "9": ["1", "SEX", "[A-Z]"],
    "A": ["6", "EDATE", "[0-9]+"],
    "B": ["1", "CTRL", "[0-9]", "A"],
    "C": ["7", "FACULT", ".+"],
    "D": ["1", "CTRL", "[0-9]", "4578ABC"]
  },
  lang.all[globs.CNIRlang]["Titre d'identité/de voyage"]
]

IDFR = [
  ["112223333333333333333333333333444444", "555566677777899999999999999AAAAAABCD"],
  {
    "1": ["2", "CODE", "ID"],
    "2": ["3", "PAYS", "FRA"],
    "3": ["25", "NOM", "([A-Z]|<)+"],
    "4": ["6", "NOINT", ".+"],
    "5": ["4", "DDATE", "[0-9]+"],
    "6": ["3", "NOINT2", "[0-9]+"],
    "7": ["5", "NOINT3", "[0-9]+"],
    "8": ["1", "CTRL", "[0-9]", "567"],
    "9": ["14", "PRENOM", "[A-Z]"],
    "A": ["6", "BDATE", "[0-9]+"],
    "B": ["1", "CTRL", "[0-9]", "A"],
    "C": ["1", "SEX", "[A-Z]"],
    "D": ["1", "CTRL", "[0-9]", "123456789ABCE"]
  },
  lang.all[globs.CNIRlang]["Pièce d'identité FR"]
]

DL = [
  ["112223333333334555555666666667", ""],
  {
    "1": ["2", "CODE", "D1"],
    "2": ["3", "PAYS", "[A-Z]+"],
    "3": ["9", "NO", "[0-9]{2}[A-Z]{2}[0-9]{5}"],
    "4": ["1", "CTRL", "[0-9]", "123"],
    "5": ["6", "EDATE", "[0-9]+"],
    "6": ["8", "NOM", "([A-Z]|<)+"],
    "7": ["1", "CTRL", "[0-9]", "123456"]
  },
  lang.all[globs.CNIRlang]["Permis de conduire"]
]

TYPES = [IDFR, TDV, VB, VA, AC, IDEUR, IP, P, DL, TSF, TSEUR]

# longest document MRZ line
longest = max([len(x[0][0]) for x in TYPES])

## THE ROOT OF THIS PROJECT !

def getDocString(doc):
    return doc[0][0] + doc[0][1]

def getFieldLimits(doc, fieldtype):
    """
    This function returns the limit of a given field string id for a given document structure
    """
    L1 = limits(doc[0][0], fieldtype)
    L2 = limits(doc[0][1], fieldtype)

    if -1 in L1:
        return 1, L2
    else:
        return 0, L1
    return

def limits(line, fieldtype):
    """
    Returns the limit of a given field structure
    """
    a = line.find(fieldtype)
    b = line.rfind(fieldtype)
    return (a,b+1)

def completeDocField(doc, code, position):
    """
    Completes with '<' the document the field that is located at given position
    """
    field = getDocString(doc)[position]
    limit = limits(getDocString(doc), field)
    res = limit[1] - position
    #print("field : {}, limit : {}, number of char to complete : {}".format(field, limit, res))
    return res


def docMatch(doc, strs):
    """
    This function calculates a regex match score for a given document and a string couple
    """
    # Global handler
    logfile = logger.logCur

    level = 0
    nchar = 0
    bonus = 0

    for i in range(0,2):
        cursor = 0
        #print("Line : {}".format(i))

        while True:
            if cursor > len(doc[0][i]) - 1:
                break
            # Getting the type of field on the cursor position
            fieldtype = doc[0][i][cursor]
            lim = limits(doc[0][i], fieldtype)
            # ready for next field
            cursor = lim[1]
            # get the current field and isolates it
            field = doc[0][i][ lim[0]:lim[1] ]
            fstr  =   strs[i][ lim[0]:lim[1] ]
            # Prepare regex compilation
            regex = re.compile(doc[1][fieldtype][2])
            # Test the match
            matching = regex.match(fstr)
            # Retrieve the mathing level
            if matching:
                level += matching.end()
                if fieldtype == "1":
                    bonus += 100
            nchar += int(doc[1][fieldtype][0])

            # Print for debug

            # print("Field : {}, type = {}, on str : {}".format(field, fieldtype, fstr))
            # logfile.printdbg("        REGEX : {}, match : {}".format(regex, matching))
            # exit the loop

    logfile.printdbg("{} level : {}/{}  (+{})".format(doc[2], level, nchar, bonus))
    return (level, nchar, bonus)

def allDocMatch(strs, final=False):
    """
    This functions test all documents types on the lines provided and returns a score for each
    """
    # Global handler
    logfile = logger.logCur

    #print(strs)

    SCORES = []
    for doc in TYPES:
        # Get the score of the document on the strings
        level, nchar, bonus = docMatch(doc, strs)
        # Number of characters compatibles + bonus with the doc indication
        SCORES += [ level + bonus ]
        # if the len of strings is the same than document, add a bonus
        #     but only if we are in a final situation
        if final:
            if len(strs[0] + strs[1]) == nchar:
                SCORES[-1] += 100
    candidate = SCORES.index(max(SCORES))
    candidates = []
    canditxt = []

    # Search the candidates
    for i in range(len(SCORES)):
        if SCORES[i] == SCORES[candidate]:
            candidates += [TYPES[i]]
            canditxt += [TYPES[i][2]]
    # Continue searching
    if len(candidates) < 2:
        tempRemovedCandidate = SCORES.pop(candidate)
        if (SCORES.index(max(SCORES)) != candidate) and (max(SCORES) >= tempRemovedCandidate - 20):
            if SCORES.index(max(SCORES)) < candidate:
                candidates += [ TYPES[SCORES.index(max(SCORES))] ]
            else:
                candidates += [ TYPES[SCORES.index(max(SCORES)) + 1] ]
        SCORES.insert(candidate, tempRemovedCandidate)

    # Return the candidates
    logfile.printdbg("Scores     : {}".format(SCORES))
    logfile.printdbg("Candidates : {}".format(canditxt))
    return candidates

def computeControlSum(code):
    """
    This function computes a control sum for the given characters
    """
    resultat = 0
    i = -1
    facteur = [7, 3, 1]
    for car in code:
        if car == '<' or car == '\n':
            valeur = 0
            i += 1
        else:
            if car in '0123456789':
                valeur = int(car)
                i += 1
            else:
                if car in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    valeur = ord(car) - 55
                    i += 1
                else:
                    break
        resultat += valeur * facteur[(i % 3)]

    return resultat % 10

def computeAllControlSum(doc, code):
    """
    This function computes all the ctrl sums on a MRZ string and returns all the results
        it returns the misc infos about the document too
    """
    ctrlSumList = []
    facult = False

    # iteration on each char of the given MRZ
    for charPos in range(len(code)):

        # Sanity check
        if len(getDocString(doc)) <= charPos:
            break

        field =  getDocString(doc)[charPos]

        if doc[1][field][1] == "CTRL":
            #print("{} is CTRL field {}".format(code[charPos], field))

            codeChain = ""
            # iteration on the fields to control
            for pos in range(len(code)):

                #print("Len : {}, pos : {}".format(len(getDocString(doc)), pos))
                # Sanity check
                if len(getDocString(doc)) <= pos:
                    break

                target =  getDocString(doc)[pos]
                if target in doc[1][field][3]:
                    #print("__field : {} {} {} {}".format(target, pos, field, doc[1][field][3]))
                    codeChain += code[pos]

            #print("chain to control : _{}_".format(codeChain))

            ctrlSum = computeControlSum(codeChain)
            #print("SUM : {} vs {}".format(code[charPos], ctrlSum))

            ctrlSumList += [ (field, charPos, ctrlSum, facult) ]

        if doc[1][field][1] == "CTRLF":
            #print("{} is CTRL field {}".format(code[charPos], field))

            codeChain = ""
            # iteration on the fields to control
            for pos in range(len(code)):
                target =  getDocString(doc)[pos]
                if target in doc[1][field][3]:
                    #print("__field : {} {} {} {}".format(target, pos, field, doc[1][field][3]))
                    codeChain += code[pos]

            #print("chain to control : _{}_".format(codeChain))

            ctrlSum = computeControlSum(codeChain)
            #print("SUM : {} vs {}".format(code[charPos], ctrlSum))

            if code[charPos] == "<":
                facult = True

            ctrlSumList += [ (field, charPos, ctrlSum, facult) ]

    return {
            "ctrlSumList" : ctrlSumList
            }


def getDocInfos(doc, code):
    # get all the types of infos that are in the document doc
    infoTypes = [ (doc[1][field][1], limits(doc[0][0] + doc[0][1], field)) for field in doc[1] ]

    res = {}

    # Length of MRZ
    length = len(code)
    if length == len(doc[0][0]+doc[0][1]):
        res["LEN"] = [length, True]
    else:
        res["LEN"] = [length, False]


    for field in infoTypes:

        value = code[ field[1][0] : field[1][1] ].replace("<", " ").strip()
        res[field[0]] = [0,0]

        # State code
        if field[0] == 'PAYS' or field[0] == 'NAT':
            try:
                if len(value) == 3 and value[-1] != "<":
                    res[field[0]] = (landcode3[value], True)
                elif len(value) == 3 and value[-1] == "<":
                    res[field[0]] = (landcode2[value[:-1]], True)
                else:
                    res[field[0]] = (landcode2[value], True)
            except KeyError:
                res[field[0]] = [value, False]

        # Dates
        elif field[0][1:] == 'DATE':
            # size adaptation
            if len(value) == 6:
                value = "{}/{}/{}".format(value[4:6], value[2:4], value[0:2])
            elif len(value) == 4:
                value = "{}/{}/{}".format("01", value[2:4], value[0:2])

            # date validation
            try:
                 datetime.datetime.strptime(value,"%d/%m/%y")
            except ValueError:
                #print(value)
                if value != "":
                    res[field[0]] = [value, False]
            else:
                res[field[0]] = [value, True]

        # Numbers
        elif field[0][:-1] == 'NOINT':
            try:
                res["NO"][0] += value
                res["NO"][1] = True
            except KeyError:
                res["NO"] = [value, True]

        elif field[0] == 'NOINT':
            try:
                res["NO"][0] += value
                res["NO"][1] = True
            except KeyError:
                res["NO"] = [value, True]

        elif field[0] == 'FACULT':
            try:
                res["INDIC"][0] += value
                res["INDIC"][1] = True
            except KeyError:
                res["INDIC"] = [value, True]

        # Sex
        elif field[0] == 'SEX':
            if not value in "MF":
                res[field[0]] = [value, False]
            else:
                res[field[0]] = [value, True]

        # All other cases
        else:
            if value != "":
                res[field[0]] = [value, True]

    return res































