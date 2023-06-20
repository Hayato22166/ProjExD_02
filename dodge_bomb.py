import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}

def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    # こうかとんsurface(kk_img)からこうかとんRect(kk_rct)を抽出する
    kk_rct = kk_img.get_rect()
    kk_rct.center = WIDTH/2, HEIGHT/2
    bm_img = pg.Surface((20, 20))  # 練習1
    bm_img.set_colorkey((0, 0, 0))  # 黒い部分を透明にする
    pg.draw.circle(bm_img, (255, 0, 0), (10, 10), 10)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    # 爆弾surface(bm_img)から爆弾Rect(bm_rct)を抽出する
    bm_rct = bm_img.get_rect()
    # 爆弾Rectの中心座標を乱数で指定する
    bm_rct.center = x, y
    vx, vy = +5, +5  # 練習２

    kk_mv = [(-5,0), (-5,+5), (0,+5), (+5,+5), (+5,0), (+5,-5), (0,-5), (-5,-5)]
    kk_imgs = []
    for i in range(8):
        kk_imgs.append(pg.transform.rotozoom(kk_img, i, 1.0))  
    kk_dic = dict(zip(kk_mv, kk_imgs))
    print(kk_dic)

    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bm_rct):  # 練習5
            print("game over")
            return  # ゲームオーバー
        
        key_list = pg.key.get_pressed()
        sum_mv = [0, 0]  # 合計移動量
        for k, mv in delta.items():
            if key_list[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
            
            
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bm_rct.move_ip(vx, vy)  # 練習２
        yoko, tate = check_bound(bm_rct)
        if not yoko:  # 横方向について画面外に行ったら
            vx *= -1
        if not tate:  # 縦方向について画面外に行ったら
            vy *= -1
        screen.blit(bm_img, bm_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()