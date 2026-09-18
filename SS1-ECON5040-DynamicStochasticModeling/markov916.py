import numpy as np
import matplotlib.pyplot as plt

# markov multiplicative growth model
# policy, grumpy[], happy[], psychotic[]
policy_pi = np.array([[0.1, 0.8, 0.1], [0.4, 0.4, 0.2], [0, 0.2, 0.8]])
identity_mat = np.eye(3)
beta = 0.8
# policy: [grumpy(violent), happy(nice), psychotic(violent)]
policy = np.array([10, 1, 2000])

#value function v=(I-(beta)policy_pi)^(-1)*policy
value_function = np.linalg.inv(identity_mat - beta*policy_pi) @ policy
print(value_function)