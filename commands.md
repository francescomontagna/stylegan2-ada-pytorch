# instagram-scraper
DO NOT RUN WITHOUT USER AND PASSWORD!
For token issue see: https://github.com/arc298/instagram-scraper/issues/231.  
Example command:  
`instagram-scraper <IG progile username> -u <my IG username> -p <my IG password> -t image`

install with  
`pip install instagram-scraper==1.7.0`

# Projection

1. Crop the image
2. Project the image
3. Generate

Example
`python projector.py --outdir=projections/latent --target=projections/images/francesco.jpeg \
    --network=/home/valerio/francescom/stylegan2-ada-pytorch/training-runs/00011-modigliani-mirror-auto1-gamma50-resumeffhq512/ network-snapshot-000192.pkl`

# Dataset preparation
First, run `dataset_resolution.py` script:  
`python dataset_resolution.py <resolution: {256, 512, 1024}>`

The, run `dataset_tool.py`
`python dataset_tool.py --source datasets/raw/<src data folder> --dest tmp/<dest data folder> --transform=center-crop --width=<resolution> --height=<resolution>`
python dataset_tool.py --source datasets/raw/modigliani-highres-1024 --dest tmp/modigliani-highres-1024 --transform=center-crop --width=1024 --height=1024

# Training: 
- Should try a couple of gamma, 50-100 if it is noisy dataset, else around 10. Stop training and lower when happy, just tweak
- --metrics=None, it takes about an hour each snap, damn!
- Custom cgf ==> does not work, leave auto at the moment
- Over 50k augmentation hurts training
- kimg: let it default and just stop when happy, it is normal to be slow (NVIDIA lies). Reasonable around 2000k
- Gamma: may be better around 50/100 if dataset is noisy/complex. Tweak and try
- --augpipe=bg see tables in the (https://arxiv.org/pdf/2006.06676.pdf)[paper]
- --gpus=1 because 2 doesn't fucking work...
- --resume=ffhq or path to the local .pkl ==> use it for any data distribution, even if they are not faces, it is still beneficial! Important


`python train.py --outdir=training-runs --data=tmp/modigliani \
--gpus=1 --mirror=1 --snap=4 --gamma=25 --metrics=None \
--resume=/home/valerio/francescom/stylegan2-ada-pytorch/training-runs/00035-modigliani-mirror-auto1-gamma25-resumecustom/network-snapshot-000448.pkl `

# Generate
`python generate.py --outdir=out/goat --trunc=0.8 --seeds=0,1,2 \
    --network=models/goat.pkl --device=cpu`
