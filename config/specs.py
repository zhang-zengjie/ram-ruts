from stlpy.benchmarks.common import inside_rectangle_formula, outside_rectangle_formula

n = 2
# Areas of interest
SAFETY = (-10, 10, -2, 10)
HOME = (-10, 10, -2, 0)
TARGETA = (-10, -8, 8, 10)
TARGETB = (7, 9, 7, 9)
CHARGER = (-8, -3, 2, 4)
OBSTACLE = (-2, 2, 3, 10)

# Objectives (conjuctions/disjuntions of normalized half-spaces)
gamma_S = inside_rectangle_formula(SAFETY, 0, 1, n)
gamma_H = inside_rectangle_formula(HOME, 0, 1, n)
gamma_TA = inside_rectangle_formula(TARGETA, 0, 1, n)
gamma_TB = inside_rectangle_formula(TARGETB, 0, 1, n)
gamma_C = inside_rectangle_formula(CHARGER, 0, 1, n)
gamma_O = outside_rectangle_formula(OBSTACLE, 0, 1, n)

# Single-Agent Version

bar_phi_B = gamma_S.always(0, 40) & gamma_O.always(0, 40)
bar_phi_T = gamma_TA.eventually(20, 30) | gamma_TB.eventually(20, 30)
bar_phi_C = gamma_C.eventually(20, 25)
bar_phi_H = gamma_H.always(0, 5).eventually(25, 30)

bar_phi_B.name = "SAFETY"
bar_phi_T.name = "GO TO TARGETS"
bar_phi_C.name = "CHARGING"
bar_phi_H.name = "GO HOME"

time_list_single = [5, 15, 20]
spec_list_single = [bar_phi_T, bar_phi_C, bar_phi_H]

