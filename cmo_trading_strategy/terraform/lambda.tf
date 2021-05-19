resource "aws_lambda_function" "cryptotradingbot_cmo" {
  filename = "../payload.zip"
  function_name = "spotify_analysis"
  handler = "avg_album_length_playlist.lambda_handler"
  role = "${aws_iam_role.crypto_lambda_execution_role.arn}"
  runtime = "python3.7"
  timeout = "300"

  environment {
    variables = {
      POLONIEX_SECRET_KEY = var.POLONIEX_SECRET_KEY,
    }
  }
}
