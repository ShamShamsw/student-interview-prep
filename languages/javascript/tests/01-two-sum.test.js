const twoSum = require('../solutions/01-two-sum');

describe('Problem 01: Two Sum', () => {
  test('should return correct indices for basic case', () => {
    expect(twoSum([2, 7, 11, 15], 9)).toEqual([0, 1]);
  });

  test('should handle middle elements', () => {
    expect(twoSum([3, 2, 4], 6)).toEqual([1, 2]);
  });

  test('should handle negative numbers', () => {
    expect(twoSum([-1, -2, -3, -4, -5], -8)).toEqual([2, 4]);
  });

  test('should handle duplicate values', () => {
    expect(twoSum([3, 3], 6)).toEqual([0, 1]);
  });

  test('should handle large numbers', () => {
    expect(twoSum([1000000, 999999, 1], 1000001)).toEqual([0, 2]);
  });

  test('should return empty array when no solution', () => {
    expect(twoSum([1, 2, 3], 10)).toEqual([]);
  });

  test('should handle single element array', () => {
    expect(twoSum([5], 5)).toEqual([]);
  });
});
