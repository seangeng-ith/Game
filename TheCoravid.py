from library.constant import *
from library.sprite import *
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from tkinter import Button, Tk, Canvas, Toplevel, mainloop, PhotoImage, BOTH, Frame, messagebox


#########################
####>>> VARIABLES <<<####
#########################

bg_img_pos = [WINDOW_WIDTH/2, WINDOW_HEIGHT/2]
player_start_pos = [WINDOW_WIDTH/2, WINDOW_HEIGHT]

player_movement_size = 40
player_health_status = 200
player_mask_status = 200
player_alcohol_status = 20

enemy_data = {}
enemy_dict = {}

level_count = 1
mask_count = 0
score_count = 0


########################
####>>> FUNCTION <<<####
########################

####>>> PLAYER FUNCTION <<<####


def movements(x=0, y=0):
    not_wall = True
    if canvas.coords(player)[0] + x >= WINDOW_WIDTH or\
            canvas.coords(player)[1] + y >= WINDOW_HEIGHT or\
            canvas.coords(player)[0] + x <= 0 or\
            canvas.coords(player)[1] + y <= 0:
        not_wall = False
        return_value = None
    else:
        return_value = canvas.move(player, x, y)
    return return_value


def move_up(event):
    movements(y=-player_movement_size)


def move_down(event):
    movements(y=player_movement_size)


def move_left(event):
    movements(x=-player_movement_size)


def move_right(event):
    movements(x=player_movement_size)


def crosshair_aim(event):
    aim_adjustment = 40
    canvas.moveto(player_crosshair, event.x -
                  aim_adjustment, event.y-aim_adjustment)


def shoot(event):
    global enemy_dict, enemy_data, score_count, score_draw, level_count, enemy_key, player_alcohol_status
    if player_alcohol_status > 0:
        player_alcohol_status -= 1
        it_hit = False
        overlaps_point_adj = 20
        lasser = canvas.create_line(
            canvas.coords(player)[0], canvas.coords(
                player)[1], event.x, event.y,
            width=6, fill="cyan")
        # >>> GUNSHOT SOUND EFFECT
        PlaySound(LASER_SHOT, SND_FILENAME | SND_ASYNC)
        aim_overlap = canvas.find_overlapping(
            event.x, event.y, event.x-overlaps_point_adj, event.y-overlaps_point_adj)
        # >>> CHECK IF HIT THE ENEMY
        if len(enemy_dict) > 0:
            for key in enemy_dict:
                if aim_overlap[1] == enemy_dict[key]:
                    enemy_key = key
                    it_hit = True
            # >>> IF HIT TRUE >>> REMOVE ENEMY
            if it_hit:
                blood_splash = canvas.create_image(
                    event.x, event.y, image=blood_img)
                canvas.after(100, lambda: canvas.delete(blood_splash))
                canvas.delete(enemy_dict[enemy_key])
                enemy_dict.pop(enemy_key)
                enemy_data.pop(enemy_key)
                score_count += 10
                canvas.itemconfigure("update_score", text=score_count)
        # >>> CHECK IF THERE IS NO ENEMY
        if len(enemy_dict) == 0:
            level_count += 1
            canvas.delete("all")
            root.bind("<Button-1>", clear_bind)
            if level_count == 2:
                canvas.create_image(bg_img_pos, image=level1_end_bg)
            elif level_count == 3:
                canvas.create_image(bg_img_pos, image=level2_end_bg)
            elif level_count == 4:
                canvas.create_image(bg_img_pos, image=level3_end_bg)
            root.bind("<space>", goto_level)
        print(aim_overlap)
        print(len(enemy_data))
        canvas.itemconfigure("update_alcohol", text=player_alcohol_status)
        canvas.after(20, lambda: canvas.delete(lasser))


def player_info_bar():
    global score_draw, health_draw, mask_draw, alcohol_draw
    score_draw = canvas.create_text(
        WINDOW_WIDTH-100, 50, text=score_count, font=("impact", 14), fill="white", tags="update_score")
    alcohol_draw = score_draw = canvas.create_text(
        WINDOW_WIDTH-100, 80, text=player_alcohol_status, font=("impact", 14), fill="white", tags="update_alcohol")
    score_label = canvas.create_text(
        WINDOW_WIDTH-150, 50, text="POINT: ", font=("verdana", 10, "bold"), fill="white")
    alcohol_label = canvas.create_text(
        WINDOW_WIDTH-150, 80, text="ALCOHOL: ", font=("verdana", 10, "bold"), fill="white")
    health_draw = canvas.create_rectangle(
        0, 10, player_health_status, 30, fill="red")
    mask_draw = canvas.create_rectangle(
        0, 30, player_mask_status, 45, fill="cyan")
    health_label = canvas.create_text(
        235, 20, text="Health", font=("verdana", 10, "bold"), fill="white")
    mask_label = canvas.create_text(
        230, 40, text="Mask", font=("verdana", 10, "bold"), fill="white")
    info_lebel = canvas.create_text(
        WINDOW_WIDTH/2, WINDOW_HEIGHT-20, text="Press I to access shops.", fill="white",
        font=("verdana", 10, "bold")
    )

####>>> ENEMY FUNCTION <<<####


def build_enemy(e_data, e_dict):
    for key in e_data:
        e_dict[key] = canvas.create_image(
            e_data[key]["position"], image=e_data[key]["img"])


def move_enemy(enemy_dict):
    global player, player_health_status, health_draw, failed_text,\
        player_mask_status, mask_draw, shops_canvas
    size_adjust = 20
    if len(enemy_dict) > 0 and player_health_status != 0:
        for key in enemy_dict:
            # >>> CHECK IF ENEMY HIT THE WALL
            if canvas.coords(enemy_dict[key])[0] >= WINDOW_WIDTH:
                enemy_data[key]["volocity"][0] = - \
                    enemy_data[key]["volocity"][0]
            elif canvas.coords(enemy_dict[key])[1] >= WINDOW_HEIGHT:
                enemy_data[key]["volocity"][1] = - \
                    enemy_data[key]["volocity"][1]
            elif canvas.coords(enemy_dict[key])[0] <= 0:
                enemy_data[key]["volocity"][0] = - \
                    1*enemy_data[key]["volocity"][0]
            elif canvas.coords(enemy_dict[key])[1] <= 0:
                enemy_data[key]["volocity"][1] = - \
                    1*enemy_data[key]["volocity"][1]
            # OVERLAPING COORDS
            overlap_player = canvas.find_overlapping(
                canvas.coords(enemy_dict[key])[
                    0]-size_adjust, canvas.coords(enemy_dict[key])[1]-size_adjust,
                canvas.coords(enemy_dict[key])[0]+size_adjust, canvas.coords(enemy_dict[key])[1]+size_adjust)
            # CHECK IF ENEMY OVERLAPING PLAYER
            if len(overlap_player) > 2:
                if overlap_player[1] == player:
                    if player_mask_status > 0:
                        player_mask_status -= 1
                        mask_draw = canvas.create_rectangle(
                            0, 30, player_mask_status, 45, fill="cyan")
                    elif mask_count <= 0:
                        player_health_status -= 1
                        health_draw = canvas.create_rectangle(
                            0, 10, player_health_status, 30, fill="red")
                if player_health_status <= 0:
                    canvas.delete("all")
                    PlaySound(GAME_OVER_SOUND, SND_FILENAME | SND_ASYNC)
                    failed_text = canvas.create_text(bg_img_pos, text="YOU DIED",
                                                     fill="red", font=("impact", 100))
                    restart_btn.place(x=420, y=400)
            canvas.move(enemy_dict[key], enemy_data[key]
                        ["volocity"][0], enemy_data[key]["volocity"][1])
        canvas.after(40, lambda: move_enemy(enemy_dict))


####>>> SPRITE DEPLOYMENT FUNCTION <<<####

def deploy_sprite(number_of_enemy: int, enemy_img):
    global player, player_crosshair
    player_info_bar()
    player = canvas.create_image(player_start_pos, image=player_img)
    enemy = MakeEnemy(enemy_data, enemy_img)
    enemy.create_enemy_data(number_of_enemy)
    build_enemy(enemy_data, enemy_dict)
    move_enemy(enemy_dict)
    player_crosshair = canvas.create_image(
        player_start_pos, image=player_crosshair_img)
    print(enemy_dict)
    root.bind("<Motion>", crosshair_aim)
    root.bind("<Button-1>", shoot)
    root.bind("<i>", shoping_window)


####>>> GAME FUNCTION <<<####

def top_window(top_wind, title: str, width: int, height: int,):
    top_wind.geometry(f"{width}x{height}")
    top_wind.title(title)
    top_wind.resizable(0, 0)


def game_start():
    PlaySound(MUSIC_HOME, SND_FILENAME | SND_ASYNC)
    home_frame.pack(expand=True, fill=BOTH)
    home_canvas.create_image(bg_img_pos, image=home_bg)
    start_btn.place(x=800, y=380)
    setting_btn.place(x=800, y=440)
    exit_btn.place(x=800, y=500)


def setting_window():
    setting_top = Toplevel(root)
    top_window(setting_top, "Settings", 400, 180)
    setting_canvas = Canvas(setting_top, background="black")
    setting_canvas.pack(expand=True, fill=BOTH)
    instruction_text = "Instruction:\n_ Use W A S D to move the character.\n_ Use Mouse to aim.\n_ Left click to shoot."
    setting_canvas.create_text(
        160, 50, text=instruction_text, font=("verdana", 11), fill="cyan")
    sound_on_btn = Button(setting_top, text="Sound On", padx=20)
    sound_on_btn.place(x=20, y=100)
    sound_off_btn = Button(setting_top, text="Sound Off", padx=20)
    sound_off_btn.place(x=20, y=130)


def shoping_window(event):
    global shops_canvas, health_info, mask_info, alcohol_info, shops_canvas, buy_mask_btn, buy_alcohol_btn
    shops = Toplevel(root)
    top_window(shops, "Inventory", 400, 300)
    shops_canvas = Canvas(shops)
    shops_canvas.pack(expand=True, fill=BOTH)
    health_info = shops_canvas.create_text(
        70, 220, text=f"Health : {player_health_status}", font=("verdana", 12))
    mask_info = shops_canvas.create_text(
        90, 245, text=f"Mask shield : {player_mask_status}", font=("verdana", 12))
    alcohol_info = shops_canvas.create_text(
        74, 270, text=f"Alcohol : {player_alcohol_status}", font=("verdana", 12))
    buy_mask_btn = Button(
        shops, text=f"Buy Mask 100/150pt", padx=20, pady=10, command=lambda: add_to_player("mask"))
    buy_alcohol_btn = Button(shops, text="Buy Alcohol Plasma 20/100pt",
                             padx=20, pady=10, command=lambda: add_to_player("alcohol"))
    buy_mask_btn.place(x=20, y=20)
    buy_alcohol_btn.place(x=180, y=20)


def add_to_player(item: str):
    global score_count, player_mask_status, player_alcohol_status, mask_draw
    if score_count >= 50:
        if item == "mask" and (180 >= player_mask_status >= 0):
            player_mask_status += 20
            score_count -= 50
            canvas.delete(mask_draw)
            mask_draw = canvas.create_rectangle(
                0, 30, player_mask_status, 45, fill="cyan")
            print(player_mask_status)
        elif item == "alcohol":
            player_alcohol_status += 20
            score_count -= 50
            canvas.itemconfigure("update_alcohol", text=player_alcohol_status)
        canvas.itemconfigure("update_score", text=score_count)

    else:
        messagebox.askokcancel(title="insufficient points!!",
                               message="You don't have enough point to buy!")


####>>> GAME LEVELS <<<####

def restart_level():
    global player_health_status, player_mask_status
    canvas.delete(failed_text)
    restart_btn.place_forget()
    player_health_status = 200
    player_mask_status = 200
    if level_count == 1:
        level_1()
    elif level_count == 2:
        level_2()
    elif level_count == 3:
        level_3()


def goto_level(event):
    if level_count == 1:
        level_1()
    elif level_count == 2:
        level_2()
    elif level_count == 3:
        level_3()
    elif level_count == 4:
        canvas.pack_forget()
        game_start()


def build_level(enemy_count=0, enemy_img=None, bg_img=None, ):
    global deploy
    canvas.delete("all")
    level_1_continue.pack_forget()
    level_2_continue.pack_forget()
    level_3_continue.pack_forget()
    canvas.pack(expand=True, fill=BOTH)
    canvas.create_image(bg_img_pos, image=bg_img)
    deploy = deploy_sprite(enemy_count, enemy_img)


def level_1():
    home_frame.pack_forget()
    build_level(10, enemy_img_lv1, level1_bg)


def level_2():
    build_level(10, enemy_img_lv2, level2_bg)


def level_3():
    build_level(10, enemy_img_lv3, level3_bg)


####>>> CLEAR KEY BINDING <<<####

def clear_bind(event):
    pass


#########################
####>>> MAIN CODE <<<####
#########################


####>>> ROOT WINDOWS <<<####
root = Tk()
root.resizable(0, 0)
root.title(WINDOW_TITLE)
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

####>>> WINDOW FRAME <<<####

home_frame = Frame(root)
level_selection_frame = Frame(root)


##########################
####>>> PHOTOIMAGE <<<####
##########################

####>>> BACKGROUND IMG <<<####
home_bg = PhotoImage(file=HOME_BACKGROUND_IMAGE_LOCATION)
level1_bg = PhotoImage(file=BACKGROUND_LEVEL1_LOCATION)
level1_end_bg = PhotoImage(file=BACKGROUND_LEVEL1_END_LOCATION)
level2_bg = PhotoImage(file=BACKGROUND_LEVEL2_LOCATION)
level2_end_bg = PhotoImage(file=BACKGROUND_LEVEL2_END_LOCATION)
level3_bg = PhotoImage(file=BACKGROUND_LEVEL3_LOCATION)
level3_end_bg = PhotoImage(file=BACKGROUND_LEVEL3_END_LOCATION)
lab_bg = PhotoImage(file=BACKGROUND_LAB_LOCATION)
####>>> BUTTON IMG <<<####
button_start_img = PhotoImage(file=BUTTON_START_IMG_LOCATION)
button_setting_img = PhotoImage(file=BUTTON_SETTING_IMG_LOCATION)
button_exit_img = PhotoImage(file=BUTTON_EXIT_IMG_LOCATION)
button_back_img = PhotoImage(file=BUTTON_BACK_IMG_LOCATION)
button_restart_img = PhotoImage(file=BUTTON_RESTART_IMG_LOCATION)

####>>> PLAYER IMG <<<####
player_img = PhotoImage(file=CHARACTER_IMG_LOCATION)
player_crosshair_img = PhotoImage(file=CROSSHAIR)

####>>> ENEMY AND ITEMS IMG <<<####
enemy_img_lv1 = PhotoImage(file=ENEMY_IMG_LOCATION)
enemy_img_lv2 = PhotoImage(file=ENEMY2_IMG_LOCATION)
enemy_img_lv3 = PhotoImage(file=ENEMY3_IMG_LOCATION)
heart_img = PhotoImage(file=HEART_LOCATION)
red_virus_img = PhotoImage(file=RED_VIRUS_LOCATION)
vacinne_img = PhotoImage(file=VACINNE_LOCATION)
blood_img = PhotoImage(file=BLOOD_LOCATION)

####>>> ITEM IMG LIST<<<####
item_img = [heart_img, vacinne_img]


######################
####>>> CANVAS <<<####
######################

canvas = Canvas(root)
home_canvas = Canvas(home_frame)
home_canvas.pack(expand=True, fill=BOTH)
level_selection_canvas = Canvas(level_selection_frame)
level_selection_canvas.pack(expand=True, fill=BOTH)

#######################
####>>> BUTTONS <<<####
#######################
restart_btn = Button(root, image=button_restart_img, command=restart_level)
start_btn = Button(home_frame, image=button_start_img, command=level_1)
setting_btn = Button(home_frame, image=button_setting_img,
                     command=setting_window)
exit_btn = Button(home_frame, image=button_exit_img)
level_1_continue = Button(root, image=button_start_img, command=level_2)
level_2_continue = Button(root, image=button_start_img, command=level_3)
level_3_continue = Button(root, image=button_start_img, command=game_start)

########################################
#>>>>>> DEPLOY FUNCTION HERE !!! <<<<<<#
########################################

a = game_start()

###########################
#>>>>>> KEY BINDING <<<<<<#
###########################

root.bind("<w>", move_up)
root.bind("<a>", move_left)
root.bind("<s>", move_down)
root.bind("<d>", move_right)


root.mainloop()
