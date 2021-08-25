SELECT user-id, tx_id, amount, account_action
FROM {{source('raw_data','Transactions')}}
WHERE amount > 5000000 AND account_action = 'WITHDRAW'