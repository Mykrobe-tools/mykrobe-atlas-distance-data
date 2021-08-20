params.probes = 'probes.fa'
params.image = 'kms.sif'
params.threshold = 1
params.classic_index_dir = 'index'
params.sample_list = 'sample.list'
params.output_genotype_call_path = 'genotype_calls'

probes = file(params.probes)
image = file(params.image)
classic_index_dir = file(params.classic_index_dir)
sample_list = file(params.sample_list)
output_genotype_call_path = file(params.output_genotype_call_path)

process splitLines {

        output:
        file 'chunk_*' into probes_chunks

        """
        #!/usr/bin/env bash
        split -a 2 -l 10000 $probes chunk_
        """
}

process queryCobs {

        input:
        file fasta from probes_chunks.flatten()

        output:
        file 'result_*' into cobsResults

        """
        sed -n 'n;p' $fasta | xargs -I{} singularity exec $image query {} $params.threshold $classic_index_dir > result_$fasta
        """
}

process parseBigsiQueryResults {
        memory '3000 MB'

        input:
        file json from cobsResults

        output:
        file 'parsed_bigsi_query_results_chunk_*' into genotype_calls_chunks

        """
        parse_bigsi_query_results.py --bigsi-result $json --sample-list ${sample_list} > parsed_bigsi_query_results_chunk_$json
        """
}

process pasteGenotypeCalls {

        input:
        file call from genotype_calls_chunks.toSortedList({ a, b -> a.name <=> b.name })

        output:
        file 'tmp.all.genotypecalls' into genotype_calls_all

        """
        paste -d "" $call > tmp.all.genotypecalls
        """
}

process pasteSamplesAndGenotypeCalls {

        input:
        file calls from genotype_calls_all

        """
        paste ${sample_list} $calls > ${output_genotype_call_path}
        """
}
