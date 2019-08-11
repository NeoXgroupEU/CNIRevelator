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
import logger    # logger.py
import re
import datetime

## SEX CODES
sexcode = {'M':'Homme', 'F':'Femme',  'X':'Non spécifié'}

## COUNTRY CODES

landcode2 = {
    'AW': 'Aruba',
    'AF': 'Afghanistan',
    'AO': 'Angola',
    'AI': 'Anguilla',
    'AL': 'Albanie',
    'AD': 'Andorre',
    'AE': 'Emirats arabes unis',
    'AR': 'Argentine',
    'AM': 'Arménie',
    'AS': 'Samoa américaines',
    'AQ': 'Antarctique',
    'TF': 'Terres australes et antarctiques françaises',
    'AG': 'Antigua-et-Barbuda',
    'AU': 'Australie',
    'AT': 'Autriche',
    'AZ': 'Azerbaidjan',
    'BI': 'Burundi',
    'BE': 'Belgique',
    'BJ': 'Benin',
    'BQ': 'Pays-Bas caribéens',
    'BF': 'Burkina Faso',
    'BD': 'Bangladesh',
    'BG': 'Bulgarie',
    'BH': 'Bahrein',
    'BS': 'Bahamas',
    'BA': 'Bosnie-Herzegovine',
    'BL': 'Saint-Barthélemy',
    'BY': 'Bielorussie',
    'BZ': 'Belize',
    'BM': 'Bermudes',
    'BO': 'Bolivie',
    'BR': 'Brésil',
    'BB': 'Barbade',
    'BN': 'Brunei',
    'BT': 'Bhoutan',
    'BW': 'Botswana',
    'CF': 'République Centrafricaine',
    'CA': 'Canada',
    'CC': 'Îles Cocos',
    'CH': 'Suisse',
    'CL': 'Chili',
    'CN': 'Chine',
    'CI': "Côte d'Ivoire",
    'CM': 'Cameroun',
    'CD': 'Congo (République démocratique)',
    'CG': 'Congo (République)',
    'CK': 'Îles Cook',
    'CO': 'Colombie',
    'KM': 'Comores',
    'CV': 'Cap-Vert',
    'CR': 'Costa Rica',
    'CU': 'Cuba',
    'CW': 'Curaçao',
    'CX': 'Île Christmas',
    'KY': 'Caimans',
    'CY': 'Chypre',
    'CZ': 'Tchéquie',
    'DE': 'Allemagne',
    'DJ': 'Djibouti',
    'DM': 'Dominique',
    'DK': 'Danemark',
    'DO': 'République dominicaine',
    'DZ': 'Algérie',
    'EC': 'Equateur',
    'EG': 'Egypte',
    'ER': 'Erythrée',
    'EH': 'Sahara occidental',
    'ES': 'Espagne',
    'EE': 'Estonie',
    'ET': 'Ethiopie',
    'FI': 'Finlande',
    'FJ': 'Fidji',
    'FK': 'Îles Malouines',
    'FR': 'France',
    'FO': 'Féroé',
    'FM': 'Micronésie',
    'GA': 'Gabon',
    'GB': 'Royaume-Uni',
    'GE': 'Géorgie',
    'GG': 'Guernesey',
    'GH': 'Ghana',
    'GI': 'Gibraltar',
    'GN': 'Guinée',
    'GP': 'Guadeloupe',
    'GM': 'Gambie',
    'GW': 'Guinée-Bissau',
    'GQ': 'Guinée équatoriale',
    'GR': 'Grèce',
    'GD': 'Grenade',
    'GL': 'Groenland',
    'GT': 'Guatemala',
    'GF': 'Guyane',
    'GU': 'Guam',
    'GY': 'Guyana',
    'HK': 'Hong Kong',
    'HN': 'Honduras',
    'HR': 'Croatie',
    'HT': 'Haïti',
    'HU': 'Hongrie',
    'ID': 'Indonésie',
    'IM': 'Île de Man',
    'IN': 'Inde',
    'IO': "Territoire britannique de l'océan Indien",
    'IE': 'Irlande',
    'IR': 'Irak',
    'IQ': 'Iran',
    'IS': 'Islande',
    'IL': 'Israël',
    'IT': 'Italie',
    'JM': 'Jamaïque',
    'JE': 'Jersey',
    'JO': 'Jordanie',
    'JP': 'Japon',
    'KZ': 'Kazakhstan',
    'KE': 'Kenya',
    'KG': 'Kirghizistan',
    'KH': 'Cambodge',
    'KI': 'Kiribati',
    'KN': 'Saint-Christophe-et-Niévès',
    'KR': 'Corée du Sud',
    'KW': 'Koweït',
    'LA': 'Laos',
    'LB': 'Liban',
    'LR': 'Liberia',
    'LY': 'Libye',
    'LC': 'Sainte-Lucie',
    'LI': 'Liechtenstein',
    'LK': 'Sri Lanka',
    'LS': 'Lesotho',
    'LT': 'Lituanie',
    'LU': 'Luxembourg',
    'LV': 'Lettonie',
    'MO': 'Macao',
    'MF': 'Sint-Maarten',
    'MA': 'Maroc',
    'MC': 'Monaco',
    'MD': 'Moldavie',
    'MG': 'Madagascar',
    'MV': 'Maldives',
    'MX': 'Mexique',
    'MH': 'Marshall',
    'MK': 'Macedoine',
    'ML': 'Mali',
    'MT': 'Malte',
    'MM': 'Birmanie',
    'ME': 'Monténégro',
    'MN': 'Mongolie',
    'MP': 'Îles Mariannes du Nord',
    'MZ': 'Mozambique',
    'MR': 'Mauritanie',
    'MS': 'Montserrat',
    'MQ': 'Martinique',
    'MU': 'Maurice',
    'MW': 'Malawi',
    'MY': 'Malaisie',
    'YT': 'Mayotte',
    'NA': 'Namibie',
    'NC': 'Nouvelle-Calédonie',
    'NE': 'Niger',
    'NF': 'Île Norfolk',
    'NG': 'Nigeria',
    'NI': 'Nicaragua',
    'NU': 'Niue',
    'NL': 'Pays-Bas',
    'NO': 'Norvège',
    'NP': 'Nepal',
    'NR': 'Nauru',
    'NZ': 'Nouvelle-Zélande',
    'OM': 'Oman',
    'PK': 'Pakistan',
    'PA': 'Panama',
    'PN': 'Îles Pitcairn',
    'PE': 'Pérou',
    'PH': 'Philippines',
    'PW': 'Palaos',
    'PG': 'Papouasie-Nouvelle-Guinée',
    'PL': 'Pologne',
    'PR': 'Porto Rico',
    'KP': 'Corée du Nord',
    'PT': 'Portugal',
    'PY': 'Paraguay',
    'PS': 'Palestine',
    'PF': 'Polynésie française',
    'QA': 'Qatar',
    'RE': 'Réunion',
    'RO': 'Roumanie',
    'RU': 'Russie',
    'RW': 'Rwanda',
    'SA': 'Arabie saoudite',
    'SD': 'Soudan',
    'SN': 'Sénégal',
    'SG': 'Singapour',
    'GS': 'Georgie du Sud-et-les iles Sandwich du Sud',
    'SH': 'Sainte-Hélène, Ascension et Tristan da Cunha',
    'SJ': 'Svalbard et île Jan Mayen',
    'SB': 'Salomon',
    'SL': 'Sierra Leone',
    'SV': 'Salvador',
    'SM': 'Saint-Marin',
    'SO': 'Somalie',
    'PM': 'Saint-Pierre-et-Miquelon',
    'RS': 'Serbie',
    'SS': 'Soudan du Sud',
    'ST': 'Sao Tomé-et-Principe',
    'SR': 'Suriname',
    'SK': 'Slovaquie',
    'SI': 'Slovénie',
    'SE': 'Suède',
    'SZ': 'eSwatani',
    'SX': 'Saint-Martin ',
    'SC': 'Seychelles',
    'SY': 'Syrie',
    'TC': 'Îles Turques-et-Caïques',
    'TD': 'Tchad',
    'TG': 'Togo',
    'TH': 'Thaïlande',
    'TJ': 'Tadjikistan',
    'TK': 'Tokelau',
    'TM': 'Turkmenistan',
    'TL': 'Timor oriental',
    'TO': 'Tonga',
    'TT': 'Trinité-et-Tobago',
    'TN': 'Tunisie',
    'TR': 'Turquie',
    'TV': 'Tuvalu',
    'TW': 'Taiwan',
    'TZ': 'Tanzanie',
    'UG': 'Ouganda',
    'UA': 'Ukraine',
    'UY': 'Uruguay',
    'US': 'Etats-Unis',
    'UZ': 'Ouzbékistan',
    'VA': 'Saint-Siège (État de la Cité du Vatican)',
    'VC': 'Saint-Vincent-et-les-Grenadines',
    'VE': 'Venezuela',
    'VG': 'Îles Vierges britanniques',
    'VI': 'Îles Vierges des États-Unis',
    'VN': 'Viêt Nam',
    'VU': 'Vanuatu',
    'WF': 'Wallis-et-Futuna',
    'WS': 'Samoa',
    'XK': 'Kosovo',
    'YE': 'Yémen',
    'ZA': 'Afrique du Sud',
    'ZM': 'Zambie',
    'ZW': 'Zimbabwe'
 }

landcode3 = {
    'ABW': 'Aruba',
    'AFG': 'Afghanistan',
    'AGO': 'Angola',
    'AIA': 'Anguilla',
    'ALB': 'Albanie',
    'AND': 'Andorre',
    'ARE': 'Emirats arabes unis',
    'ARG': 'Argentine',
    'ARM': 'Arménie',
    'ASM': 'Samoa américaines',
    'ATA': 'Antarctique',
    'ATF': 'Terres australes et antarctiques françaises',
    'ATG': 'Antigua-et-Barbuda',
    'AUS': 'Australie',
    'AUT': 'Autriche',
    'AZE': 'Azerbaidjan',
    'BDI': 'Burundi',
    'BEL': 'Belgique',
    'BEN': 'Benin',
    'BES': 'Pays-Bas caribéens',
    'BFA': 'Burkina Faso',
    'BGD': 'Bangladesh',
    'BGR': 'Bulgarie',
    'BHR': 'Bahrein',
    'BHS': 'Bahamas',
    'BIH': 'Bosnie-Herzegovine',
    'BLM': 'Saint-Barthélemy',
    'BLR': 'Bielorussie',
    'BLZ': 'Belize',
    'BMU': 'Bermudes',
    'BOL': 'Bolivie',
    'BRA': 'Brésil',
    'BRB': 'Barbade',
    'BRN': 'Brunei',
    'BTN': 'Bhoutan',
    'BWA': 'Botswana',
    'CAF': 'République Centrafricaine',
    'CAN': 'Canada',
    'CCK': 'Îles Cocos',
    'CHE': 'Suisse',
    'CHL': 'Chili',
    'CHN': 'Chine',
    'CIV': "Côte d'Ivoire",
    'CMR': 'Cameroun',
    'COD': 'Congo (République démocratique)',
    'COG': 'Congo (République)',
    'COK': 'Îles Cook',
    'COL': 'Colombie',
    'COM': 'Comores',
    'CPV': 'Cap-Vert',
    'CRI': 'Costa Rica',
    'CUB': 'Cuba',
    'CUW': 'Curaçao',
    'CXR': 'Île Christmas',
    'CYM': 'Caimans',
    'CYP': 'Chypre',
    'CZE': 'Tchéquie',
    'DEU': 'Allemagne',
    'DJI': 'Djibouti',
    'DMA': 'Dominique',
    'DNK': 'Danemark',
    'DOM': 'République dominicaine',
    'DZA': 'Algérie',
    'ECU': 'Equateur',
    'EGY': 'Egypte',
    'ERI': 'Erythrée',
    'ESH': 'Sahara occidental',
    'ESP': 'Espagne',
    'EST': 'Estonie',
    'ETH': 'Ethiopie',
    'FIN': 'Finlande',
    'FJI': 'Fidji',
    'FLK': 'Îles Malouines',
    'FRA': 'France',
    'FRO': 'Féroé',
    'FSM': 'Micronésie',
    'GAB': 'Gabon',
    'GBR': 'Royaume-Uni',
    'GEO': 'Géorgie',
    'GGY': 'Guernesey',
    'GHA': 'Ghana',
    'GIB': 'Gibraltar',
    'GIN': 'Guinée',
    'GLP': 'Guadeloupe',
    'GMB': 'Gambie',
    'GNB': 'Guinée-Bissau',
    'GNQ': 'Guinée équatoriale',
    'GRC': 'Grèce',
    'GRD': 'Grenade',
    'GRL': 'Groenland',
    'GTM': 'Guatemala',
    'GUF': 'Guyane',
    'GUM': 'Guam',
    'GUY': 'Guyana',
    'HKG': 'Hong Kong',
    'HND': 'Honduras',
    'HRV': 'Croatie',
    'HTI': 'Haïti',
    'HUN': 'Hongrie',
    'IDN': 'Indonésie',
    'IMN': 'Île de Man',
    'IND': 'Inde',
    'IOT': "Territoire britannique de l'océan Indien",
    'IRL': 'Irlande',
    'IRN': 'Irak',
    'IRQ': 'Iran',
    'ISL': 'Islande',
    'ISR': 'Israël',
    'ITA': 'Italie',
    'JAM': 'Jamaïque',
    'JEY': 'Jersey',
    'JOR': 'Jordanie',
    'JPN': 'Japon',
    'KAZ': 'Kazakhstan',
    'KEN': 'Kenya',
    'KGZ': 'Kirghizistan',
    'KHM': 'Cambodge',
    'KIR': 'Kiribati',
    'KNA': 'Saint-Christophe-et-Niévès',
    'KOR': 'Corée du Sud',
    'KWT': 'Koweït',
    'LAO': 'Laos',
    'LBN': 'Liban',
    'LBR': 'Liberia',
    'LBY': 'Libye',
    'LCA': 'Sainte-Lucie',
    'LIE': 'Liechtenstein',
    'LKA': 'Sri Lanka',
    'LSO': 'Lesotho',
    'LTU': 'Lituanie',
    'LUX': 'Luxembourg',
    'LVA': 'Lettonie',
    'MAC': 'Macao',
    'MAF': 'Sint-Maarten',
    'MAR': 'Maroc',
    'MCO': 'Monaco',
    'MDA': 'Moldavie',
    'MDG': 'Madagascar',
    'MDV': 'Maldives',
    'MEX': 'Mexique',
    'MHL': 'Marshall',
    'MKD': 'Macedoine',
    'MLI': 'Mali',
    'MLT': 'Malte',
    'MMR': 'Birmanie',
    'MNE': 'Monténégro',
    'MNG': 'Mongolie',
    'MNP': 'Îles Mariannes du Nord',
    'MOZ': 'Mozambique',
    'MRT': 'Mauritanie',
    'MSR': 'Montserrat',
    'MTQ': 'Martinique',
    'MUS': 'Maurice',
    'MWI': 'Malawi',
    'MYS': 'Malaisie',
    'MYT': 'Mayotte',
    'NAM': 'Namibie',
    'NCL': 'Nouvelle-Calédonie',
    'NER': 'Niger',
    'NFK': 'Île Norfolk',
    'NGA': 'Nigeria',
    'NIC': 'Nicaragua',
    'NIU': 'Niue',
    'NLD': 'Pays-Bas',
    'NOR': 'Norvège',
    'NPL': 'Nepal',
    'NRU': 'Nauru',
    'NZL': 'Nouvelle-Zélande',
    'OMN': 'Oman',
    'PAK': 'Pakistan',
    'PAN': 'Panama',
    'PCN': 'Îles Pitcairn',
    'PER': 'Pérou',
    'PHL': 'Philippines',
    'PLW': 'Palaos',
    'PNG': 'Papouasie-Nouvelle-Guinée',
    'POL': 'Pologne',
    'PRI': 'Porto Rico',
    'PRK': 'Corée du Nord',
    'PRT': 'Portugal',
    'PRY': 'Paraguay',
    'PSE': 'Palestine',
    'PYF': 'Polynésie française',
    'QAT': 'Qatar',
    'REU': 'Réunion',
    'ROU': 'Roumanie',
    'RUS': 'Russie',
    'RWA': 'Rwanda',
    'SAU': 'Arabie saoudite',
    'SDN': 'Soudan',
    'SEN': 'Sénégal',
    'SGP': 'Singapour',
    'SGS': 'Georgie du Sud-et-les iles Sandwich du Sud',
    'SHN': 'Sainte-Hélène, Ascension et Tristan da Cunha',
    'SJM': 'Svalbard et île Jan Mayen',
    'SLB': 'Salomon',
    'SLE': 'Sierra Leone',
    'SLV': 'Salvador',
    'SMR': 'Saint-Marin',
    'SOM': 'Somalie',
    'SPM': 'Saint-Pierre-et-Miquelon',
    'SRB': 'Serbie',
    'SSD': 'Soudan du Sud',
    'STP': 'Sao Tomé-et-Principe',
    'SUR': 'Suriname',
    'SVK': 'Slovaquie',
    'SVN': 'Slovénie',
    'SWE': 'Suède',
    'SWZ': 'eSwatani',
    'SXM': 'Saint-Martin ',
    'SYC': 'Seychelles',
    'SYR': 'Syrie',
    'TCA': 'Îles Turques-et-Caïques',
    'TCD': 'Tchad',
    'TGO': 'Togo',
    'THA': 'Thaïlande',
    'TJK': 'Tadjikistan',
    'TKL': 'Tokelau',
    'TKM': 'Turkmenistan',
    'TLS': 'Timor oriental',
    'TON': 'Tonga',
    'TTO': 'Trinité-et-Tobago',
    'TUN': 'Tunisie',
    'TUR': 'Turquie',
    'TUV': 'Tuvalu',
    'TWN': 'Taiwan',
    'TZA': 'Tanzanie',
    'UGA': 'Ouganda',
    'UKR': 'Ukraine',
    'URY': 'Uruguay',
    'USA': 'Etats-Unis',
    'UZB': 'Ouzbékistan',
    'VAT': 'Saint-Siège (État de la Cité du Vatican)',
    'VCT': 'Saint-Vincent-et-les-Grenadines',
    'VEN': 'Venezuela',
    'VGB': 'Îles Vierges britanniques',
    'VIR': 'Îles Vierges des États-Unis',
    'VNM': 'Viêt Nam',
    'VUT': 'Vanuatu',
    'WLF': 'Wallis-et-Futuna',
    'WSM': 'Samoa',
    'XKX': 'Kosovo',
    'YEM': 'Yémen',
    'ZAF': 'Afrique du Sud',
    'ZMB': 'Zambie',
    'ZWE': 'Zimbabwe',
    'NTZ': 'Zone neutre',
    'UNO': 'Fonctionnaire des Nations Unies',
    'UNA': "Fonctionnaire d'une organisation affiliée aux Nations Unies",
    'UNK': 'Représentant des Nations Unies au Kosovo',
    'XXA': 'Apatride Convention 1954',
    'XXB': 'Réfugié Convention 1954',
    'XXC': 'Réfugié autre',
    'XXX': 'Résident Légal de Nationalité Inconnue',
    'D': 'Allemagne',
    'EUE': 'Union Européenne',
    'GBD': "Citoyen Britannique d'Outre-mer (BOTC)",
    'GBN': 'British National (Overseas)',
    'GBO': 'British Overseas Citizen',
    'GBP': 'British Protected Person',
    'GBS': 'British Subject',
    'XBA': 'Banque Africaine de Développement',
    'XIM': "Banque Africaine d'Export–Import",
    'XCC': 'Caribbean Community or one of its emissaries',
    'XCO': 'Common Market for Eastern and Southern Africa',
    'XEC': 'Economic Community of West African States',
    'XPO': 'International Criminal Police Organization',
    'XOM': 'Sovereign Military Order of Malta',
    'RKS': 'Kosovo',
    'WSA': 'World Service Authority World Passport'
}

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
  "Passeport"
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
  "Carte-passeport"
]

I_ = [
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
  "Titre d'identité/de voyage"
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
  "Certificat de membre d'équipage"
]

VA = [
  ["11222333333333333333333333333333333333333333", "444444444566677777789AAAAAABCCCCCCCCCCCCCCCCC"],
  {
    "1": ["2", "CODE", "V."],
    "2": ["3", "PAYS", "[A-Z]+"],
    "3": ["39", "NOM", "[A-Z]+"],
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
  "Visa de type A"
]

VB = [
  ["112223333333333333333333333333333333", "444444444566677777789AAAAAABCCCCCC"],
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
  "Visa de type B"
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
  "Carte de séjour"
]

I__ = [
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
  "Pièce d'identité/de voyage"
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
  "Pièce d'identité FR"
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
  "Permis de conduire"
]

TYPES = [IDFR, I__, VB, VA, AC, I_, IP, P, DL, TSF]

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

    #logfile.printdbg("{} level : {}/{}  (+{})".format(doc[2], level, nchar, bonus))
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
    # Return the candidates
    #logfile.printdbg("Scores     : {}".format(SCORES))
    #logfile.printdbg("Candidates : {}".format(canditxt))
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
        field =  getDocString(doc)[charPos]

        if doc[1][field][1] == "CTRL":
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

    for field in infoTypes:

        value = code[ field[1][0] : field[1][1] ].replace("<", " ").strip()

        # State code
        if field[0] == 'PAYS' or field[0] == 'NAT':
            try:
                if len(value) == 3 and value[-1] != "<":
                    res[field[0]] = landcode3[value]
                elif len(value) == 3 and value[-1] == "<":
                    res[field[0]] = landcode2[value[:-1]]
                else:
                    res[field[0]] = landcode2[value]
            except KeyError:
                res[field[0]] = False

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
                    res[field[0]] = False
            else:
                res[field[0]] = value

        # Numbers
        elif field[0][:-1] == 'NOINT':
            try:
                res["NO"] += value
            except KeyError:
                res["NO"] = value
        elif field[0] == 'NOINT':
            try:
                res["NO"] += value
            except KeyError:
                res["NO"] = value

        elif field[0] == 'FACULT':
            try:
                res["INDIC"] += value
            except KeyError:
                res["INDIC"] = value
        # All other cases
        else:
            if value != "":
                res[field[0]] = value

    return res































