resource "aws_s3_bucket" "cmo-trading-data" {
  bucket = "cmo-trading-data"
  acl    = "private"
}
