# generic variables - MUST BE DEFINED

variable "PROJECT_NAME" {
  type = string
}

variable "PAYLOAD_FUNCTION_FILEPATH" {
  type = string
}

variable "TRADING_FREQUENCY" {
  type = string
}

variable "AWS_ACCESS_KEY" {
  type = string
}

variable "AWS_SECRET_KEY" {
  type = string
}

variable "region" {
  type = string
  default = ""
}

# strategy variables - OPTIONAL

# poloniex strategies
variable "POLONIEX_KEY" {
  type = string
  default = ""
}

variable "POLONIEX_SECRET" {
  type = string
  default = ""
}

# coinbase strategies
variable "COINBASE_API_KEY" {
  type = string
  default = ""
}

variable "COINBASE_API_SECRET" {
  type = string
  default = ""
}

variable "COINBASE_PASSPHRASE" {
  type = string
  default = ""
}
