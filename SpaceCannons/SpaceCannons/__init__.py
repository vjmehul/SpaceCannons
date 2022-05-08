import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='SpaceCannons-v2',
    entry_point='SpaceCannons.envs:SpaceCannons',
)
