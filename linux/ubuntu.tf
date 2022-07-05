terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 4.21.0" # Current value.
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"] # Canonical
}

resource "aws_spot_instance_request" "ubuntu" {
  spot_price           = "0.05" # https://aws.amazon.com/ec2/spot/pricing/
  spot_type            = "one-time"
  wait_for_fulfillment = true

  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.xlarge"

  vpc_security_group_ids = ["sg-08d9ae70c77292a48"] # Current value.
  availability_zone      = "us-east-2c"
  key_name               = "2022-07-04" # Current value.
  root_block_device {
    delete_on_termination = true
    encrypted             = true
    volume_type           = "gp3"
    volume_size           = 8
  }
  metadata_options {
    http_endpoint = "disabled"
    #http_tokens = "required"
  }

  user_data = <<EOF
#!/bin/bash
set -x
sudo apt-get update -y
sudo apt-get install qemu-system-x86 -y
sudo apt-get install build-essential cmake lld nasm -y
EOF

  tags = {
    Name = "ubuntu"
  }
}

output "ubuntu" {
  value       = aws_spot_instance_request.ubuntu.public_dns
  description = "Public DNS"
}
