"""
Utility module for reading and writing UTF-8 CSV files.

Adapted from:
http://docs.python.org/2/library/csv.html#examples
"""

import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, stream, encoding):
        self.reader = codecs.getreader(encoding)(stream)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeDictReader(object):
    """
    A CSV DictReader which will iterate over lines in the CSV file "csvfile",
    which is encoded in the given encoding.
    """

    def __init__(self, csvfile, fieldnames=None, encoding="utf-8", **kwargs):
        csvfile = UTF8Recoder(csvfile, encoding)
        self.reader = csv.DictReader(csvfile, fieldnames, **kwargs)

    def next(self):
        row = self.reader.next()
        return {unicode(k, "utf-8"): unicode(v, "utf-8")
                for k, v in row.items()}

    @property
    def fieldnames(self):
        return self.reader.fieldnames

    def __iter__(self):
        return self


class UnicodeDictWriter(object):
    """
    A CSV DictWriter which will write rows to CSV file "csvfile",
    which is encoded in the given encoding.
    """

    def __init__(self, csvfile, fieldnames, encoding="utf-8", **kwargs):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, **kwargs)
        self.stream = csvfile
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow(
                {k.encode("utf-8"): v.encode("utf-8") for k, v in row.items()})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    def writeheader(self):
        self.writer.writeheader()
