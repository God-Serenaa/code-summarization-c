from driver.driver import driver
from prettify import pretty_print

PATH_TO_DATA = "dataset/sum_sh.c"
result = driver(PATH_TO_DATA)
pretty_print(result)