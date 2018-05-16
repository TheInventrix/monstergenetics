import libtcodpy as libtcod
import shelve
import cfg
import object
import mapgen
import gui

#module used for main gameplay functions
 
def player_move_or_attack(dx, dy):
    #the coordinates the player is moving to/attacking
    x = cfg.player.x + dx
    y = cfg.player.y + dy
 
    #try to find an attackable object there
    target = None
    for obj in cfg.objects:
        if obj.fighter and obj.x == x and obj.y == y:
            target = obj
            break
 
    #attack if target found, move otherwise
    if target is not None:
        cfg.player.fighter.attack(target)
    else:
        cfg.player.move(dx, dy)
        cfg.fov_recompute = True
 
def handle_keys():
    if cfg.key.vk == libtcod.KEY_ENTER and cfg.key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif cfg.key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  #exit game
 
    if cfg.game_state == 'playing':
        #movement keys
        if cfg.key.vk == libtcod.KEY_UP or cfg.key.vk == libtcod.KEY_KP8:
            player_move_or_attack(0, -1)
        elif cfg.key.vk == libtcod.KEY_DOWN or cfg.key.vk == libtcod.KEY_KP2:
            player_move_or_attack(0, 1)
        elif cfg.key.vk == libtcod.KEY_LEFT or cfg.key.vk == libtcod.KEY_KP4:
            player_move_or_attack(-1, 0)
        elif cfg.key.vk == libtcod.KEY_RIGHT or cfg.key.vk == libtcod.KEY_KP6:
            player_move_or_attack(1, 0)
        elif cfg.key.vk == libtcod.KEY_HOME or cfg.key.vk == libtcod.KEY_KP7:
            player_move_or_attack(-1, -1)
        elif cfg.key.vk == libtcod.KEY_PAGEUP or cfg.key.vk == libtcod.KEY_KP9:
            player_move_or_attack(1, -1)
        elif cfg.key.vk == libtcod.KEY_END or cfg.key.vk == libtcod.KEY_KP1:
            player_move_or_attack(-1, 1)
        elif cfg.key.vk == libtcod.KEY_PAGEDOWN or cfg.key.vk == libtcod.KEY_KP3:
            player_move_or_attack(1, 1)
        elif cfg.key.vk == libtcod.KEY_KP5 or cfg.key.vk == libtcod.KEY_SPACE:
            pass  #do nothing ie wait for the monster to come to you
        elif cfg.key.vk == libtcod.KEY_INSERT or cfg.key.vk == libtcod.KEY_KP0:
            #toggle real time mode
            cfg.run_realtime = not cfg.run_realtime
        else:
            #test for other keys
            key_char = chr(cfg.key.c) # use for alphabetical keys
            # use key.text for symbolic keys
            '''
            if key_char == 'g':
                #pick up an item
                for obj in objects:  #look for an item in the player's tile
                    if obj.x == cfg.player.x and obj.y == cfg.player.y and obj.item:
                        obj.item.pick_up()
                        break
 
            if key_char == 'i':
                #show the inventory; if an item is selected, use it
                chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.use()
 
            if key_char == 'd':
                #show the inventory; if an item is selected, drop it
                chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.drop()
            
            if key_char == 'c':
                #show character information
                level_up_xp = cfg.LEVEL_UP_BASE + cfg.player.level * cfg.LEVEL_UP_FACTOR
                gui.msgbox('Character Information\n\nLevel: ' + str(cfg.player.level) + '\nExperience: ' + str(cfg.player.fighter.xp) +
                       '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(cfg.player.fighter.max_hp) +
                       '\nAttack: ' + str(cfg.player.fighter.power) + '\nDefense: ' + str(cfg.player.fighter.defense), cfg.CHARACTER_SCREEN_WIDTH)
            '''
            if key_char == 's':
                #show monster stats
                gui.display_monster_stats()

            if key_char == 'd':
                #show monster descriptions
                gui.display_description()
            
            if key_char == 'r':
                #toggle real time mode
                cfg.run_realtime = not cfg.run_realtime
            
            if key_char == 'q':
                #quit game while running
                return 'exit'
            '''
            if cfg.key.text == '>' or cfg.key.text == '+':
                #go down stairs, if the player is on them
                if cfg.stairs.x == cfg.player.x and cfg.stairs.y == cfg.player.y:
                    next_level()
            '''
            if cfg.run_realtime:
                return 'wait'
                
            else:
                return 'didnt-take-turn'
 
def check_level_up():
    #see if the player's experience is enough to level-up
    level_up_xp = cfg.LEVEL_UP_BASE + cfg.player.level * cfg.LEVEL_UP_FACTOR
    if cfg.player.fighter.xp >= level_up_xp:
        #it is! level up and ask to raise some stats
        cfg.player.level += 1
        cfg.player.fighter.xp -= level_up_xp
        gui.message('Your battle skills grow stronger! You reached level ' + str(cfg.player.level) + '!', libtcod.yellow)
 
        choice = None
        while choice == None:  #keep asking until a choice is made
            choice = gui.menu('Level up! Choose a stat to raise:\n',
                          ['Constitution (+20 HP, from ' + str(cfg.player.fighter.max_hp) + ')',
                           'Strength (+1 attack, from ' + str(cfg.player.fighter.power) + ')',
                           'Agility (+1 defense, from ' + str(cfg.player.fighter.defense) + ')'], cfg.LEVEL_cfg.SCREEN_WIDTH)
 
        if choice == 0:
            cfg.player.fighter.base_max_hp += 20
            cfg.player.fighter.hp += 20
        elif choice == 1:
            cfg.player.fighter.base_power += 1
        elif choice == 2:
            cfg.player.fighter.base_defense += 1
 
def save_game():
    #open a new empty shelve (possibly overwriting an old one) to write the game data
    file = shelve.open('savegame', 'n')
    file['map'] = cfg.map
    file['objects'] = cfg.objects
    file['player_index'] = cfg.objects.index(cfg.player)  #index of player in objects list
    file['stairs_index'] = cfg.objects.index(cfg.stairs)  #same for the stairs
    file['inventory'] = cfg.inventory
    file['game_msgs'] = cfg.game_msgs
    file['game_state'] = cfg.game_state
    file['population'] = cfg.population
    file['max_population'] = cfg.max_population
    file['run_realtime'] = cfg.run_realtime
    file['dungeon_level'] = cfg.dungeon_level
    file.close()
 
def load_game():
    #open the previously saved shelve and load the game data
    file = shelve.open('savegame', 'r')
    cfg.map = file['map']
    cfg.objects = file['objects']
    cfg.player = cfg.objects[file['player_index']]  #get index of player in objects list and access it
    cfg.stairs = cfg.objects[file['stairs_index']]  #same for the stairs
    cfg.inventory = file['inventory']
    cfg.game_msgs = file['game_msgs']
    cfg.game_state = file['game_state']
    cfg.population = file['population']
    cfg.max_population = file['max_population']
    cfg.run_realtime = file['run_realtime']
    cfg.dungeon_level = file['dungeon_level']
    file.close()
 
    mapgen.initialize_fov()
 
def new_game():
    #create object representing the player
    fighter_component = object.Fighter(hp=100, defense=100, power=100, dex=20, speed=100, perception=cfg.TORCH_RADIUS, luck=100, death_function=object.player_death)
    cfg.player = object.Object(0, 0, '@', 'player', libtcod.white, blocks=True, fighter=fighter_component)
 
    cfg.player.level = 1
 
    #generate map (at this point it's not drawn to the screen)
    cfg.dungeon_level = 1
    mapgen.make_bsp()
    mapgen.initialize_fov()
 
    cfg.game_state = 'playing'
    cfg.run_realtime = cfg.REAL_TIME
    cfg.inventory = []
 
    #create the list of game messages and their colors, starts empty
    cfg.game_msgs = []
    
    #create dictionaries of populations for monsters
    cfg.population = {}
    cfg.max_population = {}
    object.initialize_population()
 
    #a warm welcoming message!
    gui.message('Beginning genetic simulation.', libtcod.desaturated_red)
 
    #initial equipment: a dagger
    #equipment_component = object.Equipment(slot='right hand', power_bonus=2)
    #obj = object.Object(0, 0, '-', 'dagger', libtcod.sky, equipment=equipment_component)
    #cfg.inventory.append(obj)
    #equipment_component.equip()
    #obj.always_visible = True
 
def play_game():
    player_action = None
 
    #main loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, cfg.key, cfg.mouse)
        #render the screen
        gui.render_all()
 
        libtcod.console_flush()
 
        #level up if needed
        check_level_up()
 
        #erase all objects at their old locations, before they move
        for obj in cfg.objects:
            obj.clear()
 
        #handle keys and exit game if needed
        player_action = handle_keys()
        if player_action == 'exit':
            save_game()
            break
 
        #let monsters take their turn
        if cfg.game_state == 'playing' and player_action != 'didnt-take-turn':
            for obj in cfg.objects:
                if obj.ai:
                    obj.ai.take_turn()
                    
            #update population counts
            #update_population()
            object.update_max_population()
 
def main_menu():
    libtcod.console_set_custom_font('terminale8x12_gs_ro.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, 'Monster Genetics', False)
    libtcod.sys_set_fps(cfg.LIMIT_FPS)
    img = libtcod.image_load('menu_background.png')
 
    while not libtcod.console_is_window_closed():
        gui.display_main_menu(img)
 
        #show options and wait for the player's choice
        choice = gui.menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)
 
        if choice == 0:  #new game
            new_game()
            play_game()
        if choice == 1:  #load last game
            try:
                load_game()
            except:
                gui.msgbox('\n No saved game to load.\n', 24)
                continue
            play_game()
        elif choice == 2:  #quit
            break
