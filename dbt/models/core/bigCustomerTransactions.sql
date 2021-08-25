SELECT account, tx_id, amount, account_action
FROM {{source('raw','Transactions')}}
WHERE amount > 7000000 AND account_action = 'DEPOSIT'
GROUP BY 1,4,2,3