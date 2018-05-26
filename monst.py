#module for defining the initial properties for all the different monsters
import libtcodpy as libtcod
import cfg

class Monster:
    def __init__(self, char, color, hp, pw, df, dx, sp, pr, lk, sc=1, ag=1, chances=1, group_size=1):
        self.char = char
        self.color = color
        self.hp = hp
        self.pw = pw
        self.df = df
        self.dx = dx
        self.sp = sp
        self.pr = pr
        self.lk = lk
        self.sc = sc #social impulse
        self.ag = ag #aggression
        self.chances = chances
        self.group_size = group_size
        
class Plant:
    def __init__(self, char, color, hp, chances=1, group_size=1):
        self.char = char
        self.color = color
        self.hp = hp
        self.pw = 0
        self.df = 0
        self.dx = 0
        self.sp = 0
        self.pr = 0
        self.lk = 0
        self.sc = 0 #social impulse
        self.ag = 0 #aggression
        self.chances = chances
        self.group_size = group_size
        
properties = {
                'player' : Monster('@', libtcod.white, 100, 100, 100, 20, 100, 100, 100),
                'asmu' : Monster('a', libtcod.light_blue, 20, 3, 0, 3, 5, 5, 6, 2, 2, chances=3, group_size=5),
                'qunat' : Monster('q', libtcod.light_red, 25, 5, 1, 11, 6, 6, 4, 9, 8, chances=3, group_size=4),
                'jowiv' : Monster('j', libtcod.light_yellow, 30, 4, 7, 5, 2, 5, 3, 8, 5, chances=3, group_size=4),
                'zaeif' : Monster('Z', libtcod.light_cyan, 40, 10, 0, 4, 9, 5, 7, 2, 7, chances=2, group_size=3),
                'linorl' : Monster('L', libtcod.light_green, 45, 8, 3, 8, 7, 7, 9, 9, 8, chances=2, group_size=3),
                'miirloc' : Monster('M', libtcod.light_magenta, 60, 12, 5, 6, 3, 6, 2, 4, 10, chances=2, group_size=2),
                'wirqen\'kaak' : Monster('&', libtcod.lighter_violet, 80, 15, 7, 6, 10, 8, 1, 2, 12),
                'plant' : Plant('*', libtcod.dark_green*0.7, 5, chances=1, group_size=5),
                }
