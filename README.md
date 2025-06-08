
# Part 1 
A cube is painted orange on all six sides. It is divided into 125 (=5 x 5 x 5) equal smaller cubes. Find: 
### 1. The number of smaller cubes having:

#### a) 3 faces coloured?
8 cubes, the ones located at the corners.

#### b) exactly 2 faces coloured?
These are the cubes that are on the edges, excluding the ones on the corners, and therefore have one more face exposed.
A cube has 12 edges; excluding the corners leaves us with 3 cubes per edge, so that would be 12 x 3 = 36 cubes.

#### c) exactly 1 face coloured?
These would be the cubes that are not on the edges, so there would be 3 x 3 = 9 cubes per face. A cube has 6 faces, so the final result would be 54 (= 6 x 9).

#### d) 0 faces coloured?
These are the ones that have no face exposed. Therefore, we can imagine a smaller cube if we remove one layer of cubes per side, leaving a 3 x 3 x 3 cube, resulting in 27 cubes with no faces painted.

### 2. All 125 cubes are put into a bag. If a single cube is selected at random from the bag, find probability of picking a cube having 1 or more orange faces
There are 125 cubes, 27 of which have no orange face.
So we can deduce that the probability of picking one with one or more orange faces is (125 - 27 =) 98/125 = 0.784.
Then, multiplying by 100 gives us 78.4%.

### 3. What is the average number of orange faces on a small cube? In the above situation N = 5 (with N³ = 125)
To find the result, we first add up all the faces we know are painted:

8 cubes × 3 faces = 24

36 cubes × 2 faces = 72

54 cubes × 1 face = 54

27 cubes × 0 faces = 0

Adding them all:

24 + 72 + 54 + 0 = 150

Then we calculate the average: 150 / 125 = 1.2 average orange faces per small cube.


#### 4. For general N, give a formula for (1.b) the number with exactly 2 faces coloured
As previously stated, a cube has 12 edges, and each edge has N (or N-length in cubes) – 2 (one less at each end).
So we conclude that the formula is: 12 × (N - 2).

#### 5. For what values of N is this formula correct?
For it to be valid, we must have at least one cube between the corners, which means:
N - 2 ≥ 1, simplified as: N ≥ 3.




# Part 2
Write SQL query that returns: 
#### Why use CTEs and other functions:
Although I could have achieved the same result without using CTEs or functions like LAG() and COALESCE(), I chose to use them to demonstrate that, even if I am not yet fully accustomed to them, these tools are essential in a project that performs data transformations in SQL. They not only enhance the readability and ease of debugging but also promote reusability and modularity of the code, making it easier to maintain and extend in future use cases.

### 1. Number of registered users by country

``` sql
-- Selects the country code and counts the number of users per country.
SELECT 
    country_code, 
    COUNT(*) AS total_users
--  Reads from the user table.
FROM user
-- Groups records by country, so the count is per country.
GROUP BY country_code
-- Orders results from countries with the most users to the least.
ORDER BY total_users DESC;
```

### 2. % of users, who made their first payment in 3 days after registration by country.

``` sql
-- Finds each user's earliest payment date (MIN(created_at)), grouped by user.
WITH first_payments AS (
    SELECT 
        user_id,
        MIN(created_at) AS first_payment_date
    FROM payment
    GROUP BY user_id
),
-- Joins the users with their first payment dates (if any), including users with no payments (using LEFT JOIN).
joined_with_users AS (
    SELECT 
        u.id AS user_id,
        u.country_code,
        u.date_joined,
        fp.first_payment_date
    FROM user u
    LEFT JOIN first_payments fp ON u.id = fp.user_id
)
SELECT 
    country_code,
    -- Uses ROUND(..., 2) to round to two decimals and concatenates ' %' to format as a percentage string.
    ROUND(
        -- Uses COUNT(CASE WHEN ...) to count users whose first payment was within 3 days after joining.
        COUNT(
            CASE 
                WHEN first_payment_date IS NOT NULL 
                     AND first_payment_date <= datetime(date_joined, '+3 days') 
                THEN 1 
            END
        ) * 100.0 / COUNT(*), -- Divides by total users per country to get the percentage.
        2
    ) || ' %' AS percentage_in_3_days
FROM joined_with_users
GROUP BY country_code -- Groups by country.
ORDER BY percentage_in_3_days DESC; -- Orders by the highest percentage first.
```

### 3. % of users, who made their first payment in 3 days after registration and had 2 confirmed products in 7 days after registration by country.

``` sql
-- Finds each user's earliest payment date.
WITH first_payments AS (
    SELECT 
        user_id,
        MIN(created_at) AS first_payment_date
    FROM payment
    GROUP BY user_id
),

-- Counts the number of confirmed products per user that were created within 7 days after the user joined.
confirmed_products AS (
    SELECT 
        p.user_id,
        COUNT(*) AS confirmed_in_7_days
    FROM products p
    JOIN user u ON u.id = p.user_id
    WHERE 
        p.status = 'CONFIRMED'
        AND p.created_at BETWEEN u.date_joined AND datetime(u.date_joined, '+7 days')
    GROUP BY p.user_id
),

-- Combines users with their first payment date and count of confirmed products (using COALESCE to treat missing values as zero).
joined_all AS (
    SELECT 
        u.id AS user_id,
        u.country_code,
        u.date_joined,
        fp.first_payment_date,
        COALESCE(cp.confirmed_in_7_days, 0) AS confirmed_in_7_days
    FROM user u
    LEFT JOIN first_payments fp ON u.id = fp.user_id
    LEFT JOIN confirmed_products cp ON u.id = cp.user_id
)

-- Calculates the percentage of users per country who had their first payment within 3 days 
-- AND at least 2 confirmed products within 7 days.
SELECT 
    country_code,
    ROUND(
        COUNT(
            CASE 
                WHEN first_payment_date IS NOT NULL 
                     AND first_payment_date <= datetime(date_joined, '+3 days')
                     AND confirmed_in_7_days >= 2 
                THEN 1 
            END
        ) * 100 / COUNT(*),  -- Uses conditional counting inside COUNT(CASE WHEN ...)
        2
    ) || ' %' AS percentage  -- Formats the output as a percentage string rounded to two decimals.
FROM joined_all
GROUP BY country_code
ORDER BY percentage DESC;  -- Orders by the highest percentage.
```

### 4. % of weekly new users that never have done a payment.
``` sql
-- Extracts users and assigns them to the week they joined, formatted as "Year-Week".
WITH users_with_week AS (
    SELECT 
        id AS user_id,
        STRFTIME('%Y-%W', date_joined) AS week
    FROM user
),

-- Identifies users who have not made any payments by checking for NULLs after a LEFT JOIN.
users_without_payments AS (
    SELECT 
        u.user_id,
        u.week
    FROM users_with_week u
    LEFT JOIN payment p ON u.user_id = p.user_id
    WHERE p.user_id IS NULL
)

-- Calculates the percentage of users per week who never made a payment.
SELECT 
    uw.week,
    ROUND(
        COUNT(up.user_id) * 100.0 / COUNT(uw.user_id),  -- Percentage = (# of users without payment / total users that week) * 100
        2
    ) || '%' AS percentage_never_paid  -- Formats the result as a percentage string with 2 decimal places
FROM users_with_week uw
LEFT JOIN users_without_payments up ON uw.user_id = up.user_id
GROUP BY uw.week
ORDER BY uw.week;  -- Orders the results chronologically by week
```

### 5. Advanced level (Extra point): Write the SQL that returns how many hours of confirmed products a specific user (for example user_id=1) has taken between payments.
``` sql
-- Finds each user's earliest payment date.
WITH first_payments AS (
    SELECT 
        user_id,
        MIN(created_at) AS first_payment_date
    FROM payment
    GROUP BY user_id
),

-- Joins users with their first payment and calculates if that payment was within 3 days after registration.
joined_with_users AS (
    SELECT 
        u.id AS user_id,
        u.country_code,
        u.date_joined,
        fp.first_payment_date
    FROM user u
    LEFT JOIN first_payments fp ON u.id = fp.user_id
)

-- Calculates the percentage of users per country whose first payment occurred within 3 days of registration.
SELECT 
    country_code,
    ROUND(
        COUNT(
            CASE 
                WHEN first_payment_date IS NOT NULL 
                     AND first_payment_date <= datetime(date_joined, '+3 days')  -- Checks if payment was within 3 days
                THEN 1 
            END
        ) * 100.0 / COUNT(*),  -- Computes percentage = qualifying users / total users
        2
    ) || ' %' AS percentage_in_3_days  -- Formats result as a percentage string
FROM joined_with_users
GROUP BY country_code
ORDER BY percentage_in_3_days DESC;  -- Orders countries by highest percentage first
```
# Part 3
### 1. Write a script or use a library that would get the required information to confirm the 
bike and slot availability. (you can base your conclusions on one day of data) 

PythonPartA.py and PythonPartB.py from this repository.

### 2. In case you decide to download the bicing API information every 5 seconds. In which database would you recommend saving it? Please explain your choice.  

It would depend on the purpose we want to give to the data. If the idea is just to store it for historical records or personal use, I would prioritize using an SQL database. I would create an ETL process that appends the data once a day to build a historical record. I would delete the data generated locally once a week, during Saturday or Sunday when no data insertions would take place.

On the other hand, if the goal were to perform more in-depth analysis and not just on personal data but also to eventually expand the database by feeding it with data from all company colleagues, I would opt to set up a cloud-based architecture and use Parquet files or another format that allows me to work with large amounts of data (even if the files aren't very large at the beginning).
