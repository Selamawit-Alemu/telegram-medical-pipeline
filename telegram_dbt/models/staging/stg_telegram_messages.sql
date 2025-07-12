with raw as (
    select * from {{ source('raw', 'telegram_messages') }}
)

select
    id,
    channel,
    date,
    text,
    views,
    has_media,
    is_image,
    image_path,
    raw_json
from raw
where id is not null
