-- models/staging/stg_image_detections.sql

-- models/staging/stg_image_detections.sql

{{ config(
    materialized='table'
) }}

with source as (
    select
        message_id,
        detected_object_class,
        confidence_score,
        created_at
    from {{ source('telegram_source', 'fct_image_detections') }}
),

renamed as (
    select
        message_id,
        detected_object_class,
        confidence_score,
        created_at
    from source
)

select * from renamed
