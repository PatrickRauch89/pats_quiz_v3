import sqlite3
import csv
from random import randint, shuffle


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

            rnd = randint(1, data_count)
            term = read_infos[rnd][1]
            answer1 = read_infos[rnd][2]

            self.table = table
            if self.table == "python":
                explanation = read_infos[rnd][3]
            else:
                explanation = ""

            answer2 = read_infos[randint(1, data_count)][2]
            answer3 = read_infos[randint(1, data_count)][2]

            answers = [answer1, answer2, answer3]
            shuffle(answers)

            

            return term, answers, answer1, explanation



class Highscore:
    def __init__(self, path="data/info_score.csv"):
        pass

    def read_score(self):
        with open('data/info_score.csv', 'r', newline='', encoding='utf-8') as csvscore:
            read_score = list(csv.reader(csvscore))

            self.basic_score = read_score[0][0]
            self.python_score = read_score[0][1]
            self.eng_base_score = read_score[0][2]
            self.eng_voc_score = read_score[0][3]
            self.abbreviation_score = read_score[0][4]
    
    def write_score(self):
        highscore = [self.basic_score, self.python_score, self.eng_base_score, self.eng_voc_score, self.abbreviation_score]
        with open('data/info_score.csv', 'w', newline='', encoding='utf-8') as csvscore:
            writer = csv.writer(csvscore)
            writer.writerows(highscore)

    def change_score_plus(self, table):
        if table == "base":
            self.basic_score += 5
            self.write_score()
    

    def change_score_minus(self, table):
        if table == "base":
            self.basic_score += 3
            self.write_score()
            