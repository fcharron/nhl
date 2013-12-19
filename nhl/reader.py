

import logging 

class TableRowsIterator(object): 


    def get_rowmap():
        pass   

    def run(self, limit=None):

        row_counter = 0
        for row in self.readrows():
            if row_counter == limit:
                raise StopIteration
            
            try:
                rowdata = self.datamap._make(row)
            except Exception as e:
                logging.error("Failed to read table row {} : {}".format(row, e.message))
                raise StopIteration

            yield rowdata            
            row_counter += 1

    
    def fetch(self, limit=None):
        '''Returns the stats as a list'''
        return list(self.run(limit))

    
    def __iter__(self):
        return self.run()