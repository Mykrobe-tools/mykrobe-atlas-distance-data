params.probes = ''
params.bigsiimage = ''
params.bigsiconfig = ''

process splitLines {

        output:
        file 'probes_chunk_*' into probes_chunks

        """
        #!/usr/bin/env bash
        split -a 4 -l 1000 ${params.probes} probes_chunk_
        """
}

process bigsiQuery {

        input:
        file fasta from probes_chunks.flatten()

        output:
        file 'bigsi_query_result_probes_chunk_*' into bigsi_query_results_chunks

        """
        singularity exec ${params.bigsiimage} bigsi bulk_search --fasta $fasta --config ${params.bigsiconfig} --stream True > bigsi_query_result_$fasta
        """
}

