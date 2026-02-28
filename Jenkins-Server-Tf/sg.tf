resource "aws_security_group" "jenkins_sg" {
  name        = "jenkins-sg"
  description = "Allow SSH, HTTP, Jenkins, and SonarQube"
  vpc_id      = module.vpc.vpc_id

  ingress = [
    for port in [22, 80, 8080, 9000, 9090] : {
      description      = "Allow port ${port}"
      from_port        = port
      to_port          = port
      protocol         = "tcp"
      prefix_list_ids  = []
      security_groups  = []
      self             = false
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }
  ]

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "jenkins-sg"
  }
}


