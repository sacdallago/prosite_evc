import os
import copy
from pathlib import Path
from evcouplings.utils import read_config_file, write_config_file

master_config = read_config_file('config.txt')
alignments_folder = 'prosite_alignments'
alignment_files = [f for f in os.listdir(alignments_folder) if os.path.isfile(os.path.join(alignments_folder, f))]

for alignment_file in alignment_files:
    alignment_path = os.path.join(alignments_folder, alignment_file)
    alignment_path = str(Path(alignment_path).resolve())
    alignment_name = os.path.splitext(alignment_file)[0]

    directory = 'runs/{}'.format(alignment_name)
    current_config = copy.deepcopy(master_config)
    os.mkdir(directory)

    current_config['global']['prefix'] = str(Path(directory).resolve())
    current_config['global']['sequence_id'] = alignment_name
    current_config['align']['input_alignment'] = alignment_path
    write_config_file(directory + "/config.txt", current_config)
