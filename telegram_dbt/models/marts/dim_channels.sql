{{ config(
    materialized='table',
    description='Dimension table for Telegram channels'
) }}

select distinct
    channel,
    upper(channel) as channel_upper
from {{ ref('stg_telegram_messages') }}
where channel is not null
