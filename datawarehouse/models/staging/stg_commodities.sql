-- Importing

with source as (
    select
        date,
        symbol,
        close
    
    from {{ source ('dbsales', 'commodities') }}
),

-- Renaming

renamed as (
    select
        cast(date as date),
        close as closing_price,
        symbol
    from
        source
)

-- Selecting

select * from renamed