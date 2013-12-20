class TableReader(object): 

    def __init__(self, table):
        self.table = table


    def run(self, limit=None):
        '''Returns one row at the time'''        
        row_counter = 0
        for row in self.table.readrows():
            if row_counter == limit:
                raise StopIteration

            yield row            
            row_counter += 1

    
    def fetch(self, limit=None):
        '''Returns all table rows as one (potentially empty or very long) list
        '''
        return list(self.run(limit))

    
    def __iter__(self):
        return self.run()


