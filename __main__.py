import ac
import sys
from logging import getLogger, basicConfig, INFO

basicConfig(level=INFO)
ac.main(sys.argv[1:])
