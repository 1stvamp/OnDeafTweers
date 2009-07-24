"""Setup the OnDeafTweers_web application"""
import logging

from OnDeafTweers_web.config.environment import load_environment
from OnDeafTweers_web.model import meta

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup OnDeafTweers_web here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
