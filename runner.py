from __future__ import absolute_import, annotations
from collector import *


# OCCUPAZIONE
#rename_column("dataset/Tasso_occupazione.csv")
#delete_column("dataset_clean/Tasso_occupazione.csv", ['Territorio', 'TIPO_DATO_FOL', 'Tipo dato',
# 'Sesso', 'Classe di età', 'Seleziona periodo', 'Flag Codes', 'Flags'])

# DISOCCUPAZIONE
#rename_column("dataset/Tasso_disoccupazione.csv")
#delete_column("dataset_clean/Tasso_disoccupazione.csv", ['Territorio', 'TIPO_DATO_FOL', 'Tipo dato',
# 'Sesso', 'Classe di età', 'Seleziona periodo', 'Flag Codes', 'Flags'])

# QUALITA VITA
rename_column("dataset/Qualita_vita.csv")
delete_column("dataset_clean/Qualita_vita.csv", ['NOME PROVINCIA (ISTAT)', 'CODICE PROVINCIA ISTAT (STORICO)',
                                                 'DENOMINAZIONE CORRENTE', 'FONTE ORIGINALE'])


# DISOCCUPAZIONE
# clean_rows("dataset_clean/Tasso_disoccupazione.csv")

# OCCUPAZIONE
#clean_rows("dataset_clean/Tasso_occupazione.csv")


# QUALITA' DELLA VITA
clean_rows("dataset_clean/Qualita_vita.csv")

save(sub_table("dataset_clean\Qualita_vita.csv"))

clean_rows("dataset_clean\Qualita_vita.csv", ind=True)

# --------------------------------------------- DELETE INDECES NOT NEEDED --------------------------------------------
# ist of indicators that will be deleted due to their inconsistency with the project purpose

lst_index = list_arg("dataset_clean\indicators.json")
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
              lst_index["Pos attivi"][1],
              ]
del_indicators("dataset_clean/Qualita_vita.csv", indicators)

# --------------------------------------------- DELETE "UNITA' di MISURA" -----------------------------------------------
# Delete the column of "unità di misura"
#delete_column("dataset_clean\Qualita_vita.csv", ["UNITA' DI MISURA"])