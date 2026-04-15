"""
Karedeki 361 galaksinin SDSS optik spektrumlarını indirir.
Bu script'i kendi bilgisayarında çalıştır (sandbox'ta SDSS bloke):

    pip install requests astropy pandas
    python download_spectra.py

İndirme sonrası `spectra_csv/` klasöründe her galaksi için
`<catalog_id>_<plate>-<mjd>-<fiber>.csv` dosyaları olur:
wavelength_angstrom, flux_1e-17_erg_s_cm2_A, ivar, and_mask, model_flux
"""
import os, csv, time, requests, pandas as pd
from astropy.io import fits

CATALOG = "galaxy_catalog.csv"
OUTDIR  = "spectra_csv"
os.makedirs(OUTDIR, exist_ok=True)

# SDSS DR17 spSpec file URL pattern for DR8+ (eBOSS/BOSS legacy)
# lite files are ~100 KB each
URL_TPL = "https://dr17.sdss.org/sas/dr17/sdss/spectro/redux/26/spectra/lite/{plate:04d}/spec-{plate:04d}-{mjd}-{fiber:04d}.fits"

df = pd.read_csv(CATALOG)
print(f"{len(df)} galaksi indirilecek…")

for _, r in df.iterrows():
    cid = int(r.catalog_id); p=int(r.plate); mj=int(r.mjd); fi=int(r.fiberID)
    url = URL_TPL.format(plate=p, mjd=mj, fiber=fi)
    out = f"{OUTDIR}/{cid:04d}_{p}-{mj}-{fi}.csv"
    if os.path.exists(out): continue
    try:
        resp = requests.get(url, timeout=60)
        if resp.status_code != 200:
            print(f"  {cid}: HTTP {resp.status_code}  {url}"); continue
        # Write fits locally, parse, convert to CSV
        tmp = "/tmp/_sdss.fits"
        with open(tmp,"wb") as f: f.write(resp.content)
        with fits.open(tmp) as h:
            t = h[1].data
            loglam = t['loglam']
            flux   = t['flux']       # 1e-17 erg/s/cm^2/Å
            ivar   = t['ivar']
            andmsk = t['and_mask']
            model  = t['model']
        with open(out,"w",newline="") as f:
            w=csv.writer(f)
            w.writerow(["wavelength_angstrom","flux_1e-17","ivar","and_mask","model_flux"])
            for L,F,I,A,M in zip(loglam,flux,ivar,andmsk,model):
                w.writerow([f"{10**L:.4f}", f"{F:.5f}", f"{I:.5f}", int(A), f"{M:.5f}"])
        print(f"  ✓ {cid:4d}  {p}-{mj}-{fi}")
        time.sleep(0.2)   # be gentle to the server
    except Exception as e:
        print(f"  ! {cid}: {e}")

print("Bitti. Spektrumlar:", OUTDIR)
