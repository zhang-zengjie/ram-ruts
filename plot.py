import numpy as np
import matplotlib.pyplot as plt
from commons.functions import get_coordinates
from commons.configs import get_agent
from commons.configs import SAFETY, HOME, TARGETA, TARGETB, CHARGER, OBSTACLE

# Load data

N = 40                  # Time-horizon
n = 2                   # System dimension

agent = get_agent(n, N)

prob = np.load('data/' + agent.name + '_prob.npy')
atime = np.load('data/' + agent.name + '_accepted_time.npy')
state_meas = np.load('data/' + agent.name + '_meas_state.npy')
nom_state = np.load('data/' + agent.name + '_hist_nom_state.npy')

# Define colors
OBSTACLE_COLOR = [1, 0.3, 0.3]
TARGET_COLOR = [1, 1, 0.3]
HOME_COLOR = [0.3, 1, 0.4]
CHARGER_COLOR = [0, 0.5, 1]
SAFETY_COLOR = [0.8, 0.9, 1]
STATE_COLOR = [[0.4, 0.7, 0.4], [1, 0, 0], [1, 0.6, 0], [0, 153/255, 76/255], [0, 0, 1]]


# Create figure
plt.figure(figsize=(5, 2))

# Plot in figure
for j, t in enumerate(atime[1:]):
    plt.plot(range(t, N), prob[j, t:].T, 'o:', linewidth=2,
             markersize=4, label=r'$\rho_{}$'.format({j}) + r'$_{,k}$', color=STATE_COLOR[j])

# Limit figure
plt.xlim([0, N])
plt.yticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
# Label figure
plt.xlabel(r'Time $k$', fontsize=12)
plt.ylabel(r'Lower bounds $\rho_{i,k}$ for $\varphi_i$')
plt.legend(ncol=len(atime))

# Show figure
plt.show()

# Define figure
plt.figure(figsize=(8, 3.5))

# Fill figure
plt.fill(*get_coordinates(SAFETY), color=SAFETY_COLOR)
plt.fill(*get_coordinates(TARGETA), color=TARGET_COLOR)
plt.fill(*get_coordinates(TARGETB), color=TARGET_COLOR)
plt.fill(*get_coordinates(HOME), color=HOME_COLOR)
plt.fill(*get_coordinates(CHARGER), color=CHARGER_COLOR)
plt.fill(*get_coordinates(OBSTACLE), color=OBSTACLE_COLOR)


# plot in figure
for j, t in enumerate(atime[1:]):

    plt.plot(nom_state[t, 0], nom_state[t, 1], marker='o', color=STATE_COLOR[j+1],
             linewidth=2, markersize=4, label= f'Traj. planned at time {t}')
plt.plot(state_meas[0], state_meas[1], marker='o', color=STATE_COLOR[-1],
             linewidth=2, markersize=4, label=f'Traj. based on meas.')

# Name objects in figure
plt.text((TARGETA[0] + TARGETA[1]) / 2, (TARGETA[2] + TARGETA[3]) / 2 - 0.25, 'TARGET', weight='bold', fontsize=10, horizontalalignment='center')
plt.text((TARGETB[0] + TARGETB[1]) / 2, (TARGETB[2] + TARGETB[3]) / 2 + -0.25, 'TARGET', weight='bold', fontsize=10, horizontalalignment='center')
plt.text((HOME[0]+HOME[1])/2, (HOME[2]+HOME[3])/2-0.25, 'HOME', weight='bold',  fontsize=10, horizontalalignment='center')
plt.text((CHARGER[0]+CHARGER[1])/2, (CHARGER[2]+CHARGER[3])/2-0.2, 'CHARGER', weight='bold', fontsize=10, horizontalalignment='center')
plt.text((OBSTACLE[0]+OBSTACLE[1])/2, (OBSTACLE[2]+OBSTACLE[3])/2-0.2, 'OBSTACLE', weight='bold', fontsize=10, horizontalalignment='center')

# Limit figure
plt.xlim([SAFETY[0], SAFETY[1]])
plt.ylim([SAFETY[2], SAFETY[3]])

# Label figure
plt.xlabel(r'$x_{1}$', fontsize=18)
plt.xticks(fontsize=14)
plt.ylabel(r'$x_{2}$', fontsize=18)
plt.yticks(fontsize=14)
plt.legend(loc='lower right')

# Save figure
plt.savefig('two_dimensional.png', bbox_inches='tight', pad_inches=0.1, transparent=True)

#Show figure
plt.show()

print('Exiting program')
