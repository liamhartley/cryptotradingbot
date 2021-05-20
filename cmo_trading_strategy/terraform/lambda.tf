resource "aws_lambda_function" "cryptotradingbot_cmo" {
  filename = "../payload.zip"
  function_name = "cryptotradingbot_cmo"
  handler = "app.lambda_handler"
  role = "${aws_iam_role.crypto_lambda_execution_role.arn}"
  runtime = "python3.7"
  timeout = "300"

  environment {
    variables = {
      POLONIEX_API_KEY = var.POLONIEX_API_KEY,
      POLONIEX_SECRET_KEY = var.POLONIEX_SECRET_KEY
    }
  }
}
