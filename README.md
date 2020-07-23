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
    --samplelist sample.list
    --genotypecalls output.genotypecalls
```
The above pipeline will generate a file that contains the genotype calls for each sample 
in the input sample list. The genotype calls could then be used to calculate distances
among the samples in the sample list pairwise.
```shell script
python3 mykrobe-atlas-distance-data/nextflow/bin/calculate_distance.py \
    --genotype-calls input.genotypecalls \
    --out-distances output.distance.matrix
```