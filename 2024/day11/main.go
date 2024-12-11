package main

import (
	"fmt"
	"strconv"
	"time"
)

// countDigits returns the number of digits in a number
func countDigits(n int64) int {
	if n == 0 {
		return 1
	}
	count := 0
	for n > 0 {
		count++
		n /= 10
	}
	return count
}

// splitNumber splits a number with even digits into two halves
func splitNumber(n int64, digitCount int) (int64, int64) {
	divisor := int64(1)
	for i := 0; i < digitCount/2; i++ {
		divisor *= 10
	}
	return n / divisor, n % divisor
}

// transformStone applies transformation rules to a single stone
func transformStone(stone int64) []int64 {
	// Rule 1: If stone is 0, replace with 1
	if stone == 0 {
		return []int64{1}
	}

	// Rule 2: If stone has even number of digits, split it
	digitCount := countDigits(stone)
	if digitCount%2 == 0 {
		left, right := splitNumber(stone, digitCount)
		return []int64{left, right}
	}

	// Rule 3: Multiply by 2024
	return []int64{stone * 2024}
}

// simulateBlink performs one blink transformation on all stones
func simulateBlink(stones []int64) []int64 {
	// Pre-allocate result slice with estimated capacity
	result := make([]int64, 0, len(stones)*2)

	for _, stone := range stones {
		result = append(result, transformStone(stone)...)
	}

	return result
}

// solvePlutoStones solves the puzzle for the given input and number of blinks
func solvePlutoStones(initialStones []string, blinks int) int {
	// Convert initial stones to int64
	stones := make([]int64, len(initialStones))
	for i, s := range initialStones {
		n, _ := strconv.ParseInt(s, 10, 64)
		stones[i] = n
	}

	// Simulate blinks
	for i := 0; i < blinks; i++ {
		stones = simulateBlink(stones)

		// Optional progress tracking
		if i%5 == 0 {
			fmt.Printf("Completed blink %d, current stone count: %d\n", i, len(stones))
		}
	}

	return len(stones)
}

func main() {
	// Test case
	testStones := []string{"890", "0", "1", "935698", "68001", "3441397", "7221", "27"}

	// Measure execution time
	start := time.Now()
	result := solvePlutoStones(testStones, 75)
	duration := time.Since(start)

	fmt.Printf("Test case result: %d stones\n", result)
	fmt.Printf("Execution time: %.2f ms\n", float64(duration.Microseconds())/1000)

	// Example usage for actual puzzle:
	// puzzleInput := []string{"your", "input", "here"}
	// result := solvePlutoStones(puzzleInput, 25)
	// fmt.Printf("Puzzle solution: %d stones\n", result)
}

// Optional benchmark function
func runBenchmark() {
	testCases := []struct {
		stones []string
		blinks int
	}{
		{[]string{"125", "17"}, 6},
		{[]string{"125", "17"}, 10},
		{[]string{"125", "17"}, 15},
	}

	for _, tc := range testCases {
		start := time.Now()
		result := solvePlutoStones(tc.stones, tc.blinks)
		duration := time.Since(start)
		fmt.Printf("Blinks: %d, Stones: %d, Time: %.2f ms\n",
			tc.blinks, result, float64(duration.Microseconds())/1000)
	}
}
