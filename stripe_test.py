import stripe

stripe.api_key = 'sk_test_51J8dDBCor9GAAV0ahAXOwdMJMrlKBOSeTV4FsPn2GSsFTPFcXjI31dNdjMshsA9PelV0sYY0lnz0UxNSArqXtckT00AFKdDiAH'


stripe.PaymentIntent.create(
  amount=10,
  currency='mxn',
  payment_method_types=['card'],
  receipt_email='quantumqwrty@gmail.com',
)
