/*
    DuckDB Parser

    https://duckdb.org/2023/03/03/json.html
*/

/* Summaries */
copy (
    select
        * exclude ({{ unit_column }}),
        unnest({{ unit_column }}),
    from read_json(
        '{{ target_dir }}/summaries-*.json',
         dateformat:='%Y-%m-%dT%H:%M:%SZ'
    )
    order by obsTimeLocal
) to '{{ target_dir }}/summaries.csv'
;

/* Observations */
copy (
    select
        * exclude ({{ unit_column }}),
        unnest({{ unit_column }}),
    from read_json(
        '{{ target_dir }}/observations-*.json',
         dateformat:='%Y-%m-%dT%H:%M:%SZ'
    )
    order by obsTimeLocal
) to '{{ target_dir }}/observations.csv'
;
