# instagram-scraper
DO NOT RUN WITHOUT USER AND PASSWORD!
For token issue see: https://github.com/arc298/instagram-scraper/issues/231
instagram-scraper wblut -u _mon_fre_ -p Rolling2020 -t image

# Projection

1. Crop the image
2. Project the image
3. Generate

python projector.py --outdir=projections/latent --target=projections/images/francesco.jpeg \
    --network=/home/valerio/francescom/stylegan2-ada-pytorch/training-runs/00011-modigliani-mirror-auto1-gamma50-resumeffhq512/network-snapshot-000192.pkl

# Dataset preparation
python dataset_tool.py --source datasets/raw/modigliani-highres-256 --dest tmp/modigliani-highres --transform=center-crop --width=256 --height=256

# Training: 
- Should try a couple of gamma...
- Con --resume=ffhq does not work damn
- --metrics=None, it takes about an hour each snap, damn!
- Custom cgf ==> does not work, leave auto at the moment
- Over 50k augmentation hurts training
- kimg: juststop when happy, it is normal to be slow (NVIDIA lies). Reasonable around 2000k
- Gamma: may be better around 50/100 if dataset is noisy/complex. Tweak and try
- --augpipe=bg see tables in the (paper)[https://arxiv.org/pdf/2006.06676.pdf]
- --gpus=1 because 2 doesn't fucking work...
- --resume=ffhq ==> use it for any data distribution, even if they are not faces, it is still beneficial! Important

python train.py --outdir=training-runs --data=tmp/modigliani \
--gpus=1 --mirror=1 --snap=4 --gamma=25 --metrics=None \
--resume=/home/valerio/francescom/stylegan2-ada-pytorch/training-runs/00035-modigliani-mirror-auto1-gamma25-resumecustom/network-snapshot-000448.pkl \

# Generate
python generate.py --outdir=out/modigliani --trunc=0.3 --seeds=0,1,2\
    --network=/home/valerio/francescom/stylegan2-ada-pytorch/training-runs/00015-modigliani-mirror-auto1-gamma25-bg-resumecustom/network-snapshot-000112.pkl --device=cpu
