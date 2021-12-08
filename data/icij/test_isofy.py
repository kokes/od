# from main import isofy

# errors:
# 26/06/0206, 18/19/2015, 01.004.04, 28.02/1024
# or that xx.xx.xxxx never contains anything beyond 12 in the first two fields,
# so it's impossible to tell which is which - I suspect everything beyond 12 was removed
# cannot test 04/05/09, because we can't tell which is which (d/m or m/d, both are used)

# known good values:
# 23-MAR-2006
# 06-JAN-2006
# Sep 25, 2012
# 1996

# in the end we'll test these (TODO: prep these for some future iteration)
# entities.csv
# 	incorporation_date: {'xx-JAN-xxxx', 'JAN xx, xxxx', 'xxxx-xx-xx'}
# 	inactivation_date: {'xx-JAN-xxxx'}
# 	struck_off_date: {'xx-JAN-xxxx'}
# 	dorm_date: {'xx-JAN-xxxx'}
# others.csv
# 	incorporation_date: {'xx-JAN-xxxx'}
# 	closed_date: {'xx-JAN-xxxx'}
# 	struck_off_date: {'xx-JAN-xxxx'}

# used the following code to detect these:
# months = 'jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec'.split(", ")

# def xify(v):
#     chars = list(v.lower())
#     for j, v in enumerate(chars):
#         if v >= '0' and v <= '9':
#             chars[j] = 'x'

#     stringed = ''.join(chars)
#     for month in months:
#         stringed = stringed.replace(month, 'JAN')

#     return stringed


# def patternify():
#     from glob import glob
#     import csv
#     from collections import defaultdict

#     for filename in glob("*.csv"):
#         with open(filename, "rt") as f:
#             formats = defaultdict(set)
#             cr = csv.DictReader(f)
#             for line in cr:
#                 for k, v in line.items():
#                     if not (k.endswith("_date") and v):
#                         continue
#                     formats[k].add(xify(v))
#         print(filename)
#         for k, v in formats.items():
#             print(f"\t{k}: {v}")
