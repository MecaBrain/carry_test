import nibabel as nb
import numpy as np
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
ATLAS_FOLDER = '/hpc/meca/users/velly/Python/RESOURCES/TEMPLATE'

def linear_interp_RGBA_colormap(val_color_A, val_color_B, res=256):
    '''
    linear interpolation to create colormaps
    :param val_color_A: list of length 5 setting the value and corresponding RGBA color for the inferior bound ot he colormap.
    :param val_color_B: list of length 5 setting the value and corresponding RGBA color for the superior bound ot he colormap.
    :param res: number of intervals in the returned colormap
    :return: the resulting colormap in the form of a value-RGBAcolor matrix of size res*5 (formatted as list of list)
    '''
    acolor_A = np.array(val_color_A[1:])
    acolor_B = np.array(val_color_B[1:])
    val_A = val_color_A[0]
    val_B = val_color_B[0]
    vals = [-np.Inf]
    for t in range(res-1):
        vals.append(val_A + (val_B - val_A) * t / (res - 2))

    colors = []
    for t in range(res):
        colors.append(np.round(acolor_A + (acolor_B - acolor_A) * t / (res - 1)))
    val_colors = []
    for c,v in zip(colors,vals):
        val_colors.append([v]+c.tolist())
    return val_colors
    ###########################
    #  deprecated code that was used for defining colormaps to be used with Anatomist
    # colors = np.zeros(res*4, np.int32)
    # i=0
    # for t in range(res):
    #     j=i+4
    #     colors[i:j] = np.round(acolor_A + (acolor_B - acolor_A)*t/(res-1))
    #     i=j
    # return colors.tolist()


def invert_dict_label_name(default_label_name, lower = False):
    '''
    invert the dictionnary giving the correspondance between structures label and name
    :param default_label_name: dict of structures label:name correspondance
    :param lower: optionaly set the name in the output in lowercase
    :return: dictionnary of correspondance name:label instead of label:name
    '''
    if lower:
        inv_label_name = {v.replace('_','-').lower(): k for k, v in default_label_name.iteritems()}
    else:
        inv_label_name = {v: k for k, v in default_label_name.iteritems()}
    return inv_label_name


def readLookupTable(fname_in, separator=';'):
    f = open(fname_in, 'rU')
    l = f.readlines()
    f.close()
    d = {}
    for li in l[1:]:
        spl = li.rstrip().split(separator)
        d[int(spl[0])] = spl[1]

    return d

def readTable(fname_in,separator=','):
    '''
    simple table reader for csv files
    :param fname_in: filename of the csv table to read
    :param separator: can be changed to any separator character
    :return: col_names is a list of columns label (first row), row_names is a list of row label (first column),
    data is a numpy array of size nb_rows * nb_columns
    non-numeric entries are converted into numpy Nan
    '''
    data = []
    f = open(fname_in, 'rU')
    l = f.readlines()
    print(l)
    col_names=l[0].rstrip().split(separator)[1:]
    row_names = []
    for li in l[1:]:
        spl = li.rstrip().split(separator)
        row_names.append(spl[0])
        row=[]
        for n in spl[1:]:
            try:
                row.append(float(n.replace(',', '.')))
            except:
                row.append(np.NaN)

        data.append(row)

    f.close()
    data = np.array(data)
    print('shape of loaded data is '+str(data.shape))
    return (col_names, row_names, data)


def make_figure(table_data, col_names, output_im, default_label_name, clmap, remove_cortex=True, black_background=True, show_fig=False):
    '''
    make the figure and save it on the disk
    :param table_data:
    :param col_names:
    :param output_im:
    :param default_label_name:
    :param clmap:
    :param remove_cortex:
    :param dir_snapshots:
    :return:
    '''


    ############### color of parcels not found in the table AND BACKGROUND #####
    not_found_color = [0, 0, 0, 0]
    ############################################################################

    print(output_im)

    parcels_volume = nb.load(os.path.join(ATLAS_FOLDER, 'wmparc.nii'))
    a_parcels = np.array(parcels_volume.dataobj)

    if remove_cortex:
        inds_cortex_1 = a_parcels >= 1000
        inds_cortex_2 = a_parcels < 3000
        a_parcels[np.logical_and(inds_cortex_1, inds_cortex_2)] = 0

    JHU_parcels_volume = nb.load(os.path.join(ATLAS_FOLDER, 'mask_JHU.nii.gz'))
    a_JHU_parcels = np.array(JHU_parcels_volume.dataobj)
    inds = a_JHU_parcels > 0
    a_parcels[inds] = a_JHU_parcels[inds]
    back_inds = a_parcels == 0
    out_vol_array = np.zeros_like(a_parcels, np.int32)
    colors = []
    roi_ind = 0
    labels = np.unique(a_parcels)
    cols_done = list()
    for lab in labels:
        color = not_found_color
        print(lab)

        if lab in default_label_name.keys():
            print('---------' + default_label_name[lab])
            if default_label_name[lab] in col_names:
                col_ind = col_names.index(default_label_name[lab])
                lab_data = table_data[col_ind]
                cols_done.append(col_ind)
                print('---------data value ' + str(lab_data))
                for c in clmap:
                    if lab_data > c[0]:#< c[0]:
                        color = c[1:]
                        #color.extend([255])
        else:
            print('--------- not in dict')

        print('---------color ' + str(color))
        colors.extend(color)
        out_vol_array[a_parcels == lab] = roi_ind
        roi_ind += 1
    print('######################################## check table-dict corresp ################')
    for i,c in enumerate(col_names):
        if i not in cols_done:
            print('### table column '+c+' was not in dict')
    print('######################################## done ####################################')
    colors = np.reshape(colors,(int(len(colors)/4), 4))
    colors = colors/255.0
    #print(np.max(colors))
    #print(colors.shape)
    #print(colors)
    T1vol = nb.load(os.path.join(ATLAS_FOLDER, 'Brain.final.surf.nii.gz'))
    a_T1vol = T1vol.dataobj
    #a_T1vol = np.nan_to_num(T1vol.dataobj)
    #a_T1vol[np.isnan(a_T1vol)]=0


    zoom_min = 30
    zoom_max = 230
    sag_slices = [118, 125, 134]
    ax_slices = [113, 137, 160]
    cor_slices = [176, 136, 121]#[80, 120, 135]
    sag_T1_slice = a_T1vol[sag_slices[0], zoom_min:zoom_max, zoom_min:zoom_max].squeeze()
    sag_templ_slice = a_parcels[sag_slices[0], zoom_min:zoom_max, zoom_min:zoom_max].squeeze()
    for s in sag_slices[1:]:
        t_T1_slice = a_T1vol[s, zoom_min:zoom_max, zoom_min:zoom_max].squeeze()
        sag_T1_slice = np.hstack((sag_T1_slice,t_T1_slice))
        t_templ_slice = a_parcels[s, zoom_min:zoom_max, zoom_min:zoom_max].squeeze()
        sag_templ_slice = np.hstack((sag_templ_slice,t_templ_slice))
    ax_T1_slice = np.flipud(a_T1vol[zoom_min:zoom_max, ax_slices[0], zoom_min:zoom_max].squeeze().T)
    ax_templ_slice = np.flipud(a_parcels[zoom_min:zoom_max,ax_slices[0], zoom_min:zoom_max].squeeze().T)
    for s in ax_slices[1:]:
        t_T1_slice = np.flipud(a_T1vol[zoom_min:zoom_max, s, zoom_min:zoom_max].squeeze().T)
        ax_T1_slice = np.hstack((ax_T1_slice,t_T1_slice))
        t_templ_slice = np.flipud(a_parcels[zoom_min:zoom_max, s, zoom_min:zoom_max].squeeze().T)
        ax_templ_slice = np.hstack((ax_templ_slice,t_templ_slice))
    cor_T1_slice = a_T1vol[zoom_min:zoom_max, zoom_min:zoom_max, cor_slices[0]].squeeze().T
    cor_templ_slice = a_parcels[zoom_min:zoom_max, zoom_min:zoom_max, cor_slices[0]].squeeze().T
    for s in cor_slices[1:]:
        t_T1_slice = a_T1vol[zoom_min:zoom_max, zoom_min:zoom_max, s].squeeze().T
        cor_T1_slice = np.hstack((cor_T1_slice,t_T1_slice))
        t_templ_slice = a_parcels[zoom_min:zoom_max, zoom_min:zoom_max, s].squeeze().T
        cor_templ_slice = np.hstack((cor_templ_slice,t_templ_slice))

    T1_slice = np.vstack((sag_T1_slice, ax_T1_slice))
    T1_slice = np.vstack((T1_slice, cor_T1_slice))
    templ_slice = np.vstack((sag_templ_slice, ax_templ_slice))
    templ_slice = np.vstack((templ_slice, cor_templ_slice))
    #print(T1_slice.shape)

    #print(templ_slice.shape)
    RGBA_templ_slice = np.zeros((templ_slice.shape[0],templ_slice.shape[1],4 ))
    for ind,lab in enumerate(labels):
        RGBA_templ_slice[templ_slice == lab,:] = colors[ind, :]
    #RGBA_templ_slice = np.stack((R_templ_slice,G_templ_slice,B_templ_slice,A_templ_slice), axis=2)
    #print(RGBA_templ_slice.shape)


    cols = np.array(clmap)[:,1:4]/255.0
    #print(cols)
    cm = LinearSegmentedColormap.from_list('my cmap', cols, N=cols.shape[0])

    if black_background:
        fig, ax = plt.subplots(facecolor='black')
    else:
        fig, ax = plt.subplots()
    ax.imshow(T1_slice,cmap = plt.cm.gray)
    cax = ax.imshow(RGBA_templ_slice, cmap =cm)#, extent=(xmin, xmax, ymin, ymax))
    ax.set_axis_off()
    tks=np.array(clmap)[1:,0]
    tks_lb = [str(v) for v in tks]
    #print(tks_lb)
    cbar = fig.colorbar(cax, ticks=np.arange(1.0/(len(tks_lb)+1),1, 1.0/(len(tks_lb)+1)))
    #cbar.ax.invert_yaxis()
    if black_background:
        cbar.ax.set_yticklabels(tks_lb, color='white')  # vertically oriented colorbar
        cbar.ax.yaxis.set_tick_params(color='white')
        cbar.outline.set_color('white')
        plt.rcParams['savefig.facecolor'] = 'black'
    else:
        cbar.ax.set_yticklabels(tks_lb)
    plt.savefig(output_im, bbox_inches='tight')
    if show_fig:
        plt.show()

    # print(np.unique(templ_slice))
    # T1_slice[np.isnan(T1_slice)]=0
    # templ_slice[templ_slice==0.]=np.nan
    # fig, ax = plt.subplots()
    # ax.imshow(T1_slice,cmap = plt.cm.gray)
    # ax.imshow(templ_slice)
















    # alpha = .5
    # fig, ax = plt.subplots(1, 3)
    # ax[0].imshow(a_T1vol[center[0], :, :].squeeze(), cmap=plt.cm.gray)#, interpolation='nearest', extent=extent)
    # ax[0].imshow(a_parcels[center[0], :, :].squeeze(), alpha=alpha, interpolation='nearest')
    # ax[0].set_axis_off()
    # ax[1].imshow(a_T1vol[:, center[1], :].squeeze(), cmap=plt.cm.gray)#, interpolation='nearest', extent=extent)
    # ax[1].imshow(a_parcels[:, center[1], :].squeeze(), alpha=alpha, interpolation='nearest')
    # ax[1].set_axis_off()
    # ax[2].imshow(a_T1vol[:, :, center[2]].squeeze().T, cmap=plt.cm.gray)#, interpolation='nearest', extent=extent)
    # ax[2].imshow(a_parcels[:, :, center[2]].squeeze().T, alpha=alpha, interpolation='nearest')
    # ax[2].set_axis_off()

    # from matplotlib.colors import Normalize
    # T1_slice = a_T1vol[center[0], :, :].squeeze()
    # templ_slice = a_parcels[center[0], :, :].squeeze()
    #
    # alphas = np.ones(T1_slice.shape)
    # alphas[:, 30:] = 0
    # # Normalize the colors b/w 0 and 1, we'll then pass an MxNx4 array to imshow
    # colors = Normalize(np.min(T1_slice), np.max(T1_slice), clip=True)(T1_slice)
    # cmap = plt.cm.RdYlBu
    # colors = cmap(colors)
    # # Now set the alpha channel to the one we created above
    # colors[..., -1] = alphas
    #
    # # Create the figure and image
    # # Note that the absolute values may be slightly different
    # fig, ax = plt.subplots()
    # ax.imshow(templ_slice)
    # ax.imshow(colors)#, extent=(xmin, xmax, ymin, ymax))
    # ax.set_axis_off()
    # plt.show()

        # for slice in [113, 137, 160]:
        #
        # for slice in [118, 125, 134]:
        #
        # for slice in [80, 120, 135]:
