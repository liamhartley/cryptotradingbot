resource "aws_cloudwatch_event_rule" "cryptotradingbot" {
  name = var.PROJECT_NAME
  description = "sends a trigger to execute trading logic"
  schedule_expression = var.TRADING_FREQUENCY
  is_enabled = false
}

resource "aws_cloudwatch_event_target" "trigger_cmo_strategy" {
  rule = aws_cloudwatch_event_rule.cryptotradingbot.name
  target_id = "cryptotradingbot"
  arn = aws_lambda_function.cryptotradingbot.arn
}
