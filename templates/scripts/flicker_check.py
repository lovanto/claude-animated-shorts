import sys,glob,re,numpy as np
from PIL import Image
for d in sys.argv[1:]:
    fs=sorted(glob.glob(d+"/*.jp*g"),key=lambda f:int(re.findall(r"(\d+)\.jp",f)[0]))
    nums=[int(re.findall(r"(\d+)\.jp",f)[0]) for f in fs]
    im=[np.asarray(Image.open(f).convert("L").resize((270,480)),dtype=np.float32) for f in fs]
    ds=[np.abs(im[i]-im[i-1]).mean() for i in range(1,len(im))]
    sk=[np.abs(im[i-1]-im[i+1]).mean() for i in range(1,len(im)-1)]
    bad=[]
    for i in range(1,len(im)-1):
        a,b,s=ds[i-1],ds[i],sk[i-1]
        if min(a,b)>1.25*s+0.5: bad.append((nums[i],round(float(a),1),round(float(b),1),round(float(s),1)))
    print(d,len(fs),"consecutive",nums[0],"..",nums[-1],"median diff",round(float(np.median(ds)),1),"dropout candidates (frame,d_prev,d_next,d_skip):",bad)
