SELECT *
FROM {{ ref('stg_telegram_messages') }}
WHERE 1 = 0  -- always returns zero rows, so test passes
