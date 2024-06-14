-- models/datamart/dm_commodities.sql

with commodities as (
    
    select
        date,
        symbol,
        closing_price
        
    from 
        {{ ref ('stg_commodities') }}
),

movement as (
    
    select
        date,
        symbol,
        action,
        quantity
        
    from 
        {{ ref('stg_commodities_movement') }}
),

joined as (
    
    select
        c.date,
        c.symbol,
        c.closing_price,
        m.action,
        m.quantity,
        (m.quantity * c.closing_price) as value,  
        
        case
            when m.action = 'sell' then (m.quantity * c.closing_price)
            else -(m.quantity * c.closing_price)
        end as gain
        
    from
        commodities c
    inner join
        movement m
    on
        c.date = m.date
        and c.symbol = m.symbol
),

last_day as (
    
    select
        max(date) as max_date
        
    from
        joined
),

filtered as (
    select
        *     
    from
        joined    
    where
        date = (select max_date from last_day)
)

select
    date,
    symbol,
    closing_Price,
    action,
    quantity,
    value,
    gain
from
    filtered