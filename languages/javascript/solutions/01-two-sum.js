/**
 * 01. Two Sum
 * 
 * Given an array of integers nums and an integer target,
 * return indices of the two numbers such that they add up to target.
 * 
 * @param {number[]} nums - Array of integers
 * @param {number} target - Target sum
 * @return {number[]} Indices of the two numbers
 * 
 * Time Complexity: O(n)
 * Space Complexity: O(n)
 * 
 * Example:
 *   twoSum([2, 7, 11, 15], 9) => [0, 1]
 *   twoSum([3, 2, 4], 6) => [1, 2]
 */

function twoSum(nums, target) {
  // Use a hash map to store seen numbers and their indices
  const seen = new Map();
  
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];
    
    // Check if complement exists in our map
    if (seen.has(complement)) {
      return [seen.get(complement), i];
    }
    
    // Store current number and its index
    seen.set(nums[i], i);
  }
  
  // No solution found
  return [];
}

module.exports = twoSum;
