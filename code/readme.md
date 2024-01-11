Due to the mismatch of downloaded data (cds, pep, gff), I now provide two scripts that can quickly process them into the format required by WGDI. Please select the appropriate program according to the example format.

```python
python deal_gff.py fusarium_oxysporum_Fol007.gff3 fusarium_oxysporum_Fol007.cds-transcripts.fa fusarium_oxysporum_Fol007.proteins.fa fox1s
```

```python
python deal_gff_ncbi.py GCF_007210705.1_Tcal_SD_v2.1_genomic.gff GCF_007210705.1_Tcal_SD_v2.1_cds_from_genomic.fna GCF_007210705.1_Tcal_SD_v2.1_protein.faa tig2s
```
