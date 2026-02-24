/**
 * 15. Valid Palindrome
 * 
 * Given a string s, return true if it is a palindrome, false otherwise.
 * A phrase is a palindrome if it reads the same forward and backward after
 * converting all uppercase letters to lowercase and removing non-alphanumeric characters.
 * 
 * @param {string} s - Input string
 * @return {boolean} True if palindrome, false otherwise
 * 
 * Time Complexity: O(n)
 * Space Complexity: O(1)
 * 
 * Example:
 *   isPalindrome("A man, a plan, a canal: Panama") => true
 *   isPalindrome("race a car") => false
 */

function isPalindrome(s) {
  // Clean the string: lowercase and remove non-alphanumeric
  const cleaned = s.toLowerCase().replace(/[^a-z0-9]/g, '');
  
  // Use two pointers
  let left = 0;
  let right = cleaned.length - 1;
  
  while (left < right) {
    if (cleaned[left] !== cleaned[right]) {
      return false;
    }
    left++;
    right--;
  }
  
  return true;
}

module.exports = isPalindrome;
