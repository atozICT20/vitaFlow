# -*- coding: utf-8 -*-
# coding=utf-8
from __future__ import unicode_literals

"""
To run
    `PYTHONIOENCODING=utf-8 python3`

"""
import sys
import os
sys.path.append(os.getcwd())
import fire

# import config
from vitaflow.pipeline.interfaces.plugin import TextCombiner
from vitaflow.pipeline.postprocessor.ocr_tesseract import TessaractOcrModule
from vitaflow.pipeline.postprocessor.ocr_calamari import CalamariOcrModule
from tqdm import tqdm

os.environ['OMP_THREAD_LIMIT'] = '1'

class TextFile(TextCombiner):

    def _handle_file(self, in_file_path, out_file_path):
        lines = []

        list_of_in_txt_files = in_file_path #TODO change name in args!

        for each_in_text_prediction in tqdm(list_of_in_txt_files):
            if os.path.isfile(out_file_path):
                #  read the file and append values
                with open(out_file_path, "a") as fd:
                    line = open(each_in_text_prediction, "r").read()
                    lines.append(line)
                    fd.write(line)
                    fd.write("\n")
            else:
                # create a new file with headers
                with open(out_file_path, "w") as fd:
                    line = open(each_in_text_prediction, "r").read()
                    lines.append(line)
                    fd.write(line)
                    fd.write("\n")

        return lines

    def _handle_files(self, source_dir, destination_dir):
        """Plugin module should implement this to handle all the files in the given directory"""

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        predicted_outputs = {}

        tesseract = TessaractOcrModule.__name__
        calamari = CalamariOcrModule.__name__

        extracted_text = dict()

        for each_dir in os.listdir(source_dir):
            in_files = self.get_all_input_files(source_dir=os.path.join(source_dir, each_dir),
                                                input_files_types=[".txt"])

            #sort based on file number
            in_files = sorted(in_files,
                              key=lambda x: int(os.path.splitext(os.path.basename(x).split(os.extsep)[0])[0]))

            predicted_outputs[tesseract] = [file for file in in_files if tesseract in file]
            # TODO use calamari args; calamari latest version support renaming the output file names
            predicted_outputs[calamari] = [file for file in in_files if tesseract not in file]

            extracted_text[each_dir + "_tesseract"] = self._handle_file(in_file_path=predicted_outputs[tesseract],
                                                                        out_file_path=os.path.join(destination_dir,
                                                                                                   each_dir) + "_" + tesseract + ".txt")

            extracted_text[each_dir + "_calamari"] = self._handle_file(in_file_path=predicted_outputs[calamari],
                                                                       out_file_path=os.path.join(destination_dir,
                                                                                                  each_dir) + "_" + calamari + ".txt")

        return extracted_text


def run(source_directory,
        destination_dir):
    """
    Utility to combine all the text OCRed from cropped images. Basically this takes some assumption that the
    directory names follows certain naming convention, specific to vitaflow pipeline
    :param source_directory: Directory which has list of folders each folder containing cropped images of identified text regions
    :param destination_dir: Directory to store the extracted text from cropped images preserving the folder structure
    :return:
    """

    tt = TextFile()
    print('--' * 55)
    tt.process_files(source_dir=source_directory, destination_dir=destination_dir)


if __name__ == '__main__':
    fire.Fire(run)

