from codecs import iterdecode
from zipfile import ZipFile
import os
import csv

class CSV(object):
    """A CSV file."""

    def __init__(self, header, rows):
        self.header = header
        self.rows = rows

    def __repr__(self):
        return '<CSV %s>' % self.header

    def __iter__(self):
        return self

    def next(self):
        return dict(zip(self.header, self.rows.next()))

class Feed(object):
    """A collection of CSV files with headers, either zipped into an archive
    or loose in a folder."""

    def __init__(self, filename):
        self.filename = filename 
        self.zf = None
        if not os.path.isdir(filename):
            self.zf = ZipFile(filename)
    
    def __repr__(self):
        return '<Feed %s>' % self.filename

    def unicode_csv_reader(self, file_handle, encoding='utf-8'):
        reader = csv.reader([x.encode(encoding) for x in iterdecode(file_handle, encoding)])
        for row in reader:
            yield [unicode(x, encoding) for x in row]
        return

    def reader(self, filename, encoding='utf-8'):
        if self.zf:
            try:
                file_handle = self.zf.read(filename).split('\n')
            except IOError:
                raise IOError('%s is not present in feed' % filename)
        else:
            file_handle = open(os.path.join(self.filename, filename))
        return self.unicode_csv_reader(file_handle, encoding)

    def read_table(self, filename):
        rows = self.reader(filename)
        return CSV(header=rows.next(), rows=rows)
