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
    --genotype-calls1 input.genotypecalls1 \
    --genotype-calls2 input.genotypecalls2 \
    --out-distances output.distance.matrix
```
The above script can be used to generate matrix for the distances between sample and sample
and the distances between sample and tree leave. Once we have the distance matrix we can
generate the json that is ready for inserting into the Distance API.
For example, the following command produce the data for inserting sample's nearest leaf:
```shell script
python3 mykrobe-atlas-distance-data/nextflow/bin/generate_nearest_leaf.py \
    --distance-matrix input.distance.matrix.samples.tree \
    > output.samples.tree.jsondata
```
And for producing the data for inserting sample's nearest neighbours:
```shell script
python3 mykrobe-atlas-distance-data/nextflow/bin/generate_nearest_neighbours.py \
    --distance-matrix input.distance.matrix.samples.samples \
    --distance-threshold 20
    > output.samples.samples.jsondata.threshold.20
```