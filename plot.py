import numpy as np
import matplotlib.pyplot as plt
from commons.functions import get_coordinates
from configs import get_agent
from configs import RG, CM

# Load data

N = 40                  # Time-horizon
n = 2                   # System dimension

agent = get_agent(n, N)

prob = np.load('results/' + agent.name + '_prob.npy')
atime = np.load('results/' + agent.name + '_accepted_time.npy')
state_meas = np.load('results/' + agent.name + '_meas_state.npy')
nom_state = np.load('results/' + agent.name + '_hist_nom_state.npy')

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

plt.savefig('risk.svg', bbox_inches='tight', pad_inches=0.1, transparent=True)

# Define figure
plt.figure(figsize=(8, 3.5))

# Fill figure
plt.fill(*get_coordinates(RG['WS']), color=CM['WS'])
plt.fill(*get_coordinates(RG['TARGET-A']), color=CM['TARGET-A'])
plt.fill(*get_coordinates(RG['TARGET-B']), color=CM['TARGET-A'])
plt.fill(*get_coordinates(RG['HOME']), color=CM['HOME'])
plt.fill(*get_coordinates(RG['CHARGER']), color=CM['CHARGER'])
plt.fill(*get_coordinates(RG['OBSTACLE']), color=CM['OBSTACLE'])


# plot in figure
for j, t in enumerate(atime[1:]):

    plt.plot(nom_state[t, 0], nom_state[t, 1], marker='o', color=STATE_COLOR[j+1],
             linewidth=2, markersize=4, label= f'Traj. planned at time {t}')
plt.plot(state_meas[0], state_meas[1], marker='o', color=STATE_COLOR[-1],
             linewidth=2, markersize=4, label=f'Traj. based on meas.')

# Name objects in figure
plt.text((RG['TARGET-A'][0] + RG['TARGET-A'][1]) / 2, (RG['TARGET-A'][2] + RG['TARGET-A'][3]) / 2 - 0.25, 'TARGET', weight='bold', fontsize=10, horizontalalignment='center')
plt.text((RG['TARGET-B'][0] + RG['TARGET-B'][1]) / 2, (RG['TARGET-B'][2] + RG['TARGET-B'][3]) / 2 + -0.25, 'TARGET', weight='bold', fontsize=10, horizontalalignment='center')
plt.text((RG['HOME'][0]+RG['HOME'][1])/2, (RG['HOME'][2]+RG['HOME'][3])/2-0.25, 'HOME', weight='bold',  fontsize=10, horizontalalignment='center')
plt.text((RG['CHARGER'][0]+RG['CHARGER'][1])/2, (RG['CHARGER'][2]+RG['CHARGER'][3])/2-0.2, 'CHARGER', weight='bold', fontsize=10, horizontalalignment='center')
plt.text((RG['OBSTACLE'][0]+RG['OBSTACLE'][1])/2, (RG['OBSTACLE'][2]+RG['OBSTACLE'][3])/2-0.2, 'OBSTACLE', weight='bold', fontsize=10, horizontalalignment='center')

# Limit figure
plt.xlim([RG['WS'][0], RG['WS'][1]])
plt.ylim([RG['WS'][2], RG['WS'][3]])

# Label figure
plt.xlabel(r'$x_{1}$', fontsize=18)
plt.xticks(fontsize=14)
plt.ylabel(r'$x_{2}$', fontsize=18)
plt.yticks(fontsize=14)
plt.legend(loc='lower right')

# Save figure
plt.savefig('map.svg', bbox_inches='tight', pad_inches=0.1, transparent=True)

#Show figure
plt.show()

print('Exiting program')
