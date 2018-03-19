import numpy as np
from rl.policy import Policy


class EpsStochasticPolicy(Policy):
    def __init__(self, eps=.1,  tau=1., clip=(-500., 500.)):
        super(EpsStochasticPolicy, self).__init__()
        self.eps = eps
        self.tau = tau
        self.clip = clip

    def select_action(self, q_values):
        assert q_values.ndim == 1
        nb_actions = q_values.shape[0]

        uniform = np.random.uniform()
        if uniform < self.eps / 2:
            action = np.random.random_integers(0, nb_actions-1)
        elif uniform < self.eps:
            q_values = q_values.astype('float64')
            # softmax
            exp_values = np.exp(np.clip(q_values / self.tau, self.clip[0], self.clip[1]))
            probs = exp_values / np.sum(exp_values)
            action = np.random.choice(range(nb_actions), p=probs)
        else:
            action = np.argmax(q_values)
        return action

    def get_config(self):
        config = super(EpsStochasticPolicy, self).get_config()
        config['eps'] = self.eps
        return config
