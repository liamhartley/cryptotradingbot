resource "aws_cloudwatch_event_rule" "cryptotradingbot" {
  name = "${var.PROJECT_NAME}-event-rule"
  description = "sends a trigger to execute trading logic"
  schedule_expression = var.TRADING_FREQUENCY
  is_enabled = true
}

resource "aws_cloudwatch_event_target" "trigger_cmo_strategy" {
  rule = aws_cloudwatch_event_rule.cryptotradingbot.name
  target_id = "cryptotradingbot"
  arn = aws_lambda_function.cryptotradingbot.arn
}

module "entering_position_log_metric_filter" {
  source  = "terraform-aws-modules/cloudwatch/aws//modules/log-metric-filter"
  version = "~> 2.0"

  log_group_name = "/aws/lambda/${aws_lambda_function.cryptotradingbot.function_name}"

  name    = "${var.PROJECT_NAME}-entering-position-metric"
  pattern = var.OPENING_PATTERN

  metric_transformation_namespace = "${var.PROJECT_NAME}-entering-position-namespace"
  metric_transformation_name      = "${var.PROJECT_NAME}-entering-position-metric-name"
}

module "entering_position_metric_alarm" {
  source  = "terraform-aws-modules/cloudwatch/aws//modules/metric-alarm"
  version = "~> 2.0"

  alarm_name          = "${var.PROJECT_NAME}-entering-position-alarm"
  alarm_description   = "Triggers when bot enters a trade"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  threshold           = 0
  period              = 300
  unit                = "None"

  namespace   = "${var.PROJECT_NAME}-entering-position-namespace"
  metric_name = "${var.PROJECT_NAME}-entering-position-metric-name"
  statistic   = "Maximum"
  treat_missing_data = "notBreaching" // or ignore

  alarm_actions = [aws_sns_topic.trade-notification-sns.arn]
}

module "closing_position_log_metric_filter" {
  source  = "terraform-aws-modules/cloudwatch/aws//modules/log-metric-filter"
  version = "~> 2.0"

  log_group_name = "/aws/lambda/${aws_lambda_function.cryptotradingbot.function_name}"

  name    = "${var.PROJECT_NAME}-closing-position-metric"
  pattern = var.CLOSING_PATTERN

  metric_transformation_namespace = "${var.PROJECT_NAME}-closing-position-namespace"
  metric_transformation_name      = "${var.PROJECT_NAME}-closing-position-metric-name"
}

module "closing_position_metric_alarm" {
  source  = "terraform-aws-modules/cloudwatch/aws//modules/metric-alarm"
  version = "~> 2.0"

  alarm_name          = "${var.PROJECT_NAME}-closing-position-alarm"
  alarm_description   = "Triggers when bot closes a trade"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  threshold           = 0
  period              = 300
  unit                = "None"

  namespace   = "${var.PROJECT_NAME}-closing-position-namespace"
  metric_name = "${var.PROJECT_NAME}-closing-position-metric-name"
  statistic   = "Maximum"
  treat_missing_data = "notBreaching" // or ignore

  alarm_actions = [aws_sns_topic.trade-notification-sns.arn]
}
