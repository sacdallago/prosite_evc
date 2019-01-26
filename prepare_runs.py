import os
import copy
from pathlib import Path
from evcouplings.align import read_fasta, parse_header
from evcouplings.utils import read_config_file
from evcouplings.utils.app import run_jobs, unroll_config

master_config = read_config_file('config.yml')
alignments_folder = 'prosite_alignments'
alignment_files = [f for f in os.listdir(alignments_folder) if os.path.isfile(os.path.join(alignments_folder, f))]

for alignment_file in alignment_files:
    alignment_path = os.path.join(alignments_folder, alignment_file)
    alignment_path = str(Path(alignment_path).resolve())
    alignment_name = os.path.splitext(alignment_file)[0]
    alignment_binary = open(alignment_path)
    alignment = read_fasta(alignment_binary)

    first_sequence_id = parse_header(next(alignment)[0])

    directory = 'runs/{}'.format(alignment_name)
    current_config = copy.deepcopy(master_config)
    os.mkdir(directory)

    current_config['global']['prefix'] = directory
    current_config['global']['sequence_id'] = first_sequence_id[0]
    current_config['align']['input_alignment'] = alignment_path

    conf = unroll_config(current_config)
    run_jobs(conf, current_config, overwrite=True)
