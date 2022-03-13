resource "aws_lambda_function" "cryptotradingbot" {
  filename = var.PAYLOAD_FUNCTION_FILEPATH
  function_name = "cryptotradingbot-${var.PROJECT_NAME}"
  handler = "app.lambda_handler"
  role = aws_iam_role.crypto_lambda_execution_role.arn
  runtime = "python3.7"
  timeout = "300"

  environment {
    variables = {
      POLONIEX_KEY = var.POLONIEX_KEY,
      POLONIEX_SECRET = var.POLONIEX_SECRET,
      COINBASE_API_KEY = var.COINBASE_API_KEY,
      COINBASE_API_SECRET = var.COINBASE_API_SECRET,
      COINBASE_PASSPHRASE = var.COINBASE_PASSPHRASE
    }
  }
}
