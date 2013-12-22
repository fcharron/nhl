from datatypes import *

DEFAULT_FORMATTERS = {
    'season' : season,
    'gametype' : unicode_or_none,
    'team_id' : unicode_or_none,
    'nhl_id' : int,
    'number' : int_or_none,
    'player' : unicode_or_none,
    'team' : unicode_or_none,
    'pos' : unicode_or_none,#position


    #Skaters Summary
    'gp' : int_or_none, #games played
    'g' : int_or_none, #goals
    'a' : int_or_none, #assists
    'p' : int_or_none, #points
    'pts' : int_or_none, #points
    'plusminus' : int_or_none, #+/-
    'pim' : int_or_none, #penalty minutes
    'pp' : int_or_none,#powerplay goals
    'sh' : int_or_none,#shorthanded goals
    'gw' : int_or_none,#game winning goals
    'gt' : int_or_none,#game tying goals, not used anymore
    'ot' : int_or_none,#overtime goals
    's' : int_or_none,#shots
    'sperc' : float_or_none,#shooting percentage
    'toi_g' : minutes_as_time,#time on ice / game
    'sft_g' : int_or_none,#shifts per min / game
    'foperc' : float_or_none,#faceoff win
    'ppg' : int_or_none,
    'shg' : int_or_none,
    'gwg' : int_or_none,

    #Goalies Summary
    'gs' : int_or_none,#games started
    'ga' : int_or_none,#games started
    'gaa' : float_or_none,#goals against average
    'sv' : int_or_none,#saves
    'svperc' : float_or_none,#save percentage
    'toi' : minutes_as_time,#time on ice
    'l' : int_or_none, #losses
    'w' : int_or_none, #wins
    't' : int_or_none, #ties
    'sa' : int_or_none,#shots against
    'so' : int_or_none,#shutouts
    'min' : minutes_as_time,#time on ice
    
    #Skaters bios
    'dob' : unicode_or_none,
    'birthcity' : unicode_or_none,
    's_p' : unicode_or_none,
    'ctry' : unicode_or_none,
    'ht': int_or_none, 
    'wt': int_or_none,
    'draft' : unicode_or_none, 
    'rnd' : int_or_none, 
    'ovrl' : int_or_none, 
    'rk' : lambda x:True if x and x in ('Y') else False
}

RAW_FORMATTERS = {k:lambda x:x for k,v in DEFAULT_FORMATTERS.items()} 
