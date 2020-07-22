# mykrobe-atlas-distance-data
Pipeline and scripts for calculating genetic distance between samples

## Running the pipeline
An example of running the distance calculation pipeline:
```shell script
nextflow run -c mykrobe-atlas-distance-data/nextflow/nextflow.config 
    mykrobe-atlas-distance-data/nextflow/calculate_distances.nf 
    --probes mykrobe-atlas-distance-data/probes/probes.fa 
    --bigsiimage singularity/bigsi-latest.simg 
    --bigsiconfig bigsi/bigsi_config.yaml
    --samplelist sample.list
    --distancematrix output.distancematrix
```