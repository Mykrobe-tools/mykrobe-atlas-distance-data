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
Or alternatively running the cobs query pipeline:
```shell script
nextflow run -c mykrobe-atlas-distance-data/nextflow/nextflow.config
    mykrobe-atlas-distance-data/nextflow/cobs_query_probes.nf
    --probes mykrobe-atlas-distance-data/probes/probes.fa
    --image singularity/kms-latest.simg
    --classic_index_dir merged/index
    --sample_list sample.list
    --output_genotype_call_path genotype_calls
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
    --distance-matrix-sample-tree input.distance.matrix.samples.tree \
    > output.samples.tree.jsondata
```
And for producing the data for inserting sample's nearest neighbours:
```shell script
python3 mykrobe-atlas-distance-data/nextflow/bin/generate_nearest_neighbours.py \
    --distance-matrix-sample-sample input.distance.matrix.samples.samples \
    --distance-matrix-sample-tree input.distance.matrix.samples.tree \
    --distance-threshold 20
    > output.samples.samples.jsondata.threshold.20
```

## Distance matrix with large number of samples

The more samples, the longer it will take to generate the distance matrix. As such, to shorten the time it takes, the genotype calls file can be split. For 1000 samples, it will take a little less than 2 hours.

```shell script
split -d --lines=1000 ./all_genotype_calls ./split_genotypecalls_X
```
Where X in the command above is a 2-digits number between 00 and n-1, n being the number of files generated.

Once the genotype calls are split, create a script with distance matrix calculation commands for each of the files in the form of :

```shell script
python3 mykrobe-atlas-distance-data/nextflow/bin/calculate_distance.py \
    --genotype-calls1 split_genotypecalls_X \
    --genotype-calls2 all_genotypecalls \
    --out-distances samples_distance_sub_matrix_X
```

A job array can be launched to parallelised the jobs :
```shell script
bsub -R "select[mem>5000] rusage[mem=5000]" -M5000 -e ./array.e -o ./array.o -J arr[1-(n)]%(n) "tail -n+\$LSB_JOBINDEX jobs.sh | head -1 | bash"
```

Once all split matrixes are created, to make them into one, a script as below should be run. There is one command for the header, and one command per sub-matrix.

```shell script
head -1 samples_distance_sub_matrix_00 > samples_distance_matrix
tail -n +2 samples_distance_sub_matrix_00 >> samples_distance_matrix
[...]
tail -n +2 samples_distance_sub_matrix_(n+1) >> samples_distance_matrix
```