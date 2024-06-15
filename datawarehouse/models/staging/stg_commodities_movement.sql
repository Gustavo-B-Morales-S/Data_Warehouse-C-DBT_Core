
with source as (
    select
        date,
        symbol,
        action,
        quantity
        
    from {{ source ('dbsales', 'commodities_movement') }}
),

renamed as (
    select
        cast(date as Date),
        symbol,
        action,
        quantity
    from source
)

select * from renamed
