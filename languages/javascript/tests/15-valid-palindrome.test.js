const isPalindrome = require('../solutions/15-valid-palindrome');

describe('Problem 15: Valid Palindrome', () => {
  test('should return true for classic palindrome', () => {
    expect(isPalindrome('A man, a plan, a canal: Panama')).toBe(true);
  });

  test('should return false for non-palindrome', () => {
    expect(isPalindrome('race a car')).toBe(false);
  });

  test('should handle single character', () => {
    expect(isPalindrome('a')).toBe(true);
  });

  test('should handle empty string', () => {
    expect(isPalindrome('')).toBe(true);
  });

  test('should handle spaces only', () => {
    expect(isPalindrome(' ')).toBe(true);
  });

  test('should handle mixed case', () => {
    expect(isPalindrome('RaceCar')).toBe(true);
  });

  test('should handle numbers', () => {
    expect(isPalindrome('12321')).toBe(true);
  });

  test('should ignore special characters', () => {
    expect(isPalindrome('A@b!b@A')).toBe(true);
  });
});
