-- Importing

with source as (
    select
        date,
        symbol,
        action,
        quantity
        
    from {{ source ('dbsales', 'commodities_movement') }}
),

-- Renaming

renamed as (
    select
        cast(date as Date),
        symbol,
        action,
        quantity
    from source
)

-- Selecting

select * from renamed
