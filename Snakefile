configfile: "config.yaml"

input_dir=config["input_dir"]
output_dir=config["output_dir"]
nb_of_batches=int(config["nb_of_batches"])

rule all:
    input:
        expand(f"{output_dir}/assembly_{{batch}}.tar.gz", batch=range(nb_of_batches))

rule download_and_assembly:
    input:
        tsv_file = f"{input_dir}/data.tsv_{{batch}}.tsv"
    output:
        assembly_dir=f"{output_dir}/assembly_{{batch}}.tar.gz",
        metadata=f"{output_dir}/metadata_{{batch}}.txt"
    shadow: "shallow"
    threads: 1
    resources: mem_mb=lambda wildcards, attempt: {1: 20000, 2: 80000}[attempt]
    conda: "env.yaml"
    log: "logs/download_and_assembly_{batch}.log"
    params:
        timeout = config["timeout"],
        fast_dir = config["fast_dir"],
        skip_assembly = "--skip-assembly" if config["skip_assembly"] else "",
        keep_reads = "--keep-reads" if config["keep_reads"] else "",
    shell:
        """
        # Create the output directory
        mkdir assembly_out

        # Run the Python script on the TSV file
        python scripts/download_and_assembly.py {input.tsv_file} assembly_out metadata.tsv {params.timeout} {params.fast_dir} {params.skip_assembly} {params.keep_reads} >{log} 2>&1

        # Compress the output directory using tar.gz
        tar czf {output.assembly_dir} -C assembly_out .
        cp metadata.tsv {output.metadata}
        """
