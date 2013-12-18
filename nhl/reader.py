
class AbstractReader(object):
    '''Abstract class for reading the Player Stats tables. 

    '''
    
    def get_row_id(self, row):
        pass


    def readtables(self):
        pass
        


    def readdatarows(self, table):
        '''Reads all data rows from a table. 
        Data rows are either all inside <tbody> or all but the first and last.

        ''' 

        tbody = table.find("tbody")
        if tbody:
            rows = tbody.find_all('tr')
        else:
            rows = table.find_all("tr")[1:-1]

        for row in rows:
            yield row 


    def readdatacells(self, row):

        tds = row.find_all('td')
        
        data = []  
        for td in tds:
            try: 
                data.append(td.string.strip())
            except:
                data.append(None)

        data.append(self.get_row_id(row))

        #print data

        return self.rowdata._make(data)  

    
    def run(self, limit=None):

        row_counter = 0
        for table in self.readtables(): 
            for row in self.readdatarows(table):
                if row_counter == limit:
                    raise StopIteration
                yield self.readdatacells(row)
                row_counter  += 1

    
    def fetch(self, limit=None):
        '''Returns the stats as a list'''
        return list(self.run(limit))

    
    def __iter__(self):
        return self.run()