"""Select the vector classroom module from the common retained calculation."""
from pathlib import Path
import runpy
import sys

if __name__ == '__main__':
    source = Path(__file__).resolve().parents[1] / 'accessibilitat-vilaseca/preparar.py'
    sys.argv += ['--module', 'xarxa']
    runpy.run_path(str(source), run_name='__main__')
