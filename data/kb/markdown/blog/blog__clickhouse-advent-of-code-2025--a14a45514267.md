# Solving the "Impossible" in ClickHouse: Advent of Code 2025


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Solving the "Impossible" in ClickHouse: Advent of Code 2025

![](/_next/image?url=%2Fuploads%2FZach_Naimon_2f4cfc668e.jpeg&w=96&q=75)[Zach Naimon](/authors/zach-naimon)Dec 31, 2025 · 23 minutes read## Introduction [\#](/blog/clickhouse-advent-of-code-2025#introduction)


Every December, the programming community gathers for a collective ritual: [Advent of Code](https://adventofcode.com/). Created by Eric Wastl, it is an Advent calendar of small programming puzzles that releases a new challenge every day from December 1st through the 12th.


These aren't your typical "fix the bug" or "build an API" tasks. They are algorithmic challenges that require complex data structures, graph traversal, 3D geometry, cellular automata simulations, and pathfinding algorithms. Naturally, developers usually reach for general\-purpose languages like Python, Rust, Go, or C\+\+ to solve them.


### Why not SQL? [\#](/blog/clickhouse-advent-of-code-2025#why-not-sql)


Asking a database to solve these problems is generally considered a mistake. Standard SQL is a declarative language designed for retrieving and aggregating relational data, not for imperative game loops or complex state management. It lacks native support for the data structures usually required for these puzzles (like stacks, queues, or trees), and attempting to solve them with standard JOINs usually leads to performance disasters or syntax errors. In short, solving Advent of Code in SQL is widely considered "impossible" \- or at least, incredibly painful.


### The ClickHouse approach [\#](/blog/clickhouse-advent-of-code-2025#the-clickhouse-approach)


At ClickHouse, we don't like the word "impossible." We believe that with the right tools, **everything** is a data problem. ClickHouse isn't just a fast OLAP database; it is a vectorized query engine with a massive library of analytical functions that can be ~~abused~~ bent to solve general\-purpose computing problems.


To prove it, we decided to complete the 2025 Advent of Code unconventionally: using **pure ClickHouse SQL**.


### The rules [\#](/blog/clickhouse-advent-of-code-2025#the-rules)


To ensure we didn't take any shortcuts, we imposed three strict rules on our solutions:


1. **Pure ClickHouse SQL only**: we allowed absolutely no User Defined Functions (UDFs), and specifically no *executable* UDFs that would allow us to "cheat" by shelling out to Python or Bash. If the query engine couldn't do it natively, we couldn't do it.
2. **Raw inputs only**: in Advent of Code, the input is often a messy text file. Sometimes a list of numbers, sometimes an ASCII art map, or a block of cryptic instructions. We were not allowed to pre\-process this data. The solution query must accept the raw puzzle input string exactly as provided by the AoC challenge and parse it within the query.
3. **"Single query" constraint**: this is the hardest rule of all. We were not allowed to create tables, materialized views, or temporary tables to store intermediate state. The entire puzzle—from parsing the input, to solving Part 1, to solving the (often substantially more complex) Part 2—must be executed as a **single, atomic query**. This required us to rely heavily on CTEs to chain our logic together in one uninterrupted execution.


Below are the solutions for all 12 days of Advent of Code 2025, demonstrating how we turned "impossible" algorithmic challenges into pure ClickHouse SQL queries.



> Note: in order to comply with Advent of Code's distribution policy, the queries below use a wrapper `URL()` table to fetch the raw puzzle inputs without exposing them. The original query versions with handling for direct string inputs can be found in our [ClickHouse/TreeHouse](https://github.com/ClickHouse/TreeHouse) repository.


## Day 1: The Secret Entrance [\#](/blog/clickhouse-advent-of-code-2025#day-1-the-secret-entrance)


**The Puzzle**: The elves have locked their secret entrance with a rotating dial safe. The puzzle involves simulating the movement of a dial labeled 0\-99 based on a sequence of instructions like L68 (turn left 68 clicks) or R48 (turn right 48 clicks).


- **Part 1** asks for the final position of the dial after all rotations, starting from 50\.
- **Part 2** requires a more complex simulation: counting exactly how many times the dial points to 0 *during* the entire process, including intermediate clicks as it rotates past zero multiple times.


**How we solved this in ClickHouse SQL:** We treated this simulation as a stream processing problem rather than a procedural loop. Since the state of the dial depends entirely on the history of moves, we can calculate the cumulative position for every single instruction at once. We parsed the directions into positive (Right) and negative (Left) integers, then used a window function to create a running total of steps. For Part 2, where we needed to detect "zero crossings," we compared the current running total with the previous row's total to determine if the dial passed 0\.


**Implementation details:**


1. [`sum() OVER (...)`](https://clickhouse.com/docs/en/sql-reference/window-functions): We used standard SQL window functions to maintain the "running total" of the dial's position. By normalizing the left/right directions into positive/negative values, we tracked the cumulative position for every row in a single pass.



```
sum(normalized_steps) OVER (ORDER BY instruction_id) AS raw_position

```

2. [`lagInFrame`](https://clickhouse.com/docs/en/sql-reference/window-functions): To count how many times we passed zero, we needed to know where the dial started before the current rotation. We used `lagInFrame` to peek at the position from the previous row. This allowed us to compare the start and end points of a rotation and mathematically determine if 0 fell between them.


**Full Solution:**


```
1WITH
2--Fetch puzzle input
3input_wrapper AS (SELECT raw_blob AS input FROM aoc.input1),
4
5-- Parse the input string into individual instructions
6parsed_instructions AS (
7    -- Initial placeholder row
8    SELECT
9        0 AS instruction_id,
10        'R50' AS raw_instruction,
11        'R' AS direction,
12        50::Int16 AS steps
13    
14    UNION ALL
15    
16    -- Parse each line from input
17    SELECT
18        rowNumberInAllBlocks() + 1 AS instruction_id,
19        raw AS raw_instruction,
20        substring(raw, 1, 1) AS direction,
21        substring(raw, 2)::Int16 AS steps
22    FROM format(TSV, 'raw String', (SELECT input FROM input_wrapper))
23), 
24
25-- Part 1: Calculate positions with simple modulo wrapping
26part1_positions AS (
27    SELECT
28        instruction_id,
29        raw_instruction,
30        direction,
31        steps,
32        
33        -- Normalize direction: positive for R, negative for L
34        if(direction = 'R', steps % 100, -1 * (steps % 100)) AS normalized_steps,
35        
36        -- Calculate cumulative position
37        sum(normalized_steps) OVER (
38            ORDER BY instruction_id
39        ) AS raw_position,
40        
41        -- Wrap position to 0-99 range
42        ((raw_position % 100) + 100) % 100 AS position
43    FROM parsed_instructions
44),
45
46-- Part 2: Calculate positions with full movement tracking
47position_calculations AS (
48    SELECT
49        instruction_id,
50        raw_instruction,
51        direction,
52        steps,
53        
54        -- Normalize direction (no modulo yet)
55        if(direction = 'R', steps, -1 * steps) AS normalized_steps,
56        
57        -- Calculate cumulative raw position
58        sum(normalized_steps) OVER (
59            ORDER BY instruction_id ASC
60        ) AS raw_position,
61        
62        -- Wrap to 0-99 range
63        ((raw_position % 100) + 100) % 100 AS position
64    FROM parsed_instructions
65),
66
67-- Track turn counts based on position changes
68turn_tracking AS (
69    SELECT
70        *,
71        
72        -- Get previous position for comparison
73        lagInFrame(position) OVER (
74            ORDER BY instruction_id ASC 
75            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
76        ) AS previous_position,
77        
78        -- Calculate turns for this instruction
79        if(
80            instruction_id = 0,
81            0,
82            
83            -- Base turns from full rotations
84            floor(steps / 100) + 
85            
86            -- Additional turn if we wrapped around
87            if(
88                direction = 'R',
89                (position != 0 AND previous_position != 0 AND position < previous_position) ? 1 : 0,
90                (position != 0 AND previous_position != 0 AND position > previous_position) ? 1 : 0
91            )
92        ) + 
93        
94        -- Extra turn if we land exactly on position 0
95        if(instruction_id != 0 AND position = 0, 1, 0) AS turn_count
96    FROM position_calculations
97),
98
99-- Calculate cumulative turn counts
100part2_turn_counts AS (
101    SELECT
102        instruction_id,
103        raw_instruction,
104        direction,
105        steps,
106        position,
107        turn_count,
108        
109        -- Running sum of turns
110        sum(turn_count) OVER (
111            ORDER BY instruction_id ASC 
112            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
113        ) AS cumulative_turns
114    FROM turn_tracking
115)
116
117-- Final results for both parts
118SELECT 
119    'Part 1' AS part,
120    countIf(position = 0) AS solution -- Should be 1100 with my input
121FROM part1_positions
122
123UNION ALL
124
125SELECT 
126    'Part 2' AS part,
127    max(cumulative_turns)::UInt64 AS solution -- Should be 6358 with my input
128FROM part2_turn_counts;
```
[View full puzzle description](https://adventofcode.com/2025/day/1)




---


## Day 2: The Gift Shop [\#](/blog/clickhouse-advent-of-code-2025#day-2-the-gift-shop)


**The Puzzle**: You are helping clean up a gift shop database filled with invalid product IDs. The input is a list of ID ranges (e.g., 11\-22, 95\-115\).


- **Part 1** defines an invalid ID as one composed of a sequence repeated exactly twice (like 1212 or 55\).
- **Part 2** expands this to any sequence repeated *at least* twice (like 123123123 or 11111\). The goal is to sum up all invalid IDs found within the given ranges.


**How we solved this in ClickHouse SQL**: Instead of writing a loop to iterate through numbers, we leaned on ClickHouse's ability to "explode" data. We took the compact input ranges (like 11\-22\) and instantly expanded them into millions of individual rows \- one for every integer in the range. Once we had a row for every potential ID, we converted them to strings and applied array functions to check for the repeating patterns in parallel.


**Implementation details**:


1. [`arrayJoin`](https://clickhouse.com/docs/en/sql-reference/functions/array-functions#arrayjoin): This function is our staple for generating rows. We used `range(start, end)` to create an array of integers for each input line, and `arrayJoin` to explode that array into separate rows. This made filtering for invalid IDs a simple `WHERE` clause operation.



```
SELECT arrayJoin(range(bounds[1], bounds[2] + 1)) AS number

```

2. [`arrayExists`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arrayExists): For Part 2, we had to check if any substring length (from 1 up to the string length) formed a repeating pattern. We used `arrayExists` with a lambda function to check every possible substring length. If the lambda returns 1 for any length, the ID is flagged.



```
arrayExists(
    x -> (string_length % x = 0) AND (repeat(substring(..., x), ...) = number_string),
    range(1, string_length)
)

```

**Full Solution:**


```
1-- Define puzzle input
2WITH input_wrapper AS (SELECT trimRight(raw_blob,'\n') AS input FROM aoc.input2),
3
4-- Parse range bounds from input string
5range_bounds AS (
6    SELECT arrayMap(
7        x -> x::UInt64,
8        splitByChar('-', arrayJoin(splitByChar(',', (SELECT input FROM input_wrapper)::String)))
9    ) AS bounds
10),
11
12-- Expand ranges into individual numbers
13expanded_numbers AS (
14    SELECT
15        arrayJoin(range(bounds[1], bounds[2] + 1)) AS number,
16        toString(number) AS number_string,
17        length(number_string) AS string_length
18    FROM range_bounds
19),
20
21-- Analyze each number for repeating patterns
22repeating_analysis AS (
23    SELECT
24        number_string,
25        toUInt64(number_string) AS number,
26        
27        -- Part 2: Check if string is made of any repeating pattern
28        -- (e.g., "123123" = "123" repeated, "1111" = "1" repeated)
29        arrayExists(
30            x -> (string_length % x = 0)
31                AND (
32                    repeat(
33                        substring(number_string, 1, x),
34                        (string_length / x)::UInt32
35                    ) = number_string
36                ),
37            range(1, string_length)
38        ) AS has_pattern_repeat,
39        
40        -- Part 1: Check if second half equals first half
41        -- (e.g., "1212" -> "12" = "12", "123123" -> "123" = "123")
42        if(
43            string_length % 2 = 0 
44            AND substring(number_string, (string_length / 2) + 1, string_length / 2) 
45                = substring(number_string, 1, string_length / 2),
46            1,
47            0
48        ) AS has_half_repeat
49    FROM expanded_numbers
50    WHERE
51        has_pattern_repeat != 0 
52        OR has_half_repeat != 0
53    ORDER BY number ASC
54)
55
56-- Calculate final solutions
57SELECT 
58    sumIf(number, has_half_repeat = 1) AS part_1_solution, -- Should be 24043483400 with my input
59    sumIf(number, has_pattern_repeat = 1) AS part_2_solution -- Should be 38262920235 with my input
60FROM repeating_analysis
```
[View full puzzle description](https://adventofcode.com/2025/day/2)




---


## Day 3: The Lobby [\#](/blog/clickhouse-advent-of-code-2025#day-3-the-lobby)


**The Puzzle**: You need to jumpstart an escalator using banks of batteries, where each bank is a string of digits (e.g., 987654321\).


- **Part 1** asks you to pick exactly two batteries (digits) to form the largest possible 2\-digit number, preserving their original relative order.
- **Part 2** scales this up: pick exactly 12 batteries to form the largest possible 12\-digit number. This becomes a greedy optimization problem \- you always want the largest available digit that still leaves enough digits after it to complete the sequence.


**How we solved this in ClickHouse SQL**: Part 1 was a straightforward string manipulation, but Part 2 required us to maintain state while iterating through the digits. We needed to track how many digits we still needed to find and our current position in the string so we wouldn't pick digits out of order. We implemented this greedy algorithm directly in SQL using `arrayFold`, which allowed us to iterate through the digits while carrying an accumulator tuple containing our current constraints.


**Implementation details**:


1. [`arrayFold`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arrayFold): We used this higher\-order function to implement `reduce()`\-style logic. Our accumulator stored a tuple: `(digits_remaining, current_position, accumulated_value)`. For every step of the fold, we calculated the best valid digit to pick next and updated the state tuple accordingly.



```
arrayFold(
    (accumulator, current_element) -> ( ... ), -- Update logic
    digits,
    (num_digits_needed, 0, 0) -- Initial state
)

```

2. [`ngrams`](https://clickhouse.com/docs/sql-reference/functions/splitting-merging-functions#ngrams): To process the string of digits as an array, we used `ngrams(string, 1)`. While typically used for text analysis, here it served as a convenient way to split a string into an array of single characters, which we then cast to integers for the `arrayFold` operation.


**Full Solution:**


```
1-- Define puzzle input
2WITH input_wrapper AS (SELECT trimBoth(raw_blob,'\n') AS input FROM aoc.input3),
3
4-- Convert input to array of digit values for Part 2
5digit_array AS (
6    SELECT
7        arrayMap(
8            x -> toUInt8(x),
9            ngrams(arrayJoin(splitByChar('\n', (SELECT input FROM input_wrapper)::String)), 1)
10        ) AS digits,
11        length(digits) AS total_digits
12),
13
14-- Constants
1512 AS num_digits_needed,
16
17-- Part 1: Find largest two-digit number from each line
18part1_largest_pairs AS (
19    SELECT
20        ngrams(arrayJoin(splitByChar('\n', (SELECT input FROM input_wrapper)::String)), 1) AS chars,
21        arraySlice(chars, 1, length(chars) - 1) AS chars_without_last,
22        
23        -- Find first max digit, then find max digit after it
24        concat(
25            arrayMax(chars_without_last),
26            arrayMax(
27                arraySlice(
28                    chars,
29                    arrayFirstIndex(
30                        x -> x = arrayMax(chars_without_last),
31                        chars
32                    ) + 1
33                )
34            )
35        )::Int16 AS largest_two_digit
36),
37
38-- Part 2: Build largest N-digit number by greedily selecting max digits
39part2_greedy_selection AS (
40    SELECT
41        digits,
42        
43        -- Iteratively build number by selecting maximum available digit
44        arrayFold(
45            (accumulator, current_element) -> (
46                -- Decrement remaining digits counter
47                greatest(accumulator.1 - 1, 0)::Int64,
48                
49                -- Update position: find where max digit is in remaining slice
50                accumulator.2 + (
51                    arrayFirstIndex(
52                        x -> x = arrayMax(
53                            arraySlice(
54                                digits,
55                                accumulator.2 + 1,
56                                total_digits - accumulator.1 - accumulator.2 + 1
57                            )
58                        ),
59                        arraySlice(
60                            digits,
61                            accumulator.2 + 1,
62                            total_digits - accumulator.1 - accumulator.2 + 1
63                        )
64                    )
65                )::UInt64,
66                
67                -- Accumulate joltage: add max digit * 10^(remaining-1)
68                accumulator.3 + if(
69                    accumulator.1 = 0,
70                    0::UInt64,
71                    arrayMax(
72                        arraySlice(
73                            digits,
74                            accumulator.2 + 1,
75                            total_digits - accumulator.1 - accumulator.2 + 1
76                        )
77                    ) * intExp10(greatest(0, accumulator.1 - 1))
78                )
79            ),
80            digits,
81            
82            -- Initial accumulator state:
83            -- (digits_remaining, current_position, accumulated_value)
84            (num_digits_needed::Int64, 0::UInt64, 0::UInt64)
85        ).3 AS joltage  -- Extract the accumulated value (3rd element)
86    
87    FROM digit_array
88)
89
90-- Combine results from both parts
91SELECT
92    'Part 1' AS part,
93    sum(largest_two_digit)::UInt64 AS solution -- Should be 17263 with my input
94FROM part1_largest_pairs
95
96UNION ALL
97
98SELECT
99    'Part 2' AS part,
100    sum(joltage) AS solution -- Should be 170731717900423 with my input
101FROM part2_greedy_selection
```
[View full puzzle description](https://adventofcode.com/2025/day/3)




---


## Day 4: The Printing Department [\#](/blog/clickhouse-advent-of-code-2025#day-4-the-printing-department)


**The Puzzle**: The elves need to break through a wall of paper rolls. The puzzle is a variation of Conway's Game of Life. You are given a grid where `@` represents a roll of paper.


- **Part 1** defines a rule: a roll can be "accessed" (removed) if it has fewer than 4 neighbors. You count how many rolls fit this criteria initially.
- **Part 2** asks to simulate this process recursively. Removing a roll might open up access to others. You need to keep removing accessible rolls until the system stabilizes, then count the total removed.


**How we solved this in ClickHouse SQL**: Since this problem required iterative simulation where each step depended on the previous one, we used a Recursive CTE. We represented the grid as a set of (x, y) coordinates. In each recursive step, we performed a self\-join to count the neighbors for every point. We filtered the list to keep only the points that "survived" (had \>\= 4 neighbors), implicitly removing the others. We continued this recursion until the count of points stopped changing.


**Implementation details**:


1. [`WITH RECURSIVE`](https://clickhouse.com/docs/sql-reference/statements/select/with#recursive-queries): We used the standard SQL recursive CTE to handle the graph traversal. The base case selected all initial paper roll positions. The recursive step filtered that set down based on neighbor counts.



```
WITH RECURSIVE recursive_convergence AS (
    -- Base case: all points
    UNION ALL
    -- Recursive step: keep points with >= 4 neighbors
    SELECT ... HAVING countIf(...) >= 4
)

```

2. [`argMin`](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/argmin): To find the exact moment the simulation stabilized, we tracked the point count at every depth of the recursion. We used `argMin(point_count, depth)` to retrieve the count of remaining points exactly at the minimum depth where the count stopped changing.


**Full Solution:**


```
1WITH RECURSIVE 
2-- Define puzzle input (grid with '@' symbols)
3input_wrapper AS (SELECT raw_blob AS input FROM aoc.input4),
4
5-- Split input into lines
6input_lines AS (
7    SELECT splitByChar('\n', (SELECT input FROM input_wrapper)::String) AS lines
8),
9
10-- Find all '@' symbol positions in the grid
11grid_points AS (
12    SELECT arrayJoin(
13        arrayFlatten(
14            arrayMap(
15                line_tuple -> 
16                    arrayMap(
17                        x_pos -> (x_pos, line_tuple.2),
18                        arrayFilter(
19                            (pos, val) -> val = '@',
20                            arrayEnumerate(line_tuple.1),
21                            line_tuple.1
22                        )
23                    ),
24                arrayMap(
25                    (line, line_num) -> (ngrams(line, 1), line_num),
26                    lines,
27                    range(1, length(lines) + 1)
28                )
29            )
30        )::Array(Tuple(UInt8, UInt8))
31    ) AS point
32    FROM input_lines
33),
34
35-- Expand points into separate columns
36initial_points AS (
37    SELECT 
38        point.1 AS x,
39        point.2 AS y
40    FROM grid_points
41),
42
43-- Recursive CTE: Keep only points with 4+ neighbors at each iteration
44recursive_convergence AS (
45    -- Base case: all initial points at depth 1
46    SELECT
47        x,
48        y,
49        1 AS depth
50    FROM initial_points
51
52    UNION ALL
53
54    -- Recursive case: keep points with at least 4 neighbors
55    SELECT
56        p.x,
57        p.y,
58        depth + 1 AS depth
59    FROM recursive_convergence AS p
60    CROSS JOIN recursive_convergence AS q
61    WHERE depth < 256  -- Maximum recursion depth
62    GROUP BY p.x, p.y, depth
63    HAVING countIf(
64        q.x BETWEEN p.x - 1 AND p.x + 1
65        AND q.y BETWEEN p.y - 1 AND p.y + 1
66        AND NOT (p.x = q.x AND p.y = q.y)
67    ) >= 4
68),
69
70-- Track point counts at each depth level
71depth_statistics AS (
72    SELECT 
73        depth,
74        count() AS point_count,
75        lagInFrame(point_count, 1) OVER (ORDER BY depth) AS previous_count
76    FROM recursive_convergence
77    GROUP BY depth
78    ORDER BY depth
79),
80
81-- Find the depth where the count stabilizes (no more points removed)
82stabilization_analysis AS (
83    SELECT 
84        min(depth) AS stabilization_depth,
85        argMin(point_count, depth) AS stabilized_count
86    FROM depth_statistics
87    WHERE point_count = previous_count 
88        AND point_count > 0
89),
90
91-- Part 1: Points removed after first iteration (depth 2)
92part1_solution AS (
93    SELECT
94        (SELECT count() FROM initial_points) - 
95        (SELECT point_count FROM depth_statistics WHERE depth = 2 LIMIT 1) AS solution
96),
97
98-- Part 2: Points removed when convergence stabilizes
99part2_solution AS (
100    SELECT
101        (SELECT count() FROM initial_points) - stabilized_count AS solution
102    FROM stabilization_analysis
103),
104
105-- Combine results from both parts (necessary to prevent a bug with recursive CTE/external UNIONs)
106combined_solutions AS (
107SELECT
108    'Part 1' AS part,
109    solution -- Should be 1604 with my input
110FROM part1_solution
111
112UNION ALL
113
114SELECT
115    'Part 2' AS part,
116    solution -- Should be 9397 with my input
117FROM part2_solution)
118
119select * from combined_solutions settings use_query_cache=true, query_cache_share_between_users = 1, query_cache_nondeterministic_function_handling = 'save', query_cache_ttl = 80000000, result_overflow_mode = 'throw', read_overflow_mode = 'throw'
```
[View full puzzle description](https://adventofcode.com/2025/day/4)




---


## Day 5: The Cafeteria [\#](/blog/clickhouse-advent-of-code-2025#day-5-the-cafeteria)


**The Puzzle**: The elves have an inventory problem involving lists of "fresh" ID ranges (e.g., 3\-5, 10\-14\).


- **Part 1** asks how many specific item IDs fall into any of the fresh ranges.
- **Part 2** asks for the total count of unique integers covered by the fresh ranges (the union of all intervals). For example, if you have ranges 1\-5 and 3\-7, the union is 1\-7 (size 7\), not 1\-5 \+ 3\-7 (size 10\).


**How we solved this in ClickHouse SQL**: This is a classic interval intersection problem. While Part 1 was a simple filter, Part 2 required merging overlapping intervals. Merging intervals can be mathematically complex to implement manually, but we utilized a specialized ClickHouse aggregation function designed exactly for this purpose, turning a complex geometric algorithm into a one\-liner.


**Implementation details**:


1. [`intervalLengthSum`](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/intervallengthsum): We used this specialized aggregate function to calculate the total length of the union of intervals. It automatically handles overlapping and nested ranges, saving us from writing complex merging logic.



```
SELECT intervalLengthSum(range_tuple.1, range_tuple.2) AS solution

```

2. [`arrayExists`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arrayExists): For Part 1, we used arrayExists to check if a specific ID fell within *any* of the valid ranges in the array. This allowed us to perform the check efficiently without exploding the ranges into billions of individual rows.


**Full Solution:**


```
1-- Define puzzle input
2WITH input_wrapper AS (SELECT trimRight(raw_blob,'\n') AS input FROM aoc.input5),
3
4-- Split input into two sections
5input_sections AS (
6    SELECT
7        splitByString('\n\n', (SELECT input FROM input_wrapper)::String)[1] AS ranges_section,
8        splitByString('\n\n', (SELECT input FROM input_wrapper)::String)[2] AS ids_section
9),
10
11-- Parse ranges from first section (format: "min-max" per line)
12parsed_ranges AS (
13    SELECT arrayMap(
14        x -> (
15            toUInt64(splitByChar('-', x)[1]),
16            toUInt64(splitByChar('-', x)[2]) + 1 -- Make max half-open
17        ),
18        splitByChar('\n', ranges_section)
19    ) AS ranges
20    FROM input_sections
21),
22
23-- Parse IDs from second section (one ID per line)
24parsed_ids AS (
25    SELECT arrayMap(
26        x -> toUInt64(x),
27        splitByChar('\n', ids_section)
28    ) AS ids
29    FROM input_sections
30),
31
32-- Explode ranges into individual rows for Part 2 interval calculation
33exploded_ranges AS (
34    SELECT arrayJoin(ranges) AS range_tuple
35    FROM parsed_ranges
36),
37
38-- Part 1: Count how many IDs fall within any range
39part1_solution AS (
40    SELECT
41        length(
42            arrayFilter(
43                id -> arrayExists(
44                    range -> id BETWEEN range.1 AND range.2,
45                    ranges
46                ),
47                ids
48            )
49        ) AS solution
50    FROM parsed_ranges, parsed_ids
51),
52
53-- Part 2: Calculate total interval length (union of all ranges)
54part2_solution AS (
55    SELECT
56        intervalLengthSum(range_tuple.1, range_tuple.2) AS solution
57    FROM exploded_ranges
58)
59
60-- Combine results from both parts
61SELECT
62    'Part 1' AS part,
63    solution -- Should be 707 with my input
64FROM part1_solution
65
66UNION ALL
67
68SELECT
69    'Part 2' AS part,
70    solution -- Should be 361615643045059 with my input
71FROM part2_solution;
```
[View full puzzle description](https://adventofcode.com/2025/day/5)




---


## Day 6: The Trash Compactor [\#](/blog/clickhouse-advent-of-code-2025#day-6-the-trash-compactor)


**The Puzzle**: You find a math worksheet with problems arranged in columns.


- **Part 1** interprets the input as columns of numbers separated by spaces. You need to sum or multiply the numbers in each column based on the operator at the bottom.
- **Part 2** reveals the input is written "right\-to\-left" in columns, where digits of a single number are stacked vertically. You must re\-parse the grid to reconstruct the numbers, group them by blank columns, and apply the operators.


**How we solved this in ClickHouse SQL**: This puzzle was all about parsing and array manipulation. We treated the input text as a 2D matrix of characters. To switch from the row\-based text file to the column\-based math problems, we essentially performed a "matrix transposition." We converted the rows of text into arrays of characters, "rotated" them to process columns, and then used array functions to reconstruct the numbers and apply the math operations.


**Implementation details**:


1. [`splitByWhitespace`](https://clickhouse.com/docs/sql-reference/functions/splitting-merging-functions#splitByWhitespace): In Part 1, we used this function to parse the "horizontal" representation. It automatically handled the variable spacing between columns, which would have tripped up simple string splitting.
2. [`arrayProduct`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arrayProduct): Since ClickHouse lacks a standard `product()` aggregate function, we mapped our columns to arrays of integers and used `arrayProduct` to calculate the multiplication results.



```
toInt64(arrayProduct(
    arrayMap(x -> toInt64(x), arraySlice(column, 1, length(column) - 1))
))

```

3. [`arraySplit`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arraySplit): For Part 2, after extracting the raw digits, we needed to group them into valid expressions. We used `arraySplit` to break the large array into chunks whenever we encountered an operator column, effectively separating the mathematical problems.


**Full Solution:**


```
1-- Define puzzle input
2WITH input_wrapper AS (SELECT trimRight(raw_blob,'\n') AS input FROM aoc.input6),
3
4-- Part 1: Parse input into columns and apply operations
5part1_parsed_rows AS (
6    SELECT arrayMap(
7        x -> splitByWhitespace(x),
8        splitByChar('\n', (SELECT input FROM input_wrapper)::String)
9    ) AS rows
10),
11
12part1_columns AS (
13    SELECT arrayMap(
14        column_index -> arrayMap(
15            row -> row[column_index],
16            rows
17        ),
18        range(1, length(rows[1]) + 1)
19    ) AS columns
20    FROM part1_parsed_rows
21),
22
23part1_solution AS (
24    SELECT arraySum(
25        arrayMap(
26            column -> if(
27                -- Check if last element is multiplication operator
28                arrayLast(x -> 1, column) = '*',
29                
30                -- Multiply all numbers in column
31                toInt64(arrayProduct(
32                    arrayMap(
33                        x -> toInt64(x),
34                        arraySlice(column, 1, length(column) - 1)
35                    )
36                )),
37                
38                -- Otherwise, add all numbers in column
39                toInt64(arraySum(
40                    arrayMap(
41                        x -> toInt64(x),
42                        arraySlice(column, 1, length(column) - 1)
43                    )
44                ))
45            ),
46            columns
47        )
48    ) AS solution
49    FROM part1_columns
50),
51
52-- Part 2: Parse with character-level precision to handle multi-digit numbers
53part2_parsed_chars AS (
54    SELECT arrayMap(
55        x -> ngrams(x, 1),
56        splitByChar('\n', (SELECT input FROM input_wrapper)::String)
57    ) AS char_rows
58),
59
60part2_columns_raw AS (
61    SELECT arrayMap(
62        column_index -> arrayMap(
63            row -> row[column_index],
64            char_rows
65        ),
66        range(1, length(char_rows[1]) + 1)
67    ) AS columns
68    FROM part2_parsed_chars
69),
70
71part2_columns_filtered AS (
72    SELECT arrayFilter(
73        x -> NOT arrayAll(y -> y = ' ', x),
74        columns
75    ) AS non_empty_columns
76    FROM part2_columns_raw
77),
78
79part2_numbers_extracted AS (
80    SELECT arrayMap(
81        column -> replaceAll(
82            arrayStringConcat(
83                arraySlice(column, 1, length(column) - 1)
84            ),
85            ' ',
86            ''
87        ),
88        non_empty_columns
89    ) AS number_strings
90    FROM part2_columns_filtered
91),
92
93part2_numbers_grouped AS (
94    SELECT
95        number_strings,
96        non_empty_columns,
97        
98        -- Split numbers by operator positions
99        arraySplit(
100            (number_str, has_operator) -> has_operator,
101            number_strings,
102            arrayMap(
103                column -> hasAny(column, ['+', '*']),
104                non_empty_columns
105            )
106        ) AS number_groups
107    FROM part2_numbers_extracted, part2_columns_filtered
108),
109
110part2_operations AS (
111    SELECT arrayZip(
112        -- Extract operators from columns
113        arrayFilter(
114            x -> has(['+', '*'], x),
115            arrayFlatten(non_empty_columns)
116        ),
117        -- Pair with corresponding number groups
118        number_groups
119    ) AS operations_with_numbers
120    FROM part2_numbers_grouped
121),
122
123part2_solution AS (
124    SELECT arraySum(
125        arrayMap(
126            operation -> if(
127                -- Check operator type
128                operation.1 = '*',
129                
130                -- Multiply all numbers in group
131                toInt64(arrayProduct(
132                    arrayMap(
133                        x -> toInt64(x),
134                        operation.2
135                    )
136                )),
137                
138                -- Otherwise, add all numbers in group
139                toInt64(arraySum(
140                    arrayMap(
141                        x -> toInt64(x),
142                        operation.2
143                    )
144                ))
145            ),
146            operations_with_numbers
147        )
148    ) AS solution
149    FROM part2_operations
150)
151
152-- Combine results from both parts
153SELECT
154    'Part 1' AS part,
155    solution -- 5782351442566 with my input
156FROM part1_solution
157
158UNION ALL
159
160SELECT
161    'Part 2' AS part,
162    solution -- 10194584711842 with my input
163FROM part2_solution;
```
[View full puzzle description](https://adventofcode.com/2025/day/6)




---


## Day 7: The Teleporter Lab [\#](/blog/clickhouse-advent-of-code-2025#day-7-the-teleporter-lab)


**The Puzzle**: You are analyzing a tachyon beam in a grid.


- **Part 1** simulates a beam moving downwards. When it hits a splitter `^`, it splits into two beams (left and right). You count the total splits.
- **Part 2** introduces a "quantum many\-worlds" twist: instead of splitting the beam, the universe splits. You need to calculate the total number of active "timelines" (paths) at the bottom of the grid.


**How we solved this in ClickHouse SQL**: Simulating individual paths would have caused an exponential explosion. Instead, we approached this like a wave propagation simulation (similar to calculating Pascal's triangle). We processed the grid row\-by\-row using `arrayFold`. For each row, we maintained a map of "active world counts" at each column position and calculated how the counts flowed into the next row based on the splitters.


**Implementation details**:


1. [`arrayFold`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arrayFold): We used `arrayFold` to implement the row\-by\-row simulation state machine. We carried a complex state object \- `(left_boundary, right_boundary, worlds_map, part1_counter)` \- and updated it for each row of the grid.
2. [`sumMap`](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/summap): To handle beams merging (e.g., a left branch and a right branch meeting at the same spot), we used `sumMap`. This allowed us to aggregate values for identical keys in our world map, easily combining the counts of "timelines" converging on a single coordinate.



```
arrayReduce('sumMap', arrayMap(position -> map(...), ...))

```

**Full Solution:**


```
1-- Define puzzle input 
2WITH input_wrapper AS (SELECT raw_blob AS input FROM aoc.input7),
3
4-- Parse input into character grid
5parsed_grid AS (
6    SELECT arrayMap(
7        x -> ngrams(x, 1),
8        splitByChar('\n', (SELECT input FROM input_wrapper)::String)
9    ) AS rows
10),
11
12-- Find starting position in first row
13initial_state AS (
14    SELECT
15        arrayFirstIndex(x -> x = 'S', rows[1])::UInt8 AS start_position,
16        map(
17            arrayFirstIndex(x -> x = 'S', rows[1])::UInt8,
18            1::UInt64
19        )::Map(UInt8, UInt64) AS initial_worlds
20    FROM parsed_grid
21),
22
23-- Filter to only rows with '^' markers (active rows)
24active_rows AS (
25    SELECT arrayFilter(
26        x -> has(x, '^'),
27        rows
28    ) AS filtered_rows
29    FROM parsed_grid
30),
31
32-- Main iteration: propagate world counts through rows
33world_propagation AS (
34    SELECT
35        start_position,
36        initial_worlds,
37        filtered_rows,
38        
39        -- Fold through each row, updating state
40        arrayFold(
41            (accumulator, current_row) -> (
42                -- Update left boundary (shrink inward)
43                (accumulator.1 - 1)::UInt8,
44                
45                -- Update right boundary (shrink inward)
46                (accumulator.2 + 1)::UInt8,
47                
48                -- Update world map: propagate counts based on '^' positions
49                mapSort(
50                    (key, value) -> key,
51                    mapUpdate(
52                        accumulator.3,
53                        arrayReduce(
54                            'sumMap',
55                            arrayMap(
56                                position -> if(
57                                    -- Check if position has '^' and exists in current worlds
58                                    current_row[position] = '^'
59                                    AND mapContains(accumulator.3, position),
60                                    
61                                    -- Propagate world count to adjacent positions
62                                    map(
63                                        -- Left neighbor gets count (unless blocked by another '^')
64                                        (position - 1)::UInt8,
65                                        (
66                                            accumulator.3[position] + if(
67                                                current_row[greatest(0, position - 2)] = '^',
68                                                0,
69                                                accumulator.3[position - 1]
70                                            )
71                                        )::UInt64,
72                                        
73                                        -- Current position resets to 0
74                                        (position)::UInt8,
75                                        0::UInt64,
76                                        
77                                        -- Right neighbor gets count
78                                        (position + 1)::UInt8,
79                                        (accumulator.3[position + 1] + accumulator.3[position])::UInt64
80                                    ),
81                                    
82                                    -- No propagation if conditions not met
83                                    map()::Map(UInt8, UInt64)
84                                ),
85                                -- Only process positions within current boundaries
86                                arraySlice(
87                                    arrayEnumerate(current_row),
88                                    accumulator.1,
89                                    (accumulator.2 - accumulator.1) + 1
90                                )
91                            )
92                        )
93                    )
94                ),
95                
96                -- Part 1 counter: count '^' positions with non-zero worlds
97                accumulator.4 + arrayCount(
98                    position -> 
99                        current_row[position] = '^'
100                        AND mapContains(accumulator.3, position)
101                        AND accumulator.3[position] > 0,
102                    arraySlice(
103                        arrayEnumerate(current_row),
104                        accumulator.1,
105                        (accumulator.2 - accumulator.1) + 1
106                    )
107                )
108            ),
109            filtered_rows,
110            
111            -- Initial accumulator state:
112            -- (left_boundary, right_boundary, worlds_map, part1_counter)
113            (
114                start_position,
115                start_position,
116                initial_worlds,
117                0::UInt64
118            )
119        ) AS final_state
120    FROM initial_state, active_rows
121),
122
123-- Part 1: Count of '^' positions encountered with non-zero worlds
124part1_solution AS (
125    SELECT final_state.4 AS solution
126    FROM world_propagation
127),
128
129-- Part 2: Sum of all world counts across all positions
130part2_solution AS (
131    SELECT arraySum(mapValues(final_state.3)) AS solution
132    FROM world_propagation
133)
134
135-- Combine results from both parts
136SELECT
137    'Part 1' AS part,
138    solution -- 1633 with my input
139FROM part1_solution
140
141UNION ALL
142
143SELECT
144    'Part 2' AS part,
145    solution -- 34339203133559 with my input
146FROM part2_solution;
```
[View full puzzle description](https://adventofcode.com/2025/day/7)




---


## Day 8: The Playground [\#](/blog/clickhouse-advent-of-code-2025#day-8-the-playground)


**The Puzzle**: The elves are connecting 3D electrical junction boxes.


- **Part 1** asks to connect the 1000 closest pairs of points and analyze the resulting circuit sizes (connected components).
- **Part 2** asks to keep connecting the closest points until *all* boxes form a single giant circuit (a Minimum Spanning Tree problem).


**How we solved this in ClickHouse SQL**: This is a graph theory problem requiring a disjoint\-set (union\-find) approach. We generated all possible edges between points and sorted them by distance. Then, we used `arrayFold` to iterate through the edges, merging sets of points into connected components whenever an edge bridged two previously separate groups.


**Implementation details**:


1. [`L2Distance`](https://clickhouse.com/docs/sql-reference/functions/distance-functions#L2Distance): We used ClickHouse's native `L2Distance` function to efficiently calculate the Euclidean distance between 3D coordinates `[x, y, z]`, allowing us to sort the potential connections by length.
2. [`runningAccumulate`](https://clickhouse.com/docs/sql-reference/functions/other-functions#runningAccumulate): For Part 2, we needed to know when we had seen enough unique points to form a single circuit. Instead of running a slow `DISTINCT` count on every row, we used `uniqCombinedState` to create a compact sketch of unique elements, and `runningAccumulate` to merge these sketches row\-by\-row, providing a running count of unique points efficiently.



```
runningAccumulate(points_state) AS unique_points_seen

```

**Full Solution:**


```
1-- Define puzzle input 
2WITH input_wrapper AS (SELECT raw_blob AS input FROM aoc.input8),
3
4-- Parse 3D coordinate points
5parsed_points AS (
6    SELECT (x, y, z) AS point
7    FROM format('CSV', 'x UInt32, y UInt32, z UInt32', (SELECT input FROM input_wrapper)::String)
8),
9
10-- Generate all point pairs with L2 distances, sorted by distance
11point_pairs_by_distance AS (
12    SELECT
13        t1.point AS point1,
14        t2.point AS point2,
15        L2Distance(
16            [point1.1, point1.2, point1.3],
17            [point2.1, point2.2, point2.3]
18        ) AS distance
19    FROM parsed_points AS t1
20    CROSS JOIN parsed_points AS t2
21    WHERE point1 < point2
22    ORDER BY distance ASC
23),
24
25-- Take the 1000 closest pairs
26closest_pairs AS (
27    SELECT groupArray([point1, point2]) AS pairs
28    FROM (
29        SELECT point1, point2
30        FROM point_pairs_by_distance
31        ORDER BY distance ASC
32        LIMIT 1000
33    )
34),
35
36-- Part 1: Build connected components from closest pairs
37connected_components AS (
38    SELECT
39        pairs,
40        
41        -- Fold through pairs to merge into connected components
42        arrayFold(
43            (accumulator, pair) -> if(
44                -- Check if any existing components contain points from current pair
45                length(
46                    arrayFilter(
47                        component -> hasAny(component, pair),
48                        accumulator
49                    )
50                ) > 0,
51                
52                -- Merge matching components with current pair
53                arrayConcat(
54                    -- Keep non-matching components unchanged
55                    arrayFilter(
56                        component -> NOT hasAny(component, pair),
57                        accumulator
58                    ),
59                    -- Add merged component
60                    [
61                        arrayDistinct(
62                            arrayFlatten(
63                                arrayConcat(
64                                    arrayFilter(
65                                        component -> hasAny(component, pair),
66                                        accumulator
67                                    ),
68                                    [pair]
69                                )
70                            )
71                        )
72                    ]
73                ),
74                
75                -- No matches found, add pair as new component
76                arrayConcat(accumulator, [pair])
77            ),
78            pairs,
79            []::Array(Array(Tuple(UInt32, UInt32, UInt32)))
80        ) AS components
81    FROM closest_pairs
82),
83
84component_analysis AS (
85    SELECT
86        components,
87        arrayMap(x -> length(x), components) AS component_sizes
88    FROM connected_components
89),
90
91part1_solution AS (
92    SELECT arrayProduct(
93        arraySlice(
94            arrayReverseSort(component_sizes),
95            1,
96            3
97        )
98    ) AS solution
99    FROM component_analysis
100),
101
102-- Part 2: Find first pair where 1000 unique points have been seen
103point_pair_states AS (
104    SELECT
105        point1,
106        point2,
107        distance,
108        arrayReduce('uniqCombinedState', [point1, point2]) AS points_state
109    FROM point_pairs_by_distance
110),
111
112part2_solution AS (
113    SELECT
114        point1,
115        point2,
116        distance,
117        runningAccumulate(points_state) AS unique_points_seen,
118        point1.1 * point2.1 AS solution
119    FROM point_pair_states
120    WHERE unique_points_seen >= 1000
121    ORDER BY distance ASC
122    LIMIT 1
123)
124
125-- Combine results from both parts
126SELECT
127    'Part 1' AS part,
128    solution::UInt64 AS solution -- 135169 with my input
129FROM part1_solution
130
131UNION ALL
132
133SELECT
134    'Part 2' AS part,
135    solution::UInt64 AS solution -- 302133440 with my input
136FROM part2_solution
137
138SETTINGS allow_deprecated_error_prone_window_functions = 1;
```
[View full puzzle description](https://adventofcode.com/2025/day/8)




---


## Day 9: The Movie Theater [\#](/blog/clickhouse-advent-of-code-2025#day-9-the-movie-theater)


**The Puzzle**: The theater floor is a grid with some red tiles.


- **Part 1** asks for the largest area rectangle formed using two red tiles as opposite corners.
- **Part 2** adds a constraint: the rectangle must fit entirely inside the loop formed by all the red/green tiles.


**How we solved this in ClickHouse SQL**: We treated this as a geometry problem rather than a grid search. We constructed polygons representing the candidate rectangles and the boundary loop. By converting the bounding boxes into "rings," we could use ClickHouse's native geometry functions to calculate areas and check for containment.


**Implementation details**:


1. [`polygonAreaCartesian`](https://clickhouse.com/docs/sql-reference/functions/geo/polygons#polygonareacartesian): We avoided manual width/height calculations by constructing polygon objects for our rectangles and using `polygonAreaCartesian` to compute their area directly.
2. [`polygonsWithinCartesian`](https://clickhouse.com/docs/sql-reference/functions/geo/polygons#polygonswithincartesian): To check if a rectangle fit inside the loop, we used this containment function. We applied a clever trick here: because geometric functions can be tricky about points shared exactly on an edge, we constructed a slightly **inset** version of the candidate rectangle (shrunk by 0\.01 units). This ensured the containment check strictly validated that the rectangle fit *inside* the boundary polygon without edge alignment errors.



```
-- Create slightly inset test bounds (0.01 units inside)
(least(x1, x2) + 0.01, least(y1, y2) + 0.01) AS bottom_left, ...
polygonsWithinCartesian(test_bounds, all_points_ring)

```

**Full Solution:**


```
1-- Define puzzle input 
2WITH input_wrapper AS (SELECT raw_blob AS input FROM aoc.input9),
3
4-- Parse 2D coordinate points
5parsed_points AS (
6    SELECT *
7    FROM format('CSV', 'x Float64, y Float64', (SELECT input FROM input_wrapper)::String)
8),
9
10-- Generate all unique pairs of points
11point_pairs AS (
12    SELECT
13        c1.x AS x1,
14        c1.y AS y1,
15        c2.x AS x2,
16        c2.y AS y2
17    FROM parsed_points AS c1
18    CROSS JOIN parsed_points AS c2
19    WHERE (c1.x, c1.y) < (c2.x, c2.y)
20),
21
22-- Create bounding box polygons for each pair
23bounding_boxes AS (
24    SELECT
25        x1,
26        y1,
27        x2,
28        y2,
29        
30        -- Exact bounding box (corners at point coordinates)
31        [
32            (least(x1, x2), least(y1, y2)),        -- bottom-left
33            (least(x1, x2), greatest(y1, y2)),     -- top-left
34            (greatest(x1, x2), greatest(y1, y2)),  -- top-right
35            (greatest(x1, x2), least(y1, y2)),     -- bottom-right
36            (least(x1, x2), least(y1, y2))         -- close the ring
37        ]::Ring AS exact_bounds,
38        
39        -- Expanded bounding box (extends 0.5 units beyond points)
40        [
41            (least(x1, x2) - 0.5, least(y1, y2) - 0.5),        -- bottom-left
42            (least(x1, x2) - 0.5, greatest(y1, y2) + 0.5),     -- top-left
43            (greatest(x1, x2) + 0.5, greatest(y1, y2) + 0.5),  -- top-right
44            (greatest(x1, x2) + 0.5, least(y1, y2) - 0.5),     -- bottom-right
45            (least(x1, x2) - 0.5, least(y1, y2) - 0.5)         -- close the ring
46        ]::Ring AS expanded_bounds
47    FROM point_pairs
48),
49
50-- Create polygon containing all points (for Part 2 containment test)
51all_points_array AS (
52    SELECT groupArray((x, y)) AS points_array
53    FROM parsed_points
54),
55
56all_points_polygon AS (
57    SELECT arrayPushBack(points_array, points_array[1])::Ring AS ring
58    FROM all_points_array
59),
60
61-- Part 1: Find largest bounding box by area
62part1_candidates AS (
63    SELECT
64        x1,
65        y1,
66        x2,
67        y2,
68        exact_bounds,
69        expanded_bounds,
70        polygonAreaCartesian(expanded_bounds) AS area
71    FROM bounding_boxes
72    ORDER BY area DESC
73    LIMIT 1
74),
75
76part1_solution AS (
77    SELECT area AS solution
78    FROM part1_candidates
79),
80
81-- Part 2: Find largest bounding box that contains all points
82part2_candidates AS (
83    SELECT
84        bb.x1,
85        bb.y1,
86        bb.x2,
87        bb.y2,
88        
89        -- Create slightly inset test bounds (0.01 units inside)
90        (least(x1, x2) + 0.01, least(y1, y2) + 0.01) AS bottom_left,
91        (least(x1, x2) + 0.01, greatest(y1, y2) - 0.01) AS top_left,
92        (greatest(x1, x2) - 0.01, greatest(y1, y2) - 0.01) AS top_right,
93        (greatest(x1, x2) - 0.01, least(y1, y2) + 0.01) AS bottom_right,
94        
95        -- Create test bounds polygon
96        [
97            bottom_left,
98            top_left,
99            top_right,
100            bottom_right,
101            bottom_left
102        ]::Ring AS test_bounds,
103        
104        -- Check if all points are within test bounds
105        polygonsWithinCartesian(test_bounds, app.ring) AS all_points_contained,
106        
107        polygonAreaCartesian(bb.expanded_bounds) AS area
108    FROM bounding_boxes AS bb
109    CROSS JOIN all_points_polygon AS app
110    WHERE all_points_contained != 0
111    ORDER BY area DESC
112    LIMIT 1
113),
114
115part2_solution AS (
116    SELECT area AS solution
117    FROM part2_candidates
118)
119
120-- Combine results from both parts
121SELECT
122    'Part 1' AS part,
123    solution AS area -- 4739623064 with my input
124FROM part1_solution
125
126UNION ALL
127
128SELECT
129    'Part 2' AS part,
130    solution AS area -- 1654141440 with my input
131FROM part2_solution;
```
[View full puzzle description](https://adventofcode.com/2025/day/9)




---


## Day 10: The Factory [\#](/blog/clickhouse-advent-of-code-2025#day-10-the-factory)


**The Puzzle**: You need to configure factory machines by pressing buttons.


- **Part 1** involves toggling lights (XOR logic) to match a pattern.
- **Part 2** involves incrementing "joltage" counters to reach large target integers using the fewest button presses.


**How we solved this in ClickHouse SQL**: For Part 1, the search space was small enough that we could use brute\-force enumeration. We generated every possible button combination and checked it using bitmasks. Part 2 required a smarter approach. We implemented a custom recursive halving algorithm in SQL. We iteratively subtracted button effects and "halved" the remaining target values, reducing the large target numbers down to zero step\-by\-step.


**Implementation details**:


1. [`bitTest`](https://clickhouse.com/docs/sql-reference/functions/bit-functions#bitTest) and [`bitCount`](https://clickhouse.com/docs/sql-reference/functions/bit-functions#bitCount): We treated button combinations as binary integers. `bitTest` allowed us to check if a specific button was pressed in a combination, and `bitCount` gave us the total number of presses (the cost).
2. [`ARRAY JOIN`](https://clickhouse.com/docs/en/sql-reference/statements/select/array-join): To generate the search space for Part 1, we created a range of integers (0 to 2^N) and used `ARRAY JOIN` to explode them into rows. This created a row for every possible permutation of button presses.



```
ARRAY JOIN range(0, toUInt32(pow(2, num_buttons)))

```

**Full Solution:**


```
1WITH RECURSIVE
2-- Define puzzle input 
3    input_wrapper AS (SELECT raw_blob AS input FROM aoc.input10),
4
5-- Parse raw input into structured format
6raw_split AS (
7    SELECT
8        row_number() OVER () AS puzzle_id,
9        splitByChar(' ', raw) AS components
10    FROM format('TSVRaw', 'raw String', (SELECT input FROM input_wrapper)::String)
11),
12
13parsed_puzzles AS (
14    SELECT
15        puzzle_id,
16        
17        -- Parse diagram: '#' becomes 1, '.' becomes 0
18        arrayMap(
19            x -> if(x = '#', 1, 0),
20            ngrams(replaceRegexpAll(components[1], '[\\[\\]]', ''), 1)
21        ) AS target_diagram,
22        
23        -- Parse buttons: each button affects specific positions
24        arrayMap(
25            button_str -> arrayMap(
26                pos_str -> (toUInt16(pos_str) + 1),
27                splitByChar(',', replaceRegexpAll(button_str, '[\\(\\)]', ''))
28            ),
29            arraySlice(components, 2, length(components) - 2)
30        ) AS button_effects,
31        
32        -- Parse joltages: target values for Part 2
33        arrayMap(
34            x -> toUInt32(x),
35            splitByChar(',', replaceRegexpAll(components[-1], '[\\{\\}]', ''))
36        ) AS target_joltages
37    FROM raw_split
38),
39
40puzzle_metadata AS (
41    SELECT
42        puzzle_id,
43        target_diagram,
44        button_effects,
45        target_joltages,
46        length(button_effects) AS num_buttons,
47        length(target_joltages) AS num_positions
48    FROM parsed_puzzles
49),
50
51-- PART 1: Brute force - enumerate all button combinations
52part1_button_combinations AS (
53    SELECT
54        p.puzzle_id,
55        p.target_diagram,
56        p.button_effects,
57        p.num_buttons,
58        p.num_positions,
59        combination_id,
60        toUInt32(bitCount(combination_id)) AS button_presses,
61        
62        -- Calculate resulting diagram from this combination
63        arrayMap(
64            position -> toUInt8(
65                modulo(
66                    arrayReduce(
67                        'sum',
68                        arrayMap(
69                            button_index -> if(
70                                bitTest(combination_id, button_index)
71                                AND has(button_effects[button_index + 1], position),
72                                1,
73                                0
74                            ),
75                            range(0, num_buttons)
76                        )
77                    ),
78                    2
79                )
80            ),
81            range(1, num_positions + 1)
82        ) AS resulting_diagram
83    FROM puzzle_metadata p
84    ARRAY JOIN range(0, toUInt32(pow(2, num_buttons))) AS combination_id
85),
86
87part1_minimum_solutions AS (
88    SELECT
89        puzzle_id,
90        min(button_presses) AS minimum_presses
91    FROM part1_button_combinations
92    WHERE target_diagram = resulting_diagram
93    GROUP BY puzzle_id
94),
95
96-- PART 2: Pre-compute button combination patterns for recursive algorithm
97button_combination_patterns AS (
98    SELECT
99        p.puzzle_id,
100        p.button_effects,
101        p.num_buttons,
102        p.num_positions,
103        combination_id,
104        toUInt32(bitCount(combination_id)) AS pattern_cost,
105        
106        -- Pattern: numeric effect on each position
107        arrayMap(
108            position -> toUInt32(
109                arrayReduce(
110                    'sum',
111                    arrayMap(
112                        button_index -> if(
113                            bitTest(combination_id, button_index)
114                            AND has(button_effects[button_index + 1], position),
115                            1,
116                            0
117                        ),
118                        range(0, num_buttons)
119                    )
120                )
121            ),
122            range(1, num_positions + 1)
123        ) AS effect_pattern,
124        
125        -- Parity pattern: XOR constraint (mod 2)
126        arrayMap(
127            position -> toUInt8(
128                modulo(
129                    arrayReduce(
130                        'sum',
131                        arrayMap(
132                            button_index -> if(
133                                bitTest(combination_id, button_index)
134                                AND has(button_effects[button_index + 1], position),
135                                1,
136                                0
137                            ),
138                            range(0, num_buttons)
139                        )
140                    ),
141                    2
142                )
143            ),
144            range(1, num_positions + 1)
145        ) AS parity_pattern
146    FROM puzzle_metadata p
147    ARRAY JOIN range(0, toUInt32(pow(2, num_buttons))) AS combination_id
148),
149
150-- Group patterns by parity for efficient lookup
151patterns_grouped_by_parity AS (
152    SELECT
153        puzzle_id,
154        button_effects,
155        num_buttons,
156        num_positions,
157        parity_pattern,
158        groupArray(tuple(effect_pattern, pattern_cost)) AS available_patterns
159    FROM button_combination_patterns
160    GROUP BY puzzle_id, button_effects, num_buttons, num_positions, parity_pattern
161),
162
163-- Recursive halving algorithm: iteratively reduce joltages to zero
164recursive_halving_solver AS (
165    -- Base case: start with target joltages
166    SELECT
167        puzzle_id,
168        button_effects,
169        num_buttons,
170        num_positions,
171        target_joltages AS current_goal,
172        toUInt64(0) AS accumulated_cost,
173        0 AS recursion_depth
174    FROM puzzle_metadata
175    
176    UNION ALL
177    
178    -- Recursive case: apply pattern, subtract, halve, and continue
179    SELECT
180        puzzle_id,
181        button_effects,
182        num_buttons,
183        num_positions,
184        current_goal,
185        min(accumulated_cost) AS accumulated_cost,
186        min(recursion_depth) AS recursion_depth
187    FROM (
188        SELECT
189            solver.puzzle_id,
190            solver.button_effects,
191            solver.num_buttons,
192            solver.num_positions,
193            
194            -- New goal: (current - pattern) / 2
195            arrayMap(
196                i -> intDiv(
197                    solver.current_goal[i] - pattern_tuple.1[i],
198                    2
199                ),
200                range(1, solver.num_positions + 1)
201            ) AS current_goal,
202            
203            -- Accumulate cost: pattern_cost * 2^depth
204            solver.accumulated_cost + 
205                toUInt64(pattern_tuple.2) * toUInt64(pow(2, solver.recursion_depth)) AS accumulated_cost,
206            
207            solver.recursion_depth + 1 AS recursion_depth
208        FROM recursive_halving_solver solver
209        INNER JOIN patterns_grouped_by_parity patterns
210            ON patterns.puzzle_id = solver.puzzle_id
211            AND patterns.parity_pattern = arrayMap(
212                x -> if(x % 2 = 0, toUInt8(0), toUInt8(1)),
213                solver.current_goal
214            )
215        ARRAY JOIN patterns.available_patterns AS pattern_tuple
216        WHERE
217            solver.recursion_depth < 100
218            AND NOT arrayAll(x -> x = 0, solver.current_goal)
219            -- Ensure pattern doesn't overshoot (feasibility constraint)
220            AND arrayAll(
221                i -> pattern_tuple.1[i] <= solver.current_goal[i],
222                range(1, solver.num_positions + 1)
223            )
224    )
225    GROUP BY puzzle_id, button_effects, num_buttons, num_positions, current_goal
226),
227
228part2_minimum_solutions AS (
229    SELECT
230        puzzle_id,
231        min(accumulated_cost) AS minimum_cost
232    FROM recursive_halving_solver
233    WHERE arrayAll(x -> x = 0, current_goal)
234    GROUP BY puzzle_id
235),
236
237-- Aggregate final solutions
238combined_solutions AS (
239    SELECT 'Part 1' AS part, sum(minimum_presses) AS solution -- 527 with my input
240    FROM part1_minimum_solutions
241    
242    UNION ALL
243
244    SELECT 'Part 2' AS part, sum(minimum_cost) AS solution -- 19810 with my input
245    FROM part2_minimum_solutions
246)
247
248-- Combine results from both parts
249SELECT * FROM combined_solutions settings use_query_cache=true, query_cache_share_between_users = 1, query_cache_nondeterministic_function_handling = 'save', query_cache_ttl = 80000000, result_overflow_mode = 'throw', read_overflow_mode = 'throw';
```
[View full puzzle description](https://adventofcode.com/2025/day/10)




---


## Day 11: The Reactor [\#](/blog/clickhouse-advent-of-code-2025#day-11-the-reactor)


**The Puzzle**: You are debugging a reactor control graph.


- **Part 1** asks to count all distinct paths from `you` to `out`.
- **Part 2** asks to count paths from `svr` to `out` that satisfy a constraint: they must visit both intermediate nodes `dac` and `fft`.


**How we solved this in ClickHouse SQL**: We solved this using a Recursive CTE to traverse the graph. To handle the constraint in Part 2, we carried "visited flags" in our recursion state. As we traversed the graph, we updated these boolean flags whenever we hit a checkpoint node. At the end, we simply filtered for paths where both flags were true.


**Implementation details**:


1. [`cityHash64`](https://clickhouse.com/docs/sql-reference/functions/hash-functions#cityHash64): String comparisons can be slow in large recursive joins. We converted the node names (like `svr`, `dac`) into deterministic 64\-bit integers using `cityHash64`. This made the join operations significantly faster and reduced memory usage.



```
cityHash64('svr') AS svr_node

```

2. **State Tracking**: We added boolean columns to our recursive table to track state. This allowed us to solve the "must visit X and Y" constraint in a single pass without needing complex post\-processing.



```
paths.visited_dac OR (edges.to_node = kn.dac_node) AS visited_dac

```

**Full Solution:**


```
1WITH RECURSIVE
2-- Define puzzle input 
3input_wrapper AS (SELECT raw_blob AS input FROM aoc.input11),
4
5-- Define key node identifiers
6key_nodes AS (
7    SELECT
8        cityHash64('svr') AS svr_node,
9        cityHash64('you') AS you_node,
10        cityHash64('dac') AS dac_node,
11        cityHash64('fft') AS fft_node,
12        cityHash64('out') AS out_node
13),
14
15-- Parse input connections
16raw_connections AS (
17    SELECT splitByString(': ', raw) AS parsed_parts
18    FROM format('TSV', 'raw String', (SELECT input FROM input_wrapper)::String)
19),
20
21parsed_connections AS (
22    SELECT
23        parsed_parts[1] AS input_node,
24        splitByWhitespace(parsed_parts[2]) AS output_nodes
25    FROM raw_connections
26),
27
28-- Create graph edges with hashed node IDs
29graph_edges AS (
30    SELECT
31        cityHash64(input_node) AS from_node,
32        cityHash64(arrayJoin(output_nodes)) AS to_node
33    FROM parsed_connections
34),
35
36-- Part 2: Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'
37paths_from_svr AS (
38    -- Base case: start at 'svr' node
39    SELECT
40        0 AS generation,
41        svr_node AS current_node,
42        0::UInt8 AS visited_dac,
43        0::UInt8 AS visited_fft,
44        1::UInt64 AS paths_count
45    FROM key_nodes
46    
47    UNION ALL
48    
49    -- Recursive case: traverse edges and track checkpoint visits
50    SELECT
51        generation,
52        current_node,
53        visited_dac,
54        visited_fft,
55        sum(paths_count) AS paths_count
56    FROM (
57        SELECT
58            paths.generation + 1 AS generation,
59            edges.to_node AS current_node,
60            paths.visited_dac OR (edges.to_node = kn.dac_node) AS visited_dac,
61            paths.visited_fft OR (edges.to_node = kn.fft_node) AS visited_fft,
62            paths.paths_count AS paths_count
63        FROM paths_from_svr paths
64        JOIN graph_edges edges ON edges.from_node = paths.current_node
65        CROSS JOIN key_nodes kn
66        WHERE
67            edges.to_node != kn.out_node
68            AND paths.generation < 628
69    )
70    GROUP BY generation, current_node, visited_dac, visited_fft
71),
72
73-- Part 1: Count all paths from 'you' to 'out'
74paths_from_you AS (
75    -- Base case: start at 'you' node
76    SELECT
77        0 AS generation,
78        you_node AS current_node,
79        1::UInt64 AS paths_count
80    FROM key_nodes
81    
82    UNION ALL
83    
84    -- Recursive case: traverse edges
85    SELECT
86        generation,
87        current_node,
88        sum(paths_count) AS paths_count
89    FROM (
90        SELECT
91            paths.generation + 1 AS generation,
92            edges.to_node AS current_node,
93            paths.paths_count AS paths_count
94        FROM paths_from_you paths
95        JOIN graph_edges edges ON edges.from_node = paths.current_node
96        CROSS JOIN key_nodes kn
97        WHERE
98            edges.to_node != kn.out_node
99            AND paths.generation < 628
100    )
101    GROUP BY generation, current_node
102),
103
104-- Part 1 solution: paths from 'you' to 'out'
105part1_solution AS (
106    SELECT sum(paths.paths_count) AS solution
107    FROM paths_from_you paths
108    JOIN graph_edges edges ON edges.from_node = paths.current_node
109    CROSS JOIN key_nodes kn
110    WHERE edges.to_node = kn.out_node
111),
112
113-- Part 2 solution: paths from 'svr' to 'out' visiting both checkpoints
114part2_solution AS (
115    SELECT sum(paths.paths_count) AS solution
116    FROM paths_from_svr paths
117    JOIN graph_edges edges ON edges.from_node = paths.current_node
118    CROSS JOIN key_nodes kn
119    WHERE
120        edges.to_node = kn.out_node
121        AND paths.visited_dac = 1
122        AND paths.visited_fft = 1
123),
124
125solutions_combined as (
126SELECT 
127    'Part 1' AS part,
128    (SELECT solution FROM part1_solution) AS solution -- 724 with my input
129
130UNION ALL
131
132SELECT 
133    'Part 2' AS part,
134    (SELECT solution FROM part2_solution) AS solution -- 473930047491888 with my input
135)
136
137SELECT * FROM solutions_combined;
```
[View full puzzle description](https://adventofcode.com/2025/day/11)




---


## Day 12: Christmas Tree Farm [\#](/blog/clickhouse-advent-of-code-2025#day-12-christmas-tree-farm)


**The Puzzle**: Elves need to pack irregular presents (defined by `#` grids) into rectangular regions. This looks like a complex 2D bin\-packing problem. However, the puzzle input allows for a heuristic shortcut: checking if the *total area* of the presents is less than or equal to the *total area* of the region is sufficient.


**How we solved this in ClickHouse SQL**: Since we could solve this with a volume check, our solution focused on parsing. We converted the ASCII art shapes into binary grids (arrays of 1s and 0s) and calculated the area (count of 1s) for each. We then multiplied the requested quantity of each present by its area and compared the sum to the region's total size.


**Implementation details**:


1. [`replaceRegexpAll`](https://clickhouse.com/docs/sql-reference/functions/string-replace-functions#replaceRegexpAll): We used regex replacement to turn the visual `#` characters into `1` and `.` into `0`. This transformed the "art" into computable binary strings that we could parse into arrays.
2. [`arraySum`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arraySum): We used the lambda version of `arraySum` to perform a "dot product" operation. We multiplied the volume of each present by its area and summed the results in a single, clean expression.



```
arraySum(
    (volume, area) -> volume * area,
    requested_shape_volumes,
    areas_per_shape
)

```

**Full Solution:**


```
1-- Define puzzle input 
2WITH input_wrapper AS (SELECT trimRight(raw_blob,'\n') AS input FROM aoc.input12),
3
4-- Split input into sections
5input_sections AS (
6    SELECT arrayMap(
7        section -> splitByChar('\n', section),
8        splitByString('\n\n', (SELECT input FROM input_wrapper)::String)
9    ) AS sections
10),
11
12-- Extract regions section (last section)
13regions_section AS (
14    SELECT sections[-1] AS region_lines
15    FROM input_sections
16),
17
18-- Extract shape sections (all except last)
19shapes_sections AS (
20    SELECT arrayJoin(
21        arraySlice(sections, 1, length(sections) - 1)
22    ) AS shape_lines
23    FROM input_sections
24),
25
26-- Parse shape data
27parsed_shapes AS (
28    SELECT
29        shape_lines,
30        
31        -- Transform shape lines: first line is name, rest is pattern
32        arrayMap(
33            line_index -> if(
34                line_index = 1,
35                -- First line: remove ':' from name
36                replaceAll(shape_lines[line_index], ':', ''),
37                -- Other lines: convert '#' to 1, '.' to 0
38                replaceRegexpAll(
39                    replaceRegexpAll(shape_lines[line_index], '#', '1'),
40                    '\\.',
41                    '0'
42                )
43            ),
44            arrayEnumerate(shape_lines)
45        ) AS transformed_lines
46    FROM shapes_sections
47),
48
49-- Convert shape patterns to binary arrays
50shape_patterns AS (
51    SELECT
52        transformed_lines,
53        arrayMap(
54            line -> arrayMap(
55                char -> toUInt8(char),
56                ngrams(line, 1)
57            ),
58            arraySlice(transformed_lines, 2)
59        ) AS shape_grid
60    FROM parsed_shapes
61),
62
63-- Calculate area needed for each shape
64shape_areas AS (
65    SELECT groupArray(
66        arrayCount(
67            cell -> cell = 1,
68            arrayFlatten(shape_grid)
69        )
70    ) AS areas_per_shape
71    FROM shape_patterns
72),
73
74-- Parse region specifications
75parsed_regions AS (
76    SELECT
77        arrayJoin(
78            arrayMap(
79                line -> splitByString(': ', line),
80                region_lines
81            )
82        ) AS region_parts
83    FROM regions_section
84),
85
86-- Calculate region dimensions and requested volumes
87region_specifications AS (
88    SELECT
89        region_parts,
90        
91        -- Calculate total region area (product of dimensions)
92        arrayProduct(
93            arrayMap(
94                dim -> toUInt32(dim),
95                splitByChar('x', region_parts[1])
96            )
97        ) AS total_region_area,
98        
99        -- Extract requested volumes for each shape
100        arrayMap(
101            vol -> toUInt8(vol),
102            splitByChar(' ', region_parts[2])
103        ) AS requested_shape_volumes
104    FROM parsed_regions
105),
106
107-- Check if each region can fit the requested shapes
108region_fit_analysis AS (
109    SELECT
110        total_region_area,
111        requested_shape_volumes,
112        areas_per_shape,
113        
114        -- Calculate total area needed: sum of (volume * area) for each shape
115        arraySum(
116            (volume, area) -> volume * area,
117            requested_shape_volumes,
118            areas_per_shape
119        ) AS total_area_needed,
120        
121        -- Check if shapes fit in region
122        total_area_needed <= total_region_area AS shapes_fit
123    FROM region_specifications
124    CROSS JOIN shape_areas
125),
126
127-- Count regions where shapes fit
128solution AS (
129    SELECT countIf(shapes_fit) AS solution
130    FROM region_fit_analysis
131)
132
133-- Return final answer
134SELECT solution -- 463 with my input
135FROM solution
```
[View full puzzle description](https://adventofcode.com/2025/day/12)




---


## Conclusion [\#](/blog/clickhouse-advent-of-code-2025#conclusion)


The fact that we successfully solved all 12 of these puzzles using pure ClickHouse SQL demonstrates just how versatile our query engine truly is. This is all made possible because ClickHouse includes a massive standard library of built\-in functions that bridge the gap between SQL and general\-purpose programming. Throughout this challenge, we utilized over a dozen different [String Functions](https://clickhouse.com/docs/en/sql-reference/functions/string-functions) alongside the [format](https://clickhouse.com/docs/en/sql-reference/table-functions/format) table function to manipulate messy inputs into workable datasets. We relied heavily on [Array Functions](https://clickhouse.com/docs/en/sql-reference/functions/array-functions) like [`arrayMap`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arrayMap) and [`arrayProduct`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arrayProduct), but the real heroes were [`arrayReduce`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arrayReduce) and [`arrayFold`](https://clickhouse.com/docs/sql-reference/functions/array-functions#arrayFold), which allowed us to implement complex functional programming logic and maintain state across iterations. When combined with native [Recursive CTEs](https://clickhouse.com/docs/en/sql-reference/statements/select/with#recursive-cte) for pathfinding, [Distance Functions](https://clickhouse.com/docs/en/sql-reference/functions/distance-functions) for 3D geometry, [Polygon Functions](https://clickhouse.com/docs/sql-reference/functions/geo/polygons) for spatial analysis, and [Bitwise Operations](https://clickhouse.com/docs/en/sql-reference/functions/bit-functions) for logic gates, ClickHouse behaves less like a database and more like a high\-performance vector computation engine.


Due to our self\-imposed constraints, these SQL solutions may not be as computationally optimal as implementations written in "real" programming languages like Rust or Python, but they nevertheless yield the exact same results. This experiment proves that when you have the right tools, problems that seem "impossible" in SQL become just another interesting data challenge for ClickHouse. You can view the full set of solution queries in our [ClickHouse/TreeHouse](https://github.com/ClickHouse/TreeHouse) repository.



> Note: Thomas Neumann completed all Advent of Code puzzles in 2024 using Umbra DB. His work can be found [here.](https://github.com/neumannt/aoc24)

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
