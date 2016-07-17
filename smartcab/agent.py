import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from q import QLearning

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env, alpha, gamma, epsilon):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.qLearning = QLearning(alpha, gamma, epsilon)

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (inputs['light'], inputs['oncoming'],
            inputs['left'], self.next_waypoint)

        # TODO: Select action according to your policy
        action = self.qLearning.act(self.state)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        next_inputs = self.env.sense(self)
        next_state = (next_inputs['light'], next_inputs['oncoming'],
            next_inputs['left'], self.next_waypoint)

        self.qLearning.learn(self.state, action, reward, next_state)

        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

def run():
    """Run the agent for a finite number of trials."""

    alpha = [0.05, 0.1, 0.15, 0.2]
    gamma = [0.6, 0.7, 0.8, 0.9]
    epsilon = [0.05, 0.1, 0.15, 0.2]

    for i in alpha:
        for j in gamma:
            for k in epsilon:
                # Set up environment and agent
                e = Environment()  # create environment (also adds some dummy traffic)
                a = e.create_agent(LearningAgent, i, j, k)  # create agent
                e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
                # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

                # Now simulate it
                sim = Simulator(e, update_delay=0.000000001, display=False)  # create simulator (uses pygame when display=True, if available)
                # NOTE: To speed up simulation, reduce update_delay and/or set display=False

                sim.run(n_trials=100)  # run for a specified number of trials
                # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

                print i, j, k, e.successes / 100.0, e.net_reward

if __name__ == '__main__':
    run()
