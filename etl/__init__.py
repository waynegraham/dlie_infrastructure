# This file makes 'etl' a Python package and exposes its submodules.

# Import submodules so that attributes exist on the package
from . import etl_tasks, celeryconfig

__all__ = ['etl_tasks', 'celeryconfig']
