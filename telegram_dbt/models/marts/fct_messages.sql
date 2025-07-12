{{ config(
    materialized='table',
    description='Fact table of Telegram messages with foreign keys'
) }}

select
    id as message_id,
    channel as channel_key,
    CAST(date AS date) AS date_key,
    length(text) as message_length,
    views,
    has_media,
    is_image,
    image_path
from {{ ref('stg_telegram_messages') }}
where id is not null
