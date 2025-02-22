import os
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt


def plot_tfr_rdm(conf):
    
    """
    Plot TFR representation dissimilarity matrices 

    Function to plot RDMs. 

    :param conf: conf

    :return: time frequency representation of the RDMs.
    :rtype: float
    
    @author: Some Folk, day.month.year  
    """ 

    block   = conf['block']
    rsa     = conf['rsa']
    lump    = conf['lump']
    subset  = conf['subset']
    newData  = conf['newData']

    conds   = ['grat', 'nat']

    # results_path = '/Users/.../data/'
    plt.rcParams['figure.dpi'] = 300

    if block == 'grat':
        cond = 0
    else:
        cond = 1        


    prctl = 99
    kernel = "epa"    # "gau", "biw", "cos", "epa", "triw"
    bw = "silverman"  # "scott", "normal_reference", "silverman"
    adj = 2


    ss = 0
    #rsa = False
    trange = [-500,1500]
    n_tpoints_whole = 2800
    t0 = 400
    tf = 1000
    n_site = 4
    if rsa == True:
        n_tbin = 560
    else:
        n_tbin = n_tpoints_whole
    time = np.linspace(-800,2000, n_tbin)
    pt_t0 = np.searchsorted(time,t0,side='left', sorter=None)
    pt_tf = np.searchsorted(time,tf,side='left', sorter=None) 
    ## Compute RSA
    rho_tps = np.zeros((5,n_site, n_tbin)) 


    # Size of RDM vector to be correlated  
    if subset == True:
        #trgt = [ 0,  2,  3,  4,  7,  9, 16, 17]
        #trgt =  [0,     3,     4,     5,    9,    10,   11, 16]
        #trgt =  [0,     1,     2,     8,    12,    14,    15,    17]
        #trgt =  [ 0,  1,  2,  4,  5,  8, 10, 11]    
        trgt = [ 0,  1,  5,  6,  8,  9, 11]
        trgt = [ 0,  1,  5,  6, 7, 8,  9, 11, 14] # [ 0  1  5  6  7  8  9 11 14]
    else:
        trgt = np.arange(18)
                        

    if block == 'objects':
        trialIdx_ = np.arange(0,36)
        trialIdx = trialIdx_[1::2]  # Objects
        trialIdx = trialIdx[trgt]
    if block == 'scenes':
        trialIdx_ = np.arange(0,36)
        trialIdx = trialIdx_[::2]  # Scenes
        trialIdx = trialIdx[trgt]
    if block == 'both':
        trialIdx = np.arange(0,36)
        trialIdx = trialIdx_
    if block == 'grat':
        trialIdx_ = np.arange(0,30)
        trialIdx = trialIdx_
        

    M = np.zeros((trialIdx.shape[0],trialIdx.shape[0]))
    idx = np.tril_indices(M.shape[0], -1)
    print(trialIdx.shape[0])
    rdm_ts = np.zeros((2,n_site,trialIdx_.shape[0],trialIdx_.shape[0], n_tbin)) 
        
    # Mutliunit activity
    paths = conf['paths']
    mua_path = paths[0]
    for i_site in range(n_site):   
        # MUA
        if rsa == True:
            fname = '/unsDec_layer' + str(i_site+1) + '_mua_resampled_split1.npy'
            X1 = np.load(os.path.join(mua_path + conds[cond] + fname))
            fname = '/unsDec_layer' + str(i_site+1) + '_mua_resampled_split2.npy'
            X2 = np.load(os.path.join(mua_path + conds[cond] + fname))
            for i_tbin in range(n_tbin):
                x1 = X1[:,:,i_tbin]
                x2 = X2[:,:,i_tbin]
                x1 = x1[np.ix_(trialIdx,trialIdx)]
                x2 = x2[np.ix_(trialIdx,trialIdx)]
                rho_tps[4,i_site,i_tbin] = scipy.stats.spearmanr(x1[idx],x2[idx])[0] 
                #rho_tps[3,i_site,i_tbin] = scipy.stats.spearmanr(x1.flatten(),x2.flatten())[0] 
        else:
            n_tbin = 2800
            fname = '/unsDec_layer' + str(i_site+1) + '_mua_resampled.npy'
            X = np.load(os.path.join(mua_path + conds[cond] + fname))
            rdm_ts[0,i_site,:,:,:] = X
            for i_tbin in range(n_tbin):
                x = X[:,:,i_tbin]
                x = x[np.ix_(trialIdx,trialIdx)]
                rho_tps[4,i_site,i_tbin] = np.mean(x[idx])
        # LFP
        if rsa == True:
            fname = '/unsDec_layer' + str(i_site+1) + '_lfp_bipolar_split1.npy'
            X1 = np.load(os.path.join(mua_path + conds[cond] + fname))
            fname = '/unsDec_layer' + str(i_site+1) + '_lfp_bipolar_split2.npy'
            X2 = np.load(os.path.join(mua_path + conds[cond] + fname))
            for i_tbin in range(n_tbin):
                x1 = X1[:,:,i_tbin]
                x2 = X2[:,:,i_tbin]
                x1 = x1[np.ix_(trialIdx,trialIdx)]
                x2 = x2[np.ix_(trialIdx,trialIdx)]
                rho_tps[3,i_site,i_tbin] = scipy.stats.spearmanr(x1[idx],x2[idx])[0] 
                #rho_tps[3,i_site,i_tbin] = scipy.stats.spearmanr(x1.flatten(),x2.flatten())[0] 
        else:
            n_tbin = 560
            fname = '/unsDec_layer' + str(i_site+1) + '_lfp_bipolar.npy'
            X = np.load(os.path.join(mua_path + conds[cond] + fname))
            #rdm_ts[1,i_site,:,:,:] = X
            for i_tbin in range(n_tbin):
                x = X[:,:,i_tbin]
                x = x[np.ix_(trialIdx,trialIdx)]
                rho_tps[3,i_site,i_tbin] = np.mean(x[idx])
                
    # Frequencies


    n_fband = 3
    for fband in range(n_fband):
        # General configuration

        conf = {
            'paths'    : [
            '/Volumes/.../data/results_bckp/',
            '/Volumes/.../data/',
            '/Volumes/.../results/'
            ],
            'methods'  : ['spectral','mvpa'],
            'decvars'  : ['spw','gpr','spwgpr'],
            'method'   : 1,
            'dvar'     : 0,
            'fband'    : fband,
            'cond'     : cond,
            'sess'     : ss,
            'layers'   : False,
            'lump'     : lump,
            'rsa'      : rsa
            }

        rdms  = load_tfr_rdm(conf)

        rdm1 = rdms['rdm_split1']
        rdm2 = rdms['rdm_split2']
        rdm  = rdms['rdm_whole']
        #print(rdm1.shape)
        #print(rdm2.shape)

        if fband ==0:
            fx1 = 1
            fx2 = 20
            f0 = 6
            ff = 12
            # Time average
            t0 = 150
            tf = 400

        elif fband ==1:
            fx1 = 20 
            fx2 = 80
            f0 = 30
            ff = 60
            # Time average
            t0 = 400
            tf = 1200

        elif fband ==2:
            fx1 = 80 
            fx2 = 200
            f0 = 80
            ff = 128  
            # Time average
            t0 = 150
            tf = 400

        # Index frequency
        fps = [19,16,11] # frequency bins for each fband
        n_fbin = fps[fband]
        freq = np.linspace(fx1,fx2, fps[fband])
        pt_f0 = np.searchsorted(freq,f0,side='left', sorter=None)
        pt_fd = np.searchsorted(freq,ff,side='left', sorter=None) 

        # Index time
        tps = [57,113,141] # time bins for each fband
        n_tbin = tps[fband]
        time = np.linspace(-800,2000, tps[fband])
        pt_t0 = np.searchsorted(time,t0,side='left', sorter=None)
        pt_tf = np.searchsorted(time,tf,side='left', sorter=None) 

        # Indices to layer compartments    
        lu = [0,3,6,9]
        ld = [3,6,9,12]

        for i_tbin in range(n_tbin):
            for i_site in range(n_site):    
                x1 = np.mean(np.squeeze(np.mean(rdm1[lu[i_site]:ld[i_site],pt_f0:pt_fd,:,:,i_tbin],axis=0)),axis=0)
                x2 = np.mean(np.squeeze(np.mean(rdm2[lu[i_site]:ld[i_site],pt_f0:pt_fd,:,:,i_tbin],axis=0)),axis=0)
                x = np.mean(np.squeeze(np.mean(rdm[lu[i_site]:ld[i_site],pt_f0:pt_fd,:,:,i_tbin],axis=0)),axis=0)
                #print(x1.shape)
                x1 = x1[np.ix_(trialIdx,trialIdx)]
                x2 = x2[np.ix_(trialIdx,trialIdx)]
                x = x[np.ix_(trialIdx,trialIdx)]   
                if rsa == True:
                    rho_tps[fband,i_site,i_tbin] = scipy.stats.spearmanr(x1[idx],x2[idx])[0] 
                else:    
                    rho_tps[fband,i_site,i_tbin] = np.mean(x[idx])

    # Figure
    n_ts = 5
    fig, ax = plt.subplots(nrows=n_ts, ncols=1,figsize=(4, 6))
    n = 12
    colors = plt.cm.Paired_r(np.linspace(0,1,n))
    colors = plt.cm.viridis_r(np.linspace(0,1,n))
    #tps = [57,113,102] # time bins for each fband
    tps = [57,113,141,140] 


    for i_ts in range(n_ts):
        n = n_ts - i_ts - 1
        
        # Signals
        xx = 0.02
        yy = 0.7
        ax[0].text(xx,yy,'MUA',
                horizontalalignment='left',
                transform=ax[0].transAxes,fontsize=8)
        ax[1].text(xx,yy,'bp-LFP',
                horizontalalignment='left',
                transform=ax[1].transAxes,fontsize=8)
        ax[2].text(xx,yy,'80-128 Hz',
                horizontalalignment='left',
                transform=ax[2].transAxes,fontsize=8)
        ax[3].text(xx,yy,'30-60 Hz',
                horizontalalignment='left',
                transform=ax[3].transAxes,fontsize=8)
        ax[4].text(xx,yy,'6-12 Hz',
                horizontalalignment='left',
                transform=ax[4].transAxes,fontsize=8)
        
        if i_ts == 4:  
            if rsa == True:
                y0 = -0.5
                n_tbin = 560
                ax[n].set_ylim(y0,1)
            else:
                y0 = 0.2
                n_tbin = n_tpoints_whole
                ax[n].set_ylim(y0,1)
                ax[1].set_ylabel('                  '
                                + 'Classification accucracy', fontsize=10)
            time = np.linspace(-800,2000, n_tbin)
            y = np.squeeze(rho_tps[i_ts,:,:n_tbin])      
            ax[n].set_xlim(trange[0],trange[1])
            # baseline index
            t0 = -800
            tf = 0
        elif i_ts == 3:
            if rsa == True:
                y0 = -0.5
                n_tbin = 560 # n_tpoints_whole
                ax[n].set_ylim(y0,1)
            else:
                y0 = 0.2
                n_tbin = 560
                ax[n].set_ylim(y0,1)
                ax[1].set_ylabel('                  '
                                + 'Classification accucracy', fontsize=10)
            time = np.linspace(-800,2000, n_tbin)
            y = np.squeeze(rho_tps[i_ts,:,:n_tbin])      
            ax[n].set_xlim(trange[0],trange[1])
            # baseline index
            t0 = -800
            tf = 0
        elif i_ts == 0:
            if rsa == True:
                y0 = -0.5
            else:
                y0 = 0.2
            time = np.linspace(-800,2000, tps[i_ts])
            y = np.squeeze(rho_tps[i_ts,:,:tps[i_ts]]) 
            ax[n].set_ylim(y0,1)
            ax[n].set_xlim(trange[0],trange[1])
            # baseline index
            t0 = -600
            tf = -100
        else: 
            if rsa == True:
                y0 = -0.5
            else:
                y0 = 0.2
            time = np.linspace(-800,2000, tps[i_ts])
            y = np.squeeze(rho_tps[i_ts,:,:tps[i_ts]]) 
            ax[n].set_ylim(y0,1)
            ax[n].set_xlim(trange[0],trange[1])
            # baseline index
            t0 = -700
            tf = -50
            
        # above baseline significance
        pt_t0 = np.searchsorted(time,t0,side='left', sorter=None)
        pt_tf = np.searchsorted(time,tf,side='left', sorter=None) 
        # Time series
        for i_site in range(n_site):   
            y_bs = np.squeeze(rho_tps[i_ts,i_site,pt_t0:pt_tf])
            dens = sm.nonparametric.KDEUnivariate(y_bs)
            dens.fit(fft=False,kernel=kernel,bw=bw,adjust=adj) 
            peak = np.ones((time.shape[0]))
            peak = np.ma.masked_where(y[i_site, :]\
                                    < np.percentile(dens.support,prctl), peak)
            clust = np.asarray(np.where(peak==1))
            #if clust.size > sz: 
            #    latencies[i,1] = time[np.where(peak==1)[0][0]]
        
            c = n_site - i_site - 1
            ax[n].plot(time,y[i_site, :],color=colors[2 + c*3],
                    linewidth=1.2,alpha=0.7,label='_nolegend_')
            if i_ts == 4 or i_ts == 3:
                if rsa == True:
                    ax[n].plot(time,peak + (y0 - i_site*0.075 - 0.69), color=colors[2 + c*3], 
                        linewidth=2)
                else:
                    ax[n].plot(time,peak + (y0 - i_site*0.045 - 0.825), color=colors[2 + c*3], 
                        linewidth=2)
            else:
                if rsa == True:
                    ax[n].plot(time,peak + (y0 - i_site*0.075 - 0.69), color=colors[2 + c*3], 
                        linewidth=2)
                else:
                    ax[n].plot(time,peak + (y0 - i_site*0.045 - 0.825), color=colors[2 + c*3], 
                        linewidth=2)
        
        # Legend   
        ax[4].set_xlabel('Time (ms)', fontsize=12)
        if rsa == True:
            ax[3].set_ylabel('Spearman\'s  rho', fontsize=10)
        ax[1].legend(['L2/3',
                    'L4',
                    'L5',
                    'L6'],
                fontsize=4, frameon=False,bbox_to_anchor=(0.99999, 0.93),
                title="Layer:", loc=2, prop={'size':10})     
        
    
        if n !=4 :
            ax[n].set_xticklabels([])
            
    plt.show()

    return 
