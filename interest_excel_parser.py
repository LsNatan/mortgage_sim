
import re

import numpy as np
import xlrd


class InterestExcelParser(object):
    def __init__(self, excel_path):
        self.excel_path = excel_path

        self.track_start_row = 1
        self.interest_range_yearly_tracks = {}
        self.interest_range_textual_tracks = {}

        self.parse_excel()

    @staticmethod
    def irange(tuple):
        return range(tuple[0], tuple[1]+1)

    @staticmethod
    def extract_percentage_range(x, dtype):
        per_range = tuple([dtype(i) for i in re.findall(r'(\d+\.?\d+)%', x)])
        per_range = (0, per_range[0]) if len(per_range) == 1 else per_range
        return per_range

    def extract_track(self, x):
        track = tuple([int(i) for i in re.findall(r'(\d+)', x)])
        if len(track) != 0:
            track = (track[0], track[0]) if len(track) == 1 else track
            track = self.irange(track)
        else:
            track = x
        return track

    def query_percentage_range(self, funding, track):

        if isinstance(track, (int, float)):
            track = int(track)
            query = [self.interest_range_yearly_tracks[key] for key in self.interest_range_yearly_tracks if (funding in key[0] and track in key[1])]
        elif isinstance(track, str):
            query = [self.interest_range_textual_tracks[key] for key in self.interest_range_textual_tracks if (funding in key[0] and track in key[1])]

        assert len(query) != 0,  "The chosen track if funding is illegal"
        return query[0]

    def query_percentage(self, funding, track, metric='mean'):
        percentage_range = self.query_percentage_range(funding, track)
        if metric == 'mean':
            p = np.mean(percentage_range)
        elif metric == 'min':
            p = np.min(percentage_range)
        elif metric == 'max':
            p = np.max(percentage_range)
        else:
            assert 0, "not supported metric!"
        return p

    def parse_excel(self):
        wb = xlrd.open_workbook(self.excel_path)
        sheet = wb.sheet_by_index(0)
        funding_percentage_list = []
        for row in range(0, sheet.nrows):
            row_val = sheet.row_values(row)
            for i, col in enumerate(row_val):
                if row == 0:
                    funding_percentage_list.append(self.extract_percentage_range(col, dtype=int))
                if row >= self.track_start_row:
                    if i == 0:
                        track = self.extract_track(col)
                    else:
                        if isinstance(track, str):
                            self.interest_range_textual_tracks[(self.irange(funding_percentage_list[i]), track)] = self.extract_percentage_range(col, dtype=float)
                        else:
                            self.interest_range_yearly_tracks[(self.irange(funding_percentage_list[i]), track)] = self.extract_percentage_range(col, dtype=float)


if __name__ == '__main__':
    excel_path_kats = r"C:\Users\dp26422\PycharmProjects\mortgage\interests\joint.xlsx"
    excel_path_kalats = r"C:\Users\dp26422\PycharmProjects\mortgage\interests\not_joint.xlsx"
    ep2 = InterestExcelParser(excel_path_kalats)
    ep1 = InterestExcelParser(excel_path_kats)
    print(ep1.query_percentage_range(75, 'changing'))
    print(ep1.query_percentage(75, 'changing'))
    # print(ep2.query_percentage_range(75, 'prime'))
    # print(ep2.query_percentage_range(45, 'changing every five'))
