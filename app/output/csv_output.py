class CsvOutput(object):

    def parse_first_row(self, row):
        return self.parse_row(row)

    def parse_row(self, row):
        return ','.join(repr(cell).replace(',','\\,') for cell in row)
