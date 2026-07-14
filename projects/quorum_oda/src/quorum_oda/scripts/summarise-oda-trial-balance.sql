/*    DuckDB    */

-- set variable trial_balance_path = 'projects/quorum_oda/src/quorum_oda/data/Multi-Company Trial Balance.xlsx';
set variable trial_balance_path = 'projects/quorum_oda/src/quorum_oda/data/Multi-Company Trial Balance 2026-07-14T14:49:39.110780.xlsx';

/* Settings */
select
    *,
    hash(any_value(setting_value) filter (where setting = 'Report Generated On') over ()) as report_id,
from read_xlsx(
    getvariable('trial_balance_path'),
    sheet='Settings',
    header=false
) as xlsx(setting, setting_value)
;
/* Settings (pivoted) */
pivot (
    select
        lower(setting).replace(' ', '_') as setting,
        setting_value,
    from read_xlsx(
        getvariable('trial_balance_path'),
        sheet='Settings',
        header=false
    ) as xlsx(setting, setting_value)
)
on setting
using any_value(setting_value)
;

/* Trial Balance */
with oda_trial_balance as (
    select
        main_account,
        sub_account,
        columns('_(\d{3})_.*') as '\1'
    from (
        select *, row_number() over () as _row_id
        from read_xlsx(
            getvariable('trial_balance_path'),
            sheet='Trial Balance',
            normalize_names=true
        )
    )
    qualify _row_id != max(_row_id) over ()  /* Ignore the "totals" row */
)

from (
    unpivot oda_trial_balance
    on columns(* exclude (main_account, sub_account))
    into
        name company_id
        value amount
)
select
    concat_ws(
        '.',
        main_account,
        lpad(sub_account, 3, '0'),
        company_id
    ) as account_company_id,
    amount
-- where amount != 0
order by account_company_id
;
