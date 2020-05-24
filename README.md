# mykrobe-atlas-distance-data
Pipelines and scripts for calculating genetic distance between samples

## Running the pipelines
An example of running the bigsi query pipeline:
```shell script
nextflow run -c mykrobe-atlas-distance-data/nextflow/nextflow.config 
    mykrobe-atlas-distance-data/nextflow/bigsi_query_probes.nf 
    --probes mykrobe-atlas-distance-data/probes/probes.fa 
    --bigsiimage singularity/bigsi-latest.simg 
    --bigsiconfig bigsi/bigsi_config.yaml
```