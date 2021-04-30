from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pandas import DataFrame
import pandas as pd
import numpy as np
import re
import time
browse=webdriver.Firefox() #打开Chrome

# http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%E6%B6%A8%E5%81%9C&queryarea=