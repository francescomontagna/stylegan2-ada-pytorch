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
python dataset_tool.py --source datasets/raw/resized-512/modigliani --dest tmp/modigliani --transform=center-crop --width=512 --height=512

# Training: 
- Should try a couple of gamma...
- Con --resume=ffhq does not work damn
- --metrics=None, it takes about an hour each time damn!
- Custom cgf ==> does not work, leave auto at the moment
- Over 50k augmentation hurts training
- kimg: juststop when happy, it is normal to be slow (NVIDIA lies). Reasonable around 2000k
- Gamma: may be better around 50/100 if dataset is noisy/complex. Tweak and try
- --augpipe=bc see tables
- --gpus=1 because 2 doesn't fucking work...
- --resume=ffhq ==> use it for any data distribution, even if they are not faces, it is still beneficial! Important

python train.py --outdir=training-runs --data=tmp/modigliani \
--gpus=1 --mirror=1 --snap=4 --gamma=25 --metrics=None \
--resume=training-runs/00011-modigliani-mirror-auto1-gamma50-resumeffhq512/network-snapshot-000192.pkl \
--augpipe=bg --dry-run

# Generate
python generate.py --outdir=out/ffhq --trunc=1 --seeds=0\
    --network=pretrained/ffhq.pkl
