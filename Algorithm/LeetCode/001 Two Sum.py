"""
Given an array of intergers, return indices of the two numerbs such that they add up to a specific target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
 
Example:
Given nums = [2, 7, 11, 15], target = 9,
Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
"""

class Solution(object):
    def twoSum(self, nums, target):
        """t
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        length = (1 << len(nums)) - 1
        for i in range(1, length + 1) :
            print(bin(i))
        print(length)
        return nums

if __name__=="__main__":
    Solution().twoSum([3, 2, 4], 6)