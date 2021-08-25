SELECT account, tx_id, amount, account_action
FROM {{source('raw','Transactions')}}
WHERE amount > 5000000 AND account_action = 'WITHDRAW'