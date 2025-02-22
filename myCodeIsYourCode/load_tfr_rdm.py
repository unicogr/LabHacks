import os
import numpy as np

def load_tfr_rdm(conf):

    """
    Load TFR representation dissimilarity materices 

    Function to load RDMs. 

    
    :param float stat: un-corrected p-values for each frequency (and/or time) bin.
    :param float alpha: statistical threshold (e.g. 0.05).

    :return: list with RDMs.
    :rtype: float
    
    @author: Some Folk, day.month.year  
    """ 
    paths = conf['paths']
    cond  = conf['cond']
    decvars  = conf['decvars']
    dvar  = conf['dvar']
    method = conf['method']
    sess   = conf['sess']
    fband = conf['fband']
    layers = conf['layers']
    lump = conf['lump']
    rsa  = conf['rsa']
    input_path = paths[1]
        
    print('session: ', sess)

    
    if sess != 0:
        prefix = str('_sess_' + str(sess)+ '_') 
    else:    
        prefix = str('')
       
        
    #tps = [57,113,102]
    #fps = [19,16,25]
    tps = [57,113,141,140] 
    fps = [19,16,11,1]
    
   
    
    methods = ['hanning', 'wavelet', 'wavelet']


    blocks  = ['grat', 'nat','nat','nat','nat','nat']   
    decvars = ["spw", "gpr",'spwgpr']
    results_path = input_path + blocks[cond] + '/'
    
    if layers == True:
        depths = 4
        sufix  = 'layer' 
    else:
        depths = 12
        sufix  = 'ch' 
                 
    if cond  == 0:
        n_cond = 30      
        
    elif cond == 1:
        n_cond = 36

    elif cond  == 2:
        n_cond = 36     
        
    elif cond == 3:
        n_cond = 36
              
    rdm_split1  = np.zeros((depths,fps[fband], n_cond, n_cond,tps[fband]))
    rdm_split2  = np.zeros((depths,fps[fband], n_cond, n_cond,tps[fband]))
    rdm_whole   = np.zeros((depths,fps[fband], n_cond, n_cond,tps[fband]))
    
    for fr in range(fps[fband]):
        for ch in range(depths):

            fbands  = ['low','high','higher','mua']
            if rsa == True:
                # Load 
                X_t = np.load(os.path.join(results_path + decvars[dvar] 
                                            + '_Dec_ch' + str(ch+1) 
                                            + '_freq' + str(fr+1) 
                                            + '_' + fbands[fband] 
                                            + '_' + methods[fband] + '_split1_norm_c.npy'))
                
                # Load 
                Y_t = np.load(os.path.join(results_path + decvars[dvar] 
                                            + '_Dec_ch' + str(ch+1) 
                                            + '_freq' + str(fr+1) 
                                            + '_' + fbands[fband] 
                                            + '_' + methods[fband] + '_split2_norm_c.npy'))
                
                rdm_split1[ch,fr,:,:,:] = np.squeeze(X_t[:,:,:]) 
                rdm_split2[ch,fr,:,:,:] = np.squeeze(Y_t[:,:,:]) 
                
            if lump == True:
                Z_t = np.load(os.path.join(results_path + decvars[dvar] 
                                        + '_Dec_ch' + str(ch+1) 
                                        + '_freq' + str(fr+1) 
                                        + '_' + fbands[fband] 
                                        + '_' + methods[fband] + '_norm_c.npy'))
                
                rdm_whole[ch,fr,:,:,:] = np.squeeze(Z_t[:,:,:]) 
           
                
                
    if rsa == True:    
        rdms = {
            'rdm_split1'  : rdm_split1,
            'rdm_split2'  : rdm_split2,
            'rdm_whole' : rdm_whole
                }
    else:
         rdms = {
            'rdm_split1'  : rdm_split1,
            'rdm_split2'  : rdm_split2,
            'rdm_whole' : rdm_whole
                }    
    
    return rdms
