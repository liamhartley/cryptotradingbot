resource "aws_cloudwatch_event_rule" "every_hour" {
  name = "every-hour"
  description = "sends a trigger every hour"
  schedule_expression = "rate(1 hour)"
  is_enabled = false
}

resource "aws_cloudwatch_event_target" "trigger_cmo_strategy" {
  rule = aws_cloudwatch_event_rule.every_hour.name
  target_id = "spotify_analysis"
  arn = aws_lambda_function.cryptotradingbot_cmo.arn
}
