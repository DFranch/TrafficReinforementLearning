from gym.envs.registration import register

register(
    id='Ai-v0',
    entry_point='env.env:TrafficEnv',
)
