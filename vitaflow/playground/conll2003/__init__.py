import gin
from vitaflow.data_generators.text.conll_2003_dataset import CoNLL2003Dataset
from vitaflow.iterators.text.csv_seq_to_seq_iterator import CSVSeqToSeqIterator
from vitaflow.models.text.seq2seq.bilstm_crf import BiLSTMCrf

@gin.configurable
def get_experiment_root_directory(value):
    return value
