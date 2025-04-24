import sqlite3
import csv
from random import shuffle, sample


class DataToFile:
    def load_data(self, table):
        table_name = table
        conn = sqlite3.connect('data/infos.db')
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        with open('data/info_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            headers = [description[0] for description in cursor.description]
            csv_writer.writerow(headers)
            csv_writer.writerows(rows)
        
        conn.close()


class Randomizer:
    def read_data(self, table):
        with open('data/info_data.csv', 'r', newline='', encoding='utf-8') as csvfile:
            read_infos = list(csv.reader(csvfile))
            data_count = len(read_infos) -1

            if data_count < 3:
                data_func = DataToFile
                data_func.load_data(self, table="base")

            random_range = range(0, data_count)
            random_number = sample(random_range, 3)

            term = read_infos[random_number[0]][1]
            answer1 = read_infos[random_number[0]][2]

            self.table = table
            if self.table == "python":
                explanation = read_infos[random_number[0]][3]
            else:
                explanation = ""

            answer2 = read_infos[random_number[1]][2]
            answer3 = read_infos[random_number[2]][2]

            answers = [answer1, answer2, answer3]
            shuffle(answers)

            return term, answers, answer1, explanation


class Highscore:
    def __init__(self, path="data/info_score.csv"):
        self.path = path

        self.basic_score = 0
        self.python_score = 0
        self.eng_base_score = 0
        self.eng_voc_score = 0
        self.abbreviation_score = 0
        try:
            self.read_score()
        except Exception:
            pass

    def read_score(self):
        with open('data/info_score.csv', 'r', newline='', encoding='utf-8') as csvscore:
            reader = csv.reader(csvscore)
            row = next(reader, None)
            
            if row is None:
                return self.basic_score, self.python_score, self.eng_base_score, self.eng_voc_score, self.abbreviation_score

            self.basic_score       = int(row[0])
            self.python_score      = int(row[1])
            self.eng_base_score    = int(row[2])
            self.eng_voc_score     = int(row[3])
            self.abbreviation_score= int(row[4])
            
        return self.basic_score, self.python_score, self.eng_base_score, self.eng_voc_score, self.abbreviation_score
    
    def write_score(self):
        highscore = [self.basic_score, self.python_score, self.eng_base_score, self.eng_voc_score, self.abbreviation_score]
        with open('data/info_score.csv', 'w', newline='', encoding='utf-8') as csvscore:
            writer = csv.writer(csvscore)
            writer.writerow(highscore)

    def change_score_plus(self, table):
        if table == "base":
            self.basic_score += 5
        elif table == "python":
            self.python_score += 5
        elif table == "english_hardware":
            self.eng_base_score += 5
        elif table == "english_voc":
            self.eng_voc_score += 5
        elif table == "abbreviation":
            self.abbreviation_score += 5
        else:
            print("Error 4122")
            
        self.write_score()
    

    def change_score_minus(self, table):
        if table == "base":
            if self.basic_score <= 3:
                self.basic_score = 0
            else:
                self.basic_score -= 3
        elif table == "python":
            if self.python_score <= 3:
                self.python_score = 0
            else:
                self.python_score -= 3
        elif table == "english_hardware":
            if self.eng_base_score <= 3:
                self.eng_base_score = 0
            else:
                self.eng_base_score -= 3
        elif table == "english_voc":
            if self.eng_voc_score <= 3:
                self.eng_voc_score = 0
            else:
                self.eng_voc_score -= 3
        elif table == "abbreviation":
            if self.abbreviation_score <= 3:
                self.abbreviation_score = 0
            else:
                self.abbreviation_score -= 3
        else:
            print("Error 4123")

        self.write_score()
            