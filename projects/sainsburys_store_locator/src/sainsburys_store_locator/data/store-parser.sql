from 'src/apis/sainsburys_store_locator/data/sainsburys-stores.json'
select
    code as store_id,
    name as store_name,
    other_name,
    store_type,
    (closed is not null) as closed,
    unnest(contact),
    unnest(location),
;
