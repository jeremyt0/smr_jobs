import json
import csv

class Utils:

    @staticmethod
    def save_to_json(filename, content):
        print(f"Saving content to {filename}...")
        try:
            with open(filename, 'w') as json_file:
                json.dump(content, json_file)
        except Exception as e:
            print(e)
            return False

        print(f"- Finished save_to_json() - {filename}")
        return True

    @staticmethod
    def save_to_txt(filename, content):
        print(f"Saving content to {filename}...")
        try:
            with open(filename, 'w') as text_file:
                print(f'{content}', file=text_file)
        except Exception as e:
            print(e)
            return False
            
        print(f"- Finished save_to_txt() - {filename}")
        return True

    @staticmethod
    def save_to_CSV(filename, mylist):
        print(f"Saving content to {filename}...")
        try:
            with open(filename, 'w', newline='') as csv_file:
                wr = csv.writer(csv_file)
                wr.writerow(mylist)
        except Exception as e:
            print(e)
            return False
            
        print(f"- Finished save_to_csv() - {filename}")
        return True