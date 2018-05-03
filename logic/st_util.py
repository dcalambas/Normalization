import csv
import os
import st_root
import json
import string
import sys

class Util:
    def __init__(self):
        """
        :Date: 2018-02-06
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        Constructor for the class
        :rtype: object
        :return: Utils object
        """
        print('Hi!')

    def load_json_multiple(segments):
        chunk = ""
        for segment in segments:
            chunk += segment
            try:
                yield json.loads(chunk)
                chunk = ""
            except ValueError:
                pass

    def product_services_load(self, file_name):
        prod_serv = []
        dir = st_root.ROOT_DIR + os.sep + 'data' + os.sep + 'input' + os.sep + file_name
        with open(dir) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_row = {}
                temp_row['Origen'] = row['Origen']
                temp_row['Descripción'] = row['Descripción']
                temp_row['Tipo'] = row['Tipo']
                temp_row['Semántica'] = row['Semántica']
                prod_serv.append(temp_row)
        return prod_serv

    def find_file_with_ext(dir, ext):
        file_dir = ""
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(ext):
                    file_dir = os.path.join(root, file)
        return file_dir

    def json_chats_load():
        dir = st_root.ROOT_DIR + os.sep + 'data' + os.sep + 'input' + os.sep
        dir = Util.find_file_with_ext(dir, ".json")

        with open(dir) as infile:
            data = json.load(infile)
            return data

    @staticmethod
    def export_cvs(output_file, dict):
        """
        :Date: 2018-02-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        This method exports the contents of a dictionary to a CSV file.
        :param file_output: name of the output file
        :type file_output: text
        :param dict: dictionary of words
        :type dict: dictionary
        :rtype:
        :return: None
        """
        try:
            path_output = st_root.ROOT_DIR + os.sep + 'data' + os.sep + 'output' + os.sep + output_file + '.csv'
            with open(path_output, 'w', newline='\n', encoding='utf8') as output:
                writer = csv.writer(output, delimiter=';')
                for k,v in dict.items():
                    value = str(v).lower()
                    value.rstrip(string.whitespace)
                    writer.writerow([str(k).lower(), value])

            print('CSV file successfully exported!')
        except:
            Util.write_standard_error(sys.exc_info())
