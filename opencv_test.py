import cv2 as cv
from PIL import ImageGrab
import numpy as np
from directkey import W, Q, O, P, presskey, releasekey

"""
lit_key = cv.imread('images/lit_key.png', cv.IMREAD_UNCHANGED)
dark_key = cv.imread('images/dark_top_full.png', cv.IMREAD_GRAYSCALE)
"""
lit_key_top = cv.imread('images/lit_top_left_corner.png', cv.IMREAD_GRAYSCALE)
q_key = cv.imread('images/individual_keys/q_key_top_dark.png', cv.IMREAD_GRAYSCALE)
w_key = cv.imread('images/individual_keys/w_key_top_dark.png', cv.IMREAD_GRAYSCALE)
o_key = cv.imread('images/individual_keys/o_key_top_dark.png', cv.IMREAD_GRAYSCALE)
p_key = cv.imread('images/individual_keys/p_key_top_dark.png', cv.IMREAD_GRAYSCALE)
go_img = cv.imread('images/GO_snap.png', cv.IMREAD_UNCHANGED)
alpha = 1.7
beta = 0
q_anchor = (0,)
w_anchor = (0,)
o_anchor = (0,)
p_anchor = (0,)
roi_y1, roi_y2 = 510, 610
roi_x1, roi_x2 = 280, 760
cv_rect_area_top = (roi_x1, roi_y1)
cv_rect_area_bot = (roi_x2, roi_y2)


def init_keys(key_matches, img):
    global q_anchor
    global w_anchor
    global o_anchor
    global p_anchor
    for loc in key_matches:
        top = (roi_x1 + loc[0], roi_y1 + loc[1])
        bot = (top[0] + q_key.shape[1], top[1] + q_key.shape[0])
        if not q_anchor[0] and 350 < top[0] < 435:
            q_anchor = top
            cv.rectangle(img, top, bot, (0, 255, 0), cv.LINE_4)
        if not w_anchor[0] and 440 < top[0] < 555:
            w_anchor = top
            cv.rectangle(img, top, bot, (0, 255, 0), cv.LINE_4)
        if not o_anchor[0] and 530 < top[0] < 695:
            o_anchor = top
            cv.rectangle(img, top, bot, (0, 255, 0), cv.LINE_4)
        if not p_anchor[0] and 700 < top[0] < 765:
            p_anchor = top
            cv.rectangle(img, top, bot, (0, 255, 0), cv.LINE_4)


def main():
    global q_anchor
    global w_anchor
    global o_anchor
    global p_anchor

    while True:
        screen = np.array(ImageGrab.grab(bbox=(400, 0, 1300, 960)))
        go_check = cv.matchTemplate(screen, go_img, cv.TM_CCOEFF_NORMED)
        min_v, max_v, min_loc, max_loc = cv.minMaxLoc(go_check)
        print(f"prob: {max_v}")
        if max_v >= 0.473:
            top_left = max_loc
            bot_right = (top_left[0] + go_img.shape[1], top_left[1] + go_img.shape[0])
            cv.rectangle(screen, top_left, bot_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
        cv.rectangle(screen, cv_rect_area_top, cv_rect_area_bot,
                     color=(0, 255, 0), thickness=5, lineType=cv.LINE_4)
        cv.imshow("test", cv.cvtColor(screen, cv.COLOR_BGR2RGB))
        cv.waitKey(2)
        if max_v >= 0.472:
            print('Go seen...')
            cv.waitKey(100)
            break

    screen = np.array(ImageGrab.grab(bbox=(400, 0, 1300, 960)).convert('L'))
    hc_screen = cv.convertScaleAbs(screen, alpha=alpha, beta=beta)
    hc_q_key = cv.convertScaleAbs(q_key, alpha=alpha, beta=beta)
    hc_w_key = cv.convertScaleAbs(w_key, alpha=alpha, beta=beta)
    hc_o_key = cv.convertScaleAbs(o_key, alpha=alpha, beta=beta)
    hc_p_key = cv.convertScaleAbs(p_key, alpha=alpha, beta=beta)
    # Q key
    init_q_key = cv.matchTemplate(hc_screen[roi_y1:roi_y2, roi_x1:roi_x2],
                                  hc_q_key, cv.TM_CCOEFF_NORMED)
    q_anchor = cv.minMaxLoc(init_q_key)[3] if cv.minMaxLoc(init_q_key)[1] > 0.84 else (0, 0)
    # W key
    init_w_key = cv.matchTemplate(hc_screen[roi_y1:roi_y2, roi_x1:roi_x2],
                                  hc_w_key, cv.TM_CCOEFF_NORMED)
    w_anchor = cv.minMaxLoc(init_w_key)[3] if cv.minMaxLoc(init_w_key)[1] > 0.84 else (0, 0)
    # O key
    init_o_key = cv.matchTemplate(hc_screen[roi_y1:roi_y2, roi_x1:roi_x2],
                                  hc_o_key, cv.TM_CCOEFF_NORMED)
    o_anchor = cv.minMaxLoc(init_o_key)[3] if cv.minMaxLoc(init_o_key)[1] > 0.84 else (0, 0)
    # P key
    init_p_key = cv.matchTemplate(hc_screen[roi_y1:roi_y2, roi_x1:roi_x2],
                                  hc_p_key, cv.TM_CCOEFF_NORMED)
    p_anchor = cv.minMaxLoc(init_p_key)[3] if cv.minMaxLoc(init_p_key)[1] > 0.84 else (0, 0)
    # Lit key
    init_lit_key = cv.matchTemplate(screen[roi_y1:roi_y2, roi_x1:roi_x2],
                                    lit_key_top, cv.TM_CCOEFF_NORMED)
    loc_lit_key = np.where(init_lit_key >= 0.85)
    loc_lit_key = list(zip(*loc_lit_key[::-1]))

    if loc_lit_key:
        init_keys(loc_lit_key, screen)
        cv.rectangle(screen, cv_rect_area_top, cv_rect_area_bot,
                     color=(0, 255, 0), thickness=5, lineType=cv.LINE_4)
        cv.imshow("test", cv.cvtColor(screen, cv.COLOR_BGR2RGB))
        if not q_anchor[0]:
            q_anchor = (w_anchor[0] - 70,) if w_anchor[0] > 0 else (420,)
        if not w_anchor[0]:
            w_anchor = (o_anchor[0] - 70,) if o_anchor[0] > 0 else (505,)
        if not o_anchor[0]:
            o_anchor = (p_anchor[0] - 70,) if p_anchor[0] > 0 else (595,)
        if not p_anchor[0]:
            p_anchor = (o_anchor[0] + 75,)
        print(f'key anchor points:\n{q_anchor}\n{w_anchor}\n{o_anchor}\n{p_anchor}')
        cv.waitKey(5)

        while True:
            # Draw box, take screenshot
            screen = np.array(ImageGrab.grab(bbox=(400, 0, 1300, 960)).convert('L'))
            result = cv.matchTemplate(screen[roi_y1:roi_y2, roi_x1:roi_x2],
                                      lit_key_top, cv.TM_CCOEFF_NORMED)
            if cv.minMaxLoc(result)[1] > 0.855:
                max_loc = cv.minMaxLoc(result)[3][0] + roi_x1
                print(f"seen loc: {max_loc}")
                if q_anchor[0] - 10 <= max_loc < w_anchor[0]:
                    presskey(Q)
                    releasekey(Q)
                    print("pressed Q")
                elif q_anchor[0] + 60 < max_loc < o_anchor[0]:
                    presskey(W)
                    releasekey(W)
                    print("pressed W")
                elif w_anchor[0] + 60 < max_loc < p_anchor[0]:
                    presskey(O)
                    releasekey(O)
                    print("pressed O")
                elif o_anchor[0] + 60 < max_loc:
                    presskey(P)
                    releasekey(P)
                    print("pressed P")
            cv.rectangle(screen, cv_rect_area_top, cv_rect_area_bot,
                         color=(0, 255, 0), thickness=5, lineType=cv.LINE_4)
            cv.imshow("test", cv.cvtColor(screen, cv.COLOR_BGR2RGB))
            user_in = cv.waitKey(300)
            if user_in == ord('h'):
                cv.destroyAllWindows()
                break
    else:
        cv.imshow("test", hc_screen)
        user_in = cv.waitKey()
        if user_in == ord('h'):
            cv.destroyAllWindows()


if __name__ == '__main__':
    main()
