class QTable(object):
    def __init__(self):
        self.table = dict()

    def get(self, state, action):
        key = (state, action)
        return self.table.get(key, None)

    def set(self, state, action, q):
        key = (state, action)
        self.table[key] = q

class QLearning(object):
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.table = QTable()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.possible_actions = [None, 'forward', 'left', 'right']

    def getAction(self, state):
        if random.random() < self.epsilon:
            action = random.choice(self.possible_actions)
        else:
            q = [self.table.get(state, i) for i in self.possible_actions]
            max_q = max(q)

            if q.count(max_q) > 1:
                best_actions = [i for i in range(len(self.possible_actions)) if q[i] == max_q]
                action_id = random.choice(best_action)
            else:
                action_id = q.index(max_q)

            action = self.possible_actions(action_id)

        return action

    def learn(self, state, action, reward, next_state):
        next_q = [self.table.get(next_state, i) for i in self.possible_actions]
        max_next_q = max(next_q)

        if max_next_q is None:
            max_next_q = 0.0

        q = self.table.get(state, action)

        if q is None:
            q = reward
        else:
            q += self.alpha * (reward - self.gamma * max_next_q)

        self.table.set(state, action, q)
