-- models/marts/fct_image_detections.sql
SELECT
    message_id,
    detected_object_class,
    confidence_score,
    created_at
FROM {{ source('telegram_source', 'fct_image_detections') }}


