resource "aws_instance" "ec2" {
  ami                         = data.aws_ami.ami.image_id
  instance_type               = "t3.medium"
  key_name                    = var.key_name
  subnet_id                   = module.vpc.public_subnets[0]
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.jenkins_sg.id]
  iam_instance_profile        = aws_iam_instance_profile.instance-profile.name
  ebs_optimized               = true

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
    tags = {
      Name = "${var.instance_name}-root"
    }
  }

  user_data = templatefile("./tools-install.sh", {})

  tags = {
    Name        = var.instance_name
    Project     = "jenkins-personal"
    Environment = "dev"
    ManagedBy   = "terraform"
  }
}

data "aws_ami" "ami" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  owners = ["099720109477"]
}


resource "aws_iam_role_policy_attachment" "iam-policy" {
  role = aws_iam_role.iam-role.name
  # Just for testing purpose, don't try to give administrator access
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}


resource "aws_iam_role" "iam-role" {
  name               = var.iam_role
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_instance_profile" "instance-profile" {
  name = "${var.iam_role}-profile"
  role = aws_iam_role.iam-role.name
}
