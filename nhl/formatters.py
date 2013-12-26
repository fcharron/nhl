
'''

Unmarshalling of data from the format at NHL.com into an internal Python representation. 

'''



import datetime


class NhlFormatterException(Exception):
    pass


def minutes_as_time(s):
    '''Converted from 1,222:88 into datetime.timedelta'''
    if s:
        min_str, sec_str = None,None
        minutes, seconds = 0,0
        
        #check for seconds
        if ":" in s:
            min_str, sec_str = s.split(":")
            seconds = int(sec_str)
        else:
            #We only have minutes
            min_str = s 

        #check for 1,000 seconds            
        if "," in min_str:
            t, d = min_str.split(",")
            minutes += int(t)*1000 
            minutes += int(d)
        else:
            minutes = int(min_str)

        return datetime.timedelta(seconds=seconds,minutes=minutes)



def number(v, type_of_number):
    if '-' in v:
        return None
    else:
        v = v.replace(",","")
        return type_of_number(v)    



class Formatter(object):

    def __init__(self, mapper):
        self.mapper = mapper
    
    def format(self, name, value):
        if value is not None:

            value = value.strip()

            if len(value) < 1:
                return None

            try:
                if name in self.mapper.get('integers', None):
                    return number(value, int)

                if name in self.mapper.get('floats', None):
                    return number(value, float)

                if name in self.mapper.get('minutes', None):
                    return minutes_as_time(value)

                return unicode(value.strip())          
            except Exception as e:
                raise NhlFormatterException("Could not format {}, {}: {}".format(name, value, e.message))

        return None








