


class TableRowsIterator(object): 


    def get_rowmap():
        pass   

    def run(self, limit=None):

        row_counter = 0
        for row in self.readrows():
            if row_counter == limit:
                raise StopIteration
            
            yield self.get_rowmap()._make(row)
            
            row_counter += 1

    
    def fetch(self, limit=None):
        '''Returns the stats as a list'''
        return list(self.run(limit))

    
    def __iter__(self):
        return self.run()