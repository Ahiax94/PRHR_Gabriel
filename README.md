
# Part 1 
A cube is painted orange on all six sides. It is divided into 125 (=5 x 5 x 5) equal smaller cubes. Find: 
### 1. The number of smaller cubes having:

#### a) 3 faces coloured?
8 cubos, los que están en las esquinas.

#### b) exactly 2 faces coloured?
Estos son los cubos que están en los bordes menos los que ocupan las esquinas y, por tanto, tienen un lado más a la vista.
Un cubo tiene 12 bordes; menos las esquinas, nos deja con 3 cubos por borde, así que serían 12 x 3 = 36 cubos.

#### c) exactly 1 face coloured?
Estos serían los cubos que no están en los bordes, por tanto serían 3 x 3 = 9 cubos por lado. Un cubo tiene 6 lados, así que el resultado final sería 54 (= 6 x 9).

#### d) 0 faces coloured?
Serían todos los que no tienen una cara a la vista, por tanto podemos imaginar un cubo con unas medidas inferiores si eliminamos una capa de cubos por lado, lo que nos deja un cubo de 3 x 3 x 3, dando el resultado de 27 cubos sin ninguna cara.

### 2. All 125 cubes are put into a bag. If a single cube is selected at random from the bag, find probability of picking a cube having 1 or more orange faces
Hay 125 cubos, 27 de ellos sin una cara naranja.
Así que podemos deducir que la posibilidad de sacar uno con una cara naranja o más es de (125 - 27 =) 98/125 = 0,784. Luego sacamos el % multiplicando por 100 y nos da 78,4 %.

### 3. What is the average number of orange faces on a small cube? In the above situation N = 5 (with N³ = 125)
Para sacar el resultado, primero sumamos todas las caras que sabemos que están pintadas:
8 cubitos × 3 caras = 24
36 cubitos × 2 caras = 72
54 cubitos × 1 cara = 54
27 cubitos × 0 caras = 0
Las sumamos todas:
24 + 72 + 54 + 0 = 150

Y sacamos el promedio: 150 / 125 = 1,2 de promedio de cara naranja por cubito.


#### 4. For general N, give a formula for (1.b) the number with exactly 2 faces coloured

Como ya he dicho, hay 12 aristas en un cubo y cada una tiene N (o longitud en cubitos de la arista) – 2 (uno por lado). Así que concluimos que la fórmula sería 12 × (N - 2).

#### 5. For what values of N is this formula correct?
Para que se valga, tenemos que tener mínimo un cubito entre las esquinas, o lo que es lo mismo:
N - 2 ≥ 1. Si la simplificamos, podemos dejarla como N ≥ 3.




# Part 2
Write SQL query that returns: 

### 1. Number of registered users by country
```
SELECT 
    country_code, 
    COUNT(*) AS total_users
FROM user
GROUP BY country_code
ORDER BY total_users DESC;
```

### 2. % of users, who made their first payment in 3 days after registration by country.
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
### 3. % of users, who made their first payment in 3 days after registration and had 2 confirmed products in 7 days after registration by country.
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
# Part 3
1. 
PythonPartA.py y PythonPartB.py de este repositorio

2.
Depende de cual fuera el proposito de almacenar dicha informacion.
Si solo fuera para guardar un historial que poder revisar de vez en cuando, usaría CSV o JSON.
Por el contrario si quisiera trabajar los datos para hacer modelos predictivos o estadisticos utilizaría parquet.
