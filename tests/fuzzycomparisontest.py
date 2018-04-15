from fuzzywuzzy import fuzz
from fuzzywuzzy import process

str1 = "r2 r2d2 where are you"
str2 = "r2d2 where are you"

print(str(fuzz.ratio(str1, str2)))