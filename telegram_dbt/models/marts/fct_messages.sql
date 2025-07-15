{{ config(materialized='view') }}

select
    id as message_id,
    channel as channel_key,
    CAST(date AS date) as date_key,
    length(text) as message_length,
    views,
    has_media,
    is_image,
    image_path
from {{ source('telegram_source', 'telegram_messages') }}
where id is not null
