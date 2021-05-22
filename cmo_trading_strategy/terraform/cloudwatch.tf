resource "aws_cloudwatch_event_rule" "every_minute" {
  name = "every-minute"
  description = "sends a trigger every minute"
  schedule_expression = "rate(1 minute)"
  is_enabled = false
}

resource "aws_cloudwatch_event_target" "trigger_cmo_strategy" {
  rule = "${aws_cloudwatch_event_rule.every_minute.name}"
  target_id = "spotify_analysis"
  arn = "${aws_lambda_function.cryptotradingbot_cmo.arn}"
}
