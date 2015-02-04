import re

"""
This constant is a regural expression format for a summation
"""
PROBLEM_FORMAT = re.compile(r'^\d+\+\d+(\+\d+)*$')

def carry(nums):
    """
    Compute the numbers carried during the operation
    and return them as a reversed list to set up the order properly

    nums: a list of numbers
    """
    #See get_long_len(nums) doc string for info on this
    long_len = get_long_len(nums)
    #See format_nums(nums, sep) doc string for info on this
    str_nums = format_nums(nums, "0")
    #Used to keep track of the current carried number
    carry_num = 0
    #All the carried numbers used during the operation
    carry_list = []
    #Start from the ones digit of all numbers and move up each time, stopping
    #at the second to last digit
    for i in range(long_len-1, 0, -1):
        #The sum for the current digit starts at the previous
        #carried number
        digit_sum = carry_num
        #Reset the carried number for the beginning of the summation
        #for this digit
        carry_num = 0
        #Add all numbers in the current digit location
        digit_sum += sum([int(num[i]) for num in str_nums])
        #Find the number to be carried over by dividing by 10
        carry_num = digit_sum / 10
        #Append that number to the list of carried numbers
        carry_list.append(carry_num)

    #Return a copy of the list reversed
    return reversed(carry_list)

def format_nums(nums, sep):
    """
    Format numbers so that there is appropriate spacing for
    readability. Returns the numbers as a list of strings.

    nums: a list of numbers
    sep: a string used to fill up space for missing digit places
    """
    #See get_long_len(nums) doc string for info on this
    long_len = get_long_len(nums)
    str_nums = map(str, nums)
    for i in range(0, len(str_nums)):
        #Temporary variable to save line space
        num = str_nums[i]
        #Add the separater to the beginning of the number string
        #for each digit space missing from the longest number string
        if len(num) < long_len:
            str_nums[i] = "".join ([sep * (long_len - len(num)), num])
    
    return str_nums
    
def get_long_len(nums):
    """
    Finds the length of the longest lengthed number (either the operands
    or the sum) and returns it.

    nums: a list of numbers
    """
    return len(str(max(nums + [sum(nums)])))

def print_divider(nums):
    """
    Prints the divider.

    nums: a list of numbers
    """
    print "--" * get_long_len(nums)

def print_carry(nums):
    """
    Prints a summation equation along with its carried numbers

    nums: a list of numbers
    """
    #See format_nums(nums, sep) doc string for info on this
    str_nums = format_nums(nums, " ")
    #Obtain the carried numbers
    carry_list = carry(nums)
    for num in str_nums:
        print num
        
    print_divider(nums)
    
    print sum(nums)
    print_divider(nums)

    #Print the carried numbers. Use spaces in place of 0s
    carry_str = ""
    for num in carry_list:
        if num == 0:
            carry_str += " "
        elif num > 9:
            carry_str += "A"
        else:
            carry_str += str(num)
    
    print carry_str

def main():
    while True:
        in_put = raw_input("Enter a sum equation (or Q to quit): ")
        if in_put.upper() == 'Q':
            break
        elif PROBLEM_FORMAT.match(in_put):
            print_carry(map(int, in_put.split('+')))
        else:
            print "Invalid input!"
    
if __name__ == "__main__":
    main()
