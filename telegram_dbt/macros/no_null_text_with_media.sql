{% test no_null_text_with_media(model) %}
    select *
    from {{ model }}
    where has_media = true and (text is null or text = '')
{% endtest %}
