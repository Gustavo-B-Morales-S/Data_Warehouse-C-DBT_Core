
with source as (
    select
        date,
        symbol,
        close
    
    from {{ source ('dbsales', 'commodities') }}
),

renamed as (
    select
        cast(date as date),
        close as closing_price,
        symbol
    from
        source
)

select * from renamed