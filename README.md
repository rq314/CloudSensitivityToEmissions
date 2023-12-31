# CloudSensitivityToEmissions
[![DOI](https://zenodo.org/badge/717182360.svg)](https://zenodo.org/doi/10.5281/zenodo.10276889)

Here is the combined plume-parcel model, along with processing scripts.

## Dependencies

- numpy
- pandas
- scipy
- pysolar
- tqdm
- argparse
- multiprocessing
- matplotlib
- [pyrcel](https://github.com/darothen/pyrcel)

## Preparing your environment
Create the following directories
```
mkdir data/processed
mkdir data/raw
mkdir figs
```

Add the `only_track_data_ctrc_anonymous.csv` file to `data/raw`

## Input file

The input file for the ship track data needs to be called `only_track_data_ctrc_anonymous.csv` and it has to have the following input columns:

- (`float`)`trackno`: Ship track identifier (-)
- (`float`)`sox`: SO$`_x`$ emission rate (kg s$`^{-1}`$)
- (`float`)`cbh`: Cloud base height (m)
- (`float`)`blh`: Boundary layer height (m)
- (`float`)`cth`: Cloud top height (m)
- (`float`)`spd_res`: Relative velocity between ship velocity and wind velocity (m s$`^{-1}`$)
- (`float`)`nd_cln`: Background cloud droplet number concentration (cm$`^{-3}`$)
- (`float`)`nd_pol`: Ship track cloud droplet number concentration (cm$`^{-3}`$)
- (`float`)`cf_liq`: Liquid cloud fraction (-)
- (`float`)`lwp`: Liquid water path (g m$`^{-2}`$)
- (`float`)`t1000`: Temperature at 1000 hPa (K)
- (`float`)`LTS`: Low tropospheric stability (K)
- (`float`)`ctt`: Cloud top temperature (K)
- (`float`)`ctrc`: Cloud top radiative cooling (W m$`^{-2}`$)
- (`bool`)`is_coupled`: Flag for cloud coupling according to cloud base height indicator (`cbh`<1000 m)

## Generating output files:

Navigate to the source directory:
```bash
cd src
```

### To run ARG:
```bash
python3 generate_dat_files.py --exp bri_arg --proct
```
The flag `--ncores` can also be added to analyse the database using multiple processes.

Output files : 
- `data/processed/all_ships/all_ships_dataframe_processed_bri_arg.csv`, 
- `data/processed/only_tracks/only_tracks_dataframe_processed_bri_arg.csv`,
- `data/processed/only_tracks/correlations_bri_arg.csv` .

### To run MBN:
```bash
python3 generate_dat_files.py --exp bri_mbn --proct
```
The flag `--ncores` can also be added to analyse the database using multiple processes.

Output files : 
- `data/processed/all_ships/all_ships_dataframe_processed_bri_mbn.csv`, 
- `data/processed/only_tracks/only_tracks_dataframe_processed_bri_mbn.csv`,
- `data/processed/only_tracks/correlations_bri_mbn.csv` .

### To run RW:
```bash
python3 generate_dat_files.py --exp bri_lkup --proct
```
The flag `--ncores` can also be added to analyse the database using multiple processes.

Output files : 
- `data/processed/all_ships/all_ships_dataframe_processed_bri_lkup.csv`, 
- `data/processed/only_tracks/only_tracks_dataframe_processed_bri_lkup.csv`,
- `data/processed/only_tracks/correlations_bri_lkup.csv` .

### To estimate the sensitivities:
```bash
python3 generate_sensitivities.py
```
Output files : 
- `data/sensitivity_acruise.csv`

## Generating plots:

Navigate to the source directory:
```bash
cd src
```
To generate plots:
```bash
python3 generate_plots.py
```

Output plots:
- `figs/sensitivity_study_.pdf`
- `figs/fit_up_boxplot_.pdf`
- `figs/ctrc_all_hybrid.pdf`
- `figs/all_correlations_coupled.pdf`
- `figs/sensitivity_studybreakdown_.pdf`






