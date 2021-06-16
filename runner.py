from __future__ import absolute_import, annotations

from collector import *
from saver import MySQLManager
from backup import Backup


# file = File("dataset/Tasso_occupazione.csv")
# file.get_data()

# OCCUPAZIONE
rename_column("dataset/Tasso_occupazione.csv")
delete_column("dataset_clean/Tasso_occupazione.csv", ['Territorio', 'TIPO_DATO_FOL', 'Tipo dato',
'Sesso', 'Classe di età', 'Seleziona periodo', 'Flag Codes', 'Flags'])
#
# # DISOCCUPAZIONE
rename_column("dataset/Tasso_disoccupazione.csv")
delete_column("dataset_clean/Tasso_disoccupazione.csv", ['Territorio', 'TIPO_DATO_FOL', 'Tipo dato',
 'Sesso', 'Classe di età', 'Seleziona periodo', 'Flag Codes', 'Flags'])

# QUALITA VITA
rename_column("dataset/Qualita_vita.csv")
delete_column("dataset_clean/Qualita_vita.csv", ['NOME PROVINCIA (ISTAT)', 'CODICE PROVINCIA ISTAT (STORICO)', 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE'])

# DATA 2016
save_file("dataset/ind16_ascii/carcom16.csv")
delete_column("dataset_clean/carcom16.csv", ["parent", "eta", "cit", "isco", "aningr", "motiv", "tipolau", "votoedu", "suedu", "selode", "annoedu", "tipodip",
                                                    "univer", "apqual", "asnonoc", "nascarea", "nace", "nordp", "motent", "annoenus", "NASCREG", "ireg", "CLETA5",
                                                    "Q", "SETT", "PESOFIT", "CFRED", "PERL", "NPERL", "NPERC", "AREA3", "ACOM4C"])

#save_file("dataset/ind16_ascii/rfam16.csv")
# delete_column("dataset_clean/rfam16.csv", ['YL', 'YL1', 'YL2', 'YT', 'YTP', 'YTP1', 'YTP2', 'YTA','YTA1',
#                                            'YTA2', 'YTA3', 'YTA31', 'YTA32', 'YM', 'YMA1', 'YMA2', 'YC',
#                                            'YCA', 'YCA1', 'YCA2', 'YCF', 'YCF1', 'YCF2', 'YCF3', 'YCF4', 'CLY',
#                                            'CLY2'])

save_file("dataset/ind16_ascii/rper16.csv")
delete_column("dataset_clean/rper16.csv", ['YL1','YL2','YTP1','YTP2','YTA1','YTA2','YTA31','YTA32',
                                           'YL','YTP','YTA3','YTA','YT','YM','YCA1','YCA2','YCA','YCF1','YCF2','YCF3',
                                           'YCF4','YCF','YC','YMA1','YMA2'])

save_file("dataset/dataset_samples/isf_w2.csv")
delete_column("dataset_clean/isf_w2.csv", ["A06","A08","A11","A12","A13","A14","A15","A16_1","A16A_1","A16_2","A16A_2",
                                           "A16_3","A16A_3","A16A_4","A16A_5","A16A_6","A17","A18","A19","A20","A21","A22",
                                           "A24","A25","A26","A27","A29","A30","A31","A32","A33","A34","A35","A36","A37","A38",
                                           "A39","A41","A42","A43","A44_1","A44_2","A44_3","A44_4","A44_5","A45_1_1",
                                           "A45_2_1","A45_3_1","A45_4_1","A45_5_1","A45_1_2","A45_2_2","A45_3_2","A45_4_2",
                                           "A45_5_2","A45_1_3","A45_2_3","A45_3_3","A45_4_3","A45_5_3","A45_1_4","A45_2_4",
                                           "A45_3_4","A45_4_4","A45_5_4","PESO","pesopanel","TITOLO","A07"])

# DISOCCUPAZIONE
clean_rows("dataset_clean/Tasso_disoccupazione.csv")

# OCCUPAZIONE
clean_rows("dataset_clean/Tasso_occupazione.csv")

# QUALITA' DELLA VITA -> save indicators
save(sub_table("dataset_clean/Qualita_vita.csv", "INDEX"))

# QUALITA' DELLA VITA -> clean rows
clean_rows("dataset_clean/Qualita_vita.csv")
clean_rows("dataset_clean/Qualita_vita.csv", ind=True)

# --------------------------------------------- DELETE INDECES NOT NEEDED --------------------------------------------
# List of indicators that will be deleted due to their inconsistency with the project purpose


lst_index = list_arg("dataset_clean/indicators.json")
indicators = [lst_index["Eventi sportivi"][1],
              lst_index["Indice di lettura dei quotidiani"][1],
              lst_index["Spettacoli - Spesa al botteghino"][1],
              lst_index["Furti"][1],
              lst_index["Furti in abitazione"][1],
              lst_index["Furti in esercizi commerciali"][1],
              lst_index["Estorsioni"][1],
              lst_index["Truffe e frodi informatiche"][1],
              lst_index["Incendi"][1],
              lst_index["Omicidi da incidente stradale"][1],
              lst_index["Violenze sessuali"][1],
              lst_index["Indice di litigiosit\u00e0"][1],
              lst_index["Durata media delle cause civili"][1],
              lst_index["Indice di rotazione delle cause"][1],
              lst_index["Quota cause pendenti ultratriennali"][1],
              lst_index["Riciclaggio e impiego di denaro"][1],
              lst_index["Incidenti stradali"][1],
              lst_index["Cancellazioni anagrafiche"][1],
              lst_index["Iscrizioni anagrafiche"][1],
              lst_index["Consumo di farmaci per asma e Bpco"][1],
              lst_index["Consumo di farmaci per diabete"][1],
              lst_index["Consumo di farmaci per ipertensione"][1],
              lst_index["Consumo di farmaci per la depressione"][1],
              lst_index["Infermieri"][1],
              lst_index["Pediatri"][1],
              lst_index["Calmanti e sonniferi"][1],
              lst_index["Casi Covid-19"][1],
              lst_index["Rata media mensile"][1],
              lst_index["Popolazione con crediti attivi"][1],
              lst_index["Fatture commerciali ai fornitori oltre i 30 giorni"][1],
              lst_index["Nuovi mutui per l'acquisto di abitazioni"][1],
              lst_index["Protesti"][1],
              lst_index["Partecipazione elettorale"][1],
              lst_index["Imprese in fallimento"][1],
              lst_index["Imprese che fanno ecommerce"][1],
              lst_index["Imprese straniere"][1],
              lst_index["Imprese in rete"][1],
              lst_index["Tasso di occupazione"][1],
              lst_index["Quota di export sul Pil"][1],
              lst_index["Banda larga"][1],
              lst_index["Cig ordinaria autorizzata"][1],
              lst_index["Ecosistema urbano"][1],
              lst_index["Assegni sociali"][1],
              lst_index["Il trend del Pil pro capite"][1],
              lst_index["Riqualificazioni energetiche degli immobili"][1],
              lst_index["Nuove iscrizioni di imprese"][1],
              lst_index["Indice di Rischio Climatico (CRI)"][1],
              lst_index["Fondi europei 2014-2020 per l'Agenda digitale"][1],
              lst_index["Fondi europei 2014-2020 per l'ambiente e la prevenzione dei rischi"][1],
              lst_index["Pago Pa - enti attivi"][1],
              lst_index["Indice trasormazione digitale"][1],
              lst_index["Partecipazione alla formazione continua"][1],
              lst_index["Cie erogate"][1],
              lst_index["Spid erogate"][1],
              lst_index["Pos attivi"][1]]

del_indicators("dataset_clean/Qualita_vita.csv", indicators)

# --------------------------------------------- DELETE "UNITA' di MISURA" -----------------------------------------------
# Delete the column of "unità di misura"
delete_column("dataset_clean\Qualita_vita.csv", ["UNITA' DI MISURA"])


# --------------------------------------------- CONNECTION WITH MYSQL -------------------------------------------------
#password = "luca0405" # change with your password
password = "Pr0tett0.98"
saver = MySQLManager(host="localhost",
                      port=3306,
                      user="root",
                      password=password,
                      database = "project_bdt")


#saver.check_database("project_bdt")

# Create table
#saver.create_table(lst_tables("dataset_clean\Tasso_disoccupazione.csv"))
#saver.create_table(lst_tables("dataset_clean\Qualita_vita.csv"))
#saver.create_table(lst_tables("dataset_clean\Tasso_occupazione.csv"))
#saver.create_table(lst_tables("dataset_clean/carcom16.csv"))
#saver.create_table(lst_tables("dataset_clean/rper16.csv"))
# change_nquest("dataset_clean/rper16.csv")
#Load data

#saver.save_SQL("dataset_clean\Tasso_disoccupazione.csv")
#saver.save_SQL("dataset_clean\Qualita_vita.csv")
#saver.save_SQL("dataset_clean\Tasso_occupazione.csv")
#saver.save_SQL("dataset_clean/carcom16.csv")
#saver.save_SQL("dataset_clean/rper16.csv")

# -------------------------------------------JOIN TABLES ------------------------------------------------

saver.join_SQL(table_1= "carcom16", table_2="rfam16", table_name="data_2016_fam")
saver.join_SQL(table_1= "carcom16", table_2="rper16", table_name="data_2016")

saver.label_irpef(table_name="data_2016")
saver.label_irpef(table_name="data_2016_fam")


#backup = Backup(saver, "C:/Users/lucia/Desktop") # set here your local path
#backup.set_backup()








