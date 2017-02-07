# Connor Hause - Feb 3, 2017

# I would like to add my favorite 6 numbers to consider for a Powerball entry ticket so that I can win 1 billion dollars.
# Capture the name entering the number.
# The first 5 favorite numbers will need to be in the range of 1 to 69 and unique.
# 6th favorite number will need to be in the range of 1 to 26 and flagged as the 6th Powerball number.
# Keep count of each individual favorite number provided to determine which numbers to use in our final winning number. (i.e. count the duplicates).
# Retrieve the max count of each unique duplicate number and use them as the Powerball numbers.
# If there is a tie based on the max counts randomly select the tied number.
# Display all employees with their corresponding number entries.
# Display the final Powerball number based on the requirements above.

import pickle # for saving objects
import os # for directory interaction
import random
from collections import Counter
dir = 'lottery_numbers/' # directory to save entries in

# Record entry
class powerball:
    def __init__(self):
        self.fname = raw_input('Enter your first name: ')
        self.lname = raw_input('Enter your last name: ')
        self.nums = []
        
        # Get lottery numbers
        while len(self.nums) < 5:
            excludes = [' excluding ' + ', '.join(map(str, self.nums)) if len(self.nums) != 0 else ''][0]
            num = input('Select lottery number #%i (1-69%s): ' %(len(self.nums)+1, excludes))
            
            # Check for errors
            if type(num) is int and num<70 and num>0 and num not in self.nums:
                self.nums.append(num)
            else: # Inform if error occurs
                print 'ERROR: Duplicate, out of range, or not an integer'

        # Get Powerball number
        while len(self.nums) < 6:
            num = input('Select Powerball number (1-26): ')

            # Check for errors
            if type(num) is int and num<27 and num>0:
                self.nums.append(num)
            else: # Inform if error occurs
                print 'ERROR: Out of range, or not an integer'

# Save entry
def save_entry(entry, filename):
        pickle.dump(entry, open(filename, 'w'))

# Create 'dir'/ directory if it does not exist
try: os.mkdir(dir)
except: pass

# Get entry
entry = powerball()

# Save entry
save_entry(entry, '%s%s_%s.pb' %(dir, entry.fname, entry.lname))

# Collect all saved entries file names
files = [dir+file for file in os.listdir(dir) if file.endswith('.pb')]

# Read in saved entries
entries = [pickle.load(open(files[x], 'r')) for x in range(len(files))]

# Print entries
for x in entries:
    print '%s %s: ' %(x.fname, x.lname) + ' - '.join(map(str, x.nums))

# Get array of number pick frequencies
nums = [Counter([x.nums[y] for x in entries]).most_common() for y in range(6)]

# Select final powerball numbers
for x in range(6):
    if len(nums[x]) == 1: # Uses provided value if given only a single entry
        nums[x] = nums[x][0][0]
    elif nums[x][0][1] != 1: # Random lottery number x from most common picks - works for single mode too
        nums[x] = random.choice([nums[x][y][0] for y in range(len(nums[x])) if nums[x][y][1] == nums[x][0][1]])
    elif x < 5: # Random number from 1 to 69: no ties 
        nums[x] = random.choice(range(1,70))
    else: # Random powerball number from 1 to 26: no ties 
        nums[x] = random.choice(range(1,26))

# Print the aggregate's powerball ticket     
print 'Aggregate\'s Powerball Ticket: ' + ' - '.join(map(str, nums))
