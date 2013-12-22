'''
Some common datatypes used in the tables. 

'''
import datetime

def unicode_or_none(s): 
    if s: 
    	return unicode(s.strip()).encode('utf-8')

def float_or_none(s): 
    try:
        return float(s)
    except:
        return None

def int_or_none(s): 
    try:
        return int(s)
    except:
        return None


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


def season(s):
    '''Convert 2012-2013 to 20122013, or None'''
    if s:
        return u"".join(s.strip().split("-"))




if __name__ == '__main__':
    print minutes_as_time("4,374:21")
