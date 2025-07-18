#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides a standardized logging setup for the Git Tools project.
"""

import logging
import sys

def setup_logging() -> None:
    """
    Configures the root logger for the application.

    Sets the logging level to INFO and directs output to the console
    with a simple, clean format.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s',
        stream=sys.stdout,
    )
