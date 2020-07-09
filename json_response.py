import gfs
import pandas as pd
import datetime

class dfHandle(object):
    def __init__(self, df):
        self.df = df
        self.types = {"number": ["float" ,"int"],
                      "date": ["datetime", "Timestamp"]}

    def _transtype(self, pytype):
        strpytype = str(pytype)
        for key in self.types:
            for _type in self.types[key]:
                if _type in strpytype:
                    return key

    @staticmethod
    def _colstring(col, coltype):
        return '{"id": "%s", "label": "%s", "type": "%s"}' %(
                col, col, coltype)

    def _columns(self):
        cols = '"cols": ['
        for col in self.df.columns[:-1]:
            colstr = self._colstring(col, self._transtype(self.df[col].dtype))
            cols += "%s," % (colstr)
        col = self.df.columns[-1]
        colstr = self._colstring(col, self._transtype(self.df[col].dtype))
        cols += "%s]" % (colstr)
        return cols

    @staticmethod
    def jsDate(val):
        retval = val.strftime("Date(%Y,")
        retval += "%d," %(int(val.strftime("%m"))-1)
        retval += val.strftime("%d,%H,%M,)")
        return retval

    
    def _valstring(self, val, valtype):
        if valtype == "date":
            return '{"v": "%s", "f":None}' %(
                self.jsDate(val))
        if valtype == "number":
            return '{"v": %s}' % (str(val))

    def _rowstring(self, row):
        rowstr = '{"c":['
        for col in range(len(self.df.columns))[:-1]:
            v = row[col]
            vtype = self._transtype(type(v))

            rowstr += "%s," %(self._valstring(v, vtype))
        v = row[-1]
        vtype = self._transtype(type(v))
        rowstr += "%s]}" %(self._valstring(v, vtype))
        return rowstr

    def _rows_string(self):
        rows = '"rows": ['
        for idx in range(len(self.df))[:-1]:
            row = self.df.iloc[idx]
            rowstr = self._rowstring(row)
            rows += "%s," % (rowstr)

        row = self.df.iloc[-1]
        rowstr = self._rowstring(row)
        rows += "%s]" % (rowstr)
        return rows

    def __call__(self):
        cols = self._columns()
        rows = self._rows_string()
        retval = '{%s,%s}' % (cols, rows)

        return eval(retval)


if __name__ == '__main__':
    df = gfs.get_data()

    start = pd.Timestamp(datetime.date.today())
    end = start + pd.Timedelta(hours=40)

    data = pd.DataFrame()
    for loc in df.keys():
        data[loc] = df[loc].loc[:end].ghi

    json = dfHandle(data.reset_index())()
    print(data)

