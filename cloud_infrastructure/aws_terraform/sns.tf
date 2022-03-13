resource "aws_sns_topic" "trade-notification-sns" {
  name = "${var.PROJECT_NAME}-sns"
}