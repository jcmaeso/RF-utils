import numpy as np

def calc_eeff(h,w,er):
    return (er+1)/2 + ((er-1)/2)*(1/np.sqrt(1+12*h/w))

def _calc_A(Z0,er):
    return (Z0/60)*np.sqrt((er+1)/2)+((er-1)/(er+1))*(0.23+0.11/er)

def _calc_B(Z0,er):
    return 377*np.pi/(2*Z0*np.sqrt(er))

def _calc_k0(frequency_ghz):
    return 2*np.pi*frequency_ghz*1e9/3e8

def calc_wh(Z0,er):
    A = _calc_A(Z0,er)
    B = _calc_B(Z0,er)
    wd = 8*np.exp(A)/(np.exp(2*A)-2)
    with np.nditer(wd, op_flags=['readwrite']) as it:
        for wd_item in it:
            if wd_item > 2:
                wd_item = (2/np.pi)*(B-1-np.log(2*B-1)+((er-1)/(2*er))*(np.log(B-1)+0.39-0.61/er))
    return wd
def calc_z0(w,h,er):
    mat = np.array([])
    for w_item in np.nditer(w):
        if w_item/h < 1:
            mat = np.append(mat,(60/np.sqrt(calc_eeff(h,w_item,er)))*np.log(8*h/w_item+w_item/(4*d)))
        else:
            mat = np.append(mat, 120*np.pi/(np.sqrt(calc_eeff(h,w_item,er))*(w_item/h+1.393+0.667*np.log(w_item/h+1.444))))
    return mat



def calc_len(er,phase_shift,frequency_ghz,h,w): 
    return 1000*np.deg2rad(phase_shift)/(np.sqrt(calc_eeff(h,w,er))*_calc_k0(frequency_ghz))


def calc_phase_shift(er,l,frequency_ghz,h,w):
    return np.rad2deg(np.sqrt(calc_eeff(h,w,er))*_calc_k0(frequency_ghz)/1000*l)

def translate_len_width(freq1, er1, w1, l1, h1,freq2, er2, h2):
    phase_shift = calc_phase_shift(er1,l1,freq1,h1,w1)
    Z0 = calc_z0(w1,h1,er1)
    wh2 = calc_wh(Z0,er2)
    w2 = wh2*h2
    l2 = calc_len(er2,phase_shift,freq2,h2,w2)
    print("La nueva W es "+str(w2))
    print("La nueva L es "+str(l2))
    print("La nueva Z es "+str(Z0))
    


if __name__ == "__main__":
    #print(calc_len(9.9,270,10,0.5,0.483))
    #print(calc_phase_shift(9.9,8.72,10,0.5,0.483))
    translate_len_width(2.45,4.4,np.array([3.2,4.4]),np.array([13,14]),1.6,6.75,2.2,0.787)