params.probes = ''
params.bigsiimage = ''
params.bigsiconfig = ''
params.samplelist = ''
params.genotypecalls = ''

process splitLines {

        output:
        file 'chunk_*' into probes_chunks

        """
        #!/usr/bin/env bash
        split -a 2 -l 10000 ${params.probes} chunk_
        """
}

process queryBigsi {

        input:
        file fasta from probes_chunks.flatten()

        output:
        file 'bigsi_query_results_chunk_*' into bigsi_query_results_chunks

        """
        singularity exec ${params.bigsiimage} bigsi bulk_search --fasta $fasta --config ${params.bigsiconfig} --stream True > bigsi_query_results_$fasta
        """
}

process parseBigsiQueryResults {
        memory '3000 MB'

        input:
        file json from bigsi_query_results_chunks

        output:
        file 'parsed_bigsi_query_results_chunk_*' into genotype_calls_chunks

        """
        parse_query_results.py --query-result $json --sample-list ${params.samplelist} > parsed_$json
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
        paste ${params.samplelist} $calls > ${params.genotypecalls}
        """
}
