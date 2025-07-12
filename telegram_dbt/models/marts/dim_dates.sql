{{ config(
    materialized='table',
    description='Date dimension table for analytics'
) }}

with distinct_dates as (
    select distinct
        date::date as date_key
    from {{ ref('stg_telegram_messages') }}
    where date is not null
)

select
    date_key,
    extract(year from date_key) as year,
    extract(month from date_key) as month,
    extract(day from date_key) as day,
    to_char(date_key, 'Day') as day_of_week,
    to_char(date_key, 'Month') as month_name
from distinct_dates
