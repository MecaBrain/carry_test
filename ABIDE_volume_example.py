# VAS Y LIONEL T ES BIEN PARTIT
import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
import table_atlas_figure as tA
import numpy as np

if __name__ == "__main__":
    # load the tables that will be used in this tutorial
    df_phenotype = pd.read_excel('/mnt/data/owncloud/TP_meca_retraite/Phenotypic_V1_0b_traitements_visual_check_GA.xls', 'Feuille1')
    df_phenotype['SITE_ID'] = df_phenotype['SITE_ID'].astype('category')
    df_phenotype['DX_GROUP'] = df_phenotype['DX_GROUP'].astype('category')

    df_morphometry = pd.read_csv('/mnt/data/owncloud/TP_meca_retraite/ABIDE_aseg_stats.txt', sep='\t')
    print(df_morphometry.head())
    print(df_morphometry.columns)
    print(df_morphometry.describe())
    print(df_morphometry.dtypes)


    df_pheno_morpho = df_phenotype.merge(df_morphometry, left_on='SUB_ID', right_on='Measure:volume', how='inner')

    sns.catplot(x='SITE_ID', y='Left-Hippocampus', hue='DX_GROUP', kind="violin", inner="stick", split=True,
            palette="pastel", data=df_pheno_morpho)




    #default_label_name = {7: "Left-Cerebellum-White-Matter", 8: "Left-Cerebellum-Cortex", 9: "Left-Thalamus", 10: "Left-Thalamus-Proper", 11: "Left-Caudate", 12: "Left-Putamen", 13: "Left-Pallidum", 14: "3rd-Ventricle", 15: "4th-Ventricle", 16: "Brain-Stem", 17: "Left-Hippocampus", 18: "Left-Amygdala", 19: "Left-Insula", 26: "Left-Accumbens-area", 28: "Left-VentralDC", 46: "Right-Cerebral-White-Matter", 47: "Right-Cerebral-Cortex", 48: "Right-Thalamus", 49: "Right-Thalamus-Proper", 50: "Right-Caudate", 51: "Right-Putamen", 52: "Right-Pallidum", 53: "Right-Hippocampus", 54: "Right-Amygdala", 55: "Right-Insula", 58: "Right-Accumbens-area", 60: "Right-VentralDC", 192: "Corpus_Callosum", 1000: "ctx-lh-unknown", 1001: "ctx-lh-bankssts", 1002: "ctx-lh-caudalanteriorcingulate", 1003: "ctx-lh-caudalmiddlefrontal", 1004: "ctx-lh-corpuscallosum", 1005: "ctx-lh-cuneus", 1006: "ctx-lh-entorhinal", 1007: "ctx-lh-fusiform", 1008: "ctx-lh-inferiorparietal", 1009: "ctx-lh-inferiortemporal", 1010: "ctx-lh-isthmuscingulate", 1011: "ctx-lh-lateraloccipital", 1012: "ctx-lh-lateralorbitofrontal", 1013: "ctx-lh-lingual", 1014: "ctx-lh-medialorbitofrontal", 1015: "ctx-lh-middletemporal", 1016: "ctx-lh-parahippocampal", 1017: "ctx-lh-paracentral", 1018: "ctx-lh-parsopercularis", 1019: "ctx-lh-parsorbitalis", 1020: "ctx-lh-parstriangularis", 1021: "ctx-lh-pericalcarine", 1022: "ctx-lh-postcentral", 1023: "ctx-lh-posteriorcingulate", 1024: "ctx-lh-precentral", 1025: "ctx-lh-precuneus", 1026: "ctx-lh-rostralanteriorcingulate", 1027: "ctx-lh-rostralmiddlefrontal", 1028: "ctx-lh-superiorfrontal", 1029: "ctx-lh-superiorparietal", 1030: "ctx-lh-superiortemporal", 1031: "ctx-lh-supramarginal", 1032: "ctx-lh-frontalpole", 1033: "ctx-lh-temporalpole", 1034: "ctx-lh-transversetemporal", 1035: "ctx-lh-insula", 2000: "ctx-rh-unknown", 2001: "ctx-rh-bankssts", 2002: "ctx-rh-caudalanteriorcingulate", 2003: "ctx-rh-caudalmiddlefrontal", 2004: "ctx-rh-corpuscallosum", 2005: "ctx-rh-cuneus", 2006: "ctx-rh-entorhinal", 2007: "ctx-rh-fusiform", 2008: "ctx-rh-inferiorparietal", 2009: "ctx-rh-inferiortemporal", 2010: "ctx-rh-isthmuscingulate", 2011: "ctx-rh-lateraloccipital", 2012: "ctx-rh-lateralorbitofrontal", 2013: "ctx-rh-lingual", 2014: "ctx-rh-medialorbitofrontal", 2015: "ctx-rh-middletemporal", 2016: "ctx-rh-parahippocampal", 2017: "ctx-rh-paracentral", 2018: "ctx-rh-parsopercularis", 2019: "ctx-rh-parsorbitalis", 2020: "ctx-rh-parstriangularis", 2021: "ctx-rh-pericalcarine", 2022: "ctx-rh-postcentral", 2023: "ctx-rh-posteriorcingulate", 2024: "ctx-rh-precentral", 2025: "ctx-rh-precuneus", 2026: "ctx-rh-rostralanteriorcingulate", 2027: "ctx-rh-rostralmiddlefrontal", 2028: "ctx-rh-superiorfrontal", 2029: "ctx-rh-superiorparietal", 2030: "ctx-rh-superiortemporal", 2031: "ctx-rh-supramarginal", 2032: "ctx-rh-frontalpole", 2033: "ctx-rh-temporalpole", 2034: "ctx-rh-transversetemporal", 2035: "ctx-rh-insula", 3000: "wm-lh-unknown", 3001: "wm-lh-bankssts", 3002: "wm-lh-caudalanteriorcingulate", 3003: "wm-lh-caudalmiddlefrontal", 3004: "wm-lh-corpuscallosum", 3005: "wm-lh-cuneus", 3006: "wm-lh-entorhinal", 3007: "wm-lh-fusiform", 3008: "wm-lh-inferiorparietal", 3009: "wm-lh-inferiortemporal", 3010: "wm-lh-isthmuscingulate", 3011: "wm-lh-lateraloccipital", 3012: "wm-lh-lateralorbitofrontal", 3013: "wm-lh-lingual", 3014: "wm-lh-medialorbitofrontal", 3015: "wm-lh-middletemporal", 3016: "wm-lh-parahippocampal", 3017: "wm-lh-paracentral", 3018: "wm-lh-parsopercularis", 3019: "wm-lh-parsorbitalis", 3020: "wm-lh-parstriangularis", 3021: "wm-lh-pericalcarine", 3022: "wm-lh-postcentral", 3023: "wm-lh-posteriorcingulate", 3024: "wm-lh-precentral", 3025: "wm-lh-precuneus", 3026: "wm-lh-rostralanteriorcingulate", 3027: "wm-lh-rostralmiddlefrontal", 3028: "wm-lh-superiorfrontal", 3029: "wm-lh-superiorparietal", 3030: "wm-lh-superiortemporal", 3031: "wm-lh-supramarginal", 3032: "wm-lh-frontalpole", 3033: "wm-lh-temporalpole", 3034: "wm-lh-transversetemporal", 3035: "wm-lh-insula", 4000: "wm-rh-unknown", 4001: "wm-rh-bankssts", 4002: "wm-rh-caudalanteriorcingulate", 4003: "wm-rh-caudalmiddlefrontal", 4004: "wm-rh-corpuscallosum", 4005: "wm-rh-cuneus", 4006: "wm-rh-entorhinal", 4007: "wm-rh-fusiform", 4008: "wm-rh-inferiorparietal", 4009: "wm-rh-inferiortemporal", 4010: "wm-rh-isthmuscingulate", 4011: "wm-rh-lateraloccipital", 4012: "wm-rh-lateralorbitofrontal", 4013: "wm-rh-lingual", 4014: "wm-rh-medialorbitofrontal", 4015: "wm-rh-middletemporal", 4016: "wm-rh-parahippocampal", 4017: "wm-rh-paracentral", 4018: "wm-rh-parsopercularis", 4019: "wm-rh-parsorbitalis", 4020: "wm-rh-parstriangularis", 4021: "wm-rh-pericalcarine", 4022: "wm-rh-postcentral", 4023: "wm-rh-posteriorcingulate", 4024: "wm-rh-precentral", 4025: "wm-rh-precuneus", 4026: "wm-rh-rostralanteriorcingulate", 4027: "wm-rh-rostralmiddlefrontal", 4028: "wm-rh-superiorfrontal", 4029: "wm-rh-superiorparietal", 4030: "wm-rh-superiortemporal", 4031: "wm-rh-supramarginal", 4032: "wm-rh-frontalpole", 4033: "wm-rh-temporalpole", 4034: "wm-rh-transversetemporal", 4035: "wm-rh-insula", 10000: "Unknown", 10001: "Middle_cerebellar_peduncle", 10002: "Pontine_crossing_tract", 10003: "Genu_of_corpus_callosum", 10004: "Body_of_corpus_callosum", 10005: "Splenium_of_corpus_callosum", 10006: "Fornix", 10007: "Corticospinal_tract_rh", 10008: "Corticospinal_tract_lh", 10009: "Medial_lemniscus_rh", 10010: "Medial_lemniscus_lh", 10011: "Inferior_cerebellar_peduncle_rh", 10012: "Inferior_cerebellar_peduncle_lh", 10013: "Superior_cerebellar_peduncle_rh", 10014: "Superior_cerebellar_peduncle_lh", 10015: "Cerebral_peduncle_rh", 10016: "Cerebral_peduncle_lh", 10017: "Anterior_limb_of_internal_capsule_rh", 10018: "Anterior_limb_of_internal_capsule_lh", 10019: "Posterior_limb_of_internal_capsule_rh", 10020: "Posterior_limb_of_internal_capsule_lh", 10021: "Retrolenticular_internal_capsule_rh", 10022: "Retrolenticular_internal_capsule_lh", 10023: "Anterior_corona_radiata_rh", 10024: "Anterior_corona_radiata_lh", 10025: "Superior_corona_radiata_rh", 10026: "Superior_corona_radiata_lh", 10027: "Posterior_corona_radiata_rh", 10028: "Posterior_corona_radiata_lh", 10029: "Posterior_thalamic_radiation_rh", 10030: "Posterior_thalamic_radiation_lh", 10031: "Sagittal_stratum_rh", 10032: "Sagittal_stratum_lh", 10033: "External_capsule_rh", 10034: "External_capsule_lh", 10035: "Cingulum_(cingulate_gyrus)_rh", 10036: "Cingulum_(cingulate_gyrus)_lh", 10037: "Cingulum_(hippocampus)_rh", 10038: "Cingulum_(hippocampus)_lh", 10039: "Fornix_(cres)_Stria_terminalis_rh", 10040: "Fornix_(cres)_Stria_terminalis_lh", 10041: "Superior_longitudinal_fasciculus_rh", 10042: "Superior_longitudinal_fasciculus_lh", 10043: "Sup_fronto_occipital_fasciculus_rh", 10044: "Sup_fronto_occipital_fasciculus_lh", 10045: "Uncinate_fasciculus_rh", 10046: "Uncinate_fasciculus_lh", 10047: "Tapetum_rh", 10048: "Tapetum_lh"}
    label_name = tA.readLookupTable('/mnt/data/owncloud/TP_meca_retraite/lookuptable.csv')
    print(label_name)
    output_figure = '/mnt/data/owncloud/TP_meca_retraite/ABIDE_aseg.png'

    data = df_morphometry.values[:,1:]

    print(data.shape)
    avg = np.mean(data,0)
    avg[avg==0]=1
    fig_data = 100*np.std(data,0)/avg
    print(fig_data.shape)
    print('min of data = ', np.min(fig_data))
    print('max of data = ', np.max(fig_data))
    plt.figure()
    plt.hist(fig_data, 100)
    clmap = tA.linear_interp_RGBA_colormap([0, 0, 255, 0, 255], [100, 255, 0, 0, 255], res=256)
    #clmap = [[ -np.Inf, 205, 205, 205, 255],[ 0, 255, 204, 255, 255], [5, 255, 153, 255, 255], [10, 255, 51, 255, 255], [15, 204, 0, 204, 255], [20, 102, 0, 102, 255], [25, 51, 0, 51, 255] ]

    tA.make_figure(fig_data, df_morphometry.columns[1:].tolist(), output_figure, label_name, clmap, show_fig=True)


    plt.show()
