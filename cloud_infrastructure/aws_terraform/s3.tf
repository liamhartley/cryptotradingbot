resource "aws_s3_bucket" "audit-data" {
  bucket = "${var.PROJECT_NAME}-audit"
  acl    = "private"
}
