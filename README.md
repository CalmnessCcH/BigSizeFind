# BigSizeFind

## Installation

From source:

```
git clone https://github.com/CalmnessCcH/BigSizeFind.git
cd BigSizeFind
```

# Usage

```
Usage: BigSizeFind.py [options] arg

Options:
  -h, --help            		show this help message and exit
  -p PATH, --path=PATH  		The directory to be scanned.
  -c COMMAND, --command=COMMAND		Ncdu's path.
  -n NUM, --num=NUM     		The number of displays.
  -u UNIT, --unit=UNIT  		Size unit. MB, GB, TB
  -o OUTPUT, --output=OUTPUT		command output file path.
  -i, --ignore          		Ignore display directory.
```

# Example

```
python BigSizeFind.py /data/ -i -n 5
```
