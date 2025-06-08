
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
Although I could have achieved the same result without using CTEs or functions like LAG() and COALESCE(), I chose to use them to demonstrate that—even if I am not yet fully accustomed to using them—since the project performs transformations using SQL, these tools are necessary or can greatly improve the SQL code’s readability and ease of debugging.

### 1. Number of registered users by country
It returns the total number of registered users per country, sorted from the highest to the lowest number of users.
```
SELECT 
    country_code, 
    COUNT(*) AS total_users
FROM user
GROUP BY country_code
ORDER BY total_users DESC;
```
#### Explanation:

SELECT country_code, COUNT(*) AS total_users
Selects the country code and counts the number of users per country.

FROM user
 Reads from the user table.

GROUP BY country_code
Groups records by country, so the count is per country.

ORDER BY total_users DESC
Orders results from countries with the most users to the least.

### 2. % of users, who made their first payment in 3 days after registration by country.
It calculates the percentage of users per country who made their first payment within 3 days after registration. The result is shown as a percentage with two decimal places, ordered from highest to lowest.
```
WITH first_payments AS (
    SELECT 
        user_id,
        MIN(created_at) AS first_payment_date
    FROM payment
    GROUP BY user_id
),
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
    ROUND(
        COUNT(
            CASE 
                WHEN first_payment_date IS NOT NULL 
                     AND first_payment_date <= datetime(date_joined, '+3 days') 
                THEN 1 
            END
        ) * 100.0 / COUNT(*),
        2
    ) || ' %' AS percentage_in_3_days
FROM joined_with_users
GROUP BY country_code
ORDER BY percentage_in_3_days DESC;
```
#### Explanation:

CTE first_payments:
Finds each user's earliest payment date (MIN(created_at)), grouped by user.

CTE joined_with_users:
Joins the users with their first payment dates (if any), including users with no payments (using LEFT JOIN).

Main SELECT:

- Groups by country.

- Uses COUNT(CASE WHEN ...) to count users whose first payment was within 3 days after joining.

- Divides by total users per country to get the percentage.

- Uses ROUND(..., 2) to round to two decimals and concatenates ' %' to format as a percentage string.

- Orders by the highest percentage first.

Why CTE?
CTEs simplify complex queries by breaking them into readable parts — first getting payments, then joining users, then computing the percentage.


### 3. % of users, who made their first payment in 3 days after registration and had 2 confirmed products in 7 days after registration by country.
This SQL query calculates the percentage of users per country who:
Made their first payment within 3 days after registering, and had at least 2 confirmed products within 7 days of registration.
```
WITH first_payments AS (
    SELECT 
        user_id,
        MIN(created_at) AS first_payment_date
    FROM payment
    GROUP BY user_id
),
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
        ) * 100 / COUNT(*),
        2
    ) || ' %' AS percentage
FROM joined_all
GROUP BY country_code
ORDER BY percentage DESC;
```
#### Explanation:

CTE first_payments:
Finds each user's earliest payment date.

CTE confirmed_products:
Counts the number of confirmed products per user that were created within 7 days after the user joined.

CTE joined_all:
Combines users with their first payment date and count of confirmed products (using COALESCE to treat missing values as zero).

Main SELECT:

Calculates the percentage of users per country who had their first payment within 3 days AND at least 2 confirmed products within 7 days.

Uses conditional counting inside COUNT(CASE WHEN ...).

Formats the output as a percentage string rounded to two decimals.

Orders by the highest percentage.

Why CTE?
It organizes the logic into manageable steps: payments, products, and combined data for clarity and maintainability.

### 4. % of weekly new users that never have done a payment.
```
WITH users_with_week AS (
    SELECT 
        id AS user_id,
        STRFTIME('%Y-%W', date_joined) AS week
    FROM user
),
users_without_payments AS (
    SELECT 
        u.user_id,
        u.week
    FROM users_with_week u
    LEFT JOIN payment p ON u.user_id = p.user_id
    WHERE p.user_id IS NULL
)
SELECT 
    uw.week,
    ROUND(COUNT(up.user_id) * 100.0 / COUNT(uw.user_id), 2) || '%' AS percentage_never_paid
FROM users_with_week uw
LEFT JOIN users_without_payments up ON uw.user_id = up.user_id
GROUP BY uw.week
ORDER BY uw.week;
```
### 5. Advanced level (Extra point): Write the SQL that returns how many hours of confirmed products a specific user (for example user_id=1) has taken between payments.
```
WITH user_payments AS (
    SELECT 
        id AS payment_id,
        user_id,
        created_at,
        LAG(created_at) OVER (PARTITION BY user_id ORDER BY created_at) AS previous_payment
    FROM payment
    WHERE user_id = 1
),
confirmed_products AS (
    SELECT * 
    FROM products 
    WHERE user_id = 1 AND status = 'CONFIRMED'
),
product_ranges AS (
    SELECT 
        up.payment_id,
        up.previous_payment,
        up.created_at AS current_payment,
        SUM(cp.hours) AS confirmed_hours
    FROM user_payments up
    JOIN confirmed_products cp 
        ON cp.created_at > COALESCE(up.previous_payment, '1970-01-01')
       AND cp.created_at <= up.created_at
    GROUP BY up.payment_id, up.previous_payment, up.created_at
)
SELECT 
    payment_id,
    previous_payment,
    current_payment,
    confirmed_hours
FROM product_ranges
ORDER BY current_payment;
```
#### Explanation:

CTE user_payments:
Lists all payments of user 1, along with the previous payment date (using the window function LAG).

CTE confirmed_products:
Filters confirmed products of user 1.

CTE product_ranges:
For each payment period (from previous payment to current payment), sums the hours of confirmed products that happened between these two payment dates.
COALESCE(up.previous_payment, '1970-01-01') ensures we cover the time before the very first payment.

Final SELECT:
Outputs the payment ID, previous payment date, current payment date, and total confirmed product hours used between these payments.

SQL resources used:
Window functions (LAG), date filtering, aggregation (SUM), and COALESCE for handling nulls.

# Part 3
1. 
PythonPartA.py and PythonPartB.py from this repository.

2.
It depends on the purpose of storing such information.
If it’s only to save a history that can be reviewed from time to time, I would use CSV or JSON.
On the other hand, if I wanted to process the data to create predictive or statistical models, I would use Parquet.
